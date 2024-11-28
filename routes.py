from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import time, json, random
from datetime import datetime, timedelta
from calculator import calculator
from drink import Drink
# from simulation import Simulation

from flask_sock import Sock
import requests
from websocket import create_connection
import atexit
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes by default
sock = Sock(app)
global_socks = []
app.config['SECRET_KEY'] = 'secret!'



@sock.route('/echo')
def echo(sock):
    while True:
        data = sock.receive()
        if data == 'CHART' or data == 'TABLE' or data == 'INPUT' or data == 'WHEEL':
            global global_socks
            global_socks.append(sock)
        if len(global_socks) > 0:
            for sock in global_socks:
                sock.send(data)
        else:
            sock.send(data)


@app.route('/input')
def input():
    return render_template('OrderDrinks.html', beers=beers_names, colorSet=customColorSet)

@app.route('/wheel')
def wheel():
    return render_template('WheelOfFortune.html', beers=beers_names, colorSet=customColorSet)


@app.route('/table')
def table():  # table needs: name, price, price difference, max, min
    return render_template('beerTable.html', colorSet=customColorSet, iteration=iteration_interval)


@app.route('/data')
def data_for_table():  # table needs: name, price, price difference, max, min
    ws = create_connection("ws://localhost:8000/echo")
    ws.send(json.dumps(calculator()))
    ws.close()
    return {}


@app.route('/')
def index():
    return render_template('bierpreise.html', beers=beers_names, iteration=iteration_interval,
                           colorSet=customColorSet)


@app.route('/ordered_Drink/', methods=['POST'])
def ordered_Drink():  
    # Receives a list of orders and adds them to the drink objects
    drink_names = request.form.getlist('names[]')  # Retrieve list of drink names (IDs)

    drinks = Drink.get_allDrinks()
    print(f"Processing ordered drinks: {drink_names}")
    for ordered_drink in drink_names:
        drink = Drink.get_drink_by_name(ordered_drink)
        clock = float(time.time())
        drink.orders[clock] = 1  # Add order to drink object

    calc_new_data()  # Calculate new data after processing purchases
    return jsonify({"message": "Drinks processed successfully"}), 200


def calc_new_data():
    r = requests.get('http://127.0.0.1:8000/data')  # send request to new data

def get_drink_names():
    drinks = Drink.get_allDrinks()
    return list(map(lambda drink:drink.name, drinks))

iteration_interval = 90
customColorSet = ["#FF0000",
                  "#FF8F00",
                  "#4BF70B",
                  "#0BF7C5",
                  "#0B0FF7",
                  "#C90BF7",
                  "#F70B6F",
                  "#F9FBA7",
                  "#C930A7",
                  "#FF0FB4",
                  ]

beers_names = get_drink_names()


### Create a scheduler that executes /calculates new data every {iteration_interval} seconds
scheduler = BackgroundScheduler()

# Create the job
scheduler.add_job(
    func=calc_new_data, 
    trigger='interval', 
    seconds=iteration_interval, 
    next_run_time=datetime.now() + timedelta(seconds=5)  # Schedule the first run after x seconds
)
# Start the scheduler
scheduler.start()

# IMPORTANT: Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

app.run('127.0.0.1', 8000, debug=True, use_reloader=False)
