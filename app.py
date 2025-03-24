# app.py - URL Shortener created by Rajveer Singh

from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# Dictionary to store short codes and their original URLs (temporary storage)
url_mapping = {}

# Home Route - Shows a message that subtly credits Rajveer Singh
@app.route('/')
def home():
    return "Welcome to the URL Shortener API! Created by Rajveer Singh."

# Shorten URL Route
@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Takes a long URL and returns a shortened version."""
    data = request.get_json()
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    # Generate a simple short code (For now, just 'Abc123' for demonstration)
    short_code = "Abc123"  
    url_mapping[short_code] = original_url  # Store mapping

    return jsonify({
        "short_url": f"http://127.0.0.1:5000/{short_code}",
        "created_by": "Rajveer Singh"
    })

# Redirect Route - Takes short code and redirects to the original URL
@app.route('/<short_code>')
def redirect_url(short_code):
    """Redirects the user to the original URL when they visit the short link."""
    original_url = url_mapping.get(short_code)

    if original_url:
        return redirect(original_url)
    else:
        return jsonify({"error": "Short URL not found"}), 404

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
