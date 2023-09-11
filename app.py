from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import requests
import math

# Configure application
app = Flask(__name__)

# OpenWeatherMap API Configuration
api_key = '592184eab34bceaeae2de4baa2f05256'

# user_input = input("Enter a city: ")
# weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")

# print(weather_data.json())

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/get_time")
def get_time():
    curr_time = time.strftime("%H:%M:%S", time.localtime())
    return jsonify({"time": curr_time})
    
@app.route("/search", methods=["GET", "POST"])
def search():
    user_input = request.args.get("cityName")
    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")
    if weather_data.status_code == 200:
        name = weather_data.json()['name']
        weather = weather_data.json()['weather'][0]['main']
        weather_desc = weather_data.json()['weather'][0]['description']
        temp_fahrenheit = weather_data.json()['main']['temp']
        temp_celsius = (temp_fahrenheit - 32) * 5 / 9
        wind = round(weather_data.json()['wind']['speed'] * 1.609, 2)
        humidity = weather_data.json()['main']['humidity']
        country_code = weather_data.json()['sys']['country']

        longitude = weather_data.json()['coord']['lon']
        latitude = weather_data.json()['coord']['lat']

        mapbox_access_token = 'pk.eyJ1IjoiYm9yaXN2aWNlbmEiLCJhIjoiY2xtZXhkNjYyMDI5ZTNqcnlkZWt5aTl2NiJ9.2dOC8qHUVmf2SoSmxUleOQ'

        if not user_input:
            return render_template("404.html")
        return render_template("search.html", city=name, temperature=math.trunc(temp_celsius), weather=weather, weather_desc=weather_desc, 
                               wind=wind, humidity=humidity, country_code=country_code, longitude=longitude, latitude=latitude, mapbox_access_token=mapbox_access_token)
    else:
       return render_template("404.html")


if __name__ == '__main__':
  app.run(debug=True)