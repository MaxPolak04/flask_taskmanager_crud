from flask import Flask, request, render_template, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
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
    pagination = Todo.query \
        .filter_by(user_id=current_user.id) \
        .order_by(Todo.id.desc()) \
        .paginate(page=page, per_page=per_page)
    
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

        new_task = Todo(title=title, description=description, user_id=current_user.id)
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


@app.route('/manage_users', methods=['GET'])
@login_required
def manage_users():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = User.query \
        .order_by(User.id.desc()) \
        .paginate(page=page, per_page=per_page)
    users = pagination.items
    return render_template('manage-users.html', users=users, pagination=pagination)


@app.route('/update_user/<int:user_id>', methods=['POST'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.username = request.form.get('username') if request.form.get('username') else user.username
    profile_picture = request.files.get('profile_picture')
    if profile_picture and allowed_file(profile_picture.filename):
        filename = f"{user.id}_{profile_picture.filename}"
        profile_picture_path = Path(app.config['UPLOAD_FOLDER']) / filename
        profile_picture.save(profile_picture_path)
        user.profile_picture = filename

    if not request.form.get('password') and not request.form.get('confirm_password'):
        user.password = user.password
    elif request.form.get('password') and not request.form.get('confirm_password'):
        flash('Please confirm your password!', 'danger')
        return redirect(url_for('manage_users'))
    elif not request.form.get('password') and request.form.get('confirm_password'):
        flash('You can\'t confirm a password you didn\'t enter!', 'danger')
        return redirect(url_for('manage_users'))
    elif request.form.get('password') != request.form.get('confirm_password'):
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('manage_users'))
    
    user.is_admin = True if request.form.get('is_admin') == 'True' else False
    db.session.commit()
    flash('User updated successfully!', 'success')
    return redirect(url_for('manage_users'))


@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('manage_users'))


if __name__ == '__main__':
    app.run()
