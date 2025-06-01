from flask import request, render_template, url_for, redirect, flash
from flask_login import login_required, current_user
from . import tasks_bp
from taskmanager_app import limiter
from taskmanager_app.forms.tasks_forms import CreateTaskForm, UpdateTaskForm, DeleteTaskForm
from taskmanager_app.models import Todo, db
from taskmanager_app.utils import dynamic_limit


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
    update_forms = {task.id: UpdateTaskForm(obj=task) for task in tasks}
    delete_forms = {task.id: DeleteTaskForm() for task in tasks}
    return render_template('task.html', 
                           tasks=tasks, 
                           pagination=pagination,
                           create_form=CreateTaskForm(),
                           update_forms=update_forms,
                           delete_forms=delete_forms)


@tasks_bp.route('/create-task', methods=['POST'])
@limiter.limit(dynamic_limit)
@login_required
def create_task():
    form = CreateTaskForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data

        if description and not description.strip():
            flash('Description cannot be just whitespace!', 'danger')
            return redirect(url_for('tasks.get_all_tasks'))

        new_task = Todo(title=title, description=description, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks.get_all_tasks'))
    return render_template('task.html', 
                       tasks=Todo.query.filter_by(user_id=current_user.id).order_by(Todo.id).all(), 
                       create_form=form,
                       update_forms={task.id: UpdateTaskForm(obj=task) for task in Todo.query.filter_by(user_id=current_user.id)})


@tasks_bp.route('/update-task/<int:task_id>', methods=['POST'])
@limiter.limit(dynamic_limit)
@login_required
def update_task(task_id):
    task = Todo.query.get_or_404(task_id)
    form = UpdateTaskForm()

    if form.validate_on_submit():
        task.title = form.title.data
        
        if form.description.data and not form.description.data.strip():
            flash('Description cannot be just whitespace!', 'danger')
            return redirect(url_for('tasks.get_all_tasks'))
        else:
            task.description = form.description.data

        task.is_done = form.is_done.data
        
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.get_all_tasks'))
    return render_template('task.html', 
                       tasks=Todo.query.filter_by(user_id=current_user.id).order_by(Todo.id).all(), 
                       create_form=CreateTaskForm(),
                       update_forms={task.id: UpdateTaskForm(obj=task) for task in Todo.query.filter_by(user_id=current_user.id)},
                       form=form)


@tasks_bp.route('/delete-task/<int:task_id>', methods=['POST'])
@limiter.limit(dynamic_limit)
@login_required
def delete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.get_all_tasks'))
