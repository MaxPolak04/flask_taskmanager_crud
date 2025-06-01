from flask import request, render_template, url_for, redirect, session, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
# from flask_wtf import vali
from . import auth_bp
from taskmanager_app import limiter
from taskmanager_app.models import User, db
from taskmanager_app.forms.auth_forms import SignUpForm, SignInForm
from datetime import timedelta


@auth_bp.route('/signup', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data

        if User.query.filter_by(username=username).first():
                flash('Username already exists!', 'danger')
                return redirect(url_for('auth.signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'danger')
            return redirect(url_for('auth.signup'))
        
        password = generate_password_hash(form.password.data)

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('auth.signin'))
    return render_template('signup.html', form=form)


@auth_bp.route('/signin', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def signin():
    form = SignInForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Email not found!', 'danger')
            return redirect(url_for('auth.signin'))
        if not check_password_hash(user.password, password):
            flash('Incorrect password!', 'danger')
            return redirect(url_for('auth.signin'))
        
        session.permanent = True
        if remember_me:
            current_app.permanent_session_lifetime = timedelta(days=7)
        else:
            current_app.permanent_session_lifetime = timedelta(minutes=15)
        
        login_user(user, remember=remember_me)
        user.last_login_at = db.func.now()
        db.session.commit()

        flash('Logged in successfully!', 'success')
        return redirect(url_for('tasks.get_all_tasks'))
    return render_template('signin.html', form=form)


@auth_bp.route('/signout')
@login_required
def signout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))
