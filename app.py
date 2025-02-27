from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this in production

# Mock user database - in a real app, use a proper database
users = {}

# Mock course recommendation function (simulating ML model)
def get_course_recommendations(linkedin_username, github_username):
    # In a real app, this would call your ML model and external APIs
    
    # Mock data based on profiles
    skills = []
    if linkedin_username == "data_scientist":
        skills = ["Python", "Statistics"]
    elif linkedin_username == "web_dev":
        skills = ["HTML", "CSS"]
    else:
        skills = ["Communication"]
        
    # Add skills based on GitHub
    if github_username == "ml_expert":
        skills.append("Machine Learning")
    elif github_username == "frontend_dev":
        skills.append("JavaScript")
    
    # Mock course recommendations
    courses = [
        {
            "title": "Python for Data Science",
            "provider": "Coursera",
            "url": "https://www.coursera.org/learn/python-for-data-science",
            "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "description": "Learn Python programming basics and data analysis techniques."
        },
        {
            "title": "Machine Learning Fundamentals",
            "provider": "edX",
            "url": "https://www.edx.org/learn/machine-learning",
            "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "description": "Introduction to machine learning algorithms and applications."
        },
        {
            "title": "Web Development Bootcamp",
            "provider": "Udemy",
            "url": "https://www.udemy.com/course/the-web-developer-bootcamp/",
            "image": "https://images.unsplash.com/photo-1547658719-da2b51169166?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "description": "Complete web development course covering HTML, CSS, JavaScript, and more."
        },
        {
            "title": "Data Visualization with D3.js",
            "provider": "Pluralsight",
            "url": "https://www.pluralsight.com/courses/d3js-data-visualization-fundamentals",
            "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "description": "Learn to create interactive data visualizations with D3.js."
        },
        {
            "title": "Deep Learning Specialization",
            "provider": "Coursera",
            "url": "https://www.coursera.org/specializations/deep-learning",
            "image": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "description": "Master deep learning techniques and neural networks."
        }
    ]
    
    # In a real app, you would filter courses based on skills and profile analysis
    return courses

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        linkedin = request.form["linkedin"]
        github = request.form["github"]
        
        if username in users:
            return render_template("signup.html", error="Username already exists")
        
        users[username] = {
            "password": password,
            "linkedin": linkedin,
            "github": github,
            "joined": datetime.now().strftime("%Y-%m-%d")
        }
        
        session["user"] = username
        return redirect(url_for("dashboard"))
    
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))
    
    username = session["user"]
    user_data = users[username]
    
    # Get course recommendations
    courses = get_course_recommendations(user_data["linkedin"], user_data["github"])
    
    return render_template("dashboard.html", 
                          user=username, 
                          linkedin=user_data["linkedin"],
                          github=user_data["github"],
                          courses=courses)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)