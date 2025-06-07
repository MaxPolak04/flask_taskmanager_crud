from taskmanager_app.config import Config
from werkzeug.security import generate_password_hash
from flask import abort
from flask_login import current_user, login_required
from flask_limiter.util import get_remote_address
from functools import wraps


def create_admin_if_missing():
    from taskmanager_app.models import User
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        from taskmanager_app import db
        password = Config.ADMIN_PASSWORD
        new_admin = User(
            username='admin',
            email='admin@gmail.com',
            password=generate_password_hash(password),
            is_admin=True
        )
        db.session.add(new_admin)
        db.session.commit()


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
