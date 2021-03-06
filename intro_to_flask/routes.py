from intro_to_flask import app
from flask import Flask, render_template, request, flash, session, redirect, url_for
from forms import AnimalEntry, SignupForm, SearchForm
from flask.ext.mail import Message, Mail
#from models import db
#import MySQLdb
import sqlite3

# MySQL config
#db = MySQLdb.connect(host="localhost", port=3306, user="ark2", passwd="ark2", db="ark2")
db = sqlite3.connect('ark2.db', check_same_thread=False)
cursor = db.cursor()

mail = Mail()

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/search', methods=['GET', 'POST`'])
def search():
  cursor.execute("SELECT * FROM animal")
  result = cursor.fetchall()
#  return str(result)
  form = SearchForm()

  return render_template('search.html', data=result)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = AnimalEntry()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@sample.com', recipients=['me@home.com'])
      msg.body = """ 
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template('contact.html', success=True)
  elif request.method == 'GET':
    return render_template('contact.html', form=form)
 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup2.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      session['email'] = newuser.email
      return redirect(url_for('profile'))
       
      return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
   
  elif request.method == 'GET':
    return render_template('signup2.html', form=form)

@app.route('/profile')
def profile():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html')