import yfinance as yf
import requests
from bs4 import BeautifulSoup
import os
from sentence_transformers import SentenceTransformer, util

sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_stock_news(ticker):
    if not ALPHA_VANTAGE_API_KEY:
        raise ValueError("Alpha Vantage API key is missing. Set ALPHA_VANTAGE_API_KEY in your environment.")

    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching news:", response.status_code, response.text)
        return []

    news_data = response.json()

    if "feed" not in news_data:
        print("Unexpected API response:", news_data)
        return []

    news = []
    for article in news_data["feed"]:
        news.append({
            "title": article["title"],
            "link": article["url"]
        })

    return news

def get_yahoo_finance_news(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    news = []
    for article in soup.find_all("h3"):
        title = article.text
        link = "https://finance.yahoo.com" + article.a["href"]
        news.append({"title": title, "link": link})

    return news

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    return stock.info

def get_sec_filings(ticker):
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10-Q&count=10"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    return response.text


def rerank_results(query, retrieved_docs):
    query_embedding = sbert_model.encode(query, convert_to_tensor=True)
    doc_embeddings = [sbert_model.encode(doc.page_content, convert_to_tensor=True) for doc in retrieved_docs]
    scores = [util.pytorch_cos_sim(query_embedding, doc_emb).item() for doc_emb in doc_embeddings]

    # Sort by highest score
    ranked_docs = sorted(zip(retrieved_docs, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked_docs[:5]]  # Return top 5 ranked docs