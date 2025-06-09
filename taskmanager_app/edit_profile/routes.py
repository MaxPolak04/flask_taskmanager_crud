from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask import current_app, redirect, url_for, render_template
from flask_login import current_user
from . import edit_profile_bp
from taskmanager_app import db
from taskmanager_app.models import User
from taskmanager_app.forms.edit_profile import EditProfileForm
from pathlib import Path


@edit_profile_bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    user = User.query.get_or_404(current_user.id)

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

        if form.new_password.data:
            user.password = generate_password_hash(form.new_password.data)

        db.session.commit()

        return redirect(url_for('tasks.get_all_tasks'))
    return render_template('edit-profile.html', form=form, user=user)
