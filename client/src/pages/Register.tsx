import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../lib/api';

export default function Register() {
	const navigate = useNavigate();
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);

	const onSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setLoading(true);
		setError(null);
		try {
			const res = await api.post('/auth/register', { username: username.trim(), password: password.trim() });
			localStorage.setItem('access_token', res.data.access_token);
			navigate('/notes', { replace: true });
		} catch (err: any) {
			setError(err?.response?.data?.error ?? 'Registration failed');
		} finally {
			setLoading(false);
		}
	};

	return (
		<div style={{ display: 'grid', placeItems: 'center', minHeight: '100dvh', padding: 16 }}>
			<form onSubmit={onSubmit} style={{ width: '100%', maxWidth: 400, display: 'grid', gap: 12 }}>
				<h1>Register</h1>
				<label>
					<div>Username</div>
					<input value={username} onChange={(e) => setUsername(e.target.value)} required />
				</label>
				<label>
					<div>Password</div>
					<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
				</label>
				<button disabled={loading} type="submit">{loading ? 'Creating...' : 'Create account'}</button>
				{error && <div style={{ color: 'red' }}>{error}</div>}
				<div>
					Have an account? <Link to="/login">Login</Link>
				</div>
			</form>
		</div>
	);
}


