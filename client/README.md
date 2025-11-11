# Client (React + Vite)

## Scripts

- `npm run dev` - start dev server (proxied to backend on http://localhost:10000)
- `npm run build` - production build
- `npm run preview` - preview production build

## API Base URL

By default, the client uses `/api/v1` (Vite dev proxy sends to the Flask server).
For production, set `VITE_API_BASE` at build time (e.g. `https://your-domain/api/v1`).

