from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
from backend.database import engine  # DB 엔진 경로 확인 필요
from mecab import MeCab
from wordcloud import WordCloud
from collections import Counter
import base64
from io import BytesIO
import os

# 라우터 설정
router = APIRouter(
    prefix="/api/news_mecab",
    tags=["mecab"],
    responses={404: {"description": "Not found"}}
)

# 응답 모델 정의
class AnalysisResponse(BaseModel):
    stock_code: str
    image: str
    keywords: list

@router.get("/{code}", response_model=AnalysisResponse)
async def get_analysis(code: str):
    try:
        # 1. DB에서 데이터 로드 (기존에 수집된 news 테이블 기준)
        query = f"SELECT title, content FROM news WHERE code = '{code}'"
        df = pd.read_sql(query, engine)

        if df.empty:
            raise HTTPException(status_code=404, detail="분석할 뉴스 데이터가 DB에 없습니다. 먼저 뉴스를 수집해주세요.")

        # 2. 형태소 분석 (제목 + 본문)
        full_text = " ".join(df['title'].astype(str)) + " " + " ".join(df['content'].astype(str))
        mecab = MeCab()
        nouns = mecab.nouns(full_text)
        
        # 불용어 처리 (분석에 방해되는 단어 제거)
        stop_words = ['오늘', '기자', '뉴스', '무단', '전재', '배포', '금지', '것으로', '이번', '대해']
        filtered_nouns = [n for n in nouns if len(n) > 1 and n not in stop_words]
        
        count = Counter(filtered_nouns)
        if not count:
            raise HTTPException(status_code=400, detail="유효한 명사 데이터가 부족하여 분석할 수 없습니다.")
            
        # 프런트엔드 리스트용 상위 20개 단어
        top_keywords = [{"text": k, "value": v} for k, v in count.most_common(20)]

        # 3. 워드클라우드 이미지 생성
        # 운영체제별 폰트 경로 설정 (윈도우: malgun.ttf, 리눅스: NanumGothic.ttf)
        font_path = "malgun.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
        
        try:
            wc = WordCloud(
                font_path=font_path, 
                background_color="white", 
                width=800, 
                height=500,
                max_words=100
            )
            cloud = wc.generate_from_frequencies(dict(count.most_common(100)))
        except:
            # 폰트 경로 오류 시 기본 폰트로 생성
            wc = WordCloud(background_color="white", width=800, height=500)
            cloud = wc.generate_from_frequencies(dict(count.most_common(100)))
        
        # 4. 이미지를 Base64 문자열로 변환
        img_buffer = BytesIO()
        cloud.to_image().save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        return {
            "stock_code": code,
            "image": f"data:image/png;base64,{img_base64}",
            "keywords": top_keywords
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))