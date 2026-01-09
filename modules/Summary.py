import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/item/coinfo.naver?code=005930&target=finsum_more"
headers = {
        "User-Agent": "Mozilla/5.0 ",
        "Referer": f"https://finance.naver.com"
        }
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')

# 1. 단위 정보 추출
unit_text = soup.find("span", id="unit_text").get_text(strip=True)
# 결과: * 단위 : 억원, %, 배, 주 * 분기: 순액기준

# 2. 셀렉트 박스의 옵션들 추출 (어떤 재무기준이 있는지)
options = soup.find_all("option")
fin_options = [opt.get_text() for opt in options]

# 3. 간단한 판다스 데이터프레임화 (메타데이터 저장용)
df_info = pd.DataFrame({
    "항목": ["단위", "재무기준옵션"],
    "내용": [unit_text, ", ".join(fin_options)]
})

print(df_info)