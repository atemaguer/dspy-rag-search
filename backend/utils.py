import os
from retrievers import SemanticScholarRetriever, ColBERTRetriever
from dsp import GPT3, ColBERTv2

openai_key = os.getenv('OPENAI_API_KEY') 
colbert_server = 'http://ec2-44-228-128-229.us-west-2.compute.amazonaws.com:8893/api/search'

def get_retriever(name="ColBERT"):
    if name == "ColBERT":
        return ColBERTRetriever(url="http://localhost")

    return SemanticScholarRetriever()


def get_lm(name="GPT3"):
    if name == "GPT3":
        return GPT3(model='text-davinci-003')


def retrieve_ensembles(queries, top_k=10):
    pass
