import requests

# Base URL for Shiprocket API
BASE_URL = "https://apiv2.shiprocket.in/v1/external"

# Step 1: Authenticate and get the token
def authenticate(email, password):
    auth_url = f"{BASE_URL}/auth/login"
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(auth_url, json=payload)
    if response.status_code == 200:
        token = response.json().get('token')
        return token
    else:
        print("Failed to authenticate:", response.text)
        return None

# Step 2: Create an order
def create_order(token, order_data):
    order_url = f"{BASE_URL}/orders/create/adhoc"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(order_url, json=order_data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to create order:", response.text)
        return None

# Step 3: Generate a label for the order
def generate_label(token, shipment_id):
    label_url = f"{BASE_URL}/courier/generate/label"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "shipment_id": shipment_id
    }
    response = requests.post(label_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to generate label:", response.text)
        return None

# Step 4: Track the shipment
def track_shipment(token, awb_code):
    track_url = f"{BASE_URL}/courier/track/awb/{awb_code}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(track_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to track shipment:", response.text)
        return None

# Example usage
if __name__ == "__main__":
    # Replace with your API user credentials
    email = "atulg0736@gmail.com"
    password = "@Password1"

    # Authenticate
    token = authenticate(email, password)
    if token:
        print("Authentication successful. Token:", token)

        # Example order data
        order_data = {
            "order_id": "ORDER12345",
            "order_date": "2023-09-15 12:00:00",
            "pickup_location": "Primary",
            "channel_id": "",
            "comment": "",
            "billing_customer_name": "John Doe",
            "billing_last_name": "Doe",
            "billing_address": "123 Main St",
            "billing_address_2": "",
            "billing_city": "New York",
            "billing_pincode": "10001",
            "billing_state": "New York",
            "billing_country": "United States",
            "billing_email": "john.doe@example.com",
            "billing_phone": "1234567890",
            "shipping_is_billing": True,
            "shipping_customer_name": "",
            "shipping_last_name": "",
            "shipping_address": "",
            "shipping_address_2": "",
            "shipping_city": "",
            "shipping_pincode": "",
            "shipping_country": "",
            "shipping_state": "",
            "shipping_email": "",
            "shipping_phone": "",
            "order_items": [
                {
                    "name": "Sample Product",
                    "sku": "SP123",
                    "units": 1,
                    "selling_price": "10.00",
                    "discount": "",
                    "tax": "",
                    "hsn": ""
                }
            ],
            "payment_method": "Prepaid",
            "shipping_charges": "0.00",
            "giftwrap_charges": "0.00",
            "transaction_charges": "0.00",
            "total_discount": "0.00",
            "sub_total": "10.00",
            "length": "10",
            "breadth": "15",
            "height": "20",
            "weight": "1.5"
        }

        # Create an order
        order_response = create_order(token, order_data)
        if order_response:
            print("Order created successfully:", order_response)
            shipment_id = order_response.get('shipment_id')

            # Generate a label
            label_response = generate_label(token, shipment_id)
            if label_response:
                print("Label generated successfully:", label_response)

            # Track the shipment (replace with actual AWB code)
            awb_code = "123456789012"
            track_response = track_shipment(token, awb_code)
            if track_response:
                print("Shipment tracking details:", track_response)