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
@app.route('/')
def hello_world():
    return redirect('http://www.baidu.com')

'''
@app.route('/userid/<int:number>/')
def get_number(number):
    #user = load_user(number)
    if not user:
        abort(404)
    #return '<h1>Hello %s</h1>' % user.name
'''

@app.route('/user/<name>/')
def user(name):
    # return 'hello %s!'% name
    response = make_response('hello %s' % name)
    response.set_cookie('answer','42')
    return response


@app.route('/browser/')
def browser():
    return request.headers.get('User-Agent'),300


@app.route('/hello/')
def hello():
    return render_template('index.html')


@app.route('/hellosomeone/<name>')
def hellosomeone(name):
    list = ['hello1','hello2','hello3,he','hello4']
    return render_template('user.html',name=name,mylist=list)

a = app.url_map
print (a)

manager = Manager(app)
print (manager)
bootstrap = Bootstrap(app)



if __name__ == '__main__':
    app.run()
