from os import environ
from requests import get
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, request
from get_price import get_prices

app = Flask(__name__)
load_dotenv()

api_key = environ.get('API_KEY')
url = "https://maps.googleapis.com/maps/api/distancematrix/json"


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html', api_key=api_key)
    else:
        if 'start' in request.form and 'destination' in request.form:
            start = request.form['start']
            destination = request.form['destination']

            fuel = 0
            if 'fuel' in request.form:
                fuel = request.form['fuel']
                fuel_type = request.form['fuel_type']

            payload = {
                'origins': start,
                'destinations': destination,
                'key': api_key
            }

            response = get(url,payload).json()

            distance = response['rows'][0]['elements'][0]['distance']['text']
            distance_meters = response['rows'][0]['elements'][0]['distance']['value']
            time = response['rows'][0]['elements'][0]['duration']['text']

            fuelPrice = f"{round(int(fuel)*distance_meters/100000*get_prices(fuel_type),2)} pln"

            return render_template('index.html', api_key=api_key, distance=distance, time=time, fuelPrice=fuelPrice,
            start=start, destination=destination, fuel=fuel, fuel_type=fuel_type)