import random
import string
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# Load existing URL data from data.json
def load_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save URL data to data.json
def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

# Generate a random short code of a given length
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Helper function to check if the URL has expired
def is_url_expired(timestamp):
    return datetime.utcnow() > timestamp + timedelta(hours=24)

@app.route("/shorten", methods=["POST"])
def shorten_url():
    # Get the URL from the request
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400

    original_url = data["url"]

    # Load the existing data
    url_data = load_data()

    # Check if the URL is already shortened and return the same short code if found
    for short_code, info in url_data.items():
        if info["url"] == original_url:
            return jsonify({
                "shortened_url": f"http://127.0.0.1:5000/{short_code}",
                "created_by": "Rajveer Singh"
            })

    # Generate a new short code
    short_code = generate_short_code()
    created_at = datetime.utcnow()

    # Store the new shortened URL with the creation timestamp
    url_data[short_code] = {
        "url": original_url,
        "created_by": "Rajveer Singh",
        "created_at": created_at.isoformat()
    }

    # Save the updated data to data.json
    save_data(url_data)

    return jsonify({
        "shortened_url": f"http://127.0.0.1:5000/{short_code}",
        "created_by": "Rajveer Singh"
    })

@app.route("/<short_code>", methods=["GET"])
def redirect_to_url(short_code):
    # Load the existing data
    url_data = load_data()

    # Check if the short code exists
    if short_code not in url_data:
        return jsonify({"error": "Shortened URL not found"}), 404

    # Retrieve the URL info
    info = url_data[short_code]
    original_url = info["url"]
    created_at = datetime.fromisoformat(info["created_at"])

    # Check if the URL has expired
    if is_url_expired(created_at):
        return jsonify({"error": "This URL has expired"}), 410

    # Redirect to the original URL
    return redirect(original_url)

if __name__ == "__main__":
    app.run(debug=True)
