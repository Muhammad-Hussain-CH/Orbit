import { useState, useEffect } from "react";
import { api } from "./api";

export default function ProjectsPage({ onOpenProject }) {
  const [projects, setProjects] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  // Fetch projects when the page first loads
  async function loadProjects() {
    try {
      const data = await api.listProjects();
      setProjects(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProjects();
  }, []);

  async function handleCreate(e) {
    e.preventDefault();
    setError("");
    try {
      await api.createProject(name, description);
      setName("");
      setDescription("");
      loadProjects(); // refresh the list after creating
    } catch (err) {
      setError(err.message);
    }
  }

  if (loading) return <p>Loading projects...</p>;

  return (
    <div>
      <h2>Your Projects</h2>

      <form onSubmit={handleCreate} style={{ marginBottom: 20 }}>
        <input
          placeholder="Project name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ padding: 8, marginRight: 8 }}
          required
        />
        <input
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={{ padding: 8, marginRight: 8 }}
        />
        <button type="submit" style={{ padding: 8 }}>Add Project</button>
      </form>

      {error && <p style={{ color: "crimson" }}>{error}</p>}

      {projects.length === 0 ? (
        <p style={{ color: "#666" }}>No projects yet. Create one above.</p>
      ) : (
        <ul>
          {projects.map((p) => (
                        <li key={p.id} style={{ marginBottom: 8 }}>
              <button
                onClick={() => onOpenProject(p)}
                style={{ background: "none", border: "none", cursor: "pointer", fontSize: "1em", padding: 0, textAlign: "left" }}
              >
                <strong style={{ color: "#2563eb" }}>{p.name}</strong>
                {p.description && <span style={{ color: "#666" }}> — {p.description}</span>}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}