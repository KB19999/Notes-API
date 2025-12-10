from app import app
from models import db, User
from werkzeug.security import generate_password_hash

# SAFETY CHECKS — DO NOT REMOVE

# Guard 1: Require explicit environment confirmation
if os.getenv("ALLOW_ADMIN_RESET") != "true":
    print("REFUSING TO RUN: ALLOW_ADMIN_RESET is not set to 'true'.")
    print("This script is disabled to protect production data.")
    exit(1)

# Guard 2: Prevent running on PostgreSQL (used in Render production)
db_url = os.getenv("DATABASE_URL", "")
if db_url.startswith("postgres://") or db_url.startswith("postgresql://"):
    print("REFUSING TO RUN: Detected PostgreSQL (production) database.")
    print("This script can only run on local SQLite in development.")
    exit(1)
    
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
