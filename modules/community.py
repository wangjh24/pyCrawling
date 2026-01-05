import requests 
from bs4 import BeautifulSoup
def get_community(stock_code):
    try: 
        #URL 주소         
        url = f"https://finance.naver.com/item/frgn.naver?code={stock_code}"
        headers = {
            "User-Agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64)"
                            "AppleWebKit/537.36(KHTML,like Gecko)"
                            "Chrome/120.0.0.0 safari/537.36"
        }
        response = requests.get(url,headers=headers,timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response, "html_parser")
    except requests.exceptions.RequestException as e:
        print(f"[에러] 네트워크 요청 실패: {e}")
        return None
    except Exception as e:
        print(f"[에러] 데이터 파싱 실패: {e}")
        return None
    