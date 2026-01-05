import requests 
from bs4 import BeautifulSoup

url = "https://finance.naver.com/item/frgn.naver?code=005930"
        
        # User-Agent 헤더 설정 (봇 차단 방지)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
        }
        # HTML 요청
response = requests.get(url, headers=headers)
        
        # HTML 파싱
soup = BeautifulSoup(response.text, "lxml")
items = soup.select('td')



print(items)

soup2 = BeautifulSoup(response.text, "html.parser")


tbody = soup2.find('tbody')

print(tbody)
print("____________")