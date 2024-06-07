
---

# AGRISENSE - Smart IoT Farming 🚀

![AGRISENSE](https://github.com/benny-png/BUNI-HUB-IOT-BASED-AGRO-CHATBOT-PROJECT/raw/main/AGRISENSE.png)

## Overview

AGRISENSE is an intelligent IoT-based farming assistant that leverages sensor data and AI to provide farmers with actionable insights and recommendations. The system collects real-time data from various sensors, processes this data using OpenAI's GPT-4, and sends recommendations to farmers via SMS. The platform supports both English and Kiswahili languages.

![AGRISENSE2](https://github.com/benny-png/BUNI-HUB-IOT-BASED-AGRO-CHATBOT-PROJECT/raw/main/AGRISENSE2.png)

## Features

- **Real-time Sensor Data Collection**: Collects data on soil moisture, temperature, and humidity.
- **AI-Powered Recommendations**: Uses OpenAI's GPT-4 model to provide insights and recommendations based on sensor data.
- **Multi-Language Support**: Supports English and Kiswahili for both data input and recommendations.
- **SMS Notifications**: Sends AI-generated recommendations to farmers via SMS.
- **User Interaction**: Allows farmers to ask questions based on the sensor data and receive intelligent responses.
- **Data Visualization**: Displays sensor data using interactive charts.

## Requirements

- Python 3.9+
- Streamlit
- Plotly
- Requests
- PySerial
- Pandas

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/AGRISENSE.git
    cd AGRISENSE
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Add your OpenAI API key in the `openai_api_key` variable in the script.

4. Connect your HSUPA modem and LoRa Waziup board to the appropriate COM ports.

## Usage

1. Run the Streamlit application:
    ```bash
    streamlit run test2_streamlit_app.py
    ```

2. Access the application in your browser at `http://localhost:8501`.

![AGRISENSE3](https://github.com/benny-png/BUNI-HUB-IOT-BASED-AGRO-CHATBOT-PROJECT/raw/main/AGRISENSE3.png)

3. Enter the sensor data, crop type, and phone number.

4. Click "Get Recommendations" to receive AI-generated advice based on the input data.

5. Use the chat input to ask questions related to the sensor data and receive instant responses.

![AGRISENSE4](https://github.com/benny-png/BUNI-HUB-IOT-BASED-AGRO-CHATBOT-PROJECT/raw/main/AGRISENSE4.png)

6. The system continuously listens for incoming IoT data and SMS messages, processes them, and updates the recommendations accordingly.

## Contributing

Feel free to fork the repository, make improvements, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries or support, please contact:
- **Your Name**: your.email@example.com
- **GitHub**: [yourusername](https://github.com/yourusername)

---

