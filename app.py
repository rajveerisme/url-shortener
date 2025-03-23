from flask import Flask, request, jsonify
import string
import random

app = Flask(__name__)

# In-memory dictionary to store URLs (will be replaced by a database later)
url_mapping = {}

def generate_short_code(length=6):
    """Generates a random short URL key using Base62 encoding (letters + numbers)."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """API endpoint to shorten a URL."""
    data = request.json
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()
    url_mapping[short_code] = original_url

    return jsonify({"short_url": f"http://127.0.0.1:5000/{short_code}"})

if __name__ == '__main__':
    app.run(debug=True)
