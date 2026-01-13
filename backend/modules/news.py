import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs  
import time
import pandas as pd
from sqlalchemy import create_engine
import sys


sys.stdout.reconfigure(encoding='utf-8')
engine = create_engine('postgresql://test:1234@localhost:5432/PyCrawling')


def news_put(code):
    table_name = 'news'
    headers = {
        "User-Agent": "Mozilla/5.0 ",
        "Referer": f"https://finance.naver.com"
        }
    url = f"https://finance.naver.com/item/frgn.naver?code={code}" 
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    last_page_tag = soup.select_one('td.pgRR > a')

    if last_page_tag:
        href = last_page_tag.get('href')
        page = href.split('page=')[-1]    

    columns = ["title","contant","date"]
    data = []
    for number in range(int(1)): #page
        url = f"https://finance.naver.com/item/news_news.naver?code={code}&page={number+1}"

        response = requests.get(url, headers=headers)
        response.encoding = 'euc-kr' 
        soup = BeautifulSoup(response.text, "html.parser")

        news_items = soup.select("td.title a")
            
        if not news_items:
            print("뉴스 항목을 찾지 못했습니다.")
        else:
            unique_news_items = list({news['href']: news for news in news_items}.values())
            for news in unique_news_items:
                link = news['href']
        
                parsed_url = urlparse(link)
                params = parse_qs(parsed_url.query)
        
                office_id = params.get('office_id')[0]
                article_id = params.get('article_id')[0]

                if office_id and article_id:
                    real_link = f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}"
            
                    res1 = requests.get(real_link, headers=headers)
                    soup1 = BeautifulSoup(res1.text, "html.parser")
            
                    title_tag = soup1.find("h2", id="title_area")  
                    area_tag = soup1.find("article", id="dic_area")
                    date_tag = soup1.find("span",class_="media_end_head_info_datestamp_time _ARTICLE_DATE_TIME")
                    title = title_tag.get_text(strip=True)
                    area = area_tag.get_text(strip=True) 
                    date = date_tag.get_text(strip=True)
                    
                    data.append([title,area,date])
                    time.sleep(0.5)
    df =pd.DataFrame(data,columns=columns)
    df.insert(0, 'code', code)                

            
                    
    try : 
        df.to_sql(table_name,engine,if_exists='append',index=False)
        print(f"{table_name}를 저장했습니다.")
    except ValueError:
        print(f"----------------------------------------------------------")
    except Exception as e:
        print (f"저장 실패 :에러({e})")
    finally:
        engine.dispose()

def news_get(code):
    table_name = 'news'

    print("\n--- DB 테이블 내용 출력 ---")
    try:
        df_from_db = pd.read_sql(f"SELECT * FROM {table_name} WHERE code = '{code}'", engine)
        print(df_from_db)
        
    except Exception as e:
        print(f"출력 실패: 테이블이 존재하지 않거나 에러가 발생했습니다. ({e})")
    finally:
        engine.dispose()