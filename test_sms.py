from sms_service import send_booking_sms

if __name__ == '__main__':
    sid = send_booking_sms(
        phone="+918688012658",
        movie="Pushpa 2",
        date="2025-06-25",
        time="7:30 PM",
        seats="A1,A2",
        booking_id=101
    )

    print("SMS Sent!")
    print("SID:", sid)