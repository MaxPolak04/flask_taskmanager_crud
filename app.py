from flask import Flask, request, render_template, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required
from config import Config
from models import Todo, User, db
from utils.utils import allowed_file
from datetime import timedelta
from pathlib import Path


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.login_view = 'signin'
login_manager.login_message = 'Please log in to access this page.'
login_manager.init_app(app)


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
    

@app.route('/tasks', methods=['GET'])
@login_required
def get_all_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Todo.query.order_by(Todo.id.desc()).paginate(page=page, per_page=per_page)
    tasks = pagination.items
    return render_template('task.html', tasks=tasks, pagination=pagination)


@app.route('/create-task', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'GET':
        return render_template('task-form.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if not title:
            flash('Title is required!', 'danger')
            return redirect(url_for('create_task'))
        
        if len(title) > 100:
            flash('The title is too long (max 100 characters)!', 'danger')
            return redirect(url_for('create_task'))

        if description and len(description) > 300:
            flash('The description can be at most 300 characters long!', 'danger')
            return redirect(url_for('create_task'))

        if description and not description.strip():
            flash('Description cannot be just whitespace!', 'danger')
            return redirect(url_for('create_task'))

        new_task = Todo(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('get_all_tasks'))
    

@app.route('/update-task/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    task = Todo.query.get_or_404(task_id)
    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.is_done = True if request.form.get('is_done') == 'True' else False
    db.session.commit()
    flash('Task updated successfully!', 'success')
    return redirect(url_for('get_all_tasks'))


@app.route('/delete-task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('get_all_tasks'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        if request.form.get('password') == request.form.get('confirm_password'):
            password = generate_password_hash(request.form.get('password'))
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('signin'))
        else:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('signup'))
    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remeber_me = request.form.get('remember_me')
        user = User.query.filter_by(email=email).first()

        if remeber_me:
            app.permanent_session_lifetime = timedelta(days=7)
        else:
            app.permanent_session_lifetime = timedelta(minutes=15)
            
        if not user:
            flash('Email not found!', 'danger')
            return redirect(url_for('login'))
        if not check_password_hash(user.password, password):
            flash('Incorrect password!', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=remeber_me)
        user.last_login_at = db.func.now()
        db.session.commit()
        flash('Logged in successfully!', 'success')
        return redirect(url_for('get_all_tasks'))
    return render_template('signin.html')


@app.route('/signout')
@login_required
def signout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
