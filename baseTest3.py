import requests
from bs4 import BeautifulSoup

def get_stock_price(stock_code):
    """
    네이버 금융에서 주식 현재가를 가져오는 함수
    :param stock_code: 종목 코드 (예: 삼성전자 '005930')
    :return: 현재가 (문자열) 또는 None
    """
    try:
        # 네이버 금융 주식 상세 페이지 URL
        url = f"https://finance.naver.com/item/main.nhn?code={stock_code}"
        
        # User-Agent 헤더 설정 (봇 차단 방지)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
        
        # HTML 요청
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # HTTP 오류 발생 시 예외
        
        # HTML 파싱
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 현재가 추출 (네이버 금융의 현재가 클래스명)
        price_tag = soup.select_one("p.no_today span.blind")
        if price_tag:
            return price_tag.text.strip()
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"[에러] 네트워크 요청 실패: {e}")
        return None
    except Exception as e:
        print(f"[에러] 데이터 파싱 실패: {e}")
        return None


if __name__ == "__main__":
    # 예시: 삼성전자(005930), 카카오(035720)
    stock_codes = ["005930", "035720"]

    for code in stock_codes:
        price = get_stock_price(code)
        if price:
            print(f"종목 코드 {code} 현재가: {price}원")
        else:
            print(f"종목 코드 {code}의 데이터를 가져올 수 없습니다.")