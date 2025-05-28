from flask import Flask, request, render_template, url_for, redirect, flash, get_flashed_messages
from flask_migrate import Migrate
from config import Config
from models import Todo, db
from pathlib import Path


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)



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
        flash('Form submitted successfully!')
        return render_template('response.html', email=email, message=message)
    

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Todo.query.order_by(Todo.id.desc()).paginate(page=page, per_page=per_page)
    tasks = pagination.items
    return render_template('task.html', tasks=tasks, pagination=pagination)


@app.route('/create-task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'GET':
        return render_template('task-form.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        new_task = Todo(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        flash('Task created successfully!')
        return redirect(url_for('get_all_tasks'))
    

@app.route('/update-task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Todo.query.get_or_404(task_id)
    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.is_done = True if request.form.get('is_done') == 'True' else False
    db.session.commit()
    flash('Task updated successfully!')
    return redirect(url_for('get_all_tasks'))


@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!')
    return redirect(url_for('get_all_tasks'))

if __name__ == '__main__':
    app.run()
