from fastapi import FastAPI
from typing import List, Union, Tuple
from pydantic import BaseModel

from dsp_processor import DSPQueryProcessor
from utils import get_retriever, get_lm

app = FastAPI()

lm = get_lm()
retriever = get_retriever("SC")

query_processor = DSPQueryProcessor(policy=lm, index=retriever)

@app.get("/search")
def search(q: str):
    search_results = query_processor(q)

    return {"results":search_results}