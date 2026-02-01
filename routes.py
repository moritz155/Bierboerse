from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import time, json, random
from calculator import calculator, get_current_data
from drink import Drink
# from simulation import Simulation

from flask_sock import Sock
import requests
from websocket import create_connection
import atexit
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__)
CORS(app)
sock = Sock(app)
global_socks = []
app.config['SECRET_KEY'] = 'secret!'



@sock.route('/echo')
def echo(sock):
    while True:
        data = sock.receive()
        print("im in def echo n routes")
        if data == 'CHART' or data == 'TABLE' or data == 'INPUT':
            global global_socks
            global_socks.append(sock)
            try:
                sock.send(json.dumps(get_current_data()))
            except Exception:
                pass
        if len(global_socks) > 0:
            for sock in global_socks:
                try:
                    sock.send(data)
                except Exception:
                    global_socks.remove(sock)
        else:
            try:
                sock.send(data)
            except Exception:
                pass


@app.route('/input')
def input():
    return render_template('OrderDrinks.html', beers=beers_names, colorSet=customColorSet)


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
def ordered_Drink():  # receives the orders and adds it to the drink objects
    print('ordered_Drink')
    orders = request.get_json(force=True)
    drinks = Drink.get_allDrinks()
    print("im in def ordered_drink n routes")
    print("orders: ", orders)
    
    current_time = float(time.time())
    for name, amount in orders.items():
        print(f"DEBUG: Processing {name}: {amount}")
        for drink in drinks:
            if drink.name == name:
                # Add unique order entries for the amount purchased
                for i in range(amount):
                    drink.orders[current_time + (i * 0.000001)] = 1
                break
    calc_new_data()
    scheduler.reschedule_job('price_update_job', trigger='interval', seconds=iteration_interval)
    return ""


def calc_new_data():
    print('HERE')
    print('calc_new_data')
    r = requests.get('http://127.0.0.1:8000/data')  # send request to new data


iteration_interval = 15
customColorSet = ["#FF0000",
                  "#FF8F00",
                  "#4BF70B",
                  "#0BF7C5",
                  "#0B0FF7",
                  "#C90BF7",
                  "#F70B6F"
                  ]

beers_names = ["Gösser","Gustl","Radler","Tyskie","Cola","Wein","Luft"]

### Create a scheduler that executes /calculates new data every {iteration_interval} seconds
scheduler = BackgroundScheduler()
# Create the job
scheduler.add_job(func=calc_new_data, trigger='interval', seconds=iteration_interval, id='price_update_job')
# Start the scheduler
scheduler.start()

# /!\ IMPORTANT /!\ : Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

app.run('127.0.0.1', 8000, debug=True, use_reloader=False)
