from flask import Flask, render_template, request
import cst
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        print('inputId =', request.form['inputId'])
        print('inputPassword =', request.form['inputPassword'])
        # do something
        # show verify img if necessary
        # redirect if success else flash error message

if __name__ == '__main__':
    app.run()
