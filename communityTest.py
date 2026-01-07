import requests
from bs4 import BeautifulSoup
import time

base_url = "https://finance.naver.com"
iframe_src = "/item/board_read.naver?code=005930&nid=409760124&page=1"

url = base_url + iframe_src

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://finance.naver.com/item/main.naver?code=005930"
}

session = requests.Session()
response = session.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
title_tag = soup.find("strong",class_ = 'c p15')
iframe_tag = soup.find("iframe", id="contents")
iframe_url = iframe_tag['src']
iframe_url = "https://m.stock.naver.com/pc/domestic/stock/005930/discussion/409760124"

# User-Agent 필수
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(iframe_url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# 실제 글 내용이 있는 div 찾기
# 모바일 토론 글은 보통 class="article_body" 또는 id="content" 등
content_div = soup.find("div", class_="article_body")  # 실제 클래스 확인 필요
if content_div:
    paragraphs = content_div.find_all("p")
    content = "\n".join(p.get_text(strip=True) for p in paragraphs)
else:
    content = ""

print(content)
title= title_tag.get_text(strip = True)
print (title)
