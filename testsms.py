
#        print(f"Error: {e}")
import requests
import random
from requests.auth import HTTPBasicAuth

def send_post_request(url, username, password, body):
    """
    Sends a POST request with basic authentication.

    :param url: The URL to send the POST request to.
    :param username: The username for basic authentication.
    :param password: The password for basic authentication.
    :param body: The body of the POST request.
    :return: The response from the server.
    """
    auth = HTTPBasicAuth(username, password)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, auth=auth, json=body, headers=headers)
    print("done1")
    print(response)
    
    return response



def send_sms(api_url, username, password, phone_number, message):
    """
    Sends an SMS message using a POST request with basic authentication.

    :param api_url: The URL of the SMS gateway API.
    :param username: The username for basic authentication.
    :param password: The password for basic authentication.
    :param phone_number: The recipient's phone number.
    :param message: The message to send.
    :return: The response from the SMS gateway API.
    """

    # Split the long message into chunks of 150 characters
    chunks = [message[i:i+150] for i in range(0, len(message), 150)]
    
    # Send up to two chunks
    responses = []
    for i, chunk in enumerate(chunks[:5]):
        response = send_sms(api_url, username, password, phone_number, chunk)
        responses.append(response)
    

        body = {
            "from": "RMNDR",
            "to": phone_number,
            "text": message[:150]
    ,
            "reference": random.randint(0, 899889898)
        
        }
        response = send_post_request(api_url, username, password, body)

    return response


# Example usage
api_url = "http://sms.reubenwedson.site/api/sms/v1/text/single"
username = "SAMPLE"
password = "SAMPLE"

message = """
Based on the provided data, here's an analysis of the conditions:

Soil Moisture: The value is 45 which indicates that the soil is moderately moist. This is generally a good level for maize as the ideal soil moisture content is between 40% and 60%.

"""



