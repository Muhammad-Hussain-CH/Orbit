import { useState } from "react";
import { api } from "./api";
import LoginPage from "./LoginPage";
import ProjectsPage from "./ProjectsPage";
import ProjectDetail from "./ProjectDetail";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!api.getToken());
  const [selectedProject, setSelectedProject] = useState(null);

  function handleLogout() {
    api.clearToken();
    setSelectedProject(null);
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

      {selectedProject ? (
        <ProjectDetail project={selectedProject} onBack={() => setSelectedProject(null)} />
      ) : (
        <ProjectsPage onOpenProject={(p) => setSelectedProject(p)} />
      )}
    </div>
  );
}