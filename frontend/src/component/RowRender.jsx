import React from "react";

function RenderRow({ tabId, item }) {
  if (tabId === "frgn") {
    return (
      <tr>
        <td>{item.date}</td>
        <td>{item.close_price}</td>
        <td
          style={{
            color: item.change_val.includes("상승")
              ? "red"
              : item.change_val.includes("하락")
                ? "blue"
                : "black",
          }}
        >
          {item.change}
        </td>
        <td
          style={{
            color: item.change_val.includes("상승")
              ? "red"
              : item.change_val.includes("하락")
                ? "blue"
                : "black",
          }}
        >
          {item.change_rate}
        </td>
        <td>{item.volume}</td>
        <td
          style={{
            color: item.insstitution_net_volume?.startsWith("+")
              ? "red"
              : item.insstitution_net_volume?.startsWith("-")
                ? "blue"
                : "black",
          }}
        >
          {item.insstitution_net_volume}
        </td>
        <td
          style={{
            color: item.foreign_net_volume?.startsWith("+")
              ? "red"
              : item.foreign_net_volume?.startsWith("-")
                ? "blue"
                : "black",
          }}
        >
          {item.foreign_net_volume}
        </td>
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
        <td>{item["date"]}</td>
        <td>{item["type"]}</td>
        <td>{item["revenue"]}</td>
        <td>{item["operating_income"]}</td>
        <td>{item["net_income"]}</td>
        <td>{item["operating_margin"]}</td>
        <td>{item["net_profit_margin"]}</td>
        <td>{item["roe"]}</td>
        <td>{item["debt_to_equity"]}</td>
        <td>{item["quick_ratio"]}</td>
        <td>{item["reserve_ratio"]}</td>
        <td>{item["eps"]}</td>
        <td>{item["per"]}</td>
        <td>{item["bps"]}</td>
        <td>{item["pbr"]}</td>
        <td>{item["dps"]}</td>
        <td>{item["dividend_yield"]}</td>
        <td>{item["payout_ratio"]}</td>
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
