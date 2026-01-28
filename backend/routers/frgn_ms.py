from fastapi import APIRouter, HTTPException
from .schemas import StockPredictionResponse
from .services import get_cleaned_data, run_xgboost_analysis
router = APIRouter(
    prefix="/api/predict",
    tags=["machine Info"],
    responses={404: {"description": "Not found"}},
)
@router.get("/{code}", response_model=StockPredictionResponse)
def predict_stock(code: str):
    """
    특정 종목 코드에 대해 크롤링 후 XGBoost 예측 결과를 반환합니다.
    """
    try:
        # 1. 데이터 수집
        df = get_cleaned_data(code)
        
        # 2. 분석 수행
        prediction, rmse, current_price = run_xgboost_analysis(df)
        
        # 3. 결과 포맷팅
        direction = "상승" if prediction > 0 else "하락"
        if prediction == 0: direction = "보합"
        
        message = f"약 {abs(prediction):.0f}원 {direction}할 것으로 예측됩니다."
        
        return StockPredictionResponse(
            code=code,
            current_price=current_price,
            predicted_change=round(float(prediction), 2),
            predicted_price=current_price + prediction,
            rmse=round(float(rmse), 2),
            direction=direction,
            message=message
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")