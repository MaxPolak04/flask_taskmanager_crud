from flask import Flask, request, render_template, url_for


app = Flask(__name__)
# db = SQLAlchemy(app)


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


if __name__ == '__main__':
    app.run()
