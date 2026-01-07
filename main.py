from modules import Info 
from modules import buysell
from modules import news
if __name__ == "__main__":
  while (1):
    code = input("코드를 입력하세요:")
    service = input("원하는 서비스를 누르세요 1:종합정보 2:매매투자 동향") 
    if service == 1: 
      Info.info_get("005930")
    elif service == 2:   
      buysell.buysell_get("005930")
    elif service == 3: 
      news.news_get("005930")