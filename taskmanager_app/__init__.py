from flask import Flask, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from talisman import Talisman
from flask_limiter import Limiter
from taskmanager_app.config import Config
from taskmanager_app.utils import get_user_or_ip


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
limiter = Limiter(
    key_func=get_user_or_ip,
    default_limits=["200 per day", "50 per hour"]
)


def create_app():
    """Create and configure the Flask application."""

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)

    csp = {
        'default-src': [
            '\'self\'',
            'https://fonts.googleapis.com',
            'https://fonts.gstatic.com',
            'https://cdn.jsdelivr.net',       # np. Bootstrap z CDN
            'https://cdnjs.cloudflare.com',
        ],
        'img-src': ['*', 'data:'],
        'script-src': [
            '\'self\'',
            'https://cdn.jsdelivr.net',
            'https://cdnjs.cloudflare.com',
            'https://code.jquery.com',
        ],
        'style-src': [
            '\'self\'',
            'https://fonts.googleapis.com',
            'https://cdn.jsdelivr.net',
            'https://cdnjs.cloudflare.com',
        ],
        'object-src': ['none'],
        'base-uri': ['self']
    }

    Talisman(
        app, 
        content_security_policy=csp,
        force_https=True,
        strict_transport_security=True,
        frame_options='SAMEORIGIN',
        session_cookie_secure=True,
        session_cookie_http_only=True
    )

    login_manager.login_view = 'auth.signin'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .auth import auth_bp
    from .admin_users import admin_bp
    from .tasks import tasks_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')


    @app.route('/')
    @limiter.exempt
    def index():
        return render_template('index.html')


    @app.route('/form', methods=['GET', 'POST'])
    @limiter.limit("5 per hour")
    def form():
        if request.method == 'GET':
            return render_template('form.html')
        elif request.method == 'POST':
            email = request.form.get('email')
            message = request.form.get('message')
            flash('Form submitted successfully!', 'success')
            return render_template('response.html', email=email, message=message)


    return app
