import requests
import json
import serial
import time

# Define your OpenAI API key
openai_api_key = 'sk-proj-6ScOHbPPm8ZXZXknyqb3T3BlbkFJfhsHDurVorriE4giZj5q'

# Function to send sensor data to OpenAI API and get a response
def get_openai_response(sensor_data, crop_type):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}',
    }
    
    prompt = f"The following data has been collected from sensors for {crop_type}: {sensor_data}. Based on this data, please explain its implications for the farmer and provide specific recommendations on what actions to take if necessary."

    data = {
        'model': 'gpt-4',
        'messages': [{'role': 'system', 'content': 'You are an intelligent assistant for farmers.'},
                     {'role': 'user', 'content': prompt}]
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"OpenAI API request failed with status code {response.status_code}: {response.text}")

# Function to send SMS using HSUPA modem
def send_sms(phone_number, message):
    try:
        # Replace 'COM3' with your modem's serial port
        ser = serial.Serial('COM3', baudrate=9600, timeout=5)
        
        # Give the modem some time to initialize
        time.sleep(1)

        # Initialize the modem
        ser.write(b'AT\r')
        time.sleep(0.5)
        print(ser.read(ser.inWaiting()).decode())

        # Set text mode
        ser.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        print(ser.read(ser.inWaiting()).decode())

        # Set the phone number for SMS
        ser.write(f'AT+CMGS="{phone_number}"\r'.encode())
        time.sleep(0.5)
        print(ser.read(ser.inWaiting()).decode())

        # Send the message text
        ser.write(f'{message}\x1A'.encode())
        time.sleep(0.5)
        print(ser.read(ser.inWaiting()).decode())

        # Close the serial connection
        ser.close()
        
        print("SMS sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

# Example sensor data and crop type
sensor_data = {
    'soil_moisture': 45,  # percentage
    'temperature': 22,    # degrees Celsius
    'humidity': 60        # percentage
}
crop_type = 'maize'
phone_number = "+1234567890"  # Replace with the recipient's phone number

# Get response from OpenAI and send SMS
try:
    response = get_openai_response(sensor_data, crop_type)
    print("Response from OpenAI:")
    print(response)
    
    # Send the response via SMS
    send_sms(phone_number, response)
except Exception as e:
    print(f"Error: {e}")
