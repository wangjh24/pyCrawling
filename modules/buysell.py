import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

code = "005930"
for number in range (3):
    url = f"https://finance.naver.com/item/frgn.naver?code={code}&page={number+1}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    res.encoding = "euc-kr"

    soup = BeautifulSoup(res.text, "html.parser")

    # caption 기준으로 테이블 찾기
    table = soup.find("caption", string="외국인 기관 순매매 거래량").find_parent("table")
    rows = table.find_all("tr")

    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 9:
            data.append([c.get_text(strip=True) for c in cols])

    columns = [
        "날짜", "종가", "전일비", "등락률", "거래량",
        "기관 순매매량", "외국인 순매매량",
        "외국인 보유주수", "외국인 보유율"
    ]
    df = pd.DataFrame(data, columns=columns)
    print(df)



