from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import stock
from backend.routers import frgn
from backend.routers import board
from backend.routers import news
from backend.routers import summary
from backend.routers import news_mecab
from backend.routers import frgn_ms
import uvicorn

app = FastAPI()

# React(5173번 포트)와의 통신을 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # React 기본 포트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock.router)
app.include_router(frgn.router)
app.include_router(board.router)
app.include_router(news.router)
app.include_router(summary.router)
app.include_router(news_mecab.router)
app.include_router(frgn_ms.router)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)