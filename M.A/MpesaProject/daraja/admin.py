from django.contrib import admin
from .models import Movie, Show, Booking

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name','price_per_seat')

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie','show_time','total_seats')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','customer_name','show','seats','amount','status','ticket_code')
    list_filter = ('status','show__movie')
