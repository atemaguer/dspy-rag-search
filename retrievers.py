import requests
from typing import List
from semanticscholar import SemanticScholar


class SemanticScholarRetriever:
    def __init__(self) -> None:
        self.sch = SemanticScholar()

    def __call__(self, query: str, k=10) -> List[str]:
        results = self.sch.search_paper(
            query, fields=['title', 'abstract'], limit=k)
        passages = []

        for i in range(len(results)):
            passages.append(
                f'title->{results[i]["title"]} | abstract->{results[i]["abstract"]}')
        return passages


class ColBERTRetriever:
    def __init__(self) -> None:
        self.server_url = "http://localhost:8000/search/"

    def __call__(self, query: str, k=10) -> List[str]:
        try:
            results = requests.get(self.server_url, {"query": query}).json()
            return results["passages"]
        except Exception as err:
            print(err)
            return []
