import requests
import random
from requests.auth import HTTPBasicAuth

# Define constants for API URL, username, and password
API_URL = "http://sms.reubenwedson.site/api/sms/v1/text/single"
USERNAME = "SAMPLE"
PASSWORD = "SAMPLE"
SENDER_ID = "RMNDR"
MAX_SMS_LENGTH = 150
MAX_SMS_CHUNKS = 3

def send_sms(phone_number, message):
    # Split the long message into chunks of MAX_SMS_LENGTH characters
    chunks = [message[i:i+MAX_SMS_LENGTH] for i in range(0, len(message), 150)]
    
    # Send up to two chunks
    responses = []
    for chunk in chunks[:MAX_SMS_CHUNKS]:
        body = {
            "from": SENDER_ID,
            "to": phone_number,
            "text": chunk,
            "reference": random.randint(0, 899889898)
        }
        response = send_post_request(API_URL, USERNAME, PASSWORD, body)
        # responses = send_sms_modem(phone_number, message) # Uncomment this line to use the modem, comment the above line
        responses.append(response)
    
    return responses


def send_post_request(url, username, password, body):
    auth = HTTPBasicAuth(username, password)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, auth=auth, json=body, headers=headers)
    return response

# Function to send SMS using HSUPA modem
#def send_sms_modem(phone_number, message):
#    try:
#        # Replace 'COM3' with your modem's serial port
#        ser = serial.Serial('COM3', baudrate=9600, timeout=5)
#        
#        # Give the modem some time to initialize
#        time.sleep(1)
#
#        # Initialize the modem
#        ser.write(b'AT\r')
#        time.sleep(0.5)
#        print(ser.read(ser.inWaiting()).decode())
#
#        # Set text mode
#        ser.write(b'AT+CMGF=1\r')
#        time.sleep(0.5)
#        print(ser.read(ser.inWaiting()).decode())
#
#        # Set the phone number for SMS
#        ser.write(f'AT+CMGS="{phone_number}"\r'.encode())
#        time.sleep(0.5)
#        print(ser.read(ser.inWaiting()).decode())
#
#        # Send the message text
#        ser.write(f'{message}\x1A'.encode())
#        time.sleep(0.5)
#        print(ser.read(ser.inWaiting()).decode())
#
#        # Close the serial connection
#        ser.close()
#        
#        print("SMS sent successfully!")
#
#    except Exception as e:
#        print(f"Error: {e}")

# # Example usage
# if __name__ == "__main__":
#     phone_number = "1234567890"
#     message = """
#     Based on the provided data, here's an analysis of the conditions:

#     Soil Moisture: The value is 45 which indicates that the soil is moderately moist. This is generally a good level for maize as the ideal soil moisture content is between 40% and 60%.
#     """

#     responses = send_sms(phone_number, message)
#     for response in responses:
#         print(response)
