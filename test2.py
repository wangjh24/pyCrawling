import requests 
from bs4 import BeautifulSoup
# URL 및 헤더 설정
url = "https://finance.naver.com/"
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        }
response = requests.get(url,headers=headers, verify=False)

soup = BeautifulSoup (response.text,'lxml')
items = soup.select('#_topItems2 > tr')

print ("=================")
for item in items: 
    
    subject = item. select_one('th > a')
    tds = item.select ('td')
    if subject and len (tds) >= 3 : 
        name = subject.text.strip()
        price = tds[0].text. strip()
        change = tds[1].text.strip()
        rate= tds[2].text.strip()

        print(f"종목: {name},{price},{change},{rate}")
    else: 
        print ("데이터 형식이 맞지않음")
        