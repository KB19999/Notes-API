from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Note
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime


notes_bp = Blueprint('notes', __name__)
class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    archived = fields.Bool(dump_only=True)


class NoteUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=100))
    content = fields.Str()

@notes_bp.route('/', methods=['POST'])
@jwt_required()
def create_note():
    try:
        schema = NoteSchema()
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'validation failed', 'messages': err.messages}), 400

    current_user_id = get_jwt_identity()
    new_note = Note(title=data['title'], 
                    content=data['content'], 
                    user_id=current_user_id)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({'message': 'Note created successfully', 
                    'note': schema.dump(new_note)}), 201

    
@notes_bp.route('/', methods=['GET'])
@jwt_required()
def get_notes():
    current_user_id = get_jwt_identity()
    query = Note.query.filter_by(user_id=current_user_id)

    date_filter = request.args.get('date')
    keyword_filter = request.args.get('keyword')
    archived_filter = request.args.get('archived')

    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Note.created_at) == date_obj)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    if keyword_filter:
        query = query.filter((Note.title.ilike(f'%{keyword_filter}%')) | 
                             (Note.content.ilike(f'%{keyword_filter}%')))

    if archived_filter is not None:
        if archived_filter.lower() == 'true':
            query = query.filter_by(archived=True)
        elif archived_filter.lower() == 'false':
            query = query.filter_by(archived=False)
        else:
            return jsonify({'error': 'Invalid archived filter. Use true or false.'}), 400

    notes = query.all()
    schema = NoteSchema(many=True)
    return jsonify({'notes': schema.dump(notes)}), 200


@notes_bp.route('/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    current_user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    schema = NoteSchema()
    return jsonify({'note': schema.dump(note)}), 200


@notes_bp.route('/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    try:
        schema = NoteUpdateSchema()
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'validation failed', 'messages': err.messages}), 400

    current_user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    
    db.session.commit()

    schema = NoteSchema()
    return jsonify({'message': 'Note updated successfully', 
                    'note': schema.dump(note)}), 200

@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    current_user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note deleted successfully'}), 200


@notes_bp.route('/<int:note_id>/archive', methods=['PATCH'])
@jwt_required()
def archive_note(note_id):
    current_user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    note.archived = True
    db.session.commit()

    schema = NoteSchema()
    return jsonify({'message': 'Note archived successfully', 
                    'note': schema.dump(note)}), 200

@notes_bp.route('/<int:note_id>/unarchive', methods=['PATCH'])
@jwt_required()
def unarchive_note(note_id):
    current_user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    note.archived = False
    db.session.commit()

    schema = NoteSchema()
    return jsonify({'message': 'Note restored successfully', 
                    'note': schema.dump(note)}), 200
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': f'Hello, {user.username}! This is a protected note.'}), 200