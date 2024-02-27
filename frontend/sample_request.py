import requests
import json

def simulate_request():
    url = 'http://0.0.0.0:5000/place_order'  # Replace with your Flask app's URL
    data = {
        "store_location": '3111 Palm Way, Austin, TX 78758',
        "store_name": 'Nordstrom Domain Northside',
        "pickup_phone": '+15126054900',
        "delivery_location": '2206 Nueces St, Austin, TX 78705',
        "dropoff_name": 'The University of Texas at Austin',
        "dropoff_number": '+15124713434',
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Request successful!")
        print(response.json())
    else:
        print("Request failed!")
        print(response.text)

if __name__ == "__main__":
    simulate_request()