from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy instance globally
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'  # Explicitly defined for clarity and cross-database consistency

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Ensures no duplicate usernames
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically timestamps user creation

    # Establish one-to-many relationship with Note table
    notes = db.relationship(
        'Note',
        backref='owner',             # Enables note.owner to access related user
        lazy=True,                   # Loads related objects only when accessed (performance optimization)
        cascade='all, delete-orphan' # Ensures notes are deleted if user is deleted
    )

    # Utility Methods 
    def set_password(self, password):
        """Hashes the password before storing it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifies password against stored hash."""
        return check_password_hash(self.password, password)

    def to_dict(self):
        """Serializes the user object into a dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Note(db.Model):
    __tablename__ = 'notes'  # Explicitly named for clarity and maintainability

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    archived = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Matches 'users' table name

    def to_dict(self):
        """Serializes the note object into a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'archived': self.archived,
            'user_id': self.user_id
        }