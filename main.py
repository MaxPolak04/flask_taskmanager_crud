from flask import Flask, request, render_template, flash
from flask_migrate import Migrate
from flask_login import LoginManager
from auth import auth_bp
from admin_users import admin_bp
from tasks import tasks_bp
from config import Config
from models import User, db


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.login_view = 'signin'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(tasks_bp, url_prefix='/tasks')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


if __name__ == '__main__':
    app.run()
