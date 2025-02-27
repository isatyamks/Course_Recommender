from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import csv
import json
import re
import requests
from functools import wraps
from groq import Groq
from dotenv import load_dotenv

import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def clean_text(text):
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.replace('\n', ' ')
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_text = ' '.join([word for word in words if word.lower() not in stop_words])
    
    return filtered_text

def process_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for entry in data:
        if 'text' in entry:
            entry['text'] = clean_text(entry['text'])
        entry.pop('people_also_viewed', None)
        entry.pop('similar_profiles', None)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

input_file = 'data\\isatyamks.json'  
output_file = 'data\\isatyamks.json'
process_json(input_file, output_file)



app = Flask(__name__)
app.secret_key = os.urandom(24)

users = {}
USER_DATA_FILE = 'users.csv'

load_dotenv()
api_key = os.getenv('API_KEY')
client = Groq(api_key=api_key)

# Ensure the CSV file exists
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password', 'linkedin', 'github'])

# Load users from CSV
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

# Save user data to CSV
def save_user(username, password, linkedin, github):
    with open(USER_DATA_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, linkedin, github])

load_users()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Scrape LinkedIn profile
def scrap(linkedin):
    print(f"Scraping LinkedIn profile: {linkedin}")
    api_key = "67c0c8e1f6aabc6c38a5d2e0"
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
        username = linkedin.split('/')[-1]
        folder_path = os.path.join('data')
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f'{username}.json')

        with open(file_path, 'w') as f:
            json.dump(data, f)
            input_file = f'data\\{username}.json'  
            output_file = f'data\\{username}.json'
            process_json(input_file, output_file)

        return username, file_path
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None, None

# Extract text and generate recommendations
def extract_text(username, file_path):
    try:
        if not file_path or not os.path.exists(file_path):
            return {"error": "Profile data not found"}

        with open(file_path, 'r') as f:
            data = f.read()
        print(data)
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
            {{"title": "Machine Learning Fundamentals", "description": "Learn the basics of ML algorithms", "level": "Beginner"}},
            {{"title": "Advanced Python Programming", "description": "Master Python for data science", "level": "Intermediate"}}
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

        extracted_data = chat_completion.choices[0].message['content'].strip()
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

# Generate recommendations
def get_recommendations(linkedin, github):
    username, file_path = scrap(linkedin)
    if not username or not file_path:
        return {"error": "Failed to scrape LinkedIn profile"}
    
    recommendations = extract_text(username, file_path)
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

    if not user_data['linkedin']:
        recommendations = {"error": "No LinkedIn profile provided"}
    else:
        recommendations = get_recommendations(user_data['linkedin'], user_data['github'])

    return render_template('dashboard.html', username=username, recommendations=recommendations)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
