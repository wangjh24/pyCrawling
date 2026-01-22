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

            # td가 4개인 정상적인 데이터 행만 추출 (space 행 제외)
            if len(cols) == 4:
                # 콤마 제거 및 텍스트 정리
                sell_rank = cols[0].get_text(strip=True)
                sell_vol = cols[1].get_text(strip=True).replace(',', '')
                buy_rank = cols[2].get_text(strip=True)
                buy_vol = cols[3].get_text(strip=True).replace(',', '')

                data.append([sell_rank, sell_vol, buy_rank, buy_vol])

        if not data:
            print("추출된 데이터가 없습니다.")
            return None

        columns = ["sell_rank", "sell_volume", "buy_rank", "buy_volume"]
        df = pd.DataFrame(data, columns=columns)

        # 데이터 타입 변환 (숫자형으로 저장해야 나중에 활용하기 좋습니다)
        df["sell_volume"] = pd.to_numeric(df["sell_volume"], errors='coerce')
        df["buy_volume"] = pd.to_numeric(df["buy_volume"], errors='coerce')
        df.insert(0, "code", code)

        # 2. DB 저장
        # if_exists='append'이므로 매번 실행 시 누적됩니다.
        # 최신 데이터만 유지하려면 'replace'를 고려하세요.
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


