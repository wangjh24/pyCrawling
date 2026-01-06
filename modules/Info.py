import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')
code = "005930"
url = f"https://finance.naver.com/item/main.naver?code={code}"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
# res.encoding = "euc-kr"

soup = BeautifulSoup(res.text, "html.parser")

table = table = soup.find("caption", string="거래원 정보").find_parent("table")
rows = table.select("tbody tr")
print (rows)
data = []
for row in rows:
    cols = row.find_all("td")
    if len(cols) == 4:
        data.append([c.get_text(strip=True) for c in cols])

columns = ["매도상위", "거래량", "매수상위", "거래량"]
df = pd.DataFrame(data, columns=columns)

print(df)
