from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from marshmallow import Schema, fields, validate, ValidationError
from sqlalchemy.exc import IntegrityError

# Blueprint initialization
auth_bp = Blueprint('auth', __name__)

# Schemas for validation

class UserSchema(Schema):
    """Schema for validating registration data."""
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, validate=validate.Length(min=6))

class UserLoginSchema(Schema):
    """Schema for validating login data."""
    username = fields.Str(required=True)
    password = fields.Str(required=True)

# Schema instances
user_schema = UserSchema()
login_schema = UserLoginSchema()



# Registration Endpoint

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Handles user registration.
    Validates input, hashes password, and stores new user in DB.
    """
    try:
        # Validate input using Marshmallow
        data = user_schema.load(request.json)

        # Hash password before storing
        hashed_password = generate_password_hash(data['password'])
        new_user = User(username=data['username'], password=hashed_password)

        # Attempt database commit
        db.session.add(new_user)
        db.session.commit()

        # Generate JWT token for the new user
        access_token = create_access_token (identity=str(new_user.id))

        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token
        }), 201

    except ValidationError as err:
        # Marshmallow validation failure
        db.session.rollback()
        return jsonify({'error': 'Validation failed', 'messages': err.messages}), 400

    except IntegrityError:
        # Handles duplicate username errors gracefully
        db.session.rollback()
        return jsonify({'error': 'Username already exists'}), 400

    except Exception as e:
        # General error fallback with visible Render log for debugging
        db.session.rollback()
        print(f"Error during registration: {e}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500



# Login Endpoint

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user and returns a JWT access token.
    """
    try:
        data = login_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'messages': err.messages}), 400

    # Query for user
    user = User.query.filter_by(username=data['username']).first()

    # Verify credentials
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Generate JWT token on success
    access_token = create_access_token (identity=str(user.id))
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token
    }), 200



# Protected Test Route

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    A protected route to test token authentication.
    Only accessible with a valid JWT.
    """
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'message': f'Hello, {user.username}! This is a protected route.'
    }), 200