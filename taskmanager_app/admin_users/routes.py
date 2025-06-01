from flask import request, render_template, url_for, redirect, flash, current_app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from . import admin_bp
from taskmanager_app import limiter
from taskmanager_app.forms.admin_users_forms import CreateUserForm, UpdateUserForm, DeleteUserForm
from taskmanager_app.models import User, db
from taskmanager_app.utils import admin_required
from pathlib import Path


@admin_bp.route('/manage_users', methods=['GET'])
@limiter.exempt
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = User.query \
        .order_by(User.id) \
        .paginate(page=page, per_page=per_page)
    
    users = pagination.items
    update_forms = {user.id: UpdateUserForm(obj=user) for user in users}
    delete_forms = {user.id: DeleteUserForm() for user in users}

    return render_template('manage-users.html', 
                           users=users, 
                           pagination=pagination, 
                           form=CreateUserForm(),
                           update_forms=update_forms, 
                           delete_forms=delete_forms)


@admin_bp.route('/create_user', methods=['POST'])
@limiter.limit("10 per minute")
@admin_required
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        is_admin = form.is_admin.data

        new_user = User(username=username, email=email, password=password, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('admin.manage_users'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = User.query \
        .order_by(User.id) \
        .paginate(page=page, per_page=per_page)

    users = pagination.items
    return render_template('manage-users.html',
                           users=users,
                           pagination=pagination, 
                           form=form,
                           update_forms={user.id: UpdateUserForm(obj=user) for user in users},
                           delete_forms={user.id: DeleteUserForm() for user in users})


@admin_bp.route('/update_user/<int:user_id>', methods=['POST'])
@limiter.limit("10 per minute")
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateUserForm()

    if form.validate_on_submit():
        user.username = form.username.data

        if form.profile_picture.data:
            profile_picture = form.profile_picture.data
            filename = secure_filename(profile_picture.filename)
            upload_folder = Path(current_app.config['UPLOAD_FOLDER'])
            upload_folder.mkdir(parents=True, exist_ok=True)
            file_path = upload_folder / filename
            profile_picture.save(file_path)
            user.profile_picture = filename

        if form.password.data:
            user.password = generate_password_hash(form.password.data)

        user.is_admin = form.is_admin.data

        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.manage_users'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = User.query \
        .order_by(User.id) \
        .paginate(page=page, per_page=per_page)

    users = pagination.items
    return render_template('manage-users.html',
                           users=users,
                           pagination=pagination, 
                           create_form=CreateUserForm(),
                           update_forms={user.id: UpdateUserForm(obj=user) for user in users},
                           delete_forms={user.id: DeleteUserForm() for user in users})


@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@limiter.limit("10 per minute")
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.manage_users'))
