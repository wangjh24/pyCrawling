import requests
from bs4 import BeautifulSoup
import time

base_url = "https://finance.naver.com"
iframe_src = "/item/news.naver?code=005930"

url = base_url + iframe_src

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://finance.naver.com/item/main.naver?code=005930"
}

session = requests.Session()
response = session.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
news_items = soup.select("td.title a")
for news in news_items:
    title = news.text.strip()
    print(title)
    time.sleep(0.3)