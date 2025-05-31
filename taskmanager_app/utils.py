from taskmanager_app.config import Config
from flask import abort
from flask_login import current_user, login_required
from flask_limiter.util import get_remote_address
from functools import wraps


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


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
