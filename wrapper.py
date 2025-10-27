import sys
import os
import webbrowser
from threading import Timer
from app import app  # Import the Flask application

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Automatically open the browser after a few seconds
    Timer(2.0, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)