from flask import Flask, request, jsonify
from twilio.rest import Client
import os
import requests
from os import access
import jwt.utils
import time
import math
import random
from flask_cors import CORS
from twilio.rest import Client

app = Flask(__name__)
CORS(app)


developer_id = '8e1c7316-e66d-49f9-b915-472e17579dfa'
key_id = '9654ae50-782f-4576-83da-c019ed861b67'
signing_secret = 'kSsOCEgGBbJ4vdxsUbDgZFO-3Cr_9sTuLIuJ8fDN6uI'

account_sid = 'ACf16c24ad548522c4d85edf1268edf824'
auth_token = 'b37c169908eb592a8f93ff117fc74b38'
twilio_phone_number = '+18447953246'

# Function to send assignment message to driver via Twilio
def send_updates(event_name):

    recipient_phone_number = '+14693604599'

    if event_name == 'DASHER_CONFIRMED':
        message_body = 'Your order has been confirmed by the driver'
    elif event_name == 'DASHER_CONFIRMED_PICKUP_ARRIVAL':
        message_body = 'Your driver has arrived at the store'
    elif event_name == 'DASHER_PICKED_UP':
        message_body = 'Your driver has picked up your order'
    elif event_name == 'DASHER_CONFIRMED_DROPOFF_ARRIVAL':
        message_body = 'Your driver has arrived at the delivery location'
    elif event_name == 'DASHER_DROPPED_OFF':
        message_body = 'Your order has been delivered'

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Send SMS
    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=recipient_phone_number
    )

    print("Message sent with SID:", message.sid)



@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    data = request.get_json()
    store_location = data.get('store_location')
    delivery_location = data.get('delivery_location')
    store_name = data.get('store_name')
    pickup_phone = data.get('pickup_phone')
    dropoff_name = data.get('dropoff_name')
    dropoff_number = data.get('dropoff_number')

    if not authenticate_webhook(request):
        return jsonify({'success': False, 'message': 'Authentication failed'}), 401

    print("Received webhook payload:", payload)

    event_name = payload.get('event_name')
    print(event_name)

    if event_name == 'DASHER_CONFIRMED':
        send_updates(event_name)
    elif event_name == 'DASHER_CONFIRMED_PICKUP_ARRIVAL':
        send_updates(event_name)
    elif event_name == 'DASHER_PICKED_UP':
        send_updates(event_name)
    elif event_name == 'DASHER_CONFIRMED_DROPOFF_ARRIVAL':
        send_updates(event_name)
    elif event_name == 'DASHER_DROPPED_OFF':
        send_updates(event_name)
    else:
        query_driver(store_location, delivery_location, store_name, pickup_phone, dropoff_name, dropoff_number)


    return jsonify({'success': True}), 200

def authenticate_webhook(request):
    expected_token = 'authorizationforrift'
    token = request.headers.get('Authorization')
    if not token:
        return False
    
    if token == expected_token:
        return True
    else:
        return False



# Function to send assignment message to driver via Twilio
def query_driver(store_location, delivery_location, store_name, pickup_phone, dropoff_name, dropoff_phone):
    
    external_delivery_id = random.randint(1000, 9999)

    accessKey = {
        "developer_id": developer_id, 
        "key_id": key_id,
        "signing_secret": signing_secret
    }

    token = jwt.encode(
        {
            "aud": "doordash",
            "iss": accessKey["developer_id"],
            "kid": accessKey["key_id"],
            "exp": str(math.floor(time.time() + 300)),
            "iat": str(math.floor(time.time())),
        },
        jwt.utils.base64url_decode(accessKey["signing_secret"]),
        algorithm="HS256",
        headers={"dd-ver": "DD-JWT-V1"})

    print(token)

    endpoint = "https://openapi.doordash.com/drive/v2/deliveries/"

    headers = {"Accept-Encoding": "application/json",
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"}

    request_body = { # Modify pickup and drop off addresses below
        "external_delivery_id": external_delivery_id,
        "pickup_address": store_location,
        "pickup_business_name": store_name,
        "pickup_phone_number": pickup_phone,
        "dropoff_address": delivery_location,
        "dropoff_business_name": dropoff_name,
        "dropoff_phone_number": dropoff_phone,
    }

    create_delivery = requests.post(endpoint, headers=headers, json=request_body) # Create POST request


    print(create_delivery.status_code)
    print(create_delivery.text)
    print(create_delivery.reason)

    return 'Message sent successfully'

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.get_json()
    store_location = data.get('store_location')
    delivery_location = data.get('delivery_location')
    store_name = data.get('store_name')
    pickup_phone = data.get('pickup_phone')
    dropoff_name = data.get('dropoff_name')
    dropoff_number = data.get('dropoff_number')

    if not all([store_location, delivery_location, store_name, pickup_phone, dropoff_name, dropoff_number]):
        return jsonify({'success': False, 'message': 'Invalid request'}), 400
    else:
        # Call your function to send message to driver
        print(query_driver(store_location, delivery_location, store_name, pickup_phone, dropoff_name, dropoff_number))
        
    return jsonify({'success': True, 'message': 'Order placed successfully'}), 200

if __name__ == '__main__':
    port = 5000  # You can change this port to any other available port
    print(f"Server is running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)