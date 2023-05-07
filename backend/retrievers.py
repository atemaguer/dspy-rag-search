import requests
from typing import List, Union
from dsp.utils import dotdict
from semanticscholar import SemanticScholar

class Retriever:
    def __init__(self):
        pass
    
class SemanticScholarRetriever(Retriever):
    def __init__(self) -> None:
        self.sch = SemanticScholar()

    def _retrieve(self, query: str, top_k=10) -> List[List[str]]:

        try:
            results = self.sch.search_paper(
                query, fields=['title', 'abstract', "externalIds"], limit=top_k)
        except Exception as err:
            print(err)
            results = []

        passages = []

        for i in range(len(results)):
            passages.append(
                {"title": results[i]["title"], "long_text": results[i]["abstract"], "paper_ids": results[i]["externalIds"]})

        return passages

    def __call__(self, query_input: Union[str, List[str]], k=5, ensemble=False, simplify=False) -> any:
        results = []
        
        if ensemble:
            assert isinstance(
                query_input, list), "You must provide a list of queries, when you intend to ensemble the outputs"

            for query in query_input:
                results += self._retrieve(query, k)
        else:
            assert not isinstance(
                query_input, list), "You must set ensemble=True when you provide a list of queries"

            results = self._retrieve(query_input, k)
            
        results = [dotdict(psg) for psg in results]
        
        return results
    
class ColBERTRetriever(Retriever):
    def __init__(self, url="http://localhost", port=8000):
        self.server_url = f"{url}:{port}/search"

        self.headers = {"Content-Type": "application/json; charset=utf-8"}

    def _post(self, query: str, k: int):
        payload = {"query": query, "k": k}
        res = requests.post(self.server_url, json=payload,
                            headers=self.headers)

        return res.json()['topk'][:k]

    def _get_request(self, url: str, query: str, k: int):
        assert k <= 100, f'Only k <= 100 is supported for the hosted ColBERTv2 server at the moment.'

        payload = {"query": query, "k": k}
        data = requests.get(url, params=payload).json()
        topk_passages = data["passages"][:k]
        topk_scores = data["scores"][:k]

        results = []

        for i, passage in enumerate(topk_passages):
            paper_id, body = passage.split("|")

            results.append(
                {"paper_id": paper_id[:-7], "long_text": body, "score": topk_scores[i]})

        return results

    def __call__(self, query: str, k=10, simplify=False):

        topk = self._get_request(self.server_url, query, k)
        topk = [dotdict(psg) for psg in topk]

        if simplify:
            topk = [psg.long_text for psg in topk]

        return topk
