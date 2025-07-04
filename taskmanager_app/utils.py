from taskmanager_app.config import Config
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from flask import abort, current_app
from sqlalchemy import select, literal
from sqlalchemy.exc import OperationalError
from flask_login import current_user, login_required
from flask_limiter.util import get_remote_address
from functools import wraps
from pathlib import Path
import time


def create_admin_if_missing():
    from taskmanager_app.models import User
    print("Checking for admin user...")
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        print("Admin user not found, creating new admin...")
        from taskmanager_app import db
        password = Config.ADMIN_PASSWORD

        upload_folder = Path(current_app.config['UPLOAD_FOLDER'])
        upload_folder.mkdir(parents=True, exist_ok=True)
        admin_file_path = upload_folder / "admin.png"
        filename = "admin.png" if admin_file_path.exists() else None
            
        new_admin = User(
            username='admin',
            email='admin@gmail.com',
            password=generate_password_hash(password),
            is_admin=True,
            profile_picture=filename
        )
        db.session.add(new_admin)
        db.session.commit()


def wait_for_db(app):
    from taskmanager_app import db
    with app.app_context():
        connected = False
        while not connected:
            try:
                db.session.execute(select(literal(1)))
                connected = True
            except OperationalError:
                print("Database not ready, waiting...")
                time.sleep(2)



def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def get_user_or_ip():
    if current_user.is_authenticated:
        return str(current_user.id)
    return get_remote_address()


def dynamic_limit():
    if current_user.is_admin:
        return "100 per day"
    return "60 per day"
