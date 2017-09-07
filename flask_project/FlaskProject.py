from flask import Flask,url_for,render_template,request
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/<username>/')
def hello_username(username):
    return 'hello %s!' % username

@app.route('/int/<int:number>')
def hello_int(number):
    return 'hello %s' % number

@app.route('/float/<float:number>')
def hello_float(number):
    return 'hello %s' % number

with app.test_request_context():
    print url_for('hello_world')
    print url_for('hello_username',username='malingjun')
    print url_for('hello_int',number=5)
    print url_for('hello_float',number=12.0)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()

# url_for('static',filename='style.css')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html',name=name)






if __name__ == '__main__':
    app.run(debug = True,host = '0.0.0.0')
