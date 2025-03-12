import logging
from datetime import datetime
from fastapi import FastAPI
from rag_pipeline import get_rag_response

app = FastAPI()


# Set up logging
logging.basicConfig(filename="logs.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.get("/query")
def query_stock_assistant(question: str):
    try:
        response = get_rag_response(question)
        logging.info(f"User Query: {question} | Response: {response}")
        return {"response": response}
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        return {"error": "An error occurred. Please try again."}
