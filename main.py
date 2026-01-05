import requests
from bs4 import BeautifulSoup
from tabulate import tabulate  # pip install tabulate

def crawl_table(url):
    try:
        # 1. 웹 페이지 요청
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTP 오류 발생 시 예외

        # 2. HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. 첫 번째 테이블 찾기
        table = soup.find('table')
        if not table:
            print(" 테이블을 찾을 수 없습니다.")
            return

        # 4. 테이블 데이터 추출
        rows = []
        for tr in table.find_all('tr'):
            cols = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
            if cols:  # 빈 행 제외
                rows.append(cols)

        # 5. 표 형태로 출력
        print(tabulate(rows, headers="firstrow", tablefmt="grid"))

    except requests.exceptions.RequestException as e:
        print(f"요청 오류: {e}")
    except Exception as e:
        print(f"처리 중 오류 발생: {e}")

# 실행 예시
# if __name__ == "__main__":
#     test_url = "https://finance.naver.com/item/frgn.naver?code=005930"  # 예시 URL
#     crawl_table(test_url)
