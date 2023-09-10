from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import requests
import math

# Configure application
app = Flask(__name__)

# OpenWeatherMap API Configuration
api_key = '592184eab34bceaeae2de4baa2f05256'


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
        weather = weather_data.json()['weather'][0]['main']
        temp_fahrenheit = weather_data.json()['main']['temp']
        temp_celsius = (temp_fahrenheit - 32) * 5 / 9
        if not user_input:
            return render_template("404.html")
        return render_template("search.html", city=user_input, temperature=math.trunc(temp_celsius), weather=weather)
    else:
       return render_template("404.html")


if __name__ == '__main__':
  app.run(debug=True)