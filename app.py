from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import requests
import random
import string
import sqlite3

app = Flask(__name__)
CORS(app)

feedback_file = 'feedback.json'
database_file = 'bookings.db'  # Filnamn för SQL-databasen

def get_country_from_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            return data.get('country', 'Unknown')
        return 'Unknown'
    except requests.RequestException:
        return 'Unknown'

def generate_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def save_booking_to_json(booking_data):
    booking_list = []
    if os.path.exists(feedback_file) and os.path.getsize(feedback_file) > 0:
        with open(feedback_file, 'r') as file:
            try:
                booking_list = json.load(file)
            except json.JSONDecodeError:
                pass

    booking_list.append(booking_data)

    with open(feedback_file, 'w') as file:
        json.dump(booking_list, file, indent=2)

def save_booking_to_database(booking_data):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Skapa tabellen om den inte redan finns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id TEXT PRIMARY KEY,
            name TEXT,
            travel_from TEXT,
            travel_to TEXT,
            date TEXT,
            time TEXT,
            email TEXT,
            phone TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            country TEXT,
            ip_address TEXT
        )
    ''')

    # Generera ID för bokningen
    booking_id = generate_id()
    booking_data['id'] = booking_id

    # Lägg till bokningsdata i SQL-databasen
    cursor.execute('''
        INSERT INTO bookings (
            id, name, travel_from, travel_to, date, time, email, phone, message, country, ip_address
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        booking_id,
        booking_data['name'],
        booking_data['travel from'],
        booking_data['travel to'],
        booking_data['date'],
        booking_data['time'],
        booking_data['email'],
        booking_data['phone'],
        booking_data['message'],
        booking_data['country'],
        booking_data['ipAddress']
    ))

    conn.commit()
    conn.close()

@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    booking_data = request.json
    booking_data['ipAddress'] = request.remote_addr
    
    country = get_country_from_ip(request.remote_addr)
    booking_data['country'] = country

    # Spara bokningsdata i JSON-filen
    save_booking_to_json(booking_data)

    # Spara bokningsdata i SQL-databasen
    save_booking_to_database(booking_data)

    return 'Booking received and saved successfully.', 200

if __name__ == '__main__':
    app.run(debug=True)