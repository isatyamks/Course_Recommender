from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import csv
import random
from functools import wraps
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

users = {}
USER_DATA_FILE = 'users.csv'

if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password', 'linkedin', 'github'])

def load_users():
    global users
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row['username']] = {
                    'password': row['password'],
                    'linkedin': row['linkedin'],
                    'github': row['github']
                }

def save_user(username, password, linkedin, github):
    with open(USER_DATA_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, linkedin, github])

load_users()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def scrap(linkedin):
    # print(linkedin)
    api_key = "67c03d3d33734d79746429d7"
    url = "https://api.scrapingdog.com/linkedin"
    params = {
        "api_key": api_key,
        "type": "profile",
        "linkId":linkedin,
        "private": "false"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
    return response


def get_recommendations(linkedin, github):
    data = scrap(linkedin)
    print(data)
    courses = [
        {"title": "Machine Learning Fundamentals", "description": "Learn the basics of ML algorithms", "level": "Beginner"},
        {"title": "Advanced Python Programming", "description": "Master Python for data science", "level": "Intermediate"},
        {"title": "Web Development with Flask", "description": "Build web applications with Flask", "level": "Beginner"},
        {"title": "Data Structures and Algorithms", "description": "Essential CS concepts for coding interviews", "level": "Intermediate"},
        {"title": "Deep Learning with TensorFlow", "description": "Build neural networks with TensorFlow", "level": "Advanced"},
        {"title": "Full Stack JavaScript", "description": "Master Node.js, React, and MongoDB", "level": "Intermediate"},
        {"title": "DevOps and CI/CD", "description": "Learn modern deployment workflows", "level": "Advanced"},
        {"title": "Cloud Computing with AWS", "description": "Deploy applications on AWS", "level": "Intermediate"}
    ]
    
    recommendations = []
    
    if 'dev' in github.lower() or 'web' in github.lower():
        recommendations.append(courses[2])  
        recommendations.append(courses[5])  
    
    if 'data' in linkedin.lower() or 'science' in linkedin.lower():
        recommendations.append(courses[0])  
        recommendations.append(courses[1])  
        recommendations.append(courses[4])      
    if 'engineer' in linkedin.lower() or 'software' in github.lower():
        recommendations.append(courses[3])  
        recommendations.append(courses[6])  
    while len(recommendations) < 4:
        random_course = random.choice(courses)
        if random_course not in recommendations:
            recommendations.append(random_course)
    
    return recommendations

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        linkedin = request.form['linkedin']
        github = request.form['github']
        
        if username in users:
            flash('Username already exists!')
            return render_template('signup.html')
        
        users[username] = {
            'password': password,
            'linkedin': linkedin,
            'github': github
        }
        
        save_user(username, password, linkedin, github)
        
        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    user_data = users[username]
    recommendations = get_recommendations(user_data['linkedin'], user_data['github'])
    return render_template('dashboard.html', username=username, recommendations=recommendations)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)