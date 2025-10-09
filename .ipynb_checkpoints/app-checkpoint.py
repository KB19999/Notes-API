from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth import auth_bp
from notes import notes_bp


app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(notes_bp, url_prefix='/api/notes')


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Notes API',
                    'version': '1.0',
                    'endpoints': {
                        'auth': {
                            'register': 'POST/api/register',
                            'login': 'POST/api/login'
                        },
                        'notes': {
                            'get_all': 'GET/api/notes',
                            'create': 'POST/api/notes',
                            'get': 'GET/api/notes/<id>',
                            'update': 'PUT/api/notes/<id>',
                                'delete': 'DELETE/api/notes/<id>',
                                'archive': 'PATCH/api/notes/<id>/archive',
                                'unarchive': 'PATCH/api/notes/<id>/unarchive'
                            },
                            'filters': {
                                'by_date': 'GET/api/notes?date=YYYY-MM-DD',
                                'by_keyword': 'GET/api/notes?keyword=your_keyword',
                                'by_archived': 'GET/api/notes?archived=true|false'
                            }
                        }
                    })
@app.error_handlers(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404
@app.error_handlers(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000, debug=True)