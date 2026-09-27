const BASE_URL = "http://127.0.0.1:8000";

// Read the saved token (if any) from the browser's localStorage
function getToken() {
  return localStorage.getItem("orbit_token");
}

// Core request function — attaches the token, parses JSON, throws on error
async function request(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...options.headers };

  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });

  if (!res.ok) {
    let detail = "Request failed";
    try {
      const data = await res.json();
      detail = data.detail || detail;
    } catch {
      // response wasn't JSON — keep the default message
    }
    throw new Error(detail);
  }

  // Some responses (like 204 delete) have no body
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  login: (email, password) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  me: () => request("/auth/me"),

  setToken: (token) => localStorage.setItem("orbit_token", token),
  clearToken: () => localStorage.removeItem("orbit_token"),
  getToken,
};