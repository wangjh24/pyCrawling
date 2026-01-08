import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs  
import time
import pandas as pd
from sqlalchemy import create_engine
import sys
import json

def community_get(code):
    sys.stdout.reconfigure(encoding='utf-8')
    
    engine = create_engine('postgresql://test:1234@localhost:5432/PyCrawling')
    table_name = 'board'+code

    url = f"https://finance.naver.com/item/board.naver?code={code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ",
        "Referer": f"https://finance.naver.com"
        } 
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    last_page_tag = soup.select_one('td.pgRR > a')

    if last_page_tag:
        href = last_page_tag.get('href')
        page = href.split('page=')[-1]    

    columns = ["title","contant"]
    data = []
    for number in range(int(1)): #page
        url = f"https://finance.naver.com/item/board.naver?code={code}&page={number+1}"

        response = requests.get(url, headers=headers)
        response.encoding = 'euc-kr' 
        soup = BeautifulSoup(response.text, "html.parser")

        board_items = soup.select("td.title a")
            
        unique_board_items = list({board['href']: board for board in board_items}.values())
        for board in unique_board_items:
            link = board['href']
            real_link = f"https://finance.naver.com"+link
            res1 = requests.get(real_link, headers=headers)
            soup1 = BeautifulSoup(res1.text, "html.parser")
            
            title_tag = soup1.find("strong", class_="c p15")  
            iframe = soup1.find('iframe', id='contents')
            iframe_url = iframe['src']
            res_iframe = requests.get(iframe_url,headers=headers)
            soup_iframe = BeautifulSoup(res_iframe.text, 'html.parser')
            target_text = soup_iframe.find('script', id='__NEXT_DATA__')
            jsondata = json.loads(target_text.string)
            content_html = jsondata['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['result']['contentHtml']
            inner_soup = BeautifulSoup(content_html, 'html.parser')
            testlist = inner_soup.find_all('p', class_='se-text-paragraph')
            textlist = []
            
            for p in testlist:
                text = p.get_text().strip()
                text = text.replace('\u200b', '')
    
            if text: 
                textlist.append(text)

            
            title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
            
            
            data.append([title,*textlist])
            time.sleep(0.5)
    df =pd.DataFrame(data,columns=columns)

            
                    
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
    finally:
        engine.dispose()