from flask import Flask,redirect,url_for,render_template,request
from datetime import datetime
from flask.signals import template_rendered 

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

@app.route('/admin', methods=['GET', 'POST'])
def home():
   users = User.query.all()
   return render_template('index.html', users=users)       

@app.route('/add',methods=['GET','POST'])
def Add():
    if request.method=='POST':
        user = User(  name=request.form['name'], message=request.form['message'] )
        db.session.add(user)
        db.session.commit()
        return redirect('/admin')
    users = User.query.all()
    return render_template('add.html', users=users)

 
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    
    if request.method=='POST':
        name = request.form['title'],
        message= request.form['msg']
        users = User.query.filter_by(sno=sno).first()
        users.name= name
        users.message= message 
        # users = User(  name=request.form['name'], message=request.form['message'] ).query.filter_by(sno=sno).first
        db.session.add(users)
        db.session.commit()
        return redirect("/admin")
       
    users = User.query.filter_by(sno=sno).first()
    return render_template('update.html', users=users)



@app.route('/delete/<int:sno>', methods=['GET'])
def delete(sno):
   users = User.query.filter_by(sno=sno).first()
   db.session.delete(users)
   db.session.commit()
   return redirect('/admin')

@app.route('/delete', methods=['GET'])
def deleteall():
   db.session.query(User).delete()
   db.session.commit()
   return redirect('/admin')   

if __name__ == '__main__':
    app.run(port=5000, debug=True)