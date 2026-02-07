from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import time, json, random
from datetime import datetime, timedelta
from calculator import calculator, get_current_data
from drink import Drink
# from simulation import Simulation

from flask_sock import Sock
import requests
from websocket import create_connection
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import csv
import os

LOG_FILE = 'sales_summary.csv'
sales_stats = {}

def load_stats():
    global sales_stats
    if os.path.isfile(LOG_FILE):
        with open(LOG_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None) # skip header
            for row in reader:
                if row:
                    sales_stats[row[0]] = {'amount': int(row[1]), 'revenue': float(row[2])}

def save_stats():
    with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Drink', 'Amount', 'Total_Revenue'])
        for name, data in sales_stats.items():
            writer.writerow([name, data['amount'], f"{data['revenue']:.2f}"])

def update_stats(drink_name, price):
    if drink_name not in sales_stats:
        sales_stats[drink_name] = {'amount': 0, 'revenue': 0.0}
    sales_stats[drink_name]['amount'] += 1
    sales_stats[drink_name]['revenue'] += price

load_stats()




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
            try:
                sock.send(json.dumps(get_current_data()))
            except Exception:
                pass
        if len(global_socks) > 0:
            for s in global_socks[:]:
                try:
                    s.send(data)
                except Exception:
                    if s in global_socks:
                        global_socks.remove(s)
        else:
            try:
                sock.send(data)
            except Exception:
                pass


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
    ws.send(json.dumps({"type": "ALCOHOL", "value": Drink.total_alcohol_sold}))
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
        if drink:
             clock = float(time.time())
             current_price = drink.price
             drink.orders[clock] = 1  # Add order to drink object
             Drink.total_alcohol_sold += drink.alcohol_content
             update_stats(drink.name, current_price)
        else:
             print(f"Warning: Drink {ordered_drink} not found")

    save_stats()
    calc_new_data()  # Calculate new data after processing purchases
    return jsonify({"message": "Drinks processed successfully"}), 200


def calc_new_data():
    r = requests.get('http://127.0.0.1:8000/data')  # send request to new data

def get_drink_names():
    drinks = Drink.get_allDrinks()
    return list(map(lambda drink:drink.name, drinks))

iteration_interval = 300 # in seconds
customColorSet = ["#FF0000",
                  "#4b6e10",
                  "#4BF70B",
                  "#134191",
                  "#1da4a8",
                  "#C90BF7",
                  "#F70B6F",
                  "#6B68ED",
                  "#6b8258",
                  "#FF0FB4",
                  "#FB0B1F",
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
