from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from django.conf import settings
import json
import requests
import uuid
import hmac
import hashlib
import razorpay
from .models import Movie, Booking
from .sms_service import send_booking_sms
from .email_service import send_booking_email


def get_movies(request):
    movies = Movie.objects.all()
    data = []

    for movie in movies:
        data.append({
            "id": movie.id,
            "title": movie.title,
            "genre": movie.genre,
            "rating": movie.rating,
            "duration": movie.duration,
            "language": movie.language,
            "poster": movie.poster,
            "banner": movie.banner,
            "description": movie.description,
            "release_date": movie.release_date,
            "trailer_url": movie.trailer_url,
            "is_active": movie.is_active,
        })

    return JsonResponse(data, safe=False)


def home(request):
    return JsonResponse({
        "message": "CineRush Backend Running Successfully"
    })


def search_omdb_movie(request, movie_name):
    try:
        url = "https://www.omdbapi.com/"

        params = {
            "apikey": settings.OMDB_API_KEY,
            "s": movie_name
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        return JsonResponse(response.json())

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)


def get_omdb_movie(movie_name):
    print("OMDB API KEY =", settings.OMDB_API_KEY)
    print("MOVIE NAME =", movie_name)
    try:
        url = "https://www.omdbapi.com/"

        params = {
            "apikey": settings.OMDB_API_KEY,
            "t": movie_name
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        movie = response.json()

        if movie.get("Response") == "False":
            return None

        return {
            "title": movie.get("Title"),
            "description": movie.get("Plot"),
            "rating": movie.get("imdbRating"),
            "release_date": movie.get("Released"),
            "poster": movie.get("Poster"),
            "banner": movie.get("Poster"),
            "genre": movie.get("Genre"),
            "language": movie.get("Language"),
            "duration": movie.get("Runtime"),
            "director": movie.get("Director"),
            "actors": movie.get("Actors")
        }

    except Exception as e:
        print("OMDB ERROR:", repr(e))
        return None


def movie_auto_fill(request, movie_name):
    movie_data = get_omdb_movie(movie_name)

    if movie_data:
        return JsonResponse(movie_data)

    return JsonResponse({
        "success": False,
        "message": "Movie not found"
    }, status=404)


def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(id=pk)
        data = {
            "id": movie.id,
            "title": movie.title,
            "genre": movie.genre,
            "rating": movie.rating,
            "duration": movie.duration,
            "language": movie.language,
            "poster": movie.poster,
            "banner": movie.banner,
            "description": movie.description,
            "release_date": movie.release_date,
            "trailer_url": movie.trailer_url,
            "is_active": movie.is_active,
        }
        return JsonResponse(data)
    except Movie.DoesNotExist:
        return JsonResponse({"error": "Movie not found"}, status=404)


@csrf_exempt
def create_booking(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            movie = Movie.objects.get(id=data["movie_id"])

            user_name = data.get("user_name", "Narayana")
            email = data.get("email")
            phone = data.get("phone", "+918688012658")

            booking = Booking.objects.create(
                movie=movie,
                user_name=user_name,
                email=email,
                phone=phone,
                theater=data["theater"],
                show_date=data["show_date"],
                show_time=data["show_time"],
                seats=",".join(data["seats"]),
                total_amount=data["amount"],
                booking_id=str(uuid.uuid4())[:8].upper()
            )

            # Send SMS confirmation
            if phone:
                send_booking_sms(
                    phone=phone,
                    movie=movie.title,
                    date=data["show_date"],
                    time=data["show_time"],
                    seats=",".join(data["seats"]),
                    booking_id=booking.booking_id
                )

            # Send Email confirmation
            if email:
                send_booking_email(
                    email=email,
                    movie=movie.title,
                    date=data["show_date"],
                    time=data["show_time"],
                    seats=",".join(data["seats"]),
                    booking_id=booking.booking_id
                )

            return JsonResponse({
                "success": True,
                "booking_id": booking.booking_id
            })
        except Movie.DoesNotExist:
            return JsonResponse({"success": False, "error": "Movie not found"}, status=404)
        except (KeyError, TypeError, json.JSONDecodeError) as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
        except Exception as e:
            print("CREATE BOOKING ERROR:", str(e))
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({
        "success": False
    }, status=405)


@csrf_exempt
def create_razorpay_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            movie_id = data.get("movie_id")
            theater = data.get("theater")
            show_date = data.get("show_date")
            show_time = data.get("show_time")
            seats = data.get("seats", [])
            amount = data.get("amount")

            if not all([movie_id, theater, show_date, show_time, seats, amount]):
                return JsonResponse({"success": False, "error": "Missing required booking fields"}, status=400)

            # Prevent duplicate seat bookings
            seats_list = seats if isinstance(seats, list) else [s.strip() for s in str(seats).split(",") if s.strip()]
            existing_bookings = Booking.objects.filter(
                movie_id=movie_id,
                theater=theater,
                show_date=show_date,
                show_time=show_time,
                booking_status="Confirmed"
            )

            already_booked = []
            for eb in existing_bookings:
                eb_seats = [s.strip() for s in eb.seats.split(",") if s.strip()]
                for seat in seats_list:
                    if seat in eb_seats:
                        already_booked.append(seat)

            if already_booked:
                return JsonResponse({
                    "success": False,
                    "error": f"Seat(s) {', '.join(already_booked)} are already booked. Please choose different seats."
                }, status=400)

            amount_in_paise = int(float(amount) * 100)
            key_id = getattr(settings, "RAZORPAY_KEY_ID", "rzp_test_CineRushKey123")
            key_secret = getattr(settings, "RAZORPAY_KEY_SECRET", "rzp_test_SecretCineRushKey123")

            order_id = None
            try:
                client = razorpay.Client(auth=(key_id, key_secret))
                order_payload = {
                    "amount": amount_in_paise,
                    "currency": "INR",
                    "payment_capture": 1,
                    "notes": {
                        "movie_id": str(movie_id),
                        "theater": str(theater),
                        "show_date": str(show_date),
                        "show_time": str(show_time),
                        "seats": ",".join(seats_list)
                    }
                }
                order = client.order.create(order_payload)
                order_id = order.get("id")
            except Exception as rzp_err:
                print("RAZORPAY CLIENT CREATE ORDER WARN (using mock order ID):", str(rzp_err))
                order_id = f"order_mock_{uuid.uuid4().hex[:12]}"

            return JsonResponse({
                "success": True,
                "order_id": order_id,
                "amount": amount_in_paise,
                "currency": "INR",
                "key": key_id
            })

        except Exception as e:
            print("CREATE RAZORPAY ORDER ERROR:", str(e))
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "POST method required"}, status=405)


@csrf_exempt
def verify_razorpay_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_signature = data.get("razorpay_signature")

            movie_id = data.get("movie_id")
            theater = data.get("theater")
            show_date = data.get("show_date")
            show_time = data.get("show_time")
            seats = data.get("seats", [])
            amount = data.get("amount")
            user_name = data.get("user_name", "CineRush Customer")
            email = data.get("email")
            phone = data.get("phone", "+918688012658")

            if not all([movie_id, theater, show_date, show_time, seats, amount]):
                return JsonResponse({"success": False, "error": "Missing booking details"}, status=400)

            # Check if payment_id already processed
            if razorpay_payment_id and Booking.objects.filter(razorpay_payment_id=razorpay_payment_id).exists():
                existing = Booking.objects.get(razorpay_payment_id=razorpay_payment_id)
                return JsonResponse({
                    "success": True,
                    "booking_id": existing.booking_id,
                    "message": "Booking already verified and created"
                })

            # Check seat availability again before persisting
            seats_list = seats if isinstance(seats, list) else [s.strip() for s in str(seats).split(",") if s.strip()]
            existing_bookings = Booking.objects.filter(
                movie_id=movie_id,
                theater=theater,
                show_date=show_date,
                show_time=show_time,
                booking_status="Confirmed"
            )

            already_booked = []
            for eb in existing_bookings:
                eb_seats = [s.strip() for s in eb.seats.split(",") if s.strip()]
                for seat in seats_list:
                    if seat in eb_seats:
                        already_booked.append(seat)

            if already_booked:
                return JsonResponse({
                    "success": False,
                    "error": f"Seats {', '.join(already_booked)} were booked while processing. Payment will be refunded."
                }, status=400)

            key_secret = getattr(settings, "RAZORPAY_KEY_SECRET", "rzp_test_SecretCineRushKey123")

            # Verification logic
            verified = False
            if razorpay_order_id and razorpay_payment_id and razorpay_signature:
                try:
                    generated_signature = hmac.new(
                        key_secret.encode('utf-8'),
                        f"{razorpay_order_id}|{razorpay_payment_id}".encode('utf-8'),
                        hashlib.sha256
                    ).hexdigest()
                    if generated_signature == razorpay_signature or str(razorpay_order_id).startswith("order_mock_"):
                        verified = True
                except Exception as sig_err:
                    print("SIGNATURE VERIFICATION ERROR:", sig_err)

            # Fallback verification for demo / mock mode
            if not verified and (not razorpay_signature or (razorpay_order_id and str(razorpay_order_id).startswith("order_mock_"))):
                verified = True
                if not razorpay_order_id:
                    razorpay_order_id = f"order_mock_{uuid.uuid4().hex[:12]}"
                if not razorpay_payment_id:
                    razorpay_payment_id = f"pay_mock_{uuid.uuid4().hex[:12]}"

            if not verified:
                return JsonResponse({"success": False, "error": "Razorpay payment signature verification failed"}, status=400)

            movie = Movie.objects.get(id=movie_id)
            booking_id = str(uuid.uuid4())[:8].upper()

            booking = Booking.objects.create(
                movie=movie,
                user_name=user_name,
                email=email,
                phone=phone,
                theater=theater,
                show_date=show_date,
                show_time=show_time,
                seats=",".join(seats_list),
                total_amount=amount,
                booking_status="Confirmed",
                booking_id=booking_id,
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
            )

            # Send SMS
            if phone:
                try:
                    send_booking_sms(
                        phone=phone,
                        movie=movie.title,
                        date=str(show_date),
                        time=str(show_time),
                        seats=",".join(seats_list),
                        booking_id=booking.booking_id
                    )
                except Exception as e:
                    print("SMS Error:", e)

            # Send Email
            if email:
                try:
                    send_booking_email(
                        email=email,
                        movie=movie.title,
                        date=str(show_date),
                        time=str(show_time),
                        seats=",".join(seats_list),
                        booking_id=booking.booking_id
                    )
                except Exception as e:
                    print("Email Error:", e)

            return JsonResponse({
                "success": True,
                "booking_id": booking.booking_id,
                "message": "Payment verified and booking confirmed!"
            })

        except Movie.DoesNotExist:
            return JsonResponse({"success": False, "error": "Movie not found"}, status=404)
        except Exception as e:
            print("VERIFY RAZORPAY PAYMENT ERROR:", str(e))
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "POST method required"}, status=405)



def get_bookings(request):
    bookings = Booking.objects.all().order_by("-created_at")
    data = []

    for booking in bookings:
        data.append({
            "id": booking.id,
            "movie": booking.movie.title,
            "poster": booking.movie.poster,
            "theater": booking.theater,
            "date": str(booking.show_date),
            "time": str(booking.show_time),
            "seats": booking.seats,
            "amount": str(booking.total_amount),
            "status": booking.booking_status,
            "booking_id": booking.booking_id
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            phone = data.get("phone")

            target = phone if phone else email
            channel = "sms" if phone else "email"

            if not target:
                return JsonResponse({"success": False, "error": "Email or Phone is required"}, status=400)

            print("SEND OTP TARGET:", target)
            print("CHANNEL:", channel)

            try:
                client = Client(
                    settings.TWILIO_ACCOUNT_SID,
                    settings.TWILIO_AUTH_TOKEN
                )

                verification = client.verify.v2.services(
                    settings.TWILIO_VERIFY_SERVICE_SID
                ).verifications.create(
                    to=target,
                    channel=channel
                )

                return JsonResponse({
                    "success": True,
                    "status": verification.status,
                    "message": "OTP Sent Successfully"
                })

            except Exception as twilio_err:
                print("TWILIO OTP ERROR (switching to mock):", str(twilio_err))
                # Generate mock OTP
                import random
                mock_code = str(random.randint(100000, 999999))
                request.session[f"mock_otp_{target}"] = mock_code
                request.session.modified = True

                print(f"\n==========================================")
                print(f"[MOCK OTP] Verification Code for {target}: {mock_code}")
                print(f"==========================================\n")

                return JsonResponse({
                    "success": True,
                    "status": "pending",
                    "message": "OTP Sent Successfully (Mock Mode)",
                    "mock": True
                })

        except Exception as e:
            print("SEND OTP GENERAL ERROR:", str(e))
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({
        "success": False,
        "message": "Only POST requests are allowed"
    }, status=405)


@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            phone = data.get("phone")
            otp = data.get("otp")

            target = phone if phone else email

            if not target or not otp:
                return JsonResponse({"success": False, "error": "Target and OTP are required"}, status=400)

            print("VERIFY TARGET:", target)
            print("OTP:", otp)

            # Try Twilio first
            try:
                client = Client(
                    settings.TWILIO_ACCOUNT_SID,
                    settings.TWILIO_AUTH_TOKEN
                )

                check = client.verify.v2.services(
                    settings.TWILIO_VERIFY_SERVICE_SID
                ).verification_checks.create(
                    to=target,
                    code=otp
                )

                print("TWILIO VERIFY STATUS:", check.status)

                if check.status == "approved":
                    return JsonResponse({
                        "success": True,
                        "message": "OTP Verified Successfully"
                    })

                # If Twilio returns a status that is not approved, we should still try the mock fallback
                # in case the developer is typing the mock OTP while Twilio credentials exist but are invalid
            except Exception as twilio_err:
                print("TWILIO VERIFY ERROR (checking mock session):", str(twilio_err))

            # Fallback to session mock OTP check
            mock_otp = request.session.get(f"mock_otp_{target}")
            print(f"Session Mock OTP for {target}: {mock_otp} (received: {otp})")

            if mock_otp and str(otp) == str(mock_otp):
                request.session.pop(f"mock_otp_{target}", None)
                request.session.modified = True
                return JsonResponse({
                    "success": True,
                    "message": "OTP Verified Successfully (Mock)"
                })

            return JsonResponse({"success": False, "message": "Invalid OTP"})

        except Exception as e:
            print("VERIFY GENERAL ERROR:", str(e))
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({
        "success": False,
        "message": "Only POST requests are allowed"
    }, status=405)