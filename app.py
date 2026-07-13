from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for
)

from flask_mysqldb import MySQL
from config import Config

import os
import random

from werkzeug.utils import secure_filename
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_mail import Mail, Message

# AWS S3 Helper
from utils.s3_helper import (
    upload_file_to_s3,
    upload_profile_photo,
    delete_file_from_s3,
    delete_profile_photo,
    get_file_url,
    get_profile_photo_url
)

app = Flask(__name__)

app.secret_key = "myvault_secret_key"

app.config.from_object(Config)

# -----------------------------
# Profile Photo Folder
# -----------------------------
PROFILE_FOLDER = "static/profile_images"

app.config["PROFILE_FOLDER"] = PROFILE_FOLDER

os.makedirs(PROFILE_FOLDER, exist_ok=True)

# -----------------------------
# Mail Configuration
# -----------------------------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True


mail = Mail(app)

# -----------------------------
# MySQL
# -----------------------------
mysql = MySQL(app)

# -----------------------------
# Temporary OTP Storage
# -----------------------------
otp_storage = {}

# -----------------------------
# Home
# -----------------------------
@app.route("/")
def home():

    return render_template("index.html")


# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()

        if user and check_password_hash(
            user[6],
            password
        ):

            session["user_id"] = user[0]
            session["user_name"] = user[1]

            return redirect(
                url_for("dashboard")
            )

        else:

            return "Invalid Email or Password"

    return render_template("login.html")
# -----------------------------
# Register
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        phone = request.form["phone"]
        email = request.form["email"]
        dob = request.form["dob"]
        gender = request.form["gender"]

        password_input = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password_input != confirm_password:
            return "Passwords do not match"

        password = generate_password_hash(password_input)

        photo = request.files["profile_photo"]

        filename = None

        if photo and photo.filename:

            filename = secure_filename(photo.filename)

            # Upload profile photo to AWS S3
            upload_profile_photo(
                photo,
                filename
            )

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.close()

            return "Email already registered"

        cursor.execute(
            """
            INSERT INTO users
            (full_name, phone, email, dob, gender, password, profile_photo)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                full_name,
                phone,
                email,
                dob,
                gender,
                password,
                filename
            )
        )

        mysql.connection.commit()

        cursor.close()

        return "Registration Successful"

    return render_template("register.html")


# -----------------------------
# Forgot Password
# -----------------------------
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()

        if user:

            otp = random.randint(
                100000,
                999999
            )

            otp_storage[email] = otp

            msg = Message(
                "MyVault Password Reset OTP",
                sender=app.config["MAIL_USERNAME"],
                recipients=[email]
            )

            msg.body = (
                f"Your MyVault OTP is {otp}"
            )

            mail.send(msg)

            session["reset_email"] = email

            return redirect(
                url_for("verify_otp")
            )

        return "Email not found"

    return render_template(
        "forgot_password.html"
    )
# -----------------------------
# Verify OTP
# -----------------------------
@app.route("/verify_otp", methods=["GET", "POST"])
def verify_otp():

    if request.method == "POST":

        otp = request.form["otp"]

        email = session.get("reset_email")

        if email and otp_storage.get(email) == int(otp):

            return redirect(
                url_for("reset_password")
            )

        return "Invalid OTP"

    return render_template(
        "verify_otp.html"
    )


# -----------------------------
# Reset Password
# -----------------------------
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():

    if request.method == "POST":

        password_input = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password_input != confirm_password:

            return "Passwords do not match"

        password = generate_password_hash(
            password_input
        )

        email = session.get("reset_email")

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET password=%s
            WHERE email=%s
            """,
            (
                password,
                email
            )
        )

        mysql.connection.commit()

        cursor.close()

        otp_storage.pop(email, None)

        session.pop("reset_email", None)

        return redirect(
            url_for("login")
        )

    return render_template(
        "reset_password.html"
    )
# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    if "user_id" in session:

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT id, file_name, uploaded_at
            FROM files
            WHERE user_id=%s
            """,
            (session["user_id"],)
        )

        files = cursor.fetchall()

        cursor.close()

        return render_template(
            "dashboard.html",
            name=session["user_name"],
            files=files
        )

    return redirect(
        url_for("login")
    )


# -----------------------------
# Profile
# -----------------------------
@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT full_name, phone, email, dob, gender, profile_photo
        FROM users
        WHERE id=%s
        """,
        (session["user_id"],)
    )

    user = cursor.fetchone()

    cursor.close()

    photo_url = None

    if user and user[5]:
        photo_url = get_profile_photo_url(
            user[5]
        )

    return render_template(
        "profile.html",
        user=user,
        photo_url=photo_url
    )


# -----------------------------
# Edit Profile
# -----------------------------
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    if request.method == "POST":

        full_name = request.form["full_name"]
        phone = request.form["phone"]
        dob = request.form["dob"]
        gender = request.form["gender"]

        # Profile photo
        photo = request.files.get("profile_photo")

        # Get existing photo
        cursor.execute(
            "SELECT profile_photo FROM users WHERE id=%s",
            (session["user_id"],)
        )
        old_photo = cursor.fetchone()[0]

        filename = old_photo

        if photo and photo.filename != "":
            filename = secure_filename(photo.filename)

            # Delete old photo from S3
            if old_photo:
                delete_profile_photo(old_photo)

            # Upload new photo
            upload_profile_photo(photo, filename)

        cursor.execute(
            """
            UPDATE users
            SET
                full_name=%s,
                phone=%s,
                dob=%s,
                gender=%s,
                profile_photo=%s
            WHERE id=%s
            """,
            (
                full_name,
                phone,
                dob,
                gender,
                filename,
                session["user_id"]
            )
        )

        mysql.connection.commit()
        session["user_name"] = full_name

        cursor.close()

        return redirect(url_for("profile"))

    cursor.execute(
        """
        SELECT full_name, phone, dob, gender
        FROM users
        WHERE id=%s
        """,
        (session["user_id"],)
    )

    user = cursor.fetchone()
    cursor.close()

    return render_template(
        "edit_profile.html",
        user=user
    )
# -----------------------------
# Upload File (AWS S3)
# -----------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        file = request.files["file"]

        category = request.form["category"]

        if file and file.filename:

            filename = secure_filename(
                file.filename
            )

            # Upload file to AWS S3
            upload_file_to_s3(
                file,
                filename
            )

            cursor = mysql.connection.cursor()

            cursor.execute(
                """
                INSERT INTO files
                (user_id, file_name, file_path,category)
                VALUES (%s, %s, %s,%s)
                """,
                (
                    session["user_id"],
                    filename,
                    filename,
                    category
                )
            )

            mysql.connection.commit()

            cursor.close()

            return redirect(
                url_for("dashboard")
            )

    return render_template(
        "upload.html"
    )


# -----------------------------
# Download File (AWS S3)
# -----------------------------
@app.route("/download/<filename>")
def download(filename):

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    download_url = get_file_url(filename)

    return redirect(download_url)


# -----------------------------
# Delete File (AWS S3)
# -----------------------------
@app.route("/delete/<int:file_id>")
def delete(file_id):

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT file_name
        FROM files
        WHERE id=%s AND user_id=%s
        """,
        (
            file_id,
            session["user_id"]
        )
    )

    file = cursor.fetchone()

    if file:

        # Delete file from AWS S3
        delete_file_from_s3(
            file[0]
        )

        # Delete database record
        cursor.execute(
            """
            DELETE FROM files
            WHERE id=%s
            """,
            (file_id,)
        )

        mysql.connection.commit()

    cursor.close()

    return redirect(
        url_for("dashboard")
    )
# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":

    app.run(
        debug=True
    )
