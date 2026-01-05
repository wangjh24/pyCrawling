import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://finance.naver.com/item/frgn.naver?code=005930&page=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
response.encoding = "euc-kr"  # 네이버 금융 필수
html = response.text
soup = BeautifulSoup(html, "html.parser")
table = soup.find("table", summary="외국인 기관 순매매 거래량")
rows = table.find_all("tr")
data = []

for row in rows:
    cols = row.find_all("td")
    if len(cols) == 9:
        data.append([col.get_text(strip=True) for col in cols])
columns = [
    "날짜", "종가", "전일비", "등락률", "거래량",
    "기관 순매매량", "외국인 순매매량",
    "외국인 보유주수", "외국인 보유율"
]

df = pd.DataFrame(data, columns=columns)
print(df)
