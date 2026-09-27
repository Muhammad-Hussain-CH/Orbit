import { useState } from "react";
import { api } from "./api";
import LoginPage from "./LoginPage";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!api.getToken());

  function handleLogout() {
    api.clearToken();
    setLoggedIn(false);
  }

  if (!loggedIn) {
    return <LoginPage onLoggedIn={() => setLoggedIn(true)} />;
  }

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>Orbit</h1>
        <button onClick={handleLogout}>Log out</button>
      </div>
      <p>You're logged in. 🎉 Projects coming next.</p>
    </div>
  );
}