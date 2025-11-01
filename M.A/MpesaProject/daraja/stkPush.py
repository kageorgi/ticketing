import base64
from datetime import datetime
import requests

# CONFIGURATION (replace with real credentials)
MPESA_CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
MPESA_CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
SHORTCODE = '174379'  # example
PASSKEY = 'YOUR_PASSKEY'
CALLBACK_URL = 'https://your-server.com/mpesa/callback/'

def generate_password(shortcode: str, passkey: str, timestamp: str) -> str:
    data_to_encode = shortcode + passkey + timestamp
    encoded = base64.b64encode(data_to_encode.encode('utf-8')).decode('utf-8')
    return encoded

def get_access_token():
    """
    Implement token retrieval. Here we return a dummy token for local testing.
    """
    # Real implementation:
    # r = requests.get('https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
    #                  auth=(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET))
    # token = r.json()['access_token']
    return 'SIMULATED_TOKEN'

def stk_push(phone: str, amount: float, account_reference: str, transaction_desc: str):
    """
    Simulate STK push. In production, call Safaricom's endpoint and handle responses.
    """
    # For real STK push you'd:
    # - get token
    # - build payload with password generated from passkey+shortcode+timestamp
    # - POST to /mpesa/stkpush/v1/processrequest
    # - return the JSON Safaricom returns
    return {
        "MerchantRequestID": "SIM1234",
        "CheckoutRequestID": "CHECKOUT_SIM_1234",
        "ResponseCode": "0",
        "ResponseDescription": "Success. Request accepted for processing",
    }
