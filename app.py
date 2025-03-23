from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "URL Shortener API is running on Python 3!"

if __name__ == '__main__':
    app.run(debug=True)
