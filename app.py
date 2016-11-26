from flask import Flask, render_template, request, \
      redirect, url_for, session, flash, g
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
#import sqlite3
#import sqlalchemy

app = Flask(__name__)

app.secret_key = "-my-secret-key"
#app.database = "sample.db"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'

db = SQLAlchemy(app)

from models import *


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You must login')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def root():
    ##sqlie3 database queries
    #g.db = connect_db()
    #cursor = g.db.execute('select * from posts')
    #posts = [dict(title=row[0], description=row[1]) for row in cursor.fetchall()]
    #g.db.close()
    ##sqlAlchemy query is much easier
    posts = db.session.query(WallPost).all()
    return render_template("index.html", posts=posts)

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
          error = 'Invalid username or password. Please try again'
        else:
          session['logged_in'] = True
          flash('You have successfully logged in!')
          return redirect(url_for('root'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You logged out successfully')
    return redirect(url_for('welcome'))

#def connect_db():
 #   return sqlite3.connect(app.database)

if __name__ == '__main__':
      app.run(host='0.0.0.0', debug=True)
