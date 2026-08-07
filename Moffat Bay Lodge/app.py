"""
Moffat Bay Lodge
Combined Website Backend

Team Members:
Jackson Webster
Kimberly Orozco
Darreon Tolen
"""

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    session
)

import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "moffatbaysecretkey"


# =====================================================
# Database Connection
# You will need to change the database settigns to match your database
# =====================================================

def get_connection():
    return mysql.connector.connect(
        host="localhost", 
        port=3309,
        user="root",
        password="",
        database="MoffatBay"
    )



# =====================================================
# Kimberly Orozco
# Landing Page Backend
# =====================================================

@app.route("/")
def home():
    return render_template("index.html")


# =====================================================
# Kimberly Orozco
# About Us Backend
# =====================================================

@app.route("/about")
def about():
    return render_template("about.html")


# =====================================================
# Kimberly Orozco
# Contact Us Backend
# =====================================================

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact", methods=["POST"])
def submit_contact():

    fullName = request.form["fullName"]
    email = request.form["email"]
    phoneNumber = request.form["phoneNumber"]
    message = request.form["message"]

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    INSERT INTO contact
    (fullName, email, phoneNumber, message, dateSubmitted)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        fullName,
        email,
        phoneNumber,
        message,
        datetime.now()
    )

    cursor.execute(sql, values)

    connection.commit()

    cursor.close()
    connection.close()

    return "Message Sent Successfully!"

# =====================================================
# Darreon Tolen
# Login Backend
# =====================================================

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_user():

    email = request.form["email"]
    password = request.form["password"]

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT customerID, firstName, lastName
        FROM Customer
        WHERE email=%s AND password=%s
        """,
        (email, password)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:

        session["customerID"] = user["customerID"]
        session["name"] = user["firstName"]

        return redirect(url_for("home"))

    return "Invalid email or password."

# =====================================================
# Jackson Webster
# Registration Backend
# =====================================================

@app.route("/registration")
def registration():
    return render_template("registration.html")


@app.route("/register", methods=["POST"])
def register():

    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    email = request.form["email"]
    phone_number = request.form["phoneNumber"]
    password = request.form["password"]

    connection = get_connection()
    cursor = connection.cursor()

    # Check if email already exists
    cursor.execute(
        "SELECT customerID FROM Customer WHERE email=%s",
        (email,)
    )

    if cursor.fetchone():
        cursor.close()
        connection.close()
        return "Error: That email is already registered."

    # Check if phone number already exists
    cursor.execute(
        "SELECT customerID FROM Customer WHERE phoneNumber=%s",
        (phone_number,)
    )

    if cursor.fetchone():
        cursor.close()
        connection.close()
        return "Error: That phone number is already registered."

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

# =====================================================
# Jackson Webster
# Room Reservation Backend
# =====================================================

@app.route("/reservation")
def reservation():
    return render_template("reservation.html")


@app.route("/reserve", methods=["POST"])
def reserve():

    customer_id = request.form["customerID"]
    room_type = request.form["roomType"]
    check_in = request.form["checkIn"]
    check_out = request.form["checkOut"]
    guests = request.form["guests"]
    special_requests = request.form.get("specialRequests", "")

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    INSERT INTO Reservation
    (customerID, roomType, checkInDate, checkOutDate, guests, specialRequests)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    values = (
        customer_id,
        room_type,
        check_in,
        check_out,
        guests,
        special_requests
    )

    cursor.execute(sql, values)

    reservation_id = cursor.lastrowid

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("reservation_summary", reservationID=reservation_id))


# =====================================================
# Jackson Webster
# Reservation Summary Backend
# =====================================================

@app.route("/summary")
def reservation_summary():

    reservation_id = request.args.get("reservationID")

    if reservation_id is None:
        return redirect(url_for("reservation"))

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM Reservation
        WHERE reservationID=%s
        """,
        (reservation_id,)
    )

    reservation = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "summary.html",
        reservation=reservation,
        message="Reservation Created Successfully!"
    )


@app.route("/confirm", methods=["POST"])
def confirm_reservation():
    return "Reservation Confirmed!"


@app.route("/cancel", methods=["POST"])
def cancel_reservation():
    return "Reservation Cancelled!"


# =====================================================
# Darreon Tolen
# Reservation Lookup Backend
# =====================================================

@app.route("/lookup")
def lookup():
    return render_template("lookup.html")


@app.route("/lookup", methods=["POST"])
def lookup_reservation():

    reservation_id = request.form["reservationID"]

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM Reservation
        WHERE reservationID=%s
        """,
        (reservation_id,)
    )

    reservation = cursor.fetchone()

    cursor.close()
    connection.close()

    if reservation is None:
        return "Reservation not found."

    return render_template(
        "summary.html",
        reservation=reservation,
        message=""
    )

# =====================================================
# Jackson Webster
# Attractions Backend
# =====================================================

@app.route("/attractions")
def attractions():
    return render_template("attractions.html")


# =====================================================
# Utility Routes
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


@app.route("/health")
def health():
    return "Moffat Bay Website Running Successfully!"


# =====================================================
# Run Flask Application
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)