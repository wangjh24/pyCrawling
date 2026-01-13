import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://test:1234@localhost:5432/PyCrawling')

def Summary_put(code):
    url = f"https://finance.naver.com/item/main.naver?code={code}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')

    table = soup.select_one('.section.cop_analysis div.sub_section table')
    table_name = "summary"

    if table:
        thead = table.find('thead')
        rows = thead.find_all('tr')
        dates = [th.text.strip() for th in rows[1].find_all('th')]
        
        unique_dates = []
        counts = {}
        for date in dates:
            if date in counts:
                counts[date] += 1
                unique_dates.append(f"{date}_{counts[date]}")
            else:
                counts[date] = 0
                unique_dates.append(date)

        tbody = table.find('tbody')
        data_list = []
        index_list = []
        
        for tr in tbody.find_all('tr'):
            th_tag = tr.find('th')
            if not th_tag: continue
            
            th_text = th_tag.get_text(strip=True)
            index_list.append(th_text)
            
            tds = [td.get_text(strip=True).replace(',', '') for td in tr.find_all('td')]
            tds = (tds + [''] * len(unique_dates))[:len(unique_dates)]
            data_list.append(tds)

        df = pd.DataFrame(data_list, index=index_list, columns=unique_dates)
        df.index.name = "item" 
        df = df.reset_index() 
        df.insert(0, "code", code)

        try: 
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"{table_name}에 {code} 데이터를 저장했습니다.")
        except Exception as e:
            print(f"저장 실패 : 에러({e})")

def Summary_get(code):
    table_name = "summary"
    print("\n--- DB 테이블 내용 출력 ---")

    try:
    
        query = f'SELECT * FROM "{table_name}" WHERE code = %s'
        df_from_db = pd.read_sql(query, engine, params=(code,))

        if df_from_db.empty:
            print(f"코드 {code}에 해당하는 데이터가 없습니다.")
        else:
            print(df_from_db)
    except Exception as e:
        print(f"출력 실패: {e}")

