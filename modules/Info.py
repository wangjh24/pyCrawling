import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import psycopg2
from sqlalchemy import create_engine

def info_get(code):
    sys.stdout.reconfigure(encoding='utf-8')

    engine = create_engine('postgresql://test:1234@localhost:5432/PyCrawling')
    table_name = 'info'+code
    url = f"https://finance.naver.com/item/main.naver?code={code}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

    table = table = soup.find("caption", string="거래원 정보").find_parent("table")
    rows = table.select("tbody tr")

    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 4:
            data.append([c.get_text(strip=True) for c in cols])
    
    columns = ["sell_rank", "sell_volume", "buy_rank", "buy_volume"]
    df = pd.DataFrame(data, columns=columns)
    try : 
        df.to_sql(table_name,engine,if_exists='fail',index=False)
        print(f"{table_name}를 저장했습니다.")
    except ValueError:
        print(f"----------------")
    except Exception as e:
        print (f"저장 실패 :에러({e})")

    print("\n--- DB 테이블 내용 출력 ---")
    try:
        df_from_db = pd.read_sql(f'SELECT * FROM "{table_name}"', engine)
        print(df_from_db)
    except Exception as e:
        print(f"출력 실패: 테이블이 존재하지 않거나 에러가 발생했습니다. ({e})")