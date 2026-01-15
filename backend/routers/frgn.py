from fastapi import APIRouter, HTTPException
from backend.database import engine
import requests
from bs4 import BeautifulSoup
import pandas as pd

router = APIRouter(
    prefix="/api/frgn",
    tags=["frgn Info"],
    responses={404: {"description": "Not found"}},
)


def buysell_crawl_and_save(code: str):
    url = f"https://finance.naver.com/item/frgn.naver?code={code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://finance.naver.com"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 페이지 수 계산 안전하게 처리
    last_page_tag = soup.select_one('td.pgRR > a')
    page_count = 1
    if last_page_tag:
        page_count = int(last_page_tag.get('href').split('page=')[-1])

    all_data = []  # 모든 페이지 데이터를 담을 리스트

    # 실제로는 너무 많은 페이지를 크롤링하면 차단되므로 범위를 제한하는 것이 좋습니다 (예: 5페이지)
    for number in range(1, min(page_count + 1, 6)):
        page_url = f"{url}&page={number}"
        res = requests.get(page_url, headers=headers)
        res.encoding = "euc-kr"
        soup = BeautifulSoup(res.text, "html.parser")

        table = soup.find("caption", string="외국인 기관 순매매 거래량").find_parent("table")  # 더 정확한 셀렉터 사용
        if not table:
            continue

        rows = table.select("tr")
        for row in rows:
            cols = row.find_all("td")
            # 날짜 데이터가 있는 행만 추출 (보통 9개 컬럼)
            if len(cols) == 9 and cols[0].get_text(strip=True):
                raw_data = [c.get_text(strip=True).replace(",", "") for c in cols]
                change_text = raw_data[2]  # 예: "상승200", "하락100", "0"

                change_1 = ""  # 상승, 하락, 보합
                change_2 = 0  # 수치

                if "상승" in change_text:
                    change_1 = "상승"
                    change_2 = change_text.replace("상승", "")
                elif "하락" in change_text:
                    change_1 = "하락"
                    change_2 = change_text.replace("하락", "")
                else:
                    change_1 = "보합"
                    change_2 = change_text.replace("보합","")

                # 새로운 리스트 구성 (change 대신 change_1, change_2 삽입)
                processed_row = [
                    raw_data[0],  # date
                    raw_data[1],  # close_price
                    change_1,  # change_1 (상태)
                    change_2,  # change_2 (수치)
                    raw_data[3],  # change_rate
                    raw_data[4],  # volume
                    raw_data[5],  # institution_net_volume
                    raw_data[6],  # foreign_net_volume
                    raw_data[7],  # foreign_holding_shares
                    raw_data[8]  # foreign_holding_ratio
                ]
                all_data.append(processed_row)

    if not all_data:
        return None

    columns = [
        "date", "close_price", "change_val","change", "chage_rate", "volume",
        "insstitution_net_volume", "foreign_net_volume",
        "foreign_holding_shares", "foreign_holding_ratio"
    ]

    df = pd.DataFrame(all_data, columns=columns)
    df.insert(0, "code", code)

    try:
        # 여기서는 간단하게 일단 저장 후 리턴
        df.to_sql('frgn', engine, if_exists='append', index=False)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"DB Save Error: {e}")
        return None

@router.get("/{code}")
async def get_buysell(code: str):
    # 1. 크롤링 및 DB 업데이트
    result = buysell_crawl_and_save(code)

    if result is None:
        # 크롤링 실패 시 DB에서 기존 데이터라도 찾음
        try:
            df = pd.read_sql(f"SELECT * FROM frgn WHERE code = '{code}'", engine)
            if df.empty:
                raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
            result = df.to_dict(orient="records")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return result