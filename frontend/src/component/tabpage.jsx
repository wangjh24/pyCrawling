import React, { useState } from "react";
import axios from "axios";
import RenderRow from "./RowRender";
import styles from "./css/font.module.css";

const API_BASE_URL = "http://localhost:8000/api";

function TabPage() {
  const [code, setCode] = useState("");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("stock");
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

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
    setCurrentPage(1);
    if (code) handleSearch(tabId);
  };

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = data.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(data.length / itemsPerPage);

  return (
    <div className={styles.wrapper}>
      <h1 className={styles.mainTitle}>주식 종목 정보 조회</h1>

      <div className={styles.searchContainer}>
        <input
          className={styles.searchInput}
          type="text"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="종목코드 (예: 005930)"
        />
        <button
          className={styles.btnPrimary}
          onClick={() => handleSearch()}
          disabled={loading}
        >
          {loading ? "조회 중..." : "데이터 조회"}
        </button>
      </div>

      <div className={styles.contentContainer}>
        <div className={styles.tabContainer}>
          {tabs.map((tab) => (
            <button
              key={tab.id}
              className={`${styles.tabButton} ${activeTab === tab.id ? styles.active : ""}`}
              onClick={() => changeTab(tab.id)}
            >
              {tab.name}
            </button>
          ))}
        </div>

        {loading && <p className={styles.statusMsg}>데이터를 불러오는 중...</p>}

        {!loading && data && data.length > 0 ? (
          <>
            <table className={styles.mainTable}>
              {activeTab === "frgn" && (
                <colgroup>
                  <col style={{ width: "12%" }} />
                  <col style={{ width: "10%" }} />
                  <col style={{ width: "10%" }} />
                  <col style={{ width: "8%" }} />
                  <col style={{ width: "15%" }} />
                  <col style={{ width: "12%" }} />
                  <col style={{ width: "12%" }} />
                  <col style={{ width: "13%" }} />
                  <col style={{ width: "8%" }} />
                </colgroup>
              )}
              {activeTab === "stock" && (
                <colgroup>
                  <col style={{ width: "25%" }} />
                  <col style={{ width: "25%" }} />
                  <col style={{ width: "25%" }} />
                  <col style={{ width: "25%" }} />
                </colgroup>
              )}
              {(activeTab === "news" || activeTab === "board") && (
                <colgroup>
                  <col style={{ width: "30%" }} />
                  <col style={{ width: "55%" }} />
                  <col style={{ width: "15%" }} />
                </colgroup>
              )}

              <thead>
                {activeTab === "frgn" && (
                  <tr>
                    <th>날짜</th>
                    <th>종가</th>
                    <th>전일비</th>
                    <th>등락률</th>
                    <th>거래량</th>
                    <th>기관순매수</th>
                    <th>외인순매수</th>
                    <th>외인보유</th>
                    <th>비중</th>
                  </tr>
                )}
                {activeTab === "stock" && (
                  <tr>
                    <th>매도기업</th>
                    <th>매도거래량</th>
                    <th>매수기업</th>
                    <th>매수거래량</th>
                  </tr>
                )}
                {(activeTab === "news" || activeTab === "board") && (
                  <tr>
                    <th>제목</th>
                    <th>내용</th>
                    <th>날짜</th>
                  </tr>
                )}
                {activeTab === "summary" && (
                  <tr>
                    <th>날짜</th>
                    <th>구분</th>
                    <th>매출액</th>
                    <th>영업이익</th>
                    <th>당기순이익</th>
                    <th>영업이익률</th>
                    <th>순이익률</th>
                    <th>ROE(지배주주)</th>
                    <th>부채비율</th>
                    <th>당좌비율</th>
                    <th>유보율</th>
                    <th>EPS(원)</th>
                    <th>PER(배)</th>
                    <th>BPS(원)</th>
                    <th>PBR(배)</th>
                    <th>주당배당금(원)</th>
                    <th>시가배당률(%)</th>
                    <th>배당성향(%)</th>
                  </tr>
                )}
              </thead>
              <tbody>
                {currentItems.map((item, index) => (
                  <RenderRow key={index} tabId={activeTab} item={item} />
                ))}
              </tbody>
            </table>

            <div className={styles.pagination}>
              <button
                disabled={currentPage === 1}
                onClick={() => setCurrentPage((prev) => prev - 1)}
              >
                이전
              </button>
              <span>
                {currentPage} / {totalPages}
              </span>
              <button
                disabled={currentPage === totalPages}
                onClick={() => setCurrentPage((prev) => prev + 1)}
              >
                다음
              </button>
            </div>
          </>
        ) : (
          !loading && <p className={styles.statusMsg}>데이터가 없습니다.</p>
        )}
      </div>
    </div>
  );
}

export default TabPage;
