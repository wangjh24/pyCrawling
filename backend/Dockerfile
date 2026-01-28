# backend/Dockerfile
FROM python:3.9-slim

# 1. 시스템 의존성 설치 (Mecab 빌드용)
RUN apt-get update && apt-get install -y \
    g++ curl git make --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 2. Mecab 및 한국어 사전 설치
RUN curl -sL https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | bash

WORKDIR /app

# 3. 라이브러리 설치 (캐시 활용을 위해 COPY 순서 중요)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 복사
COPY . .

# 5. 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]