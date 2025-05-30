from flask import request, render_template, url_for, redirect, session, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from . import auth_bp
from taskmanager_app.models import User, db
from datetime import timedelta


@auth_bp.route('/signup', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.signin'))
        else:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.signup'))
    return render_template('signup.html')


@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = True if request.form.get('remember_me') == 'on' else False
        user = User.query.filter_by(email=email).first()

        session.permanent = True
        if remember_me:
            current_app.permanent_session_lifetime = timedelta(days=7)
        else:
            current_app.permanent_session_lifetime = timedelta(minutes=15)

        if not user:
            flash('Email not found!', 'danger')
            return redirect(url_for('auth.signin'))
        if not check_password_hash(user.password, password):
            flash('Incorrect password!', 'danger')
            return redirect(url_for('auth.signin'))
        login_user(user, remember=remember_me)
        user.last_login_at = db.func.now()
        db.session.commit()
        flash('Logged in successfully!', 'success')
        return redirect(url_for('get_all_tasks'))
    return render_template('signin.html')


@auth_bp.route('/signout')
@login_required
def signout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))
