from flask import Flask, render_template, request, session
from main import comp
from icnode import printable_code

app = Flask(__name__, template_folder='./uimamalona/templates', static_folder="./uimamalona/static")
app.secret_key = "yeahbuddy"

@app.route('/')
def code():
    code = ""
    if session.get('code'):
        code = session['code']
    return render_template('code.html', code=code)

@app.route('/', methods=['POST'])
def build():
    code = request.form['src']
    session["code"] = code
    visited, cg = comp(code)
    session["errors"] = visited.TypeValidator.errors
    session["ic"] = printable_code(cg.code)
    return render_template('code.html', code=code)

@app.route('/tree')
def tree():
    return render_template('tree.html')

@app.route('/errors')
def errors():
    e = session.get('errors')
    return render_template('errors.html', errors=e)

@app.route('/ic')
def ic():
    e = session.get('ic')
    return render_template('ic.html', ic=e)