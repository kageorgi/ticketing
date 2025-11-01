from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from decimal import Decimal
from .models import Movie, Show, Booking
from .forms import BookingForm
from .stkPush import stk_push
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return render(request, 'daraja/home.html', {'today': timezone.localdate()})

def movie_list(request):
    movies = Movie.objects.prefetch_related('show_set').all()
    return render(request, 'daraja/movie_list.html', {'movies': movies})

def book_ticket(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    available = show.available_seats()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            seats_wanted = form.cleaned_data['seats']
            with transaction.atomic():
                show_locked = Show.objects.select_for_update().get(pk=show.pk)
                if seats_wanted > show_locked.available_seats():
                    messages.error(request, f"Only {show_locked.available_seats()} seats available.")
                    return redirect('book_ticket', show_id=show.pk)

                amount = Decimal(seats_wanted) * show.movie.price_per_seat
                booking = form.save(commit=False)
                booking.show = show_locked
                booking.amount = amount
                booking.status = Booking.STATUS_PENDING
                booking.save()

                # initiate STK Push (simulated). Provide phone in international format e.g. 2547XXXXXXXX
                resp = stk_push(booking.phone, float(amount), account_reference=str(booking.id),
                                transaction_desc=f"Booking {booking.id} for {show.movie.name}")
                # resp is simulated: store checkout id? for real flow you must persist CheckoutRequestID
                messages.info(request, "Payment request sent (simulated). Proceed to payment page.")
                return redirect('pay', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'daraja/book_ticket.html', {
        'show': show,
        'available': available,
        'form': form,
    })

def pay(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.status != Booking.STATUS_PENDING:
        messages.info(request, "Booking already processed.")
        return redirect('booking_detail', booking_id=booking.id)

    if request.method == 'POST':
        # This simulates a successful payment (for testing). In production,
        # you'd wait for mpesa callback and update booking there.
        booking.status = Booking.STATUS_ACTIVE
        booking.save()
        messages.success(request, f"Payment received. Ticket code: {booking.ticket_code}")
        return redirect('payment_result', booking_id=booking.id)

    return render(request, 'daraja/payment.html', {'booking': booking})


def payment_result(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'daraja/payment_result.html', {'booking': booking})

def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'daraja/booking_detail.html', {'booking': booking})

def booking_list(request):
    bookings = Booking.objects.select_related('show', 'show__movie').order_by('-created_at')
    return render(request, 'daraja/booking_list.html', {'bookings': bookings})

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        if booking.status != Booking.STATUS_CANCELLED:
            booking.status = Booking.STATUS_CANCELLED
            booking.save()
            messages.success(request, f"Booking {booking.id} cancelled.")
        return redirect('booking_detail', booking_id=booking.id)
    return render(request, 'daraja/cancel_booking.html', {'booking': booking})

def reports(request):
    total_revenue = Booking.objects.filter(status=Booking.STATUS_ACTIVE).aggregate(s=Sum('amount'))['s'] or Decimal('0.00')
    active_count = Booking.objects.filter(status=Booking.STATUS_ACTIVE).count()
    canceled_count = Booking.objects.filter(status=Booking.STATUS_CANCELLED).count()

    shows_list = []
    for show in Show.objects.select_related('movie').all():
        booked = show.booked_seats()
        total = show.total_seats
        pct = (booked / total * 100) if total else 0
        shows_list.append({
            'show': show,
            'booked_seats': booked,
            'total_seats': total,
            'percent_full': round(pct, 1)
        })
    context = {
        'total_revenue': total_revenue,
        'active_count': active_count,
        'canceled_count': canceled_count,
        'shows': shows_list,
    }
    return render(request, 'daraja/reports.html', context)

@csrf_exempt
def mpesa_callback(request):
    """
    Endpoint to receive real Safaricom callback.
    You must secure this endpoint and verify payload in production.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'only POST'}, status=405)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'status': 'bad request'}, status=400)

    # Example: find booking by account reference (you must adapt to actual callback shape)
    # For demo we won't update anything automatically.
    # Real implementation:
    # checkout_id = payload['Body']['stkCallback']['CheckoutRequestID']
    # result_code = payload['Body']['stkCallback']['ResultCode']
    # if result_code == 0: find booking and set active
    return JsonResponse({'status': 'received'})
