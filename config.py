import os
from datetime import timedelta


class Config:
    # Secret key for session management and security
    SECRET_KEY = os.getenv('SESSION_SECRET')

    # Retrieve database URL from environment variable, fallback to local SQLite
    database_url = os.getenv('DATABASE_URL', 'sqlite:///notes.db')

    # Convert old postgres:// URL to postgresql:// for SQLAlchemy compatibility
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable unnecessary event notifications

    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # Secret key for token generation
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)  # Token lifespan set to 2 hours