import requests
from bs4 import BeautifulSoup

url = "https://n.news.naver.com/mnews/article/020/0003687545"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# <h2 id="title_area" class="media_end_head_headline">
title_tag = soup.find("h2", id="title_area")  # id 기준
# 또는 title_tag = soup.find("h2", class_="media_end_head_headline")
area_tag = soup.find("article",id="dic_area")
title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
area = area_tag.get_text(strip=True) if title_tag else "제목 없음"
print(title)
print(area)