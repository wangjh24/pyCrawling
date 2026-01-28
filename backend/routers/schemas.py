from pydantic import BaseModel
from typing import Optional

class StockPredictionResponse(BaseModel):
    code: str
    current_price: float
    predicted_change: float  # 예측된 변동폭
    predicted_price: float   # 예측된 내일 가격 (단순 계산)
    rmse: float              # 모델 오차
    direction: str           # 상승/하락/보합
    message: str