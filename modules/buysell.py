import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
from sqlalchemy import create_engine

def buysell_get(code):
    sys.stdout.reconfigure(encoding='utf-8')
    
    engine = create_engine('postgresql://test:1234@localhost:5432/PyCrawling')
    table_name = 'buysell'+code

    url = f"https://finance.naver.com/item/frgn.naver?code={code}"
    headers = {'User-Agent': 'Mozilla/5.0'} 
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    last_page_tag = soup.select_one('td.pgRR > a')

    if last_page_tag:
        href = last_page_tag.get('href')
        page = href.split('page=')[-1]    

    for number in range (int(page)):
        url = f"https://finance.naver.com/item/frgn.naver?code={code}&page={number+1}"

        res = requests.get(url, headers=headers)
        res.encoding = "euc-kr"

        soup = BeautifulSoup(res.text, "html.parser")

        table = soup.find("caption", string="외국인 기관 순매매 거래량").find_parent("table")
        rows = table.find_all("tr")

        data = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 9:
                data.append([c.get_text(strip=True) for c in cols])

        columns = [
            "date", "close_price", "change", "chage_rate", "volume",
            "insstitution_net_volume", "foreign_net_volume",
            "foreign_holding_shares", "foreign_holding_ratio"
        ]
    df = pd.DataFrame(data, columns=columns)
        #print(df)
    try : 
        df.to_sql(table_name,engine,if_exists='replace',index=False)
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



