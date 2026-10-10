import { useState, useEffect } from "react";
import { api } from "./api";

export default function ProjectDetail({ project, onBack }) {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  async function loadTasks() {
    try {
      const data = await api.listTasks(project.id);
      setTasks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTasks();
  }, []);

  async function handleCreate(e) {
    e.preventDefault();
    setError("");
    try {
      await api.createTask(project.id, title, "");
      setTitle("");
      loadTasks();
    } catch (err) {
      setError(err.message);
    }
  }

  async function toggleDone(task) {
    const newStatus = task.status === "done" ? "todo" : "done";
    try {
      await api.updateTaskStatus(task.id, newStatus);
      loadTasks();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <button onClick={onBack} style={{ marginBottom: 12 }}>← Back to projects</button>
      <h2>{project.name}</h2>
      {project.description && <p style={{ color: "#666" }}>{project.description}</p>}

      <form onSubmit={handleCreate} style={{ marginBottom: 20 }}>
        <input
          placeholder="New task"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{ padding: 8, marginRight: 8 }}
          required
        />
        <button type="submit" style={{ padding: 8 }}>Add Task</button>
      </form>

      {error && <p style={{ color: "crimson" }}>{error}</p>}

      {loading ? (
        <p>Loading tasks...</p>
      ) : tasks.length === 0 ? (
        <p style={{ color: "#666" }}>No tasks yet.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {tasks.map((t) => (
            <li key={t.id} style={{ marginBottom: 8 }}>
              <label style={{ cursor: "pointer" }}>
                <input
                  type="checkbox"
                  checked={t.status === "done"}
                  onChange={() => toggleDone(t)}
                  style={{ marginRight: 8 }}
                />
                <span style={{ textDecoration: t.status === "done" ? "line-through" : "none", color: t.status === "done" ? "#999" : "inherit" }}>
                  {t.title}
                </span>
              </label>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}