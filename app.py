from flask import Flask,redirect,url_for,render_template,request
from datetime import datetime 

from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    """Model for user accounts."""
    __tablename__ = 'users'

    sno = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String,
                         nullable=False,
                         unique=False)
    message = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    date = db.Column(db.DateTime, default= datetime.utcnow) 

    def __repr__(self):
        return '<User {}>'.format(self.name)

@app.route('/index',methods=['GET','POST'])
def home():
    if request.method=='POST':
        user = User(  name=request.form['name'], message=request.form['message'] )
        db.session.add(user)
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/', methods=['GET', 'POST'])
def Users():
   if request.method=='POST':
        name = request.form['name']
        message = request.form['message']
        if message == User.message:
            redirect('/index')
   return render_template('login.html')   

if __name__ == '__main__':
    app.run(port=5000, debug=True)