import os
import dsp
from typing import List, Any
from retrievers import Retriever
from utils import get_lm, get_retriever

sentence = dsp.Type(prefix="Sentence:",
                    desc="${the sentence from which to extract keywords and phrases}")
                    
output = dsp.Type(prefix="Output:",
                  desc="${a comma-seperated list of keywords and phrases}", format=dsp.format_answers)

KEYWORDS_TEMPLATE = dsp.Template(
    instructions="Extract and provide a comma-seperated list of keywords and phrases from the following sentences.", sentence=sentence(), output=output())

context = dsp.Type(
    prefix="Text:\n",
    desc="${text that might contain information that fulfills the question}",
    format=dsp.passages2text
)

question = dsp.Type(
    prefix="Question: Do you think the paper above answers this question:",
    desc="${a question from a user looking for a paper}",
    format=dsp.passages2text
)

answer = dsp.Type(prefix="Answer:", desc="${a Yes, or No answer}", format=dsp.format_answers)

QUERY_PROCESSING_TEMPLATE = dsp.Template(
    instructions="Does the following piece of text fullfil this question? The text should be relevant to the question below. Give a Yes or No answer.",
    context=context(), question=question(), answer=answer()
)

samples = [
    ("find papers that ensemble generations of in-context learning across prompts, where each prompt has different demonstrating examples", ["in-context learning across prompts, ensemble generations"]),
    ("that paper that proposes a multi-vector retriever but it changes the scoring mechanism of ColBERT to make it more efficient", ["ColBERT scoring mechanism, multi-vector retriever"])
]

samples = [dsp.Example(sentence=sentence, keywords=keywords) for sentence, keywords in samples]

class DSPQueryProcessor:
    def __init__(self, policy: Any = None, index: Retriever = None, k=10) -> None:
        self.policy = policy
        self.index = index
        self.k = k

        if policy is None:
            self.policy = get_lm()
        if index is None:
            self.index = get_retriever()

        dsp.settings.configure(lm=self.policy, rm=self.index)


    def __call__(self, task) -> List[str]:
        return self._tot_pipeline(task)

    @dsp.transformation
    def _demonstrate(self, query: str):
        
        demos = dsp.sample(samples, k=1)    
        example = dsp.Example(sentence=query, demos=demos)
        _, completions = dsp.generate(KEYWORDS_TEMPLATE, n=1, temperature=0.0)(example, stage='qa')
        
        return completions[0].output, demos

    @dsp.transformation
    def _tot_pipeline(self, query: str):
        keywords, demos = self._demonstrate(query)

        try:
            passages = self.index(keywords, k=10)
        except Exception as err:
            passages = []
        
        results = []

        for passage in passages:
            try:
                example = dsp.Example(question=query, context= passage.title + "\n" + passage.long_text, demos=demos)
                _, completions = dsp.generate(QUERY_PROCESSING_TEMPLATE)(example, stage='qa')

                if "yes" in completions[0].answer.lower() or "unknown" in completions[0].answer.lower():
                    results.append(passage)
            except:
                pass
            
        return results

    
