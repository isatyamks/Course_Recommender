# AI-Powered Course Recommendation System

## Overview
This is a Flask-based web application that extracts LinkedIn profile data and recommends career-enhancing courses using AI. The system scrapes a LinkedIn profile, cleans the extracted text, and uses an AI model to generate personalized course recommendations.

## Features
- **User Authentication:** Signup and login functionality with session management.
- **LinkedIn Profile Scraping:** Extracts and cleans data from a LinkedIn profile.
- **AI-Powered Recommendations:** Uses the Groq API to generate a list of courses based on the user's skills and expertise.
- **Dashboard Display:** Displays personalized course recommendations on the user dashboard.

## Technologies Used
- **Backend:** Flask (Python)
- **Frontend:** Jinja2 (HTML, CSS)
- **Database:** CSV-based user storage
- **API Integration:** ScrapingDog API for LinkedIn scraping, Groq API for AI-generated recommendations
- **Natural Language Processing:** NLTK for text cleaning

## Installation
### Prerequisites
- Python 3.x
- Virtual environment (optional but recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your API key:
   ```
   API_KEY=your_groq_api_key
   ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Open your browser and navigate to `http://127.0.0.1:5000`

## Usage
- **Signup/Login:** Users create an account and log in.
- **Profile Setup:** Users provide their LinkedIn profile link.
- **Recommendations:** The system extracts relevant skills and generates recommended courses.
- **Dashboard:** Users view their personalized recommendations.

## API Configuration
- **ScrapingDog API:** Used to scrape LinkedIn profile data.
- **Groq AI API:** Used to generate course recommendations.

## File Structure
```
project/
│── app.py              # Main Flask application
│── templates/          # HTML templates
│── static/             # Static files (CSS, JS)
│── users.csv           # CSV file for storing user data
│── .env                # Environment variables (API keys)
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation
```

## Demo Video
[Watch the demo](https://youtu.be/bDYaAq4sMcY?si=0LO5jQGf4PZcApV9)

## Future Enhancements
- **Database Integration:** Replace CSV with MongoDB or PostgreSQL.
- **OAuth Authentication:** Allow users to log in with LinkedIn.
- **Enhanced NLP:** Improve text processing with more advanced AI models.
- **Email Notifications:** Notify users about new recommended courses.

## License
This project is licensed under the MIT License.

## Contact
For any queries or contributions, contact isatyamks@gmail.com or visit https://github.com/isatyamks.

