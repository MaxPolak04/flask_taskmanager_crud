from flask import Flask, request, render_template, url_for, redirect
from config import Config
from models import Todo, db
from pathlib import Path


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


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
        return render_template('response.html', email=email, message=message)
    

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = Todo.query.all()
    return render_template('task.html', tasks=tasks)


@app.route('/create-task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'GET':
        return render_template('create_task.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        new_task = Todo(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('get_all_tasks'))
    

if __name__ == '__main__':
    app.run()
