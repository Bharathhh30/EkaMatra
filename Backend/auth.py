from flask import Flask, render_template, request, redirect, url_for, Blueprint ,flash
from .models import add_user, get_user_by_email , get_user_by_username , get_user_by_id, User
from flask_login import login_user , current_user , logout_user
from . import *
from flask_bcrypt import Bcrypt

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()


@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        user = get_user_by_email(email)
        user2 = get_user_by_username(username)
        if user:
            flash('Email already exists', category='error')
            return redirect(url_for('auth.signup'))

        elif password != confirm_password:
            flash('Passwords do not match', category='error')
            return redirect(url_for('auth.signup'))
        
        elif user2:
            flash('Username already exists', category='error')
            return redirect(url_for('auth.signup'))

        else:
            user3=add_user(username,email,password)

            
            login_user(user3, remember=True)

            flash('Account created!', category='success')

            return redirect(url_for('views.home'))
    return render_template('signup.html')

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_data = get_user_by_email(email)
        if user_data:
            if bcrypt.check_password_hash(user_data.password, password):
                # Create a User instance from the retrieved data
                user = User(user_data._id, user_data.username, user_data.email, user_data.password)
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.story'))
            else:
                flash('Incorrect password, try again.', category='error')
                return redirect(url_for('auth.signin'))
        else:
            flash('Email does not exist.', category='error')
            return redirect(url_for('auth.signin'))
    return render_template('signin.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))