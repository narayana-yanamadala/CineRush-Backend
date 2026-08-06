from django.db import models

from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    rating = models.FloatField()
    duration = models.CharField(max_length=50)
    language = models.CharField(max_length=50)

    poster = models.URLField()

    banner = models.URLField(blank=True)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    trailer_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    



class Booking(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)

    theater = models.CharField(max_length=200)
    show_date = models.DateField()
    show_time = models.CharField(max_length=20)

    seats = models.CharField(max_length=100)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    booking_status = models.CharField(
        max_length=20,
        default="Confirmed"
    )

    booking_id = models.CharField(
        max_length=20,
        unique=True
    )

    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.booking_id