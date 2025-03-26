import os
import json
import random
import string
from flask import Flask, request, jsonify, redirect
from urllib.parse import urlparse

app = Flask(__name__)

# File to store the short URLs
DATA_FILE = "data.json"

# Load existing URL mappings if the file exists
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

url_mapping = load_data()

def save_to_file():
    """Save the current URL mappings to data.json"""
    with open(DATA_FILE, "w") as file:
        json.dump(url_mapping, file)

def generate_short_code():
    """Generate a random 6-character short code"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def is_valid_url(url):
    """Check if the given URL is valid"""
    parsed = urlparse(url)
    return parsed.scheme in ["http", "https"] and bool(parsed.netloc)

@app.route("/")
def home():
    return "Welcome to the URL Shortener API! Created by Rajveer Singh."

@app.route("/shorten", methods=["POST"])
def shorten_url():
    """Shorten a URL and return the short version"""
    data = request.get_json()
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "Missing URL"}), 400

    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    # Check if URL is already shortened
    for short_code, url in url_mapping.items():
        if url == original_url:
            return jsonify({"short_url": f"http://127.0.0.1:5000/{short_code}"}), 200

    # Generate a new short code
    short_code = generate_short_code()
    url_mapping[short_code] = original_url
    save_to_file()

    return jsonify({"short_url": f"http://127.0.0.1:5000/{short_code}"}), 201

@app.route("/<short_code>")
def redirect_url(short_code):
    """Redirect a short URL to the original URL"""
    original_url = url_mapping.get(short_code)
    if original_url:
        return redirect(original_url)
    return jsonify({"error": "Short URL not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
