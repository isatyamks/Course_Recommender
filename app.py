from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/linkedin', methods=['POST'])
def scrape_profile():
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({"error": "Invalid input. 'username' is required."}), 400

    username = data['username']
    api_key = "67c0284dc3c25e43dac2171b"
    url = "https://api.scrapingdog.com/linkedin"
    params = {
        "api_key": api_key,
        "type": "profile",
        "linkId": username,
        "private": "false"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": f"Request failed with status code: {response.status_code}"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
