# setup_admin.py
from app import app
from models import db, User
from werkzeug.security import generate_password_hash

# Configuration for first admin user
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin@1JudeAndKwaku"  

with app.app_context():
    # Drop all tables (WARNING: deletes ALL existing data)
    db.drop_all()
    print("All tables dropped successfully.")

    # Recreate tables with updated schema
    db.create_all()
    print("All tables created successfully with updated schema.")

    # Check if admin already exists (should be empty since we dropped all)
    admin_user = User.query.filter_by(username=ADMIN_USERNAME).first()
    if not admin_user:
        admin_user = User(
            username=ADMIN_USERNAME,
            password=generate_password_hash(ADMIN_PASSWORD),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{ADMIN_USERNAME}' created successfully with password '{ADMIN_PASSWORD}'")
    else:
        print("Admin user already exists.")
def promote_user(user_id):
    """Demote an admin user to regular user."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.is_admin = False
    db.session.commit()
    return jsonify({'message': f'User {user.username} demoted to regular user'}), 200