import axios from "axios";

/**
 * This removes hydration timing issues on Netlify/Vite.
 */
function resolveBaseURL() {
  const url = import.meta.env.VITE_API_URL;
  if (url) return `${url}/api/v1`;
  return "http://localhost:10000/api/v1";
}

// Debug notice to help diagnose missing environment variable issues in deployment
if (!import.meta.env.VITE_API_URL) {
  console.warn("VITE_API_URL is not defined — using localhost fallback.");
}

const api = axios.create();

/**
 * Ensures:
 * - baseURL is always fresh
 * - Authorization header always present
 */
api.interceptors.request.use((config) => {
  config.baseURL = resolveBaseURL();

  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

/**
 * Handles token expiry / forced logout
 */
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const status = err?.response?.status;

    if (status === 401) {
      localStorage.removeItem("access_token");
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
    }

    return Promise.reject(err);
  }
);

export default api;
