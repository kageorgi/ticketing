from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('book/<int:show_id>/', views.book_ticket, name='book_ticket'),
    path('pay/<int:booking_id>/', views.pay, name='pay'),
    path('payment_result/<int:booking_id>/', views.payment_result, name='payment_result'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('reports/', views.reports, name='reports'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),  # endpoint for real callback
]
