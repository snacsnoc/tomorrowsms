# tomorrowsms - Weather Forecast SMS Bot

A simple SMS bot built with Flask and Twilio that sends weather forecasts for the next two days based on the user's location. 
Users can provide their location as a postal code, city name, or latitude and longitude.

## Features

- Responds to SMS messages with location information
- Retrieves weather data from the Tomorrow.io API
- Provides a two-day forecast with the following details:
  - Date
  - Weather description
  - Temperature range
  - Precipitation probability

For the full list, see: https://docs.tomorrow.io/reference/weather-forecast
## Installation

1. Clone this repository:

```bash
git clone https://github.com/snacsnoc/tomorrowsms.git
```
2. Change into the project directory:
```bash
cd tomorrowsms
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Set your Tomorrow.io API key as an environment variable:
```bash
export API_KEY="your_tomorrow_io_api_key"
```
## Usage
Run the Flask application:
```bash
python app.py
```
2. Expose your local server using ngrok:
```bash

./ngrok http 5000
```
3. Set up your Twilio phone number's webhook to point to the ngrok URL with /sms appended.

4 .Send an SMS to your Twilio phone number with a postal code, city name, or latitude and longitude (e.g., 42.34, -71.06) to receive a weather forecast for the next two days.

## License
This project is licensed under the MIT License.