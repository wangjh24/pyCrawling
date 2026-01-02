import requests as rq 
from bs4 import BeautifulSoup

url = "https://finance.naver.com/item/main.naver?code=005930"
html = rq.get (url)
soup = BeautifulSoup (html,"lxml")
print (soup)
