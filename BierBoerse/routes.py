from flask import Flask, render_template, request, jsonify
import time, json, random


class Drink:

    def __init__(self, name, allPrices):
        self.name = name
        self.allPrices = allPrices
        self.maxPrice = allPrices[0] * 1.4
        self.minPrice = allPrices[0] * 0.7
        self.newDict = {}
        self.newCounter = 0
        self.price_was_changed = 0

    def addPrice(self, newPrice):
        self.allPrices.append(newPrice)

    def update_recentlyChangedPrices(self):
        for drink in recentlyChangedPrices:
            if self == drink:
                recentlyChangedPrices.remove(drink)
                recentlyChangedPrices.append(drink)
                return
        recentlyChangedPrices.append(self)  # if price of drink wasnt changed yet

    def addNewRandomPrice(self, high, change):
        if change:
            self.price_was_changed = self.price_was_changed + 1
            multiplicator = random.randint(0, 5)  # max -50 cent
            oldPrice = self.allPrices[-1]
            if high:
                newPrice = oldPrice + (multiplicator * 0.1)  # get a random lower price
            elif not high:
                newPrice = oldPrice - (multiplicator * 0.1)  # get a random higher price
            if self.minPrice < newPrice < self.maxPrice:
                self.addPrice(newPrice)
            else:
                self.addPrice(oldPrice)
            self.update_recentlyChangedPrices()
        else:
            self.addPrice(self.allPrices[-1])

    def newOrders(self):
        current_time = time.time()
        listOfItemsToRemove = []
        self.newCounter = 0
        for element_time in self.newDict:
            if current_time - element_time > iterate * 2:
                listOfItemsToRemove.append(element_time)
            else:
                self.newCounter = self.newCounter + 1
        for i in listOfItemsToRemove:
            del self.newDict[i]


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
uhrzeit = float(time.time())
iterate = 5   #in seconds
data = {}
customColorSet = ["#FF0000",
                  "#FF8F00",
                  "#4BF70B",
                  "#0BF7C5",
                  "#0B0FF7",
                  "#C90BF7",
                  "#F70B6F"
                  ]


def updateData():  # data returns the last eight prices only
    for drink in allDrinks:
        mult = 0
        list = []
        for price in drink.allPrices:
            list.append((uhrzeit + 30 * mult, round(price, 2)))
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
        for price in drink.allPrices:
            p = p + price
        print(drink.name + " average price: " + str(p / len(drink.allPrices)))
    print(changed)


@app.route('/input')
def input():
    return render_template('OrderDrinks.html', beers=beers_names, colorSet=customColorSet)


@app.route('/ordered_Drink/', methods=['POST'])
def ordered_Drink():
    name = request.form.get('name', 0)
    for drink in allDrinks:
        if drink.name == name:
            uhrzeit = float(time.time())
            drink.newDict[uhrzeit] = 1
    return ""


@app.route('/')
def index():
    return render_template('bierpreise.html', beers=beers_names, iteration=iterate, colorSet=customColorSet)


@app.route('/data/preise')
def preise():
    simulation()
    timestamp = request.args.get('timestamp')
    if timestamp is not None:
        timestamp = float(timestamp)
    result = {}
    newly_bought = 0
    for drink in allDrinks:
        drink.newOrders()
        newly_bought = newly_bought + drink.newCounter
    counter = 0
    changePrice = []  # takes drink if price was added in this period
    for drink in allDrinks:
        relative_part = 0
        if not newly_bought == 0:
            relative_part: float = drink.newCounter / newly_bought
        if relative_part >= 0.25:  # relative part must be higher than 25% to increase price
            drink.addNewRandomPrice(True, True)
            changePrice.append(drink)
            continue
        elif relative_part == 0 and counter == 0:
            counter = 1  # secures that only one price will fall
            drink.addNewRandomPrice(False, True)
            changePrice.append(drink)
            continue
    if len(recentlyChangedPrices) == len(allDrinks):
        recentlyChangedPrices[0].addNewRandomPrice(False, True)
        changePrice.append(recentlyChangedPrices[-1])
    else:
        notChangedYet = [x for x in allDrinks if x not in recentlyChangedPrices]
        drink = random.choice(notChangedYet)
        drink.addNewRandomPrice(False, True)  # takes random drink of those without price change
        changePrice.append(drink)
    addPriceTo = [x for x in allDrinks if x not in changePrice]  # includes all drinks that do not have enough prices
    for drink in addPriceTo:
        drink.addNewRandomPrice(True, False)  # all drinks now have same number of prices
    updateData()
    global clock
    if time.time() - clock >= 140:
        analysis()
        clock = time.time()
    for drink in data:
        result[drink] = []
        for i in data[drink]:
            if timestamp is None or i[1] >= timestamp:
                result[drink].append(i)
    return json.dumps(result)


Drink1 = Drink("Gösser", [2.10])
Drink2 = Drink("Gustl", [2.0])
Drink3 = Drink("Radler", [2.3])
Drink4 = Drink("Tyskie", [2.2])
Drink5 = Drink("Cola", [1.9])
Drink6 = Drink("Wein", [1.7])
Drink7 = Drink("Luft", [1.5])
allDrinks = [Drink1, Drink2, Drink3, Drink4, Drink5, Drink6, Drink7]
clock = time.time()
recentlyChangedPrices = []
beers_names = []
for beer in allDrinks:
    beers_names.append(beer.name)

app.run('localhost', 8000, debug=True)
