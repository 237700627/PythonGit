# !usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'quyong'

# 引入Form基类
from flask.ext.wtf import Form
# 引入Form元素父类
from wtforms import StringField, PasswordField
# 引入Form验证父类
from wtforms.validators import DataRequired, Length

__author__ = 'kikay'

# 登录表单类,继承与Form类
class BaseLogin(Form):
    # 用户名
    name = StringField('name', validators=[DataRequired(message = u"用户名不能为空")
        , Length(10, 20, message=u'长度位于10~20之间')], render_kw = {'placeholder': u'输入用户名'})
    # 密码
    password = PasswordField('password', validators=[DataRequired(message = u"密码不能为空")
        ,Length(10,20, message = u'长度位于10~20之间')], render_kw = {'placeholder': u'输入密码'})