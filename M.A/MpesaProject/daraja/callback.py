import json
from django.http import JsonResponse

def handle_callback(request):
    """
    Parse mpesa callback JSON. This is a simplified example.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'status': 'bad request'}, status=400)

    # Here you would:
    # - verify the transaction
    # - find the related Booking (by account_reference or CheckoutRequestID)
    # - update booking.status = 'active' and save
    return JsonResponse({'status': 'ok'})
