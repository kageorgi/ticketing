from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class Movie(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=90)
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('250.00'))

    def __str__(self):
        return self.name

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['show_time']

    def __str__(self):
        return f"{self.movie.name} @ {self.show_time}"

    def booked_seats(self):
        from django.db.models import Sum
        res = self.booking_set.filter(status=Booking.STATUS_ACTIVE).aggregate(s=Sum('seats'))['s'] or 0
        return res

    def available_seats(self):
        return max(self.total_seats - self.booked_seats(), 0)


class Booking(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACTIVE = 'active'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending Payment'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    show = models.ForeignKey(Show, on_delete=models.PROTECT)
    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    ticket_code = models.CharField(max_length=36, default=uuid.uuid4, unique=True)

    def __str__(self):
        return f"Booking {self.id} ({self.customer_name})"
