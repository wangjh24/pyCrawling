from fastapi import APIRouter, HTTPException
from backend.database import engine
import requests
from bs4 import BeautifulSoup
import pandas as pd

router = APIRouter(
    prefix="/api/summary",
    tags=["summary Info"],
    responses={404: {"description": "Not found"}},
)

def summary_crawl_and_save(code: str):
    url = f"https://finance.naver.com/item/main.naver?code={code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://finance.naver.com"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 거래원 정보 추출
    try:
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

        df.insert(0, "code", code)

        # DB 저장 (replace)
        df.to_sql('summary', engine, if_exists='replace', index=False)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Crawling Error: {e}")
        return None

@router.get("/{code}")
async def get_summary(code: str):
    # 1. 크롤링 및 DB 업데이트
    result = summary_crawl_and_save(code)

    if result is None:
        # 크롤링 실패 시 DB에서 기존 데이터라도 찾음
        try:
            df = pd.read_sql(f"SELECT * FROM summary WHERE code = '{code}'", engine)
            if df.empty:
                raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
            result = df.to_dict(orient="records")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return result


