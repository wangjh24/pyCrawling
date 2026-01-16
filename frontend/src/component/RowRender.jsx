import React from "react";

// 컴포넌트로 변경: props로 tabId와 item을 받습니다.
// (index는 호출하는 부모 쪽에서 key로 사용하므로 여기선 굳이 안 받아도 됩니다.)
function RenderRow({ tabId, item }) {
  if (tabId === "frgn") {
    return (
      <tr>
        <td>{item.date}</td>
        <td>{item.close_price}</td>
        <td>{item.change_val}</td>
        <td>{item.change}</td>
        <td>{item.chage_rate}</td>
        <td>{item.volume}</td>
        <td>{item.insstitution_net_volume}</td>
        <td>{item.foreign_net_volume}</td>
        <td>{item.foreign_holding_shares}</td>
        <td>{item.foreign_holding_ratio}</td>
      </tr>
    );
  } else if (tabId === "stock") {
    return (
      <tr>
        <td>{item.sell_rank}</td>
        <td>{item.sell_volume}</td>
        <td>{item.buy_rank}</td>
        <td>{item.buy_volume}</td>
      </tr>
    );
  } else if (tabId === "news" || tabId === "board") {
    return (
      <tr>
        <td>
          <strong>{item.title}</strong>
        </td>
        <td>
          {item.content ? item.content.substring(0, 50) + "..." : "내용 없음"}
        </td>
        <td>{item.date}</td>
      </tr>
    );
  } else if (tabId === "summary") {
    return (
      <tr>
        <td>{item["2022.12"]}</td>
        <td>{item["2023.12"]}</td>
        <td>{item["2024.12"]}</td>
        <td>{item["2025.12(E)"]}</td>
        <td>{item["2024.09"]}</td>
        <td>{item["2024.12_1"]}</td>
        <td>{item["2025.03"]}</td>
        <td>{item["2025.06"]}</td>
        <td>{item["2025.09"]}</td>
        <td>{item["2025.12(E)_1"]}</td>
      </tr>
    );
  }

  return (
    <tr>
      <td>데이터 형식 미지정 (Tab: {tabId})</td>
    </tr>
  );
}

export default RenderRow;
