import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs  
import time

base_url = "https://finance.naver.com"
iframe_src = "/item/news_news.naver?code=005930"
url = base_url + iframe_src

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ",
    "Referer": "https://finance.naver.com/item/main.naver?code=005930"
}

response = requests.get(url, headers=headers)
response.encoding = 'euc-kr' 
soup = BeautifulSoup(response.text, "html.parser")

news_items = soup.select("td.title a")

if not news_items:
    print("뉴스 항목을 찾지 못했습니다.")
else:
    for news in news_items:
        relative_link = news['href']
        
        parsed_url = urlparse(relative_link)
        params = parse_qs(parsed_url.query)
        
        office_id = params.get('office_id')[0]
        article_id = params.get('article_id')[0]

        if office_id and article_id:
            real_link = f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}"
            
            res1 = requests.get(real_link, headers=headers)
            soup1 = BeautifulSoup(res1.text, "html.parser")
            
            title_tag = soup1.find("h2", id="title_area")  
            area_tag = soup1.find("article", id="dic_area")
            
            title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
            area = area_tag.get_text(strip=True) if area_tag else "본문 없음"
            
            print(f"제목: {title}")
            print(f"본문 요약: {area[:100]}...") 
            print("-" * 50)
            
            time.sleep(0.5)