import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState("loading");

  useEffect(() => {
    fetch("http://localhost:5000/")
      .then(res => res.json())
      .then(data => {
        setMessage(data.message);
        setStatus("success");
      })
      .catch(() => {
        setMessage("Server not reachable");
        setStatus("error");
      });
  }, []);

  return (
    <div className="app">
      <div className="container">
        <h1>Client Service</h1>
        <p className="description">
          Health check for backend service running inside Docker
        </p>

        <div className={`status ${status}`}>
          {status === "loading" ? "Checking server status..." : message}
        </div>

        <div className="meta">
          API Endpoint: <span>server:5000/</span>
        </div>
      </div>
    </div>
  );
}

export default App;
