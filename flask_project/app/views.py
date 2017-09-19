# !usr/bin/python
# -*- coding: utf-8 -*-
import os

__author__ = 'quyong'

from app import app
from flask import render_template, flash, redirect, session
from flask import url_for
# 导入定义的BaseLogin
from app.forms import BaseLogin, NameForm
from datetime import datetime


@app.route('/first/')
def first():
    author = {
        'name': 'kikay',
        'age': 24
    }
    return render_template('first.html', author=author, title='Welcome')


@app.route('/bootstrap/')
def bootstrap():
    author = {
        'name': 'kikay',
        'age': 20,
        'friends': [
            {'name': 'Andy', 'age': 60},
            {'name': 'Tom', 'age': 29},
            {'name': u'小花', 'age': 18}
        ]
    }
    return render_template('bootstrap.html', author=author, title='Bootstrap')


@app.route('/momentTest/')
def momenttest():
    current_time = datetime.utcnow()
    return render_template('momentTest.html', current_time=current_time)


# 定义处理函数和路由规则，接收GET和POST请求
@app.route('/baselogin/', methods=('POST', 'GET'))
def baselogin():
    form = BaseLogin()
    # 判断是否是验证提交
    if form.validate_on_submit():
        # 跳转
        flash(form.name.data+'|'+form.password.data)
        return redirect(url_for('success'))
    else:
        # 渲染
        return render_template('baselogin.html', form=form)


@app.route('/success/')
def success():
    return '<h1>Success</h1>'


@app.route('/baselogin2/', methods=('POST', 'GET'))
def baselogin2():
    form = BaseLogin()
    # 判断是否是验证提交
    if form.validate_on_submit():
        name = session.get('name')
        if name is None and name != form.name.data:
            flash(u'您已经切换了用户')
            return redirect(url_for('success'))
        elif name == None:
            session['name'] = form.name.data
    # 渲染
    return render_template('baselogin.html', form=form)


@app.route('/123/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('123.html', form=form, name=name)




