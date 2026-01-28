import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def clean_value(val, is_change=False):
    """텍스트 데이터를 숫자로 변환"""
    if not val or val == '-' or val == '0': return 0
    clean_val = re.sub(r'[^\d.-]', '', str(val).replace(',', ''))
    try:
        num = float(clean_val)
        if is_change and ('하락' in str(val) or '▼' in str(val) or '내림' in str(val)):
            return -abs(num)
        return num
    except ValueError:
        return 0

def get_cleaned_data(code: str) -> pd.DataFrame:
    """네이버 금융 크롤링 및 데이터프레임 반환"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = []
    
    # 속도를 위해 페이지 수를 5로 조정 (필요시 늘리세요)
    for number in range(5): 
        url = f"https://finance.naver.com/item/frgn.naver?code={code}&page={number+1}"
        res = requests.get(url, headers=headers)
        res.encoding = "euc-kr"
        soup = BeautifulSoup(res.text, "html.parser")

        # 테이블 찾기 예외처리
        caption = soup.find("caption", string="외국인 기관 순매매 거래량")
        if not caption:
            continue
            
        table = caption.find_parent("table")
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 9:
                row_data = [c.get_text(strip=True) for c in cols]
                data.append(row_data)

    columns = [
        "date", "close_price", "change", "change_rate", "volume",
        "institution_net_volume", "foreign_net_volume",
        "foreign_holding_shares", "foreign_holding_ratio"
    ]
    
    df = pd.DataFrame(data, columns=columns)
    if df.empty:
        raise ValueError("데이터를 수집하지 못했습니다.")

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['change'] = df['change'].apply(lambda x: clean_value(x, is_change=True))
    
    numeric_cols = ['close_price', 'change_rate', 'volume', 'institution_net_volume', 
                    'foreign_net_volume', 'foreign_holding_shares', 'foreign_holding_ratio']
    for col in numeric_cols:
        df[col] = df[col].apply(lambda x: clean_value(x))

    df = df.dropna().sort_values('date').reset_index(drop=True)
    return df

def run_xgboost_analysis(df: pd.DataFrame):
    """XGBoost 학습 및 예측"""
    # 특성 및 타겟 생성
    df['target'] = df['change'].shift(-1)
    
    features = ["close_price", "change", "change_rate", "volume", 
                "institution_net_volume", "foreign_net_volume", "foreign_holding_ratio"]
    
    # 예측용 마지막 데이터 (내일 예측을 위해 사용)
    latest_data = df.iloc[[-1]][features]
    current_price = latest_data['close_price'].values[0]
    
    # 학습용 데이터
    train_df = df.dropna(subset=['target'])
    
    if len(train_df) < 10: # 데이터가 너무 적으면 예외 처리
        raise ValueError("학습할 데이터가 충분하지 않습니다.")

    X = train_df[features]
    y = train_df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = xgb.XGBRegressor(
        n_estimators=100, learning_rate=0.1, max_depth=5, objective='reg:squarederror'
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    
    # 결과 예측
    next_day_change = model.predict(latest_data)[0]
    
    return next_day_change, rmse, current_price