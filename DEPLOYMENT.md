Deployment Guide — Notes API & Client Web App

This guide outlines the steps required to deploy the Flask backend on Render and the Vite/React frontend on Netlify. It covers build settings, environment variables, routing configuration, and verification steps.

1. Backend Deployment (Render)
1.1 Project Structure

The backend codebase is located at the root of the repository:
Notes-API/
  app.py
  models.py
  config.py
  notes.py
  admin.py
  auth.py
  requirements.txt
  ...

1.2 Render Web Service Setup
Navigate to: https://dashboard.render.com
Select New → Web Service
Connect the GitHub repository
Configure the service as follows:
Setting	Value
Runtime	Python
Build Command	pip install -r requirements.txt
Start Command	gunicorn app:app
Environment	Production
Port	Auto-detected ($PORT)

Render automatically assigns the runtime port.

1.3 Required Environment Variables

Add the following under Render → Environment:
SESSION_SECRET = your_generated_secret
JWT_SECRET_KEY = your_jwt_secret
DATABASE_URL = your_postgres_database_url
FRONTEND_URL = https://journalq.netlify.app

These values allow the backend to authenticate users, connect to PostgreSQL, and communicate with the deployed frontend.

1.4 CORS Configuration
The backend must allow only the deployed frontend to access protected API routes.

Ensure your app.py includes:
allowed_origins = ["https://journalq.netlify.app"]

CORS(app, resources={
    r"/api/*": {"origins": allowed_origins}
})

This is required for Render → Netlify communication.

2. Frontend Deployment (Netlify)
The frontend resides in the client/ directory.

2.1 Netlify Build Settings
Go to Netlify → Site Settings → Build & Deploy and configure:
Setting	Value
Base Directory	client
Build Command	npm run build
Publish Directory	dist

Netlify will automatically detect Node and install dependencies.

2.2 Required Environment Variable
Add this in Netlify → Site Configuration → Environment Variables:
VITE_API_URL = https://your-render-backend.onrender.com
Notes:
Do not include a trailing slash.
The frontend automatically appends /api/v1 when making requests.

2.3 Required Redirect File (React Router)
To support client-side routing:
Create a file at:
client/public/_redirects
Add this line:
/*   /index.html   200

This ensures paths like /login and /notes load correctly.

3. Common Deployment Errors & Fixes
Error: client/dist does not exist
Cause: Netlify did not run the build.

Fix:
Base Directory must be client
Publish Directory must be dist
Build Command must be set to npm run build

Error: React routes show 404 on refresh
Fix: Confirm _redirects is correctly placed in client/public/.

Error: Login or Register fails in production
Fixes:
Confirm VITE_API_URL is correctly set
Ensure no trailing slash
Verify backend is reachable at .../api/v1/...

4. Deployment Verification Checklist
Backend (Render)
Registration returns a 201 status
Login returns a valid JWT
Notes CRUD operations work
Archive/unarchive works
Admin routes respond for admin accounts

Frontend (Netlify)
Registration works
Login redirects to /notes
Notes list loads and filters correctly
Create/Edit/Delete functions operate as expected Logout clears token and redirects
Refreshing any route does not 404
