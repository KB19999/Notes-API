from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash   
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from marshmallow import Schema, fields, validate, ValidationError

auth_bp = Blueprint('auth', __name__)

class userSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, validate=validate.Length(min=6))
user_schema = userSchema()
validate=validate.Length(min=6)
login_schema = userSchema()

class userloginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        schema = userSchema()
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'validation failed', 'messages': err.messages}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)

    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        schema = userloginSchema()
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'validation failed', 'messages': err.messages}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({'message': f'Hello, {user.username}! This is a protected route.'}), 200
