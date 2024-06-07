import requests
import json
import serial
import time
import streamlit as st
import plotly.express as px
import pandas as pd
import threading
from testsms import send_sms

# Define your OpenAI API key
openai_api_key = 'EXPAMPLE - KEY HERE'

# Function to send sensor data to OpenAI API and get a response
def get_openai_response(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}',
    }

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
#def send_smsNew(phone_number, message):
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
import requests
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
    print(response)
    return response

def send_smsNew(api_url, username, password, phone_number, message):
    # Example usage
    api_url = "http://sms.reubenwedson.site/api/sms/v1/text/single"
    username = "fredygerman"
    password = "gafhy3-tEpxax-doqnuc"

    response = send_sms(api_url, username, password, phone_number, message)

    return response


# Example usage
api_url = "http://sms.reubenwedson.site/api/sms/v1/text/single"
username = "fredygerman"
password = "gafhy3-tEpxax-doqnuc"





# Function to listen for incoming data from the LoRa Waziup board
def listen_for_lora_data():
    try:
        # Replace 'COM4' with your LoRa board's serial port
        ser = serial.Serial('COM4', baudrate=9600, timeout=5)
        
        # Give the board some time to initialize
        time.sleep(1)

        if ser.inWaiting() > 0:
            incoming_data = ser.readline().decode('utf-8').strip()
            sensor_data = json.loads(incoming_data)
            return sensor_data

        # Close the serial connection
        ser.close()
        
    except Exception as e:
        print(f"Error: {e}")
    
    return None

# Function to handle user questions based on sensor data
def answer_user_question(question, sensor_data, crop_type, language):
    if language == 'English':
        prompt = f"Given the following sensor data for {crop_type}: {sensor_data}, please answer the following question: {question}"
    elif language == 'Kiswahili':
        prompt = f"Ukipatiwa takwimu zifuatazo za sensa kwa {crop_type}: {sensor_data}, tafadhali jibu swali lifuatalo: {question}"
    
    return get_openai_response(prompt)

# Function to listen for incoming SMS
def listen_for_sms():
    try:
        # Replace 'COM3' with your modem's serial port
        ser = serial.Serial('COM3', baudrate=9600, timeout=5)
        
        while True:
            # Give the modem some time to initialize
            time.sleep(1)

            # Check for incoming SMS
            ser.write(b'AT+CMGL="REC UNREAD"\r')
            time.sleep(0.5)
            response = ser.read(ser.inWaiting()).decode()
            
            if "CMGL" in response:
                # Extract phone number and message from the response
                lines = response.split("\n")
                for line in lines:
                    if line.startswith("+CMGL"):
                        parts = line.split(",")
                        phone_number = parts[2].strip('"')
                        message_index = parts[0].split()[1]
                    elif not line.startswith("AT") and line.strip() != "":
                        user_question = line.strip()
                
                if user_question:
                    try:
                        response = answer_user_question(user_question, predefined_data, crop_type, language)
                        send_smsNew(api_url, username, password,phone_number, response)
                        
                    except Exception as e:
                        print(f"Error: {e}")

                # Delete the message
                ser.write(f'AT+CMGD={message_index}\r'.encode())
                time.sleep(0.5)
                ser.read(ser.inWaiting()).decode()

    except Exception as e:
        print(f"Error: {e}")

# Streamlit interface
st.title("AGRISENSE - Smart IoT Farming 🚀")

# Sidebar for language selection
language = st.sidebar.selectbox("Select Language", ["English", "Kiswahili"])

# Input fields for sensor data with default values
soil_moisture = st.number_input('Soil Moisture (%)', min_value=0, max_value=100, value=45)
temperature = st.number_input('Temperature (°C)', min_value=-50, max_value=100, value=22)
humidity = st.number_input('Humidity (%)', min_value=0, max_value=100, value=60)
crop_type = st.text_input('Crop Type', value='maize')
phone_number = st.text_input('Phone Number', value='+255745676696')

# Initial predefined sensor data
predefined_data = {
    'soil_moisture': soil_moisture,
    'temperature': temperature,
    'humidity': humidity
}

# Button to process data and get recommendations
if st.button('Get Recommendations'):
    sensor_data = {
        'soil_moisture': soil_moisture,
        'temperature': temperature,
        'humidity': humidity
    }

    if language == 'English':
        prompt = f"The following data has been collected from sensors for {crop_type}: {sensor_data}. Based on this data, please explain its implications for the farmer and provide specific recommendations on what actions to take if necessary."
    elif language == 'Kiswahili':
        prompt = f"Takwimu zifuatazo zimekusanywa kutoka kwa sensa kwa {crop_type}: {sensor_data}. Kulingana na takwimu hizi, tafadhali eleza athari zake kwa mkulima na toa mapendekezo maalum ya hatua za kuchukua ikiwa ni lazima."

    try:
            response = get_openai_response(prompt)
            st.success("Response from AgrisenseAI:")
            st.write(response)

            api_url = "http://sms.reubenwedson.site/api/sms/v1/text/single"
            username = "fredygerman"
            password = "gafhy3-tEpxax-doqnuc"
            
            # Send the response via SMS
            response2v = send_smsNew(api_url, username, password,phone_number, response)
            st.success(f"SMS sent successfully!{response2v} in {phone_number}")
    except Exception as e:
        st.error(f"Error: {e}")

# Create a DataFrame from predefined sensor data
df = pd.DataFrame([predefined_data])

# Reshape the DataFrame for Plotly
df_melted = df.melt(var_name='Sensor', value_name='Value')

# Create a bar chart using Plotly
fig = px.bar(df_melted, x='Sensor', y='Value', title='Sensor Data Visualization')
st.plotly_chart(fig)

# Chat input for user questions
user_question = st.chat_input("Ask a question based on the data:")

if user_question:
    try:
        response = answer_user_question(user_question, predefined_data, crop_type, language)
        st.success("Response from AgrisenseAI:")
        st.write(response)
    except Exception as e:
        st.error(f"Error: {e}")

# Start the SMS listener thread
sms_listener_thread = threading.Thread(target=listen_for_sms)
sms_listener_thread.daemon = True
sms_listener_thread.start()

# Continuous loop to listen for incoming IoT data
st.write("Listening for incoming IoT data...")

while True:
    lora_data = listen_for_lora_data()
    if lora_data:
        st.write("Incoming IoT data:", lora_data)
        if language == 'English':
            prompt = f"The following data has been collected from sensors for {crop_type}: {lora_data}. Based on this data, please explain its implications for the farmer and provide specific recommendations on what actions to take if necessary."
        elif language == 'Kiswahili':
            prompt = f"Takwimu zifuatazo zimekusanywa kutoka kwa sensa kwa {crop_type}: {lora_data}. Kulingana na takwimu hizi, tafadhali eleza athari zake kwa mkulima na toa mapendekezo maalum ya hatua za kuchukua ikiwa ni lazima."

        try:
            response = get_openai_response(prompt)
            st.success("Response from OpenAI:")
            st.write(response)
            api_url = "http://sms.reubenwedson.site/api/sms/v1/text/single"
            username = "fredygerman"
            password = "gafhy3-tEpxax-doqnuc"
            
            # Send the response via SMS
            response2v = send_smsNew(api_url, username, password,phone_number, response)
            st.success(f"SMS sent successfully!{response2v} in {phone_number}")

            # Update the bar chart with the new data
            df = pd.DataFrame([lora_data])
            df_melted = df.melt(var_name='Sensor', value_name='Value')
            fig = px.bar(df_melted, x='Sensor', y='Value', title='Sensor Data Visualization')
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Error: {e}")
    time.sleep(10)  # Adjust the sleep interval as needed
