from flask import Flask, request, make_response, redirect, abort, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)


@app.route('/user/<name>')
def user(name):
    list = ['one', 'two', '3', 'four']
    i = 3
    return render_template('extends.html')


@app.route('/hao/<int:number>/')
def hao(number):
    return '<h1>Hello,%d</h1>' % number



@app.route('/browser/')
def index0():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent


@app.route('/make_response/')
def index1():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response


@app.route('/redirect/')
def index2():
    return redirect('http://www.baidu.com')

'''
@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name
'''

manager = Manager(app)
bootstrap = Bootstrap(app)

if __name__ == '__main__':
    app.run(debug=True)
