from flask import Flask, render_template, request, jsonify
import time, json, random
from drink import Drink


def update_data():  # data returns the last eight prices only
    drinks = Drink.get_allDrinks()
    for drink in drinks:
        mult = 0
        list = []
        counter = 0
        for price in drink.price_history:
            list.append((counter, round(price, 1)))
            mult = mult + 1
            counter += 1
        counter -= 1
        if len(list) > 8:
            data[drink.name] = list[-8:]
        else:
            data[drink.name] = list


def calculator():  # calculates the new prices and returns a json with all necessary datapoints
    # create json object with following attributes
    # name, price, price difference, max, min
    global current_time, updated_last_time, old_table_data
    updated_last_time = time.time()
    current_time = time.time()
    all_drinks_data = {}
    newly_bought = 0  # sum of all drinks that were newly bought
    counter = 0
    changePrice = []  # takes drink if price was added in this period
    drinks = Drink.get_allDrinks()

    for drink in drinks:  # calculate all ordered drinks --> store in variable newly_bought
        drink.newOrders()
        newly_bought = newly_bought + drink.newCounter
    for drink in drinks:
        # calculate relative parts
        relative_part = 0.0
        if not newly_bought == 0:
            relative_part = drink.newCounter / newly_bought
        # increase prices if relative part higher than X
        if relative_part >= drink_threshold:  # relative part must be higher than 25% to increase price
            drink.addNewRandomPrice(price_increase=True, change_price=True)
            changePrice.append(drink)
            continue
        elif relative_part == 0 and counter == 0:  # decrease price of first drink that wasnt bought in this period
            counter = 1  # ensures that only one price will decrease
            drink.addNewRandomPrice(False, True)
            changePrice.append(drink)
            continue
    addPriceTo = [x for x in drinks if
                x not in changePrice]  # includes all drinks that do not have enough prices
    for drink in addPriceTo:
        drink.addNewRandomPrice(True, False)  # all drinks now have same number of prices
        update_data()
    for drink in drinks:
        # part for table data
        single_drink_dict = {"name": drink.name, "price": str(drink.price_history[-1])[0:3]}
        try:
            single_drink_dict["price_diff"] = str(drink.price_history[-1] - drink.price_history[-2])[0:4]
        except IndexError:  # if price history has only one price
            single_drink_dict["price_diff"] = 0
        single_drink_dict["min"] = str(drink.minPrice)[0:3]
        single_drink_dict["max"] = str(drink.maxPrice)[0:3]
        history_list = []

        timestamp = request.args.get('timestamp')
        if timestamp is not None:
            timestamp = float(timestamp)
        for i in data[drink.name]:
            if timestamp is None or i[1] >= timestamp:
                history_list.append(i)
        single_drink_dict["history"] = history_list
        all_drinks_data[drink.name] = single_drink_dict
    old_table_data = all_drinks_data
    return old_table_data






# old_table_data = []
# updated_last_time = time.time()
# current_time: float = time.time()
start_time = float(time.time())
# iteration_interval = 5  # in seconds
data = {}
drink_threshold = 0.25
# customColorSet = ["#FF0000",
#                   "#FF8F00",
#                   "#4BF70B",
#                   "#0BF7C5",
#                   "#0B0FF7",
#                   "#C90BF7",
#                   "#F70B6F"
#                   ]

# allDrinks = [
# Drink("Gösser", [2.10]), 
# Drink("Gustl", [2.0]), 
# Drink("Radler", [2.3]), 
# Drink("Tyskie", [2.2]),
# Drink("Cola", [1.9]),
# Drink("Wein", [1.7]),
# Drink("Luft", [1.5])]
# beers_names = ["Gösser","Gustl","Radler","Tyskie","Cola","Wein","Luft"]
# clock_for_analysis = time.time()
# recentlyChangedPrices = []
