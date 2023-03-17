import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re

app = Flask(__name__)

TOMORROW_IO_API_KEY = os.getenv("API_KEY")


# Remove whitespace and any non alpha-numeric characters
def sanitize_input(input_text):
    sanitized_text = re.sub(r'\W+', '', input_text)
    return sanitized_text.strip()


# See https://docs.tomorrow.io/reference/data-layers-weather-codes
def get_weather_description(weather_code):
    weather_descriptions = {
        "0": "Unknown",
        "1000": "Clear, Sunny",
        "1100": "Mostly Clear",
        "1101": "Partly Cloudy",
        "1102": "Mostly Cloudy",
        "1001": "Cloudy",
        "2000": "Fog",
        "2100": "Light Fog",
        "4000": "Drizzle",
        "4001": "Rain",
        "4200": "Light Rain",
        "4201": "Heavy Rain",
        "5000": "Snow",
        "5001": "Flurries",
        "5100": "Light Snow",
        "5101": "Heavy Snow",
        "6000": "Freezing Drizzle",
        "6001": "Freezing Rain",
        "6200": "Light Freezing Rain",
        "6201": "Heavy Freezing Rain",
        "7000": "Ice Pellets",
        "7101": "Heavy Ice Pellets",
        "7102": "Light Ice Pellets",
        "8000": "Thunderstorm",
    }

    return weather_descriptions.get(weather_code, "Unknown")


def get_weather(location):
    url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&fields=core&timesteps=1d&units=metric&apikey={TOMORROW_IO_API_KEY}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        daily_forecast = data["timelines"]["daily"]
        forecast = ""

        for day in daily_forecast[:2]:  # Get the forecast for the next two days
            weather_code = day["values"]["weatherCodeMin"]
            weather_description = get_weather_description(str(weather_code))
            date = day["time"][:10]
            temperature_min = day["values"]["temperatureMin"]
            temperature_max = day["values"]["temperatureMax"]
            precipitation_probability = day["values"]["precipitationProbabilityAvg"]
            forecast += f"Date: {date}\n"
            forecast += f"Weather: {weather_description}\n"
            forecast += f"Temperature: {temperature_min}°C - {temperature_max}°C\n"
            forecast += f"Precipitation Probability: {precipitation_probability}%\n"

        return forecast

    else:
        return "Error: Unable to fetch weather data. Please check your input and try again."


"""
 Respond to an incoming SMS
 Performs a weather lookup from the message body
 Reply with forecast for the next two days
"""


@app.route("/sms", methods=["GET", "POST"])
def incoming_sms():
    body = request.values.get("Body", None)
    sanitized_body = sanitize_input(body)

    resp = MessagingResponse()

    if sanitized_body.lower() in ["hello", "hi", "help"]:
        resp.message(
            "Hi! Please send a postal code, city name, or latitude & longitude (eg 42.34, -71.06) to get the weather forecast for the next two days."
        )
    elif sanitized_body.lower() == "bye":
        resp.message("Goodbye")
    else:
        try:
            forecast = get_weather(sanitized_body)
            resp.message(forecast)
        except Exception as e:
            print(e)
            resp.message(
                "Sorry, we couldn't process your request. Please make sure you provided a valid postal code or city name.")

    return str(resp)


@app.route("/", methods=["GET"])
def index():
    return "Here is a 200 web page"


if __name__ == "__main__":
    app.run(debug=True)
