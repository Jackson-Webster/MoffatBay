"""
Kimberly Orozco
Contact Us Backend
Moffat Bay Lodge
"""

from flask import Flask, request, send_from_directory
from datetime import datetime
import mysql.connector

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "contact.html")

@app.route("/contact.css")
def css():
    return send_from_directory(".", "contact.css")

@app.route("/contact", methods=["POST"])
def contact():

    full_name = request.form["fullName"]
    email = request.form["email"]
    phone_number = request.form["phoneNumber"]
    message = request.form["message"]

    connection = mysql.connector.connect(
        host="localhost",
        port=3306,      # My port is in 3306 but you can change it to your own port if u need :D
        user="root",
        password="",
        database="MoffatBay"
    )

    cursor = connection.cursor()

    sql = """
    INSERT INTO Contact
    (fullName, email, phoneNumber, message, dateSubmitted)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        full_name,
        email,
        phone_number,
        message,
        datetime.now()
    )

    cursor.execute(sql, values)

    connection.commit()

    cursor.close()
    connection.close()

    return """
    <h2>Thank you!</h2>
    <p>Your message has been sent successfully.</p>
    <br>
    <a href="/">Return to Contact Page</a>
    """

if __name__ == "__main__":
    app.run(debug=True)