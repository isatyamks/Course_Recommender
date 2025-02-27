from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
import os
import csv
import random
from functools import wraps
from groq import Groq
import requests
from dotenv import load_dotenv
import os

import re
import json






app = Flask(__name__)
app.secret_key = os.urandom(24)

users = {}
USER_DATA_FILE = 'users.csv'

load_dotenv()
api_key = os.getenv('API_KEY')
client = Groq(api_key=api_key)


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
    print(linkedin)
    api_key = "67c0b380bd375d7bb8171f90"
    url = "https://api.scrapingdog.com/linkedin"
    params = {
        "api_key": api_key,
        "type": "profile",
        "linkId": linkedin,
        "private": "false"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        data = {}
    return data

data = scrap(linkedin)






def extract_text(data):
    try:
        prompt = f"""
        Given the following LinkedIn profile data:
        {data}
        
        Identify the user's skills, interests, and current expertise level. Based on this information, recommend a list of courses they should take next to enhance their career. 
        
        The output should be a Python list of dictionaries, where each dictionary contains:
        - "title": The course name
        - "description": A brief summary of the course
        - "level": One of "Beginner", "Intermediate", or "Advanced"
        
        Example output:
        [
            {"title": "Machine Learning Fundamentals", "description": "Learn the basics of ML algorithms", "level": "Beginner"},
            {"title": "Advanced Python Programming", "description": "Master Python for data science", "level": "Intermediate"}
        ]
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an AI that extracts structured information from resumes and recommends career-enhancing courses."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            top_p=1,
            stop=None,
            stream=False,
        )

        extracted_data = chat_completion.choices[0].message.content.strip()
        json_match = re.search(r"\[.*\]", extracted_data, re.DOTALL)
        if not json_match:
            return {"error": "Invalid format received from API"}

        json_str = json_match.group(0)  

        try:
            parsed_data = json.loads(json_str)  
            return parsed_data
        except json.JSONDecodeError:
            return {"error": "Received malformed data from API"}

    except Exception as e:
        return {"error": str(e)}






def get_recommendations(linkedin, github):
    data = scrap(linkedin)
    # print(data)
    recommendations =extract_text(data)
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