#import os

from flask import Flask, render_template, request
#from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
#heroku = Heroku(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/invitation', methods=['POST'])
def invite():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')

if __name__ == '__main__':
    #app.debug = True
    app.run()