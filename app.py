from flask import Flask, request, render_template, url_for
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
    

@app.route('/task', methods=['GET'])
def get_all_task():
    tasks = Todo.query.all()
    return render_template('task.html', tasks=tasks)
    

if __name__ == '__main__':
    app.run()
