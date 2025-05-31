from flask import request, render_template, url_for, redirect, flash
from flask_login import login_required, current_user
from . import tasks_bp
from taskmanager_app import limiter
from taskmanager_app.models import Todo, db


@tasks_bp.route('/', methods=['GET'])
@limiter.exempt
@login_required
def get_all_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Todo.query \
        .filter_by(user_id=current_user.id) \
        .order_by(Todo.id) \
        .paginate(page=page, per_page=per_page)
    
    tasks = pagination.items
    return render_template('task.html', tasks=tasks, pagination=pagination)


@tasks_bp.route('/create-task', methods=['POST'])
@limiter.limit("60 per hour")
@login_required
def create_task():
    title = request.form.get('title')
    description = request.form.get('description')

    if not title:
        flash('Title is required!', 'danger')
        return redirect(url_for('tasks.get_all_tasks'))

    if len(title) > 100:
        flash('The title is too long (max 100 characters)!', 'danger')
        return redirect(url_for('tasks.get_all_tasks'))

    if description and len(description) > 300:
        flash('The description can be at most 300 characters long!', 'danger')
        return redirect(url_for('tasks.get_all_tasks'))

    if description and not description.strip():
        flash('Description cannot be just whitespace!', 'danger')
        return redirect(url_for('tasks.get_all_tasks'))

    new_task = Todo(title=title, description=description, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    flash('Task created successfully!', 'success')
    return redirect(url_for('tasks.get_all_tasks'))


@tasks_bp.route('/update-task/<int:task_id>', methods=['POST'])
@limiter.limit("60 per hour")
@login_required
def update_task(task_id):
    task = Todo.query.get_or_404(task_id)
    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.is_done = True if request.form.get('is_done') == 'True' else False
    db.session.commit()
    flash('Task updated successfully!', 'success')
    return redirect(url_for('tasks.get_all_tasks'))


@tasks_bp.route('/delete-task/<int:task_id>', methods=['POST'])
@limiter.limit("60 per hour")
@login_required
def delete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.get_all_tasks'))
