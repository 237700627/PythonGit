# !usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'quyong'

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object('config')
moment = Moment(app)

from app import views
