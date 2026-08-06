from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

def send_booking_sms(phone, movie, date, time, seats, booking_id):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    phone_number = os.getenv("TWILIO_PHONE_NUMBER")

    body = f"""
🎬 CineRush Booking Confirmed

Movie: {movie}
Date: {date}
Time: {time}
Seats: {seats}

Booking ID: CR-{booking_id}

Enjoy your show!
"""

    if not account_sid or not auth_token or not phone_number or "YOUR_" in account_sid:
        print("\n=== [MOCK SMS CONFIRMATION] ===")
        print(f"To: {phone}")
        print(body)
        print("===============================\n")
        return "SMmock1234567890abcdef"

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=body,
            from_=phone_number,
            to=phone
        )
        return message.sid
    except Exception as e:
        print(f"SMS SEND ERROR: {str(e)}")
        print("\n=== [MOCK SMS CONFIRMATION] ===")
        print(f"To: {phone}")
        print(body)
        print("===============================\n")
        return "SMmock1234567890abcdef"
