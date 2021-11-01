from flask import Flask, render_template, request, jsonify
import time, json, random


class Drink:
    def __init__(self, name, init_price):  # array with one price - the starting price
        self.name = name
        self.price_history = init_price  # former allPrices
        self.maxPrice = init_price[0] * 1.4
        self.minPrice = init_price[0] * 0.7
        self.newDict = {}  # gives every order a time; size of dict is equal to amount of orders
        self.newCounter = 0  # counter of orders in a period
        self.price_was_changed = 0  # counts the times the price is changed

    def addPrice(self, newPrice):
        self.price_history.append(newPrice)

    def update_recentlyChangedPrices(self):
        for drink in recentlyChangedPrices:
            if self == drink:
                recentlyChangedPrices.remove(drink)
                recentlyChangedPrices.append(drink)
                return
        recentlyChangedPrices.append(self)  # if price of drink wasnt changed yet

    def addNewRandomPrice(self, price_increase, change_price):
        if change_price:
            self.price_was_changed = self.price_was_changed + 1
            multiplicator = random.randint(0, 5)  # max -50 cent
            oldPrice = self.price_history[-1]
            if price_increase:
                newPrice = oldPrice + (multiplicator * 0.1)  # get a random lower price
            elif not price_increase:
                newPrice = oldPrice - (multiplicator * 0.1)  # get a random higher price
            if self.minPrice < newPrice < self.maxPrice:
                self.addPrice(newPrice)
            else:
                self.addPrice(oldPrice)
            self.update_recentlyChangedPrices()
        else:
            self.addPrice(self.price_history[-1])

    def newOrders(self):
        current_time = time.time()
        listOfItemsToRemove = []
        self.newCounter = 0
        for element_time in self.newDict:
            if current_time - element_time > iteration_interval * 10:
                listOfItemsToRemove.append(element_time)
            else:
                self.newCounter = self.newCounter + 1
        for i in listOfItemsToRemove:
            del self.newDict[i]


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


def update_data():  # data returns the last eight prices only
    for drink in allDrinks:
        mult = 0
        list = []
        for price in drink.price_history:
            list.append((start_time + 30 * mult, str(price)[0:3]))
            mult = mult + 1
        if len(list) > 8:
            data[drink.name] = list[-8:]
        else:
            data[drink.name] = list


def simulation():
    numberOfDrinks = random.randint(3, 10)
    for j in range(numberOfDrinks):
        drink = random.randint(0, (len(allDrinks) - 1))
        allDrinks[drink].newDict[time.time()] = 1


def analysis():
    changed = 0
    for drink in allDrinks:
        print(drink.name)
        changed = changed + drink.price_was_changed
        p = 0
        for price in drink.price_history:
            p = p + price
        print(drink.name + " average price: " + str(p / len(drink.price_history)))
    print(changed)


def build_data_for_table():
    table_data = []
    for drink in allDrinks:
        single_drink_data = []
        single_drink_data.append(drink.name)
        single_drink_data.append(str(drink.price_history[-1])[0:3])  # current price
        try:
            single_drink_data.append(str(drink.price_history[-1] - drink.price_history[-2])[0:4])  # price difference
        except IndexError:  # if price history has only one price
            single_drink_data.append(0)
        single_drink_data.append(str(drink.minPrice)[0:3])
        single_drink_data.append(str(drink.maxPrice)[0:3])
        table_data.append(single_drink_data)
    global old_table_data
    old_table_data = table_data
    return table_data


@app.route('/input')
def input():
    return render_template('OrderDrinks.html', beers=beers_names, colorSet=customColorSet)


@app.route('/fullScreen')
def fullScreen():
    return render_template('fullScreen_test.html', beers=beers_names, colorSet=customColorSet,
                           iteration=iteration_interval)


@app.route('/table')
def table():  # table needs: name, price, price difference, max, min
    table_data = calculator()
    return render_template('beerTable.html', beers=table_data, colorSet=customColorSet, iteration=iteration_interval)


@app.route('/data/table')
def data_for_table():  # table needs: name, price, price difference, max, min
    return calculator()


@app.route('/')
def index():
    return render_template('bierpreise.html', beers=beers_names, iteration=iteration_interval, colorSet=customColorSet)


@app.route('/ordered_Drink/', methods=['POST'])
def ordered_Drink():  # receives the orders and adds it to the drink objects
    name = request.form.get('name', 0)
    for drink in allDrinks:
        if drink.name == name:
            clock = float(time.time())
            drink.newDict[clock] = 1
    return ""


def calculator():  # calculates the new prices and returns a json with all necessary datapoints
    # create json object with following attributes
    # name, price, price difference, max, min
    global current_time, updated_last_time, old_table_data

    if time.time() - updated_last_time >= iteration_interval:
        updated_last_time = time.time()
        all_drinks_data = {}
        result = {}
        timestamp = request.args.get('timestamp')
        if timestamp is not None:
            timestamp = float(timestamp)
        if time.time() - current_time > iteration_interval:  # ensure that prices never update more often than interval
            current_time = time.time()
            simulation()
            newly_bought = 0
            for drink in allDrinks:
                drink.newOrders()
                newly_bought = newly_bought + drink.newCounter
                # print(drink.name + str(drink.newCounter))
            counter = 0
            changePrice = []  # takes drink if price was added in this period
            table_data = []
            # snd part of logic
            for drink in allDrinks:
                relative_part = 0.0
                if not newly_bought == 0:
                    relative_part = drink.newCounter / newly_bought
                if relative_part >= 0.25:  # relative part must be higher than 25% to increase price
                    drink.addNewRandomPrice(True, True)
                    changePrice.append(drink)
                    continue
                elif relative_part == 0 and counter == 0:  # decrease price of first drink that wasnt bought in this period
                    counter = 1  # secures that only one price will decrease
                    drink.addNewRandomPrice(False, True)
                    changePrice.append(drink)
                    continue
            if len(recentlyChangedPrices) == len(allDrinks):
                recentlyChangedPrices[0].addNewRandomPrice(False, True)
                changePrice.append(recentlyChangedPrices[-1])
            else:
                notChangedYet = [x for x in allDrinks if x not in recentlyChangedPrices]
                drink = random.choice(notChangedYet)
                drink.addNewRandomPrice(False, True)  # takes random drink of those without price change_price
                changePrice.append(drink)
            addPriceTo = [x for x in allDrinks if
                          x not in changePrice]  # includes all drinks that do not have enough prices
            for drink in addPriceTo:
                drink.addNewRandomPrice(True, False)  # all drinks now have same number of prices
            update_data()
        for drink in allDrinks:
            # part for table data
            single_drink_dict = {"name": drink.name, "price": str(drink.price_history[-1])[0:3]}
            try:
                single_drink_dict["price_diff"] = str(drink.price_history[-1] - drink.price_history[-2])[0:4]
            except IndexError:  # if price history has only one price
                single_drink_dict["price_diff"] = 0
            single_drink_dict["min"] = str(drink.minPrice)[0:3]
            single_drink_dict["max"] = str(drink.maxPrice)[0:3]
            history_list = []
            for i in data[drink.name]:
                if timestamp is None or i[1] >= timestamp:
                    history_list.append(i)
            single_drink_dict["history"] = history_list
            all_drinks_data[drink.name] = single_drink_dict
        old_table_data = all_drinks_data
    return old_table_data


old_table_data = []
updated_last_time = time.time()
current_time: float = time.time()
start_time = float(time.time())
iteration_interval = 5  # in seconds
data = {}
customColorSet = ["#FF0000",
                  "#FF8F00",
                  "#4BF70B",
                  "#0BF7C5",
                  "#0B0FF7",
                  "#C90BF7",
                  "#F70B6F"
                  ]
Drink1 = Drink("Gösser", [2.10])
Drink2 = Drink("Gustl", [2.0])
Drink3 = Drink("Radler", [2.3])
Drink4 = Drink("Tyskie", [2.2])
Drink5 = Drink("Cola", [1.9])
Drink6 = Drink("Wein", [1.7])
Drink7 = Drink("Luft", [1.5])
allDrinks = [Drink1, Drink2, Drink3, Drink4, Drink5, Drink6, Drink7]
clock_for_analysis = time.time()
recentlyChangedPrices = []
beers_names = []
for beer in allDrinks:
    beers_names.append(beer.name)
app.run('127.0.0.1', 8000, debug=True)
