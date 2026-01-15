from fastapi import APIRouter, HTTPException
from backend.database import engine
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from sqlalchemy import text

router = APIRouter(
    prefix="/api/board",
    tags=["board Info"],
)


def board_crawl_and_save(code: str):
    list_url = f"https://finance.naver.com/item/board.naver?code={code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://finance.naver.com"
    }

    try:
        # 1. 기존 데이터 확인 (중복 방지)
        existing_board = pd.read_sql(f"SELECT title FROM board WHERE code = '{code}'", engine)
        existing_titles = set(existing_board['title'].tolist())
    except Exception:
        existing_titles = set()

    all_data = []

    # 최근 2페이지 정도만 크롤링 (성능 타협)
    for number in range(1, 3):
        page_url = f"{list_url}&page={number}"
        res = requests.get(page_url, headers=headers)
        res.encoding = "euc-kr"
        soup = BeautifulSoup(res.text, "html.parser")

        board_items = soup.select("td.title a")
        if not board_items: break

        for item in board_items:
            title_text = item.get('title') or item.get_text(strip=True)
            link = item['href']

            if title_text in existing_titles: continue

            try:
                # 상세 페이지 진입
                detail_url = "https://finance.naver.com" + link
                detail_headers = headers.copy()
                detail_headers["Referer"] = page_url

                res_detail = requests.get(detail_url, headers=detail_headers)
                soup_detail = BeautifulSoup(res_detail.text, "html.parser")

                title_tag = soup_detail.find("strong", class_="c p15")
                date_tag = soup_detail.find("th", class_="gray03 p9 tah")
                iframe = soup_detail.find('iframe', id='contents')

                if not iframe: continue

                # iframe 내부 본문 추출
                iframe_url = iframe['src']
                if iframe_url.startswith('/'):
                    iframe_url = "https://finance.naver.com" + iframe_url

                iframe_headers = headers.copy()
                iframe_headers["Referer"] = detail_url
                res_iframe = requests.get(iframe_url, headers=iframe_headers)
                soup_iframe = BeautifulSoup(res_iframe.text, 'html.parser')

                # JSON 데이터 파싱 (본문 내용)
                target_script = soup_iframe.find('script', id='__NEXT_DATA__')
                if target_script:
                    jsondata = json.loads(target_script.string)
                    # 구조 변경 대응을 위한 safe get
                    try:
                        content_html = \
                        jsondata['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['result'][
                            'contentHtml']
                        inner_soup = BeautifulSoup(content_html, 'html.parser')
                        content = inner_soup.get_text(" ", strip=True)
                    except (KeyError, IndexError):
                        content = "본문을 가져올 수 없습니다."
                else:
                    content = "데이터 스크립트를 찾을 수 없습니다."

                all_data.append({
                    "code": code,
                    "title": title_tag.get_text(strip=True) if title_tag else title_text,
                    "content": content,
                    "date": date_tag.get_text() if date_tag else "날짜없음"
                })
                existing_titles.add(title_text)  # 이번 루프 내 중복 방지

            except Exception as e:
                print(f"Error on {link}: {e}")
                continue

    # 2. 새로운 데이터 DB 저장
    if all_data:
        new_df = pd.DataFrame(all_data)
        new_df.to_sql('board', engine, if_exists='append', index=False)

    return True


@router.get("/{code}")
async def get_board(code: str):
    board_crawl_and_save(code)
    try:
        query = text("SELECT * FROM board WHERE code = :code ORDER BY date DESC LIMIT 50")
        df = pd.read_sql(query, engine, params={"code": code})
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))