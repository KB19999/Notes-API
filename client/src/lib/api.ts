import axios from 'axios';

const baseURL = (import.meta as any).env?.VITE_API_BASE ?? '/api/v1';

const api = axios.create({ baseURL });

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


