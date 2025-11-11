import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../lib/api';
import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';

type Note = {
	id: number;
	title: string;
	content: string;
	created_at: string;
	updated_at: string;
	archived: boolean;
};

export default function Notes() {
	const navigate = useNavigate();
	const queryClient = useQueryClient();
	const [keyword, setKeyword] = useState('');
	const [archived, setArchived] = useState<'all' | 'true' | 'false'>('all');
	const [editingId, setEditingId] = useState<number | null>(null);
	const [editTitle, setEditTitle] = useState('');
	const [editContent, setEditContent] = useState('');

	const queryKey = useMemo(() => ['notes', { keyword, archived }], [keyword, archived]);

	const { data, isPending, error } = useQuery({
		queryKey,
		queryFn: async () => {
			const params: Record<string, string> = {};
			if (keyword) params.keyword = keyword;
			if (archived !== 'all') params.archived = archived;
			const res = await api.get('/notes/', { params });
			return res.data.notes as Note[];
		},
	});

	const createMutation = useMutation({
		mutationFn: async (note: { title: string; content: string }) => {
			const res = await api.post('/notes/', note);
			return res.data.note as Note;
		},
		onSuccess: () => queryClient.invalidateQueries({ queryKey }),
	});

	const archiveMutation = useMutation({
		mutationFn: async (note: Note) => {
			const path = note.archived ? `/notes/${note.id}/unarchive` : `/notes/${note.id}/archive`;
			await api.patch(path);
		},
		onSuccess: () => queryClient.invalidateQueries({ queryKey }),
	});

	const deleteMutation = useMutation({
		mutationFn: async (note: Note) => {
			await api.delete(`/notes/${note.id}`);
		},
		onSuccess: () => queryClient.invalidateQueries({ queryKey }),
	});

	const updateMutation = useMutation({
		mutationFn: async (payload: { id: number; title: string; content: string }) => {
			const body: Record<string, string> = {};
			if (payload.title) body.title = payload.title;
			if (payload.content) body.content = payload.content;
			const res = await api.put(`/notes/${payload.id}`, body);
			return res.data.note as Note;
		},
		onSuccess: () => {
			setEditingId(null);
			setEditTitle('');
			setEditContent('');
			queryClient.invalidateQueries({ queryKey });
		},
	});

	const logout = () => {
		localStorage.removeItem('access_token');
		navigate('/login', { replace: true });
	};

	return (
		<div style={{ maxWidth: 900, margin: '0 auto', padding: 16 }}>
			<header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12 }}>
				<h1>My Notes</h1>
				<button onClick={logout}>Logout</button>
			</header>

			<section style={{ display: 'flex', gap: 8, marginTop: 12 }}>
				<input placeholder="Search keyword" value={keyword} onChange={(e) => setKeyword(e.target.value)} />
				<select value={archived} onChange={(e) => setArchived(e.target.value as any)}>
					<option value="all">All</option>
					<option value="false">Active</option>
					<option value="true">Archived</option>
				</select>
			</section>

			<section style={{ marginTop: 16, border: '1px solid #ddd', padding: 12 }}>
				<h3>Create note</h3>
				<form
					onSubmit={(e) => {
						e.preventDefault();
						const form = e.target as HTMLFormElement;
						const title = (form.elements.namedItem('title') as HTMLInputElement).value;
						const content = (form.elements.namedItem('content') as HTMLTextAreaElement).value;
						createMutation.mutate({ title, content });
						form.reset();
					}}
					style={{ display: 'grid', gap: 8 }}
				>
					<input name="title" placeholder="Title" required />
					<textarea name="content" placeholder="Content" required />
					<button type="submit" disabled={createMutation.isPending}>
						{createMutation.isPending ? 'Adding...' : 'Add note'}
					</button>
				</form>
				{createMutation.error ? <div style={{ color: 'red' }}>Failed to add note</div> : null}
			</section>

			<section style={{ marginTop: 24 }}>
				{isPending ? (
					<div>Loading notes...</div>
				) : error ? (
					<div style={{ color: 'red' }}>Failed to load notes</div>
				) : (
					<ul style={{ display: 'grid', gap: 8, padding: 0, listStyle: 'none' }}>
						{(data ?? []).map((n) => (
							<li key={n.id} style={{ border: '1px solid #eee', padding: 12, borderRadius: 6 }}>
								{editingId === n.id ? (
									<form
										onSubmit={(e) => {
											e.preventDefault();
											updateMutation.mutate({ id: n.id, title: editTitle, content: editContent });
										}}
										style={{ display: 'grid', gap: 8 }}
									>
										<input
											value={editTitle}
											onChange={(e) => setEditTitle(e.target.value)}
											placeholder="Title"
											required
										/>
										<textarea
											value={editContent}
											onChange={(e) => setEditContent(e.target.value)}
											placeholder="Content"
											required
										/>
										<div style={{ display: 'flex', gap: 8 }}>
											<button type="submit" disabled={updateMutation.isPending}>
												{updateMutation.isPending ? 'Saving...' : 'Save'}
											</button>
											<button
												type="button"
												onClick={() => {
													setEditingId(null);
													setEditTitle('');
													setEditContent('');
												}}
											>
												Cancel
											</button>
										</div>
									</form>
								) : (
									<>
										<div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
											<strong>{n.title}</strong>
											<div style={{ display: 'flex', gap: 8 }}>
												<button
													onClick={() => {
														setEditingId(n.id);
														setEditTitle(n.title);
														setEditContent(n.content);
													}}
												>
													Edit
												</button>
												<button onClick={() => archiveMutation.mutate(n)} disabled={archiveMutation.isPending}>
													{n.archived ? 'Unarchive' : 'Archive'}
												</button>
												<button onClick={() => deleteMutation.mutate(n)} disabled={deleteMutation.isPending}>
													Delete
												</button>
											</div>
										</div>
										<p style={{ marginTop: 8, whiteSpace: 'pre-wrap' }}>{n.content}</p>
									</>
								)}
							</li>
						))}
					</ul>
				)}
			</section>
		</div>
	);
}


