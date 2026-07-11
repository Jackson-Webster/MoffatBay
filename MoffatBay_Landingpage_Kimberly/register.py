"""
Jackson Webster
Registration Page Backend
Moffat Bay Lodge
"""

from flask import Flask, request, send_from_directory
import mysql.connector

app = Flask (__name__)

@app.route("/")
def home():
    return send_from_directory(".", "registration.html")

@app.route("/registration.css")
def css():
    return send_from_directory(".", "registration.css")

@app.route("/register", methods=["POST"])
def register():

    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    email = request.form["email"]
    phone_number = request.form["phoneNumber"]
    password = request.form["password"]
    

    connection = mysql.connector.connect(
        host="localhost",
        port=3309,
        user="root",
        password="",
        database="MoffatBay"
    )

    cursor = connection.cursor()

    # Check if the email already exists
    cursor.execute(
        "SELECT customerID FROM Customer WHERE email = %s",
        (email,)
    )

    if cursor.fetchone():
        cursor.close()
        connection.close()
        return "Error: That email is already registered."

    # Check if the phone number already exists
    cursor.execute(
        "SELECT customerID FROM Customer WHERE phoneNumber = %s",
        (phone_number,)
    )

    if cursor.fetchone():
        cursor.close()
        connection.close()
        return "Error: That phone number is already registered."
    
    # SQL statment
    sql = """
    INSERT INTO Customer
    (firstName, lastName, email, phoneNumber, password)
    VALUES (%s, %s, %s, %s, %s)
    """


    
    
    values = (
        first_name,
        last_name,
        email,
        phone_number,
        password
    )

    
    
    cursor.execute(sql, values)

    connection.commit()

    cursor.close()

    connection.close()

    return "Registration Successful!"

if __name__ == "__main__":
    app.run(debug=True)