import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
sys.stdout.reconfigure(encoding="utf-8")

# 키워드, URL
keyword = '005930'
url = f'https://finance.naver.com/item/news.naver?code={keyword}'

# 웹 페이지 요청
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print (soup)
# 뉴스 제목 포함 부분 필터링
# articles = soup.select('a[data-heatmap-target=".tit"]')
# articles

# # 뉴스 제목 확인
# article = articles[0]
# title = article.text
# title

# # 뉴스 제목 데이터프레임 생성
# title_tot = pd.DataFrame([article.text for article in articles], columns=['title'])
# title_tot.head()

# print (title_tot)
