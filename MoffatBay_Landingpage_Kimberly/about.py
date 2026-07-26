"""
Kimberly Orozco
About Us Page Backend
Moffat Bay Lodge
"""
from flask import Flask, send_from_directory
app = Flask(__name__)

@app.route("/")
def about():
    return send_from_directory(".", "about.html")

@app.route("/about.css")
def css():
    return send_from_directory(".", "about.css")

@app.route("/images/<path:filename>")
def images(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(debug=True)