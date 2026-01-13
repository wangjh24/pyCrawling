# from modules import Info 
# from modules import buysell
# from modules import news
# from modules import community
# from modules import Summary
# if __name__ == "__main__":
#   code = input("코드를 입력하세요:")
#   while True:
#     service = input("원하는 서비스를 누르세요 1:종합정보 2:매매투자 동향 3:종목 뉴스 4:종목 토론 etc: 종료") 
#     if service == "1": 
#       Info.info_put(code)
#       Info.info_get(code)
#       Summary.Summary_put(code)
#       Summary.Summary_get(code)
#     elif service == "2":   
#       buysell.buysell_put(code)
#       buysell.buysell_get(code)

#     elif service == "3": 
#       news.news_put(code)
#       news.news_get(code)

#     elif service == "4":
#       community.community_put(code)
#       community.community_get(code)

#     else : 
#       print("종료합니다")
#       break
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정 (프런트엔드에서 API 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Vite 기본 포트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}