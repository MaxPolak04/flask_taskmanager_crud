from flask import Flask, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from taskmanager_app.config import Config
# from .models import db


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    """Create and configure the Flask application."""

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

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
    def index():
        return render_template('index.html')


    @app.route('/form', methods=['GET', 'POST'])
    def form():
        if request.method == 'GET':
            return render_template('form.html')
        elif request.method == 'POST':
            email = request.form.get('email')
            message = request.form.get('message')
            flash('Form submitted successfully!', 'success')
            return render_template('response.html', email=email, message=message)


    return app
