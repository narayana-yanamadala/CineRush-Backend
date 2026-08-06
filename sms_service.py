from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

def send_booking_sms(phone, movie, date, time, seats, booking_id):
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

    body = f"""
🎬 CineRush Booking Confirmed

Movie: {movie}
Date: {date}
Time: {time}
Seats: {seats}

Booking ID: CR-{booking_id}

Enjoy your show!
"""

    try:
        message = client.messages.create(
            body=body,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
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