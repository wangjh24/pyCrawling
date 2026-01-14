import React, { useState } from "react";
import axios from "axios";

function App() {
  const [code, setCode] = useState("");
  const [stockData, setStockData] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!code) return alert("종목 코드를 입력하세요.");

    setLoading(true);
    try {
      // FastAPI 엔드포인트 호출
      const response = await axios.get(
        `http://localhost:8000/api/stock/${code}`
      );
      setStockData(response.data);
    } catch (error) {
      console.error("데이터 호출 실패:", error);
      alert("데이터를 가져오는데 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>주식 종목 정보 조회</h1>

      <div>
        <input
          type="text"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="종목코드 (예: 005930)"
        />
        <button onClick={handleSearch}>
          {loading ? "조회 중..." : "조회"}
        </button>
      </div>

      {stockData.length > 0 && (
        <table border="1">
          <thead>
            <tr>
              <th>매도상위</th>
              <th>매도거래량</th>
              <th>매수상위</th>
              <th>매수거래량</th>
            </tr>
          </thead>
          <tbody>
            {stockData.map((item, index) => (
              <tr key={index}>
                <td>{item.sell_rank}</td>
                <td>{item.sell_volume}</td>
                <td>{item.buy_rank}</td>
                <td>{item.buy_volume}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
