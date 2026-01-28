import React, { useState } from "react";
import axios from "axios";
import RenderRow from "./RowRender";
import styles from "./css/font.module.css";

const API_BASE_URL = "http://localhost:8000/api";

function TabPage() {
  const [code, setCode] = useState("");
  const [data, setData] = useState([]); // 일반 테이블용 데이터
  const [analysisData, setAnalysisData] = useState(null); // 뉴스 분석용 데이터
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("stock");
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;
  const [predictData, setPredictData] = useState(null); // 예측 데이터용 상태

  const tabs = [
    { id: "stock", name: "종합정보", endpoint: "stock" },
    { id: "frgn", name: "외인/기관", endpoint: "frgn" },
    { id: "news", name: "최신뉴스", endpoint: "news" },
    { id: "board", name: "종목토론", endpoint: "board" },
    { id: "summary", name: "기업실적", endpoint: "summary" },
    { id: "news_mecab", name: "뉴스분석", endpoint: "news_mecab" },
    { id: "predict", name: "AI 예측", endpoint: "predict" }, // AI 예측 탭 추가
  ];

  const handleSearch = async (targetTab = activeTab) => {
    if (!code) return alert("종목코드를 입력하세요");
    setLoading(true);

    // 모든 데이터 초기화
    setData([]);
    setAnalysisData(null);
    setPredictData(null);
    setCurrentPage(1);

    try {
      // 백엔드 엔드포인트와 일치시키기 위해 targetTab 분기 처리 가능
      const endpoint = targetTab === "predict" ? "frgn-ms" : targetTab;
      const response = await axios.get(`${API_BASE_URL}/${endpoint}/${code}`);

      if (targetTab === "news_mecab") {
        setAnalysisData(response.data);
      } else if (targetTab === "predict") {
        // 2. 예측 데이터 별도 저장
        setPredictData(response.data);
      } else {
        setData(Array.isArray(response.data) ? response.data : []);
      }
    } catch (error) {
      console.error("데이터 호출 실패:", error);
      alert(
        error.response?.data?.detail || "데이터 로드 중 오류가 발생했습니다.",
      );
    } finally {
      setLoading(false);
    }
  };

  const changeTab = (tabId) => {
    setActiveTab(tabId);
    if (code) handleSearch(tabId);
  };

  // 페이징 처리 (일반 데이터용)
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

        {loading && (
          <p className={styles.statusMsg}>데이터를 불러오는 중입니다...</p>
        )}

        {!loading && (
          <>
            {/* 뉴스 분석 전용 화면 */}
            {activeTab === "news_mecab" && analysisData ? (
              <div className={styles.analysisBox}>
                <h2 className={styles.subTitle}>
                  뉴스 키워드 분석 (워드클라우드)
                </h2>
                <div style={{ textAlign: "center", margin: "20px 0" }}>
                  <img
                    src={analysisData.image}
                    alt="Wordcloud"
                    style={{
                      width: "100%",
                      borderRadius: "10px",
                      boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
                    }}
                  />
                </div>
                <h3 className={styles.subTitle}>핵심 키워드 TOP 20</h3>
                <table className={styles.mainTable}>
                  <thead>
                    <tr>
                      <th>순위</th>
                      <th>키워드</th>
                      <th>빈도수</th>
                    </tr>
                  </thead>
                  <tbody>
                    {analysisData.keywords.map((kw, idx) => (
                      <tr key={idx}>
                        <td style={{ textAlign: "center" }}>{idx + 1}</td>
                        <td style={{ textAlign: "center" }}>{kw.text}</td>
                        <td style={{ textAlign: "center" }}>{kw.value}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : null}
            {activeTab === "predict" && predictData && (
              <div className={styles.analysisBox}>
                <h2 className={styles.subTitle}>
                  XGBoost 기반 다음 거래일 예측
                </h2>
                <div className={styles.predictCard}>
                  <div className={styles.predictGrid}>
                    <div className={styles.predictItem}>
                      <span>현재가</span>
                      <strong>
                        {predictData.current_price?.toLocaleString()}원
                      </strong>
                    </div>
                    <div className={styles.predictItem}>
                      <span>예상 변동폭</span>
                      <strong
                        className={
                          predictData.predicted_change > 0
                            ? styles.up
                            : styles.down
                        }
                      >
                        {predictData.predicted_change > 0 ? "▲" : "▼"}{" "}
                        {Math.abs(
                          predictData.predicted_change,
                        ).toLocaleString()}
                        원
                      </strong>
                    </div>
                    <div className={styles.predictItem}>
                      <span>예상 종가</span>
                      <strong>
                        {predictData.predicted_price?.toLocaleString()}원
                      </strong>
                    </div>
                    <div className={styles.predictItem}>
                      <span>모델 신뢰도 (RMSE)</span>
                      <span>{predictData.rmse}</span>
                    </div>
                  </div>
                  <div className={styles.predictMessage}>
                    <p>{predictData.message}</p>
                  </div>
                </div>
              </div>
            )}

            {/* 일반 테이블 화면 */}
            {activeTab !== "news_mecab" &&
            activeTab !== "predict" &&
            data.length > 0 ? (
              <>
                <table className={styles.mainTable}>
                  {/* ... colgroup 로직 (생략 없이 유지됨) ... */}
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
                        <th>ROE</th>
                        <th>부채비율</th>
                        <th>당좌비율</th>
                        <th>유보율</th>
                        <th>EPS</th>
                        <th>PER</th>
                        <th>BPS</th>
                        <th>PBR</th>
                        <th>배당금</th>
                        <th>배당률</th>
                        <th>성향</th>
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
                    {" "}
                    {currentPage} / {totalPages}{" "}
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
              !loading &&
              !analysisData &&
              !predictData &&
              data.length === 0 && (
                <p className={styles.statusMsg}>표시할 데이터가 없습니다.</p>
              )
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default TabPage;
