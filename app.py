from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth import auth_bp
from notes import notes_bp
from admin import admin_bp

# Initialize Flask app
app = Flask(__name__)

# Load configuration (secret keys, DB URI, etc.)
app.config.from_object(Config)

# Enable Cross-Origin Resource Sharing (CORS)
allowed_origins = [
    "https://journalq.netlify.app"
]

CORS(app, resources={
    r"/api/*": {"origins": allowed_origins}
})

# Initialize SQLAlchemy database
db.init_app(app)

# Initialize JWT Manager
jwt = JWTManager(app)

# Ensure all database tables exist before serving requests
with app.app_context():
    db.create_all()

# Register Blueprints (modular endpoints)
# Keeping URL prefixes consistent and descriptive
app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(notes_bp, url_prefix='/api/v1/notes') 
app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

# Welcome route
@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to the Notes API',
        'version': '1.0',
        'status': 'running',
        'endpoints': {
            'auth': {
                'register': 'POST /api/v1/auth/register',
                'login': 'POST /api/v1/auth/login'
            },
            'notes': {
                'get_all': 'GET /api/v1/notes',
                'create': 'POST /api/v1/notes',
                'get': 'GET /api/v1/notes/<id>',
                'update': 'PUT /api/v1/notes/<id>',
                'delete': 'DELETE /api/v1/notes/<id>',
                'archive': 'PATCH /api/v1/notes/<id>/archive',
                'unarchive': 'PATCH /api/v1/notes/<id>/unarchive'
            },
            'filters': {
                'by_date': 'GET /api/v1/notes?date=YYYY-MM-DD',
                'by_keyword': 'GET /api/v1/notes?keyword=your_keyword',
                'by_archived': 'GET /api/v1/notes?archived=true|false'
            }
        }
    }), 200


# Custom error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# Entry point
# Using port 10000 for Render
# Setting debug=False for deployment.

for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
