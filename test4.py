import requests
from bs4 import BeautifulSoup

# 1. 크롤링할 대상 URL
target_url = "https://finance.naver.com/" # 예시 URL입니다. 실제 사용 시 주의

# 2. 웹 페이지 요청
try:
    response = requests.get(target_url, timeout=5) # 5초 타임아웃 설정
    response.raise_for_status() # 오류 발생 시 예외 발생
except requests.exceptions.RequestException as e:
    print(f"Error during requests to {target_url} : {e}")
    exit()

# 3. HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 4. 모든 <a> 태그 (링크) 찾기
links = soup.find_all('') # <a> 태그를 모두 찾습니다.

# 5. 링크의 href 속성 값 출력
print(f"--- {target_url} 에서 찾은 링크들 ---")
for link in links:
    href = link.get('href') # <a> 태그의 'href' 속성 값을 가져옵니다.
    if href: # href 속성이 있는 경우만 출력
        print(href)

print("--- 크롤링 완료 ---")
