# 1. Python 3.10 슬림 이미지를 기반으로 사용
FROM python:3.10-slim

# 2. 필수 시스템 패키지 및 MeCab 설치
# news_mecab.py의 기능을 위해 MeCab과 한글 폰트(Nanum) 설치가 필요합니다.
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    fonts-nanum \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 의존성 파일 복사 및 설치
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 전체 소스 코드 복사
# 현재 로컬의 파일들을 컨테이너 내부 /app으로 복사합니다.
COPY . .

# 6. 환경 변수 설정 (Python 경로 설정)
ENV PYTHONPATH=/app

# 7. 포트 노출 (FastAPI 기본 포트)
EXPOSE 8000

# 8. 애플리케이션 실행
# main.py가 루트가 아닌 backend 폴더 내부에 있다면 경로 수정이 필요할 수 있습니다.
# 제공된 main.py 내용을 기준으로 실행 명령어를 작성합니다.
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]