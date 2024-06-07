from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_login import current_user, login_required


# Creating a blueprint
views = Blueprint('views', __name__)

# Creating a routes

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/story')
@login_required
def story():
    return render_template('story.html')

@views.route('/therapist')
@login_required
def therapist():
    return render_template('therapist.html')

@views.route('/ngoservices')
@login_required
def ngoservices():
    return render_template('ngoservices.html')

@views.route('/news')
@login_required
def news():
    return render_template('news.html')

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)