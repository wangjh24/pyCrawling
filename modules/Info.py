import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://finance.naver.com/item/main.naver?code=005930"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
res.encoding = "euc-kr"

soup = BeautifulSoup(res.text, "html.parser")

table = soup.select_one("div.section.invest_trend table.tb_type1")
rows = table.select("tbody tr")

data = []
for row in rows:
    cols = row.find_all("td")
    if len(cols) == 4:
        data.append([c.get_text(strip=True) for c in cols])

columns = ["매도상위", "거래량", "매수상위", "거래량"]
df = pd.DataFrame(data, columns=columns)

print(df)
