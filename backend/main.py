from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import info
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

app.include_router(info.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)