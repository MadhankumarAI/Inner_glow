from flask import Flask, render_template, request, jsonify,url_for,redirect
import numpy as np
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import pandas as pd

from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import string

import MySQLdb.cursors
import random

from flask import session, flash
from flask_mysqldb import MySQL
import smtplib, os, random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'inner_glow'
mysql = MySQL(app)


app.secret_key = 'dabcdefgheuyijdbf'  

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load AI Model
MODEL_PATH = r"C:\Users\jaip7\Downloads\madhan\innergl\skin_disease_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Load Treatment Data
treatment_df = pd.read_csv(r"C:\Users\jaip7\Downloads\madhan\innergl\dataset\treatments.csv")

# Class labels
CLASS_NAMES = ['MEL', 'NV', 'BCC', 'AKIEC', 'BKL', 'DF', 'VASC']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    print("Dashboard route accessed")  # Debugging log
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')


def generate_otp():
    return str(random.randint(100000, 999999))

# Function to send OTP email
def send_otp_email(email, otp_code):
    sender_email = "madhan786819@gmail.com"
    sender_password = "eyoq ucyg wxks dwjw"  # Use an App Password

    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp_code}. It will expire in 5 minutes."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Error sending email:", str(e))
        return False

# Route to request OTP
@app.route('/get-otp', methods=['POST'])
def get_otp():
    email = request.form.get('email')

    if not email:
        return jsonify({"success": False, "message": "Email is required."})

    otp_code = generate_otp()
    expires_at = datetime.now() + timedelta(minutes=5)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Delete any previous unused OTP for this email
    cursor.execute("DELETE FROM otp_codes WHERE email=%s AND is_used=FALSE", (email,))

    # Insert new OTP
    cursor.execute("INSERT INTO otp_codes (email, otp_code, expires_at, is_used) VALUES (%s, %s, %s, FALSE)", 
                   (email, otp_code, expires_at))
    mysql.connection.commit()
    cursor.close()

    if send_otp_email(email, otp_code):
        return jsonify({"success": True, "message": "OTP sent successfully."})
    else:
        return jsonify({"success": False, "message": "Failed to send OTP. Try again."})


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        otp_code = request.form.get('otp')

        # Store form data in session to preserve input
        session['email'] = email
        session['username'] = username

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Validate OTP
        cursor.execute(
            "SELECT * FROM otp_codes WHERE email=%s AND otp_code=%s AND is_used=FALSE AND expires_at > NOW()",
            (email, otp_code)
        )
        otp_record = cursor.fetchone()

        if not otp_record:
            flash("Invalid or expired OTP.", "danger")
            return redirect('/signup')

        # Check if username is taken
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already taken. Choose a different one.", "danger")
            return redirect('/signup')

        # Secure password hashing
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        # Insert new user
        cursor.execute(
            "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s)",
            (email, username, hashed_password)
        )

        # Mark OTP as used
        cursor.execute(
            "UPDATE otp_codes SET is_used=TRUE WHERE email=%s AND otp_code=%s",
            (email, otp_code)
        )

        mysql.connection.commit()
        cursor.close()

        # Clear session data after successful signup
        session.pop('email', None)
        session.pop('username', None)

        flash("Registration successful! Please log in.", "success")
        return redirect('/login')

    return render_template('signup.html', email=session.get('email', ''), username=session.get('username', ''))




@app.route('/about')
def about():
    # return render_template('about.html')
    return

@app.route('/services')
def services():
    # return render_template('services.html')
    return

@app.route('/resources')
def resources():
    # return render_template('resources.html')
    return

@app.route('/contact')
def contact():
    # return render_template('contact.html')
    return

import requests  

OPENROUTER_API_KEY = "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"

@app.route('/chatbot', methods=['POST','GET'])
def chatbot():
    if request.method == 'POST':
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://www.sitename.com",
            "X-Title": "SiteName",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "deepseek/deepseek-r1:free",
            "messages": [{"role": "user", "content": user_input}],
        }

        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            chatbot_reply = data.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
            return jsonify({"response": chatbot_reply})
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Request failed: {str(e)}"}), 500
    return render_template('chatbot.html')

@app.route('/skin_concerns')
def skin_concerns():
    return render_template('skin_concerns.html')


@app.route('/skin_analysis')
def skin_analysis():
    return render_template('skin_analysis.html')


app.config['UPLOAD_FOLDER'] = r'C:\Users\jaip7\Downloads\madhan\innergl\uploads'


@app.route('/skin_image', methods=['GET', 'POST'])
def skin_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        return jsonify({'message': 'Image uploaded successfully'})
    
    return render_template('skin_image.html')


# @app.route('/skin_results', methods=['POST','GET'])
# def skin_results():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file uploaded'})
        
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No file selected'})
        
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
#         file.save(filepath)
        
#         # Load image
#         img = image.load_img(filepath, target_size=(224, 224))
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array = img_array.astype(np.float32) / 255.0  # Normalize
        
#         # Predict skin condition
#         predictions = model.predict(img_array)
#         predicted_class = CLASS_NAMES[np.argmax(predictions)]
#         confidence = float(np.max(predictions))
        
#         # Fetch detailed treatment info
#         treatment_info = treatment_df[treatment_df['Condition'] == predicted_class]
        
#         print("Predicted Condition:", predicted_class)
#         print("Matched Data:", treatment_info)  # This will show if the match is failing

        
#         if treatment_info.empty:
#             treatment = "No treatment found"
#         else:
#             treatment = {
#                 'natural_treatment': treatment_info.iloc[0]['Natural Treatment'],
#                 'natural_dosage': treatment_info.iloc[0]['Dosage & Instructions (Natural)'],
#                 'clinical_treatment': treatment_info.iloc[0]['Clinical Treatment'],
#                 'medications': treatment_info.iloc[0]['Medications'],
#                 'diagnosis_procedures': treatment_info.iloc[0]['Diagnosis Procedures']
#             }
        
#         return jsonify({
#             'condition': predicted_class,
#             'confidence': confidence,
#             'treatment': treatment
#         })
#     return render_template('skin_results.html')

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded images from the uploads folder."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/get_latest_image', methods=['GET'])
def get_latest_image():
    """Fetch the most recent uploaded image."""
    image_files = sorted(
        os.listdir(app.config['UPLOAD_FOLDER']), 
        key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)), 
        reverse=True
    )
    
    if not image_files:
        return jsonify({'error': 'No images found'})

    latest_image = image_files[0]  # Most recent image
    image_url = url_for('uploaded_file', filename=latest_image)  # Use new route
    
    return jsonify({'image_url': image_url})


@app.route('/skin_results', methods=['GET', 'POST'])
def skin_results():
    if request.method == 'POST':
        # Get the latest uploaded image
        image_files = sorted(
            os.listdir(app.config['UPLOAD_FOLDER']), 
            key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)), 
            reverse=True
        )

        if not image_files:
            return jsonify({'error': 'No images found'})

        latest_image = image_files[0]  # Most recent image
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], latest_image)

        # Load image and preprocess
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array.astype(np.float32) / 255.0  # Normalize

        # Predict skin condition
        predictions = model.predict(img_array)
        predicted_class = CLASS_NAMES[np.argmax(predictions)]
        confidence = float(np.max(predictions))

        # Fetch treatment info
        treatment_info = treatment_df[treatment_df['Condition'] == predicted_class]

        treatment = "No treatment found" if treatment_info.empty else {
            'natural_treatment': treatment_info.iloc[0]['Natural Treatment'],
            'natural_dosage': treatment_info.iloc[0]['Dosage & Instructions (Natural)'],
            'clinical_treatment': treatment_info.iloc[0]['Clinical Treatment'],
            'medications': treatment_info.iloc[0]['Medications'],
            'diagnosis_procedures': treatment_info.iloc[0]['Diagnosis Procedures']
        }

        return jsonify({
            'condition': predicted_class,
            'confidence': confidence,
            'treatment': treatment
        })

    return render_template('skin_results.html')


if __name__ == '__main__':
    app.run(debug=True)
