from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from vector_store import create_vector_store, get_retriever
from retriever import get_stock_news

from langchain_core.documents import Document
from retriever import get_stock_news

from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain

# Fetch stock news
news_articles = get_stock_news("TSLA")

# Convert raw text into Document objects with metadata
news_docs = [Document(page_content=article["title"], metadata={"source": article["link"]}) for article in news_articles]

# Debugging print statement
print("Processed News Documents:", news_docs)

if not news_docs:
    raise ValueError("No news articles retrieved. Check API issues.")

vector_db = create_vector_store(news_docs)
retriever = get_retriever(vector_db)


# LLM-powered RAG response
def get_rag_response(query):
    llm = ChatOpenAI(model_name="gpt-4")

    qa_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="You are an AI assistant. Answer the following question based on the context:\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:",
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": qa_prompt}
    )
    return qa_chain.run(query)
