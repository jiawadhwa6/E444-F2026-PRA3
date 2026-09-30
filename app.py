from flask import Flask, render_template, session, redirect, url_for
from forms import NameEmailForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-123'

@app.route('/')
def index():
    return render_template('index.html', name='Jia')

@app.route('/form', methods=['GET', 'POST'])
def form_page():
    form = NameEmailForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('result'))
    return render_template('form.html', form=form)

@app.route('/result')
def result():
    name = session.get('name', 'Stranger')
    email = session.get('email', '')
    return render_template('result.html', name=name, email=email)

if __name__ == '__main__':
    app.run(debug=True, port=5000)