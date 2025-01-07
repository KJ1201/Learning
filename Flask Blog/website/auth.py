from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        fname=request.form.get("fname")
        email=request.form.get("email")
        password =request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged In.', category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            
            else:
                flash('Password is incorrect', category="error")

        else:
            flash('User does not exists.', category="error")


    return render_template("login.html", user=current_user, cuser=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        fname=request.form.get("fname")
        email=request.form.get("email")
        pass1=request.form.get("password1")
        pass2=request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        fname_exists = User.query.filter_by(username=fname).first()

        if email_exists:
            flash('Email already exists.', category="error")

        elif fname_exists:
            flash('Username is already taken.', category="error")

        elif pass1!=pass2:
            flash('Password does not match.', category="error")

        elif len(fname) < 2:
            flash('Username is too short.', category="error")

        elif len(pass1) < 6:
            flash('Password should be more than 6 characters.', category="error")

        elif len(email) < 4:
            flash('Email is invalid.', category="error")

        else:
            new_user = User(email=email, username=fname, password=generate_password_hash(pass1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created successfully.', category="success")
            return redirect(url_for('views.home'))
    
    return render_template("signup.html", user=current_user, cuser=current_user)

@login_required
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("views.home"))