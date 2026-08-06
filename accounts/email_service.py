from django.core.mail import send_mail
from django.conf import settings

def send_booking_email(email, movie, date, time, seats, booking_id):
    if not email:
        return False

    subject = f"🎬 CineRush Booking Confirmed - CR-{booking_id}"
    
    body = f"""Hello,

Your booking at CineRush has been successfully confirmed!

Here are your ticket details:
------------------------------------------
Booking ID: CR-{booking_id}
Movie: {movie}
Date: {date}
Time: {time}
Seats: {seats}
------------------------------------------

Thank you for choosing CineRush! Enjoy your show!

Best regards,
The CineRush Team
"""

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"EMAIL SEND ERROR: {str(e)}")
        # Print fallback to console in case EMAIL_BACKEND is not default or prints error
        print("\n=== [MOCK EMAIL CONFIRMATION] ===")
        print(f"To: {email}")
        print(f"Subject: {subject}")
        print(body)
        print("==================================\n")
        return False
