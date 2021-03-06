# !usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, request, make_response, redirect, abort, render_template, url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
# 创建一个flask对象app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

# 定义一个首页模板
@app.route('/index/')
def index_page():
    return render_template('index.html')


# 定义一个使用整数变量的模板
@app.route('/int/<int:number>/')
def hello_int(number):
    return '<h1>Hello,%d</h1>' % number


# 定义一个使用浮点数的模板
@app.route('/float/<float:number>')
def hello_float(number):
    return 'hello %s' % number


# 定义一个使用列表、变量的模板
@app.route('/use_list/<name>')
def use_list(name):
    list = ['hello1','hello2', 'hello3,he', 'hello4']
    return render_template('user.html', name=name, mylist=list)


# 使用全局变量打印浏览器信息
@app.route('/browser/')
def browser_print():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent


# 使用cookie存储数据
@app.route('/save_cookie/')
def save_cookie():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response


# 路由跳转
@app.route('/redirect/')
def route_redirect():
    return redirect('http://www.baidu.com')


# 定义两个路由
@app.route('/route_one/')
@app.route('/route_two/<name>')
def two_route(name=None):
    return render_template('hello.html', name=name)

'''
@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name
'''


# 定义一个通过url_for使用图片作为图标的模板
@app.route('/user_picture/<name>')
def user_pic(name):
    return render_template('extends.html')

# 使用url_for来通过视图函数名打印路由地址
with app.test_request_context():
    print url_for('index_page')
    print url_for('use_list', name='malingjun')
    print url_for('hello_int', number=5)
    print url_for('hello_float', number=12.0)

# 打印flask对象app中的映射关系
a = app.url_map
print (a)


# 定义一个表单类
class NameForm(Form):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('hello.html', form=form, name=name)

manager = Manager(app)
print (manager)
bootstrap = Bootstrap(app)



from flask.ext.sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

if __name__ == '__main__':
    app.run(debug=True)
