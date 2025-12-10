Deployment Guide — Notes API & Client Web App

This guide documents how to deploy the Flask backend to Render and the Vite React frontend to Netlify, including environment variables, build settings, routing configuration, and troubleshooting.

1. Backend Deployment (Render)
1.1 Project Structure
The backend lives at the root of the repository:

Notes-API/
  app.py
  models.py
  config.py
  notes.py
  admin.py
  auth.py
  requirements.txt
  ...

1.2 Render Setup

Visit: https://dashboard.render.com
Click New → Web Service
Connect this GitHub repo

Configure as follows:
Setting	Value
Runtime	Python
Build Command	pip install -r requirements.txt
Start Command	gunicorn app:app
Environment	Production
Port	Auto-detected (Flask reads $PORT)
1.3 Required Environment Variables

Add the following in Render → Environment:
SESSION_SECRET = your_generated_secret
JWT_SECRET_KEY = your_jwt_secret
DATABASE_URL = your_postgres_database_url


Render will automatically provide the PORT environment variable.

1.4 CORS

The application uses:
CORS(app)
This allows requests from your Netlify frontend.
For production hardening, consider locking this down (see security audit).


2. Frontend Deployment (Netlify)
The frontend codebase is located in:
client/

2.1 Build Settings
Configure Netlify → Site Settings → Build & Deploy:
Setting	Value
Base Directory	client
Build Command	npm run build
Publish Directory	dist

This ensures Netlify builds the React/Vite app correctly.

2.2 Environment Variable
Add in Netlify:
VITE_API_URL = https://your-render-backend.onrender.com
MUST NOT end with a trailing slash.

Your frontend axios instance will automatically append /api/v1 to this base URL.

2.3 Required Redirect Rule (React Router Fix)
React Router requires Netlify to serve index.html on all paths.
Create:
client/public/_redirects
With the following content:
/*   /index.html   200


This prevents 404 errors when visiting /login, /notes, etc.

3. Common Deployment Errors & Fixes
Error: client/dist does not exist
Cause: Netlify did not run npm run build.

Fix:
Base Directory must be client
Publish Directory must be dist
Build command must be set

Error: React routes (e.g., /login) show 404

Fix:
_redirects file missing or incorrect.
Error: Login/Register fails in production

Fix:
Ensure VITE_API_URL is correct
Ensure no trailing slash
Verify axios baseURL includes /api/v1

4. Deployment Verification Checklist
Backend (Render)
Register user returns 201
Login returns JWT
CRUD notes operations work
Admin endpoints respond for admin accounts

Frontend (Netlify)
Register works
Login redirects correctly
Notes page loads data
Create/Edit/Delete note works
Archive/Unarchive works
Logout works
Refreshing /notes or /login does not show a 404
