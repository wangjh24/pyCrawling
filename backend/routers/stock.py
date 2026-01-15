from fastapi import APIRouter, HTTPException
from backend.database import engine
import requests
from bs4 import BeautifulSoup
import pandas as pd

router = APIRouter(
    prefix="/api/stock",
    tags=["Stock Info"],
    responses={404: {"description": "Not found"}},
)

def stock_crawl_and_save(code: str):
    url = f"https://finance.naver.com/item/main.naver?code={code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://finance.naver.com"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 거래원 정보 추출
    try:
        caption = soup.find("caption", string="거래원 정보")
        if not caption:
            return None

        table = caption.find_parent("table")
        rows = table.select("tbody tr")

        data = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 4:
                data.append([c.get_text(strip=True) for c in cols])

        columns = ["sell_rank", "sell_volume", "buy_rank", "buy_volume"]
        df = pd.DataFrame(data, columns=columns)
        df.insert(0, "code", code)

        # DB 저장 (replace)
        df.to_sql('stock', engine, if_exists='replace', index=False)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Crawling Error: {e}")
        return None

@router.get("/{code}")
async def get_stock(code: str):
    # 1. 크롤링 및 DB 업데이트
    result = stock_crawl_and_save(code)

    if result is None:
        # 크롤링 실패 시 DB에서 기존 데이터라도 찾음
        try:
            df = pd.read_sql(f"SELECT * FROM stock WHERE code = '{code}'", engine)
            if df.empty:
                raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
            result = df.to_dict(orient="records")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return result


