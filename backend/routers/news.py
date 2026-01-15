from fastapi import APIRouter, HTTPException
from backend.database import engine
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qs
from sqlalchemy import text
router = APIRouter(
    prefix="/api/news",
    tags=["news Info"],
    responses={404: {"description": "Not found"}},
)


def news_crawl_and_save(code: str):
    url = f"https://finance.naver.com/item/news_news.naver?code={code}"
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

    try:
        existing_news = pd.read_sql(f"SELECT title FROM news WHERE code = '{code}'", engine)
        existing_titles = set(existing_news['title'].tolist())
    except Exception:
        existing_titles = set()

    all_data = []

    # 실제로는 너무 많은 페이지를 크롤링하면 차단되므로 범위를 제한하는 것이 좋습니다 (예: 5페이지)
    for number in range(1, min(page_count + 1, 6)):
        page_url = f"{url}&page={number}"
        res = requests.get(page_url, headers=headers)
        res.encoding = "euc-kr"
        soup = BeautifulSoup(res.text, "html.parser")

        news_items = soup.select("td.title a")
        if not news_items:
            break
        unique_news_items = {news.get_text(strip=True): news['href'] for news in news_items}

        for title_text, link in unique_news_items.items():
            # [핵심] 이미 DB에 있는 제목이면 상세 페이지에 접속하지 않고 스킵
            if title_text in existing_titles:
                continue

            try:
                # 상세 페이지 URL 파싱
                parsed_url = urlparse(link)
                params = parse_qs(parsed_url.query)

                # 네이버 금융 뉴스 링크가 아닌 경우 예외 처리
                if 'office_id' not in params or 'article_id' not in params:
                    continue

                office_id = params.get('office_id')[0]
                article_id = params.get('article_id')[0]
                real_link = f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}"

                # 상세 페이지 요청
                res_detail = requests.get(real_link, headers=headers, timeout=5)
                soup_detail = BeautifulSoup(res_detail.text, "html.parser")

                # 데이터 추출 (요소가 없는 경우를 대비해 find 사용)
                title_tag = soup_detail.find("h2", id="title_area")
                content_tag = soup_detail.find("article", id="dic_area")
                date_tag = soup_detail.find("span", class_="media_end_head_info_datestamp_time")

                if title_tag and content_tag:
                    title = title_tag.get_text(strip=True)
                    # 본문은 너무 길면 DB 성능에 좋지 않으므로 1000자 내외로 자르는 것을 권장
                    content = content_tag.get_text(strip=True)
                    date = date_tag.get_text(strip=True) if date_tag else "날짜 정보 없음"

                    all_data.append([title, content, date])
                    # 메모리 내 세트에도 추가하여 이번 루프 내 중복 방지
                    existing_titles.add(title)

            except Exception as e:
                print(f"상세 페이지 크롤링 에러 ({link}): {e}")
                continue

            # 3. 새로운 데이터가 있을 때만 DB에 저장
        if all_data:
            new_df = pd.DataFrame(all_data, columns=["title", "content", "date"])
            new_df.insert(0, "code", code)
            try:
                new_df.to_sql('news', engine, if_exists='append', index=False)
            except Exception as e:
                print(f"DB 저장 에러: {e}")

        return True


@router.get("/{code}")
async def get_news(code: str):
    # 1. 새로운 뉴스 크롤링 및 저장
    news_crawl_and_save(code)

    # 2. DB에서 해당 종목의 전체 뉴스 최신순으로 가져오기
    try:
        query = text("SELECT * FROM news WHERE code = :code ORDER BY date DESC")
        df = pd.read_sql(query, engine, params={"code": code})

        if df.empty:
            return []  # 데이터가 없으면 빈 리스트 반환

        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB 조회 에러: {str(e)}")
