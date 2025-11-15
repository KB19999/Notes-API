from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Note

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    """Decorator to restrict access to admin users."""
    from functools import wraps
    from flask import jsonify
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    users = User.query.all()
    return jsonify({'users': [u.to_dict() for u in users]}), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User {user.username} deleted'}), 200

@admin_bp.route('/notes', methods=['GET'])
@jwt_required()
@admin_required
def get_all_notes():
    notes = Note.query.all()
    return jsonify({'notes': [n.to_dict() for n in notes]}), 200

@admin_bp.route('/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': f'Note {note.id} deleted'}), 200
