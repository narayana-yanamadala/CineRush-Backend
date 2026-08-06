from django.urls import path
from . import views
from .views import home

urlpatterns = [
    path('', views.home),

    # Movies
    path('movies/', views.get_movies),
    path('movies/<int:pk>/', views.movie_detail),

    # OMDb
    path('omdb/search/<str:movie_name>/', views.search_omdb_movie),
    path('omdb/autofill/<str:movie_name>/', views.movie_auto_fill),

    # Booking
    path('book-ticket/', views.create_booking),
    path('my-bookings/', views.get_bookings),

    # Razorpay Payment
    path('razorpay/create-order/', views.create_razorpay_order),
    path('razorpay/verify-payment/', views.verify_razorpay_payment),
    path('create-razorpay-order/', views.create_razorpay_order),
    path('verify-razorpay-payment/', views.verify_razorpay_payment),

    # OTP
    path('send-otp/', views.send_otp),
    path('verify-otp/', views.verify_otp),
]