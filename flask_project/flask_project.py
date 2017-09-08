from flask import Flask, request, make_response, redirect, abort, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask import Flask, request, make_response, redirect, abort, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)


class NameForm(Form):
    name = StringField('what is your name?',validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/hello/')
def hello():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    list = ['one', 'two', '3', 'four']
    i = 3
    return render_template('extends.html')


@app.route('/hellosomeone/<name>')
def hellosomeone(name):
    list = ['hello1','hello2','hello3,he','hello4']
    return render_template('user.html',name=name,mylist=list)


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
a = app.url_map
print (a)

manager = Manager(app)
print (manager)
bootstrap = Bootstrap(app)

if __name__ == '__main__':
    app.run(debug=True)
