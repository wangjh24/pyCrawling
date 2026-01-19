from fastapi import APIRouter, HTTPException
from backend.database import engine
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

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

    try:
        res = requests.get(url, headers=headers)
        # 한글 깨짐 방지를 위해 content 사용
        soup = BeautifulSoup(res.content, "html.parser")

        # 재무제표 테이블 선택
        table = soup.select_one('.section.cop_analysis div.sub_section table')

        if not table:
            print(f"[{code}] 데이터를 찾을 수 없습니다.")
            return None

        # 1. 날짜 헤더 추출 (연간 4개, 분기 6개 순서)
        thead = table.find('thead')
        dates = [th.get_text(strip=True) for th in thead.find_all('tr')[1].find_all('th')]

        # 2. 본문 데이터 추출 및 피벗 구조 생성
        tbody = table.find('tbody')
        financial_data = {}

        for tr in tbody.find_all('tr'):
            th_tag = tr.find('th')
            if not th_tag: continue

            item_name = th_tag.get_text(strip=True)
            values = []
            for td in tr.find_all('td'):
                val = td.get_text(strip=True).replace(',', '')
                # 수치 변환 (N/A, 빈값 처리)
                try:
                    values.append(float(val) if val not in ['', '-', 'N/A'] else np.nan)
                except ValueError:
                    values.append(np.nan)

            # 데이터 길이가 날짜 수와 맞지 않을 경우를 대비해 슬라이싱
            financial_data[item_name] = values[:len(dates)]

        # 3. 데이터프레임 생성
        df = pd.DataFrame(financial_data, index=dates)
        df.index.name = 'date'
        df = df.reset_index()

        # 영문 컬럼명 매핑
        rename_map = {
            '매출액': 'revenue',
            '영업이익': 'operating_income',
            '당기순이익': 'net_income',
            '영업이익률': 'operating_margin',
            '순이익률': 'net_profit_margin',
            'ROE(지배주주)': 'roe',
            '부채비율': 'debt_to_equity',
            '당좌비율': 'quick_ratio',
            '유보율': 'reserve_ratio',
            'EPS(원)': 'eps',
            'PER(배)': 'per',
            'BPS(원)': 'bps',
            'PBR(배)': 'pbr',
            '주당배당금': 'dps',
            '시가배당률': 'dividend_yield',
            '배당성향': 'payout_ratio'
        }
        df = df.rename(columns=rename_map)

        # 4. 연간(Annual) / 분기(Quarterly) 구분 컬럼 추가
        # 네이버 기준 앞 4개는 연간, 뒤 6개는 분기 데이터
        types = []
        for i in range(len(dates)):
            if i < 4:
                types.append('연간')
            else:
                types.append('분기')
        df['type'] = types

        # 종목코드 삽입
        df.insert(0, 'code', code)

        # DB 저장 (해당 종목의 데이터만 교체하는 것이 좋으나, 요청대로 replace 사용)
        # 실제 운영시에는 if_exists='append'와 unique 제약조건을 활용하는 것을 권장합니다.
        df.to_sql('summary', engine, if_exists='replace', index=False)

        return df.replace({np.nan: None}).to_dict(orient="records")

    except Exception as e:
        print(f"Crawling Error: {e}")
        return None


@router.get("/{code}")
async def get_summary(code: str):
    # 1. 크롤링 및 DB 업데이트
    result = summary_crawl_and_save(code)

    if result is None:
        # 크롤링 실패 시 DB에서 기존 데이터 조회
        try:
            df = pd.read_sql(f"SELECT * FROM summary WHERE code = '{code}'", engine)
            if df.empty:
                raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
            result = df.to_dict(orient="records")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return result