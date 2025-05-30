from flask import request, render_template, url_for, redirect, flash, current_app
from werkzeug.security import generate_password_hash
from . import admin_bp
from models import User, db
from utils.utils import allowed_file, admin_required
from pathlib import Path


@admin_bp.route('/manage_users', methods=['GET'])
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = User.query \
        .order_by(User.id.desc()) \
        .paginate(page=page, per_page=per_page)
    users = pagination.items
    return render_template('manage-users.html', users=users, pagination=pagination)


@admin_bp.route('/create_user', methods=['POST'])
@admin_required
def create_user():
    username = request.form.get('username')
    email = request.form.get('email')
    if not request.form.get('password') or not request.form.get('confirm_password'):
        flash('Password is required!', 'danger')
        return redirect(url_for('admin.manage_users'))
    elif request.form.get('password') != request.form.get('confirm_password'):
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('admin.manage_users'))
    password = generate_password_hash(request.form.get('password'))
    is_admin = True if request.form.get('is_admin') == 'True' else False
    new_user = User(username=username, email=email, password=password, is_admin=is_admin)
    db.session.add(new_user)
    db.session.commit()
    flash('User created successfully!', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/update_user/<int:user_id>', methods=['POST'])
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.username = request.form.get('username') if request.form.get('username') else user.username
    profile_picture = request.files.get('profile_picture')
    if profile_picture and allowed_file(profile_picture.filename):
        filename = f"{user.id}_{profile_picture.filename}"
        profile_picture_path = Path(current_app.config['UPLOAD_FOLDER']) / filename
        profile_picture.save(profile_picture_path)
        user.profile_picture = filename

    if not request.form.get('password') and not request.form.get('confirm_password'):
        user.password = user.password
    elif request.form.get('password') and not request.form.get('confirm_password'):
        flash('Please confirm your password!', 'danger')
        return redirect(url_for('admin.manage_users'))
    elif not request.form.get('password') and request.form.get('confirm_password'):
        flash('You can\'t confirm a password you didn\'t enter!', 'danger')
        return redirect(url_for('admin.manage_users'))
    elif request.form.get('password') != request.form.get('confirm_password'):
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('admin.manage_users'))
    else:
        hashed_password = generate_password_hash(request.form.get('password'))
        user.password = hashed_password
    
    user.is_admin = True if request.form.get('is_admin') == 'True' else False
    db.session.commit()
    flash('User updated successfully!', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.manage_users'))
