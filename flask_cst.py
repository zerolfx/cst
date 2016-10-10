from flask import Flask, render_template, request, session, redirect, url_for
import cst
import random
app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY='development key'
))

#  TODO absolute path

@app.route('/main')
def main():
    username = cst.get_username(session['cookies'])
    return render_template('index.html', username=username)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():

    def vcode():
        random.seed()
        filename = str(random.randint(100000, 999999))
        print(filename)
        session['filename'] = filename
        session['cookies'] = cst.get_verify(filename)
        return filename

    if request.method == 'POST':
        print(request.form)
        rf = request.form
        error = cst.login(rf['inputId'], rf['inputPassword'], rf['verifyCode'], session.get('cookies'))
        if error:
            return render_template('login.html', error=error, filename=vcode(),
                                   username=rf['inputId'], password=rf['inputPassword'])
        #  todo 明文密码？
        cst.delete_img(session.pop('filename'))
        # print(cst.get_username(session.get('cookies')))
        return redirect(url_for('main'))
    else:
        if session.get('cookies'):
            username = cst.get_username(session['cookies'])
            if username:
                return redirect(url_for('main'))
            else:
                cst.delete_img(session.pop('filename'))
        return render_template('login.html', filename=vcode())

if __name__ == '__main__':
    app.run(debug=True)
