from flask import render_template, request, redirect, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash


bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "bio": request.form['bio'],
        "profile_picture": request.form['profile_picture'],
        "email": request.form['email'],
        "password": pw_hash
        }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['first_name'] = data['first_name']
    session['last_name'] = data['last_name']
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = { 
        "email" : request.form["email"] 
        }
    user = User.get_by_email(data)
    if not user:
        flash(u"Invalid Email/Password", 'login error')
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash(u"Invalid Email/Password", 'login error')
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect('/dashboard')

@app.route('/log-out')
def clear():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if session.get("user_id") == None:
        return redirect('/')
    user = User.get_one(session['user_id'])
    return render_template("dashboard.html" , user = user)

@app.route('/account')
def account():
    id=session['user_id']
    if session.get("user_id") == None:
        return redirect('/')
    user = User.get_one(id)
    return render_template("account.html", user = user)

@app.route('/edit_user/<int:id>', methods=['POST'])
def edit_user(id):
    if not User.validate_update(request.form):
        return redirect(f'/account/{id}')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "bio": request.form['bio'],
        "profile_picture": request.form['profile_picture'],
        "id": id
        }
    User.edit(data, id)
    return redirect(f'/account')