import { Navigate, Route, Routes } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Notes from './pages/Notes';
import { useMemo } from 'react';

export default function App() {
	const isAuthed = useMemo(() => {
		return Boolean(localStorage.getItem('access_token'));
	}, []);

	return (
		<Routes>
			<Route path="/" element={isAuthed ? <Navigate to="/notes" replace /> : <Navigate to="/login" replace />} />
			<Route path="/login" element={<Login />} />
			<Route path="/register" element={<Register />} />
			<Route path="/notes" element={isAuthed ? <Notes /> : <Navigate to="/login" replace />} />
			<Route path="*" element={<Navigate to="/" replace />} />
		</Routes>
	);
}


