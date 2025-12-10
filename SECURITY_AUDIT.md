Security Audit — Notes API (Flask + SQLAlchemy + JWT)

This security audit provides a structured review of authentication, authorization, database handling, input validation, error management, and deployment posture for the Notes API backend.

1. Authentication & JWT Security
Strengths
Passwords securely hashed using Werkzeug.
JWT used for stateless authentication.
Token expiration set (2 hours).

Concerns
JWT identity stored as string instead of integer.
No refresh token mechanism.
Admin roles not reinforced with multi-factor or permission model.

Recommendations
Change JWT identity to:
create_access_token(identity=user.id)
Add refresh token endpoint (optional).
Rotate JWT secret key periodically for long-term deployments.

2. Authorization & Access Control
Strengths
Notes filtered by authenticated user (user_id).
admin_required decorator protects admin endpoints.

Concerns
setup_admin.py contains a hardcoded admin password because the repo is public its unsafe but a working progress.
Incorrect indentation of the promote_user function.
No rate-limiting to brute-force login attempts possible.

Recommendations
Remove hardcoded passwords from repository.
Use environment variables or one-time admin setup script.
Add login rate-limiting (Flask-Limiter recommended).

3. Input Validation
Strengths
Marshmallow schemas validate user and note data.
Descriptive validation errors returned.

Concerns
No maximum length constraints for username/password → brute force/DoS vulnerability.
Note content not sanitized → possible XSS if frontend renders unsafely.

Recommendations
Add length constraints:
username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
password = fields.Str(required=True, validate=validate.Length(min=6, max=128))
Escape HTML content in UI or sanitize before storage.

4. Error Handling & Logging
Strengths
Custom JSON error handlers for 404 and 500.

Concerns
Printing raw exceptions to console may leak sensitive information.
No structured logging for audit trails.

Recommendations
Replace print() with Python’s logging module.
Mask internal errors in production responses.

5. Database Security
Strengths
SQLAlchemy ORM protects against SQL injection.
Foreign key constraints correctly maintained.

Concerns
SQLite fallback should not be used in production.
Lack of DB indexes for frequent filtered queries (e.g., created_at).

Recommendations
Enforce PostgreSQL for production via configuration.
Consider adding indexes for performance.

6. CORS & Deployment Hardening
Strengths
CORS enabled allowing Netlify frontend to access backend.
High-Risk Concerns
CORS(app) allows all origins, which is unsafe in production.

Recommendation
Restrict to your frontend domain:
CORS(app, origins=["https://your-netlify-site.netlify.app"])

7. Admin Security
Concerns
Admin delete operations have no confirmation or logging.
Destructive actions (delete user) are irreversible.

Recommendations
Add audit logging for admin actions.
Implement soft-deletes for users or archived backups.

Overall Security Score: I will give this a B- as a first project but would improve over time
