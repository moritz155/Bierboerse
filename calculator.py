from flask import Flask, render_template, request, jsonify
import time, json, random
from drink import Drink


# def update_data():  # data returns the last eight prices only
#     drinks = Drink.get_allDrinks()
#     for drink in drinks:
#         mult = 0
#         list = []
#         counter = 0
#         for price in drink.price_history:
#             list.append((counter, round(price, 1)))
#             mult = mult + 1
#             counter += 1
#         counter -= 1
#         if len(list) > 8:
#             data[drink.name] = list[-8:]
#         else:
#             data[drink.name] = list


def calculator():  
   
    data_set = {}
    drink_threshold = get_drink_threshold()
    drinks = Drink.get_allDrinks()
    total_sales = get_total_sales() #last 2 periods

    print(drink_threshold)
    print(len(drinks))
    print(total_sales)
    for drink in drinks:
        relative_part = calc_relative_part(drink.newCounter, total_sales) #drink.orders, sales
        print("relative " + str(relative_part))

        # if can_change_price(relative_part):
        change_price(drink, relative_part, drink_threshold)
        print(drink.name)
        print(drink.price)
        print(get_price_difference(drink))
        time.sleep(1000)
        print(drink.maxPrice)
        print(drink.minPrice)
        print(drink.price_history)
        data_set[drink.name] = {
            "name": drink.name, 
            "price": drink.price, 
            "price_diff": get_price_difference(drink), 
            "min": str(drink.minPrice)[0:3], 
            "max": str(drink.maxPrice)[0:3], 
            "history": drink.price_history}

    print(data_set)
    return data_set
   

def change_price(drink, relative_part, drink_threshold):
    old_price = drink.price
    new_price = 0
    multiplicator = random.randint(0, 5)  # max -50 cent
 
    if relative_part > drink_threshold:
        new_price += old_price + (multiplicator * 0.1)  # get a random higher price
    elif relative_part < drink_threshold:
        new_price += old_price - (multiplicator * 0.1)  # get a random lower price
    else:
        new_price = old_price    
    update_price_history(drink, old_price)
    drink.price = new_price

def get_total_sales():
    drinks = Drink.get_allDrinks()
    total_sales = 0
    for drink in drinks:
        total_sales += drink.newOrders() 
    return total_sales

def update_price_history(drink, old_price):
    drink.price_history.append([time.time(), old_price])

def get_price_difference(drink):
    #import ipdb; ipdb.set_trace()
    return abs(round(drink.price - drink.price_history[-1][1], 2))

def calc_relative_part(drink_sales, total_sales):
    if drink_sales == 0:
        return 0
    else:
        return drink_sales / total_sales # can be between 0 and 1

def can_change_price(relative_part):
    drink_threshold = get_drink_threshold()
    # TODO
    # INCLUDE PRICE-CHANGE-PROBABILITY
    # drink.prob > threshold ...
    return relative_part != 0 and relative_part != drink_threshold


def get_drink_threshold():
    return drink_threshold
   



    # # create json object with following attributes
    # # name, price, price difference, max, min
    # global current_time, updated_last_time, old_table_data
    # updated_last_time = time.time()
    # current_time = time.time()
    # all_drinks_data = {}
    # newly_bought = 0  # sum of all drinks that were newly bought
    # counter = 0
    # changePrice = []  # takes drink if price was added in this period
    # drinks = Drink.get_allDrinks()

    # for drink in drinks:  # calculate all ordered drinks --> store in variable newly_bought
    #     drink.newOrders()
    #     newly_bought = newly_bought + drink.newCounter
   
    # for drink in drinks:
    #     # calculate relative parts
    #     relative_part = 0.0
    #     if not newly_bought == 0:
    #         relative_part = drink.newCounter / newly_bought
    #     # increase prices if relative part higher than X
    #     if relative_part >= drink_threshold:  # relative part must be higher than 25% to increase price
    #         drink.addNewRandomPrice(price_increase=True, change_price=True)
    #         changePrice.append(drink)
    #         continue
    #     elif relative_part == 0 and counter == 0:  # decrease price of first drink that wasnt bought in this period
    #         counter = 1  # ensures that only one price will decrease
    #         drink.addNewRandomPrice(False, True)
    #         changePrice.append(drink)
    #         continue

    #         # changePrice = [drink_1, drink_2]

    # addPriceTo = [x for x in drinks if
    #             x not in changePrice]  # includes all drinks that do not have enough prices
    
    # for drink in addPriceTo:
    #     drink.addNewRandomPrice(True, False)  # all drinks now have same number of prices
    #     update_data()

    # for drink in drinks:
    #     # part for table data
    #     single_drink_dict = {"name": drink.name, "price": str(drink.price_history[-1])[0:3]}
    #     try:
    #         single_drink_dict["price_diff"] = str(drink.price_history[-1] - drink.price_history[-2])[0:4]
    #     except IndexError:  # if price history has only one price
    #         single_drink_dict["price_diff"] = 0
    #     single_drink_dict["min"] = str(drink.minPrice)[0:3]
    #     single_drink_dict["max"] = str(drink.maxPrice)[0:3]
      

    #     history_list = []
    #     timestamp = request.args.get('timestamp')
    #     if timestamp is not None:
    #         timestamp = float(timestamp)
    #     for i in data[drink.name]:
    #         if timestamp is None or i[1] >= timestamp:
    #             history_list.append(i)
    #     single_drink_dict["history"] = history_list

    #     all_drinks_data[drink.name] = single_drink_dict

    # old_table_data = all_drinks_data
    # print(old_table_data)
    # return old_table_data

# {
# 'G▒sser': 
#     {'name': 'G▒sser', 'price': '1.5', 'price_diff': '0.0', 'min': '1.4', 'max': '2.9', 'history': 
#         [(1675599840.6523569, 1.5), (1675599870.6523569, 1.5), (1675599900.6523569, 1.5), (1675599930.6523569, 1.5), (1675599960.6523569, 1.5), (1675599990.6523569, 1.5), (1675600020.6523569, 1.5), (1675600050.6523569, 1.5)]
#     }, 
# 'Gustl': 
#     {'name': 'Gustl', 'price': '2.0', 'price_diff': '0.0', 'min': '1.4', 'max': '2.8', 'history': 
#         [(1675599840.6523569, 2.0), (1675599870.6523569, 2.0), (1675599900.6523569, 2.0), (1675599930.6523569, 2.0), (1675599960.6523569, 2.0), (1675599990.6523569, 2.0), (1675600020.6523569, 2.0), (1675600050.6523569, 2.0)]
#     },
# 'Radler': 
#     {'name': 'Radler', 'price': '2.3', 'price_diff': '0.0', 'min': '1.6', 'max': '3.2', 'history':
#         [(1675599840.6523569, 2.3), (1675599870.6523569, 2.3), (1675599900.6523569, 2.3), (1675599930.6523569, 2.3), (1675599960.6523569, 2.3), (1675599990.6523569, 2.3), (1675600020.6523569, 2.3), (1675600050.6523569, 2.3)]
#     },
# 'Tyskie': 
#     {'name': 'Tyskie', 'price': '2.2', 'price_diff': '0.0', 'min': '1.5', 'max': '3.0', 'history': 
#         [(1675599840.6523569, 2.2), (1675599870.6523569, 2.2), (1675599900.6523569, 2.2), (1675599930.6523569, 2.2), (1675599960.6523569, 2.2), (1675599990.6523569, 2.2), (1675600020.6523569, 2.2), (1675600050.6523569, 2.2)]
#     }, 
# 'Cola': 
#     {'name': 'Cola', 'price': '1.9', 'price_diff': '0.0', 'min': '1.3', 'max': '2.6', 'history': 
#         [(1675599840.6523569, 1.9), (1675599870.6523569, 1.9), (1675599900.6523569, 1.9), (1675599930.6523569, 1.9), (1675599960.6523569, 1.9), (1675599990.6523569, 1.9), (1675600020.6523569, 1.9), (1675600050.6523569, 1.9)]
#     },
# 'Wein': 
#     {'name': 'Wein', 'price': '1.7', 'price_diff': '0.0', 'min': '1.1', 'max': '2.3', 'history':
#         [(1675599840.6523569, 1.7), (1675599870.6523569, 1.7), (1675599900.6523569, 1.7), (1675599930.6523569, 1.7), (1675599960.6523569, 1.7), (1675599990.6523569, 1.7), (1675600020.6523569, 1.7), (1675600050.6523569, 1.7)]
#     }, 
# 'Luft':
#     {'name': 'Luft', 'price': '1.5', 'price_diff': '0.0', 'min': '1.0', 'max': '2.0', 'history': 
#         [(1675599840.6523569, 1.5), (1675599870.6523569, 1.5), (1675599900.6523569, 1.5), (1675599930.6523569, 1.5), (1675599960.6523569, 1.5), (1675599990.6523569, 1.5), (1675600020.6523569, 1.5), (1675600050.6523569, 1.5)]
#     }
# }






# old_table_data = []
# updated_last_time = time.time()
# current_time: float = time.time()
# start_time = float(time.time())
# iteration_interval = 5  # in seconds
# data = {}
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
