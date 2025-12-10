import axios from 'axios';

// Compute API URL at runtime to avoid Netlify hydration issues
function getBaseURL() {
  const url = import.meta.env.VITE_API_URL;
  if (url) return `${url}/api/v1`;
  return "http://localhost:10000/api/v1";
}

// Debug log to help diagnose missing environment variable issues
if (!import.meta.env.VITE_API_URL) {
  console.warn("VITE_API_URL is not defined — falling back to localhost API.");
}

const api = axios.create({
  baseURL: getBaseURL()
});

api.interceptors.request.use((config) => {
	const token = localStorage.getItem('access_token');
	if (token) {
		config.headers = config.headers ?? {};
		config.headers.Authorization = `Bearer ${token}`;
	}
	return config;
});

api.interceptors.response.use(
	(res) => res,
	(err) => {
		const status = err?.response?.status;
		if (status === 401) {
			localStorage.removeItem('access_token');
			if (typeof window !== 'undefined') {
				window.location.href = '/login';
			}
		}
		return Promise.reject(err);
	}
);

export default api;


