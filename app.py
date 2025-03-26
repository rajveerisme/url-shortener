import os
import json
import random
import string
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# Load existing URL mappings from a JSON file
DATA_FILE = "data.json"

def load_data():
    """Load URL mappings from data.json file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}  # Return an empty dictionary if file is empty or corrupted
    return {}

def save_data(data):
    """Save URL mappings to data.json file"""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Load existing data
url_mapping = load_data()

def generate_short_code(length=6):
    """Generate a random short code of given length"""
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def home():
    """Home route with a subtle attribution"""
    return "Welcome to the URL Shortener API!<br>Created by Rajveer Singh."

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Shorten a URL and return the same short code if already shortened"""
    data = request.get_json()
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    # Check if the URL was already shortened
    for short_code, url in url_mapping.items():
        if url == original_url:
            return jsonify({
                "short_url": f"http://127.0.0.1:5000/{short_code}",
                "created_by": "Rajveer Singh"
            })

    # Generate a unique short code for a new URL
    short_code = generate_short_code()
    url_mapping[short_code] = original_url
    save_data(url_mapping)

    return jsonify({
        "short_url": f"http://127.0.0.1:5000/{short_code}",
        "created_by": "Rajveer Singh"
    })

@app.route('/<short_code>')
def redirect_url(short_code):
    """Redirect a short URL to the original URL"""
    original_url = url_mapping.get(short_code)
    if original_url:
        return redirect(original_url)
    return jsonify({"error": "Short URL not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
