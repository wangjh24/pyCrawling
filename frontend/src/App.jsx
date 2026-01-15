import React, { useState } from "react";
import axios from "axios";

// API 기본 URL 설정
const API_BASE_URL = "http://localhost:8000/api";

function App() {
  const [code, setCode] = useState("");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("stock"); // 현재 선택된 탭

  // 탭 구성 정보
  const tabs = [
    { id: "frgn", name: "외인/기관", endpoint: "frgn" },
    { id: "news", name: "최신뉴스", endpoint: "news" },
    { id: "board", name: "종목토론", endpoint: "board" },
    { id: "stock", name: "매매동향", endpoint: "stock" },
  ];

  const handleSearch = async (targetTab = activeTab) => {
    if (!code) return alert("종목 코드를 입력하세요.");

    setLoading(true);
    setData([]); // 이전 데이터 초기화
  };

  // 탭 변경 핸들러
  const changeTab = (tabId) => {
    setActiveTab(tabId);
    if (code) handleSearch(tabId); // 코드가 입력되어 있다면 바로 검색
  };

  return (
    <div>
      <h1>주식 종목 정보 조회</h1>

      {/* 검색 바 */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="종목코드 (예: 005930)"
          style={{ padding: "8px", marginRight: "10px" }}
        />
        <button onClick={() => handleSearch()} disabled={loading}>
          {loading ? "조회 중..." : "데이터 조회"}
        </button>
      </div>
    </div>
  );
}

export default App;
