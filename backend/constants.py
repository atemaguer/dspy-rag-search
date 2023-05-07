DEFAULT_ROUTER_TEMPLATE = """task: Classify this sentence as one of TOT or ST
sentence: that paper that proposes a multi-vector retriever but it changes the scoring mechanism of ColBERT to make it more efficient by authors from Austria
label: TOT

task: Classify this sentence as one of TOT or ST
sentence: BERT transformer
label: ST

task: Classify this sentence as one of TOT or ST
sentence: paper that plugs in a frozen retriever with an LM and fine-tunes the retriever
label: TOT

task: Classify this sentence as one of TOT or ST
sentence: Roberta Question Answering
label: ST

task: Classify this sentence as one of TOT or ST
sentence: ColBERT Late Interaction
label: ST

task: Classify this sentence as one of TOT or ST
sentence: find a paper on using kNN over examples that are fed in the prompt to learn from user feedback without updating the model
label: TOT

task: Classify this sentence as one of TOT or ST
"""

training_samples = [
    ("find papers that ensemble generations of in-context learning across prompts, where each prompt has different demonstrating examples", ["in-context learning across prompts, ensemble generations"]),
    ("that paper that proposes a multi-vector retriever but it changes the scoring mechanism of ColBERT to make it more efficient", ["ColBERT scoring mechanism, multi-vector retriever"])
]

