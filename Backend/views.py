from flask import Flask, render_template, request, redirect, url_for, Blueprint,flash
from flask_login import current_user, login_required
from .models import *
from datetime import datetime
import requests
import os

# API for news
NEWS_API_KEY=os.environ.get('NEWS_API_KEY')
NEWS_API_URL = 'https://newsapi.org/v2/everything'


# Creating a blueprint
views = Blueprint('views', __name__)

# Creating a routes

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/story', methods=['GET'])
@login_required
def story():
    posts = get_blog_posts()
    if posts:
        return render_template('story.html',posts=posts)
    else:
        flash('No posts found!', category='warning')
        return render_template('story.html' ,posts=[])
    


@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if title and content:
            # creating a document for this information named post
            insert_blog_post(title, content, current_user._id)
            flash('Post created successfully!', category='success')
            return redirect(url_for('views.story'))
        
        else:
            flash('Post creation failed!', category='error')

    return render_template('create-post.html')  

@views.route('/delete-post/<post_id>',methods=['GET'])
@login_required
def delete_post(post_id):
    # Delete the post
    delete_post_in_collections(post_id)
    flash('Post deleted successfully!', category='success')
    return redirect(url_for('views.story'))

@views.route('/therapist')
@login_required
def therapist():
    return render_template('therapist.html')

@views.route('/ngoservices')
@login_required
def ngoservices():
    return render_template('ngoservices.html')

# @views.route('/news')
# @login_required
# def news():
#     return render_template('news.html')

@views.route('/news', methods=['GET', 'POST'])
def news():
    topic = request.args.get('topic')
    if request.method == 'POST':
        topic = request.form.get('topic')
    
    news_data = []
    if topic:
        params = {
            'apiKey': NEWS_API_KEY,
            'q': topic,
            'sortBy': 'publishedAt',
            'language': 'en'
        }
        try:
            response = requests.get(NEWS_API_URL, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            news_data = response.json().get('articles', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")

    return render_template('news.html', news=news_data, topic=topic)


@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

