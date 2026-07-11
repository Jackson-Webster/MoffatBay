"""
Kimberly Orozco
Index/Landing Page Backend
Moffat Bay Lodge
"""
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/index.css")
def css():
    return send_from_directory(".", "index.css")

# this is for the image in the index so that way it can for sure work
@app.route("/images/<path:filename>")
def images(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(debug=True)