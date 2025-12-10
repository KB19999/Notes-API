Security Audit — Notes API (Flask + SQLAlchemy + JWT)

This security audit evaluates the authentication logic, authorization flow, database handling, input validation, error management, and deployment posture of the Notes API backend. It also incorporates recent improvements, including hardened CORS rules and safeguarding of administrative database scripts.

1. Authentication & JWT Security
Strengths
Passwords are securely hashed using Werkzeug.
Stateless authentication implemented with JWT.
Access tokens are short-lived (2-hour expiration).

Concerns
JWT identity is stored as a string instead of an integer.
No refresh token mechanism.
Admin role is binary, without additional permission layers or MFA.

Recommendations
Use an integer identity:
create_access_token(identity=user.id)
Add optional refresh token support for long-lived sessions.
Periodically rotate the JWT_SECRET_KEY in production.

2. Authorization & Access Control
Strengths
Notes are always queried by user_id, preventing cross-user data access.
The admin_required decorator ensures privileged operations are restricted.

Concerns
The original setup_admin.py contained a hardcoded admin password.
No rate-limiting on login → vulnerable to brute-force attempts.
Legacy issues with the indentation of the promote_user function.

Data Protection Enhancement
A major improvement has now been implemented:
setup_admin.py is protected by multiple safety guards
Requires a specific environment variable (ALLOW_ADMIN_RESET=true).
Automatically refuses to run on PostgreSQL (production).
Prevents accidental or malicious execution on Render.
This significantly reduces the risk of unintended production data deletion.

Recommendations
Store sensitive admin credentials in environment variables or generate them once per environment.
Implement rate-limiting on authentication endpoints (e.g., Flask-Limiter).

3. Input Validation
Strengths
Marshmallow is used consistently for validation.
Validation errors are descriptive and user-friendly.

Concerns
No maximum length limits on username/password → DoS/brute force vector.
Note content is not sanitized, leaving potential for XSS vulnerabilities.

Recommendations
Add validation constraints such as:
username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
password = fields.Str(required=True, validate=validate.Length(min=6, max=128))
Sanitize or escape note content on the frontend before rendering.

4. Error Handling & Logging
Strengths
Clear JSON responses for 404 and 500 errors.
Controlled error output improves client-side debugging.

Concerns
Printing Python exceptions to console may leak internals.
No structured logging for auditing or incident analysis.

Recommendations
Replace print() statements with Python’s logging module.
Configure log levels differently for development vs. production.
Avoid exposing detailed internal errors to the client.

5. Database Security
Strengths
SQLAlchemy ORM prevents raw SQL injection vectors.
Proper foreign key relationships enforce user–note association.

Concerns
SQLite fallback should not be used in production.
No indexing on frequently filtered columns (e.g., timestamps).

Recommendations
Enforce PostgreSQL strictly in production by configuration.
Add indexes (e.g., created_at) to improve query performance.

6. CORS & Deployment Hardening
Strengths
CORS is now configured using an explicit allowlist.
Major Improvement — Locked CORS
The previous CORS(app) allowed all origins, creating a high-risk exposure.
This has now been replaced with a hardened configuration:
allowed_origins = ["https://journalq.netlify.app"]
CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

Impact of This Improvement
Only the official frontend may access API endpoints.
Prevents third-party sites from making authenticated API calls.
Reduces CSRF-like risk scenarios involving token misuse.

7. Admin Security
Concerns
Admin delete operations lack secondary confirmation.
User deletions are irreversible without backups.

Recommendations
Implement audit logging for all admin actions.
Consider using soft-deletes for users/notes.
Restrict admin functionality to a dedicated interface or endpoint group.
