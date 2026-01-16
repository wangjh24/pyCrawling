import React, { useState } from "react";
import axios from "axios";
import RenderRow from "./RowRender";
import style from "./css/font.css";
const API_BASE_URL = "http://localhost:8000/api";

function TabPage() {
  const [code, setCode] = useState("");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("stock");

  const tabs = [
    { id: "stock", name: "종합정보", endpoint: "stock" },
    { id: "frgn", name: "외인/기관", endpoint: "frgn" },
    { id: "news", name: "최신뉴스", endpoint: "news" },
    { id: "board", name: "종목토론", endpoint: "board" },
    { id: "summary", name: "기업실적", endpoint: "summary" },
  ];

  const handleSearch = async (targetTab = activeTab) => {
    if (!code) return alert("종목코드를 입력하세요");

    setLoading(true);
    setData([]);
    try {
      const response = await axios.get(`${API_BASE_URL}/${targetTab}/${code}`);
      setData(response.data);
    } catch (error) {
      console.error("데이터 호출 실패:", error);
      alert("데이터가 없거나 서버 오류 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  const changeTab = (tabId) => {
    setActiveTab(tabId);
    if (code) handleSearch(tabId);
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
        <button onClick={() => handleSearch()} disabled={loading}>
          {loading ? "조회 중..." : "데이터 조회"}
        </button>
      </div>
      <div>
        {tabs.map((tab) => (
          <button key={tab.id} onClick={() => changeTab(tab.id)}>
            {tab.name}
          </button>
        ))}
      </div>

      {loading && <p>데이터를 불러오는 중...</p>}

      {!loading && data && data.length > 0 ? (
        <table border="1">
          <tbody>
            {data.map((item, index) => (
              <RenderRow key={index} tabId={activeTab} item={item} />
            ))}
          </tbody>
        </table>
      ) : (
        !loading && <p>데이터가 없습니다.</p>
      )}
    </div>
  );
}

export default TabPage;
