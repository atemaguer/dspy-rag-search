from retrievers import SemanticScholarRetriever, ColBERTRetriever

def get_retriever(name="ColBERT"):
    if name == "ColBERT":
        return ColBERTRetriever()
        
    return  SemanticScholarRetriever()
