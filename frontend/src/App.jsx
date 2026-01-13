import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState("");

  useEffect(() => {
    // FastAPI 서버로 요청 보내기
    axios
      .get("http://127.0.0.1:8000/")
      .then((res) => setData(res.data.message))
      .catch((err) => console.log(err));
  }, []);

  return (
    <div>
      <h1>React + FastAPI 연동 테스트</h1>
      <p>백엔드에서 받은 데이터: {data}</p>
    </div>
  );
}

export default App;
