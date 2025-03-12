from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


def create_vector_store(documents):
    embedding_function = OpenAIEmbeddings()

    if not documents:
        raise ValueError("No documents available for FAISS. Ensure data retrieval works correctly.")

    # Create FAISS vector store
    vector_db = FAISS.from_documents(documents, embedding=embedding_function)
    return vector_db


# ✅ Fix: Define get_retriever() function
def get_retriever(vector_db):
    return vector_db.as_retriever()
