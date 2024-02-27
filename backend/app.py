from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')


# Function to send assignment message to driver via Twilio
def send_assignment_message(assignment_details):

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body={assignment_details},
                        from_='+18447953246',
                        to='+14693604599'
                    )

    print(message.sid)

    return 'Message sent successfully'

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.get_json()
    order_items = data.get('items')
    store_location = data.get('store_location')
    delivery_location = data.get('delivery_location')

    if not order_items or not store_location or not delivery_location:
        return jsonify({'success': False, 'message': 'Invalid request'}), 400
    else:
        # send_assignment_message(f"Pick up {order_items} from {store_location} and deliver to {delivery_location}")
        print(f"Pick up {order_items} from {store_location} and deliver to {delivery_location}")
        
    return jsonify({'success': True, 'message': 'Order placed successfully'}), 200

if __name__ == '__main__':
    port = 5000  # You can change this port to any other available port
    print(f"Server is running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)