from flask import Flask, render_template, request, jsonify
import time, json, random
from drink import Drink
from PriceChange import PriceChange


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
    total_sales = get_total_sales()  # last 2 periods

    for drink in drinks:
        relative_part = calc_relative_part(drink.newCounter, total_sales)  # drink.orders, sales

        if above_threshold(relative_part, drink_threshold):
            change_price(drink=drink, interval_start=0.3, price_change=PriceChange.UP)
        elif randomly_change_price(drink):
            direction = get_random_direction()
            change_price(drink=drink, interval_start=0.1, price_change=direction)
        else:  # price was not changed --> old price = current price
            update_price_history(drink, drink.price)

        data_set[drink.name] = {
            "name": drink.name,
            "price": drink.price,
            "price_diff": get_price_difference(drink),
            "min": str(drink.minPrice)[0:3],
            "max": str(drink.maxPrice)[0:3],
            "history": drink.price_history
        }
    #print(data_set)
    #with open("output.txt", "w") as f: f.write(str(data_set) + "\n\n")

    return data_set


# interval is always 0.3 percent big. It influences the size of the price change.
# EXAMPLE: interval_start=0.3; minPrice=0.6; maxPrice=1.6;
# --> interval goes from 0.3 to 0.6; deviation = 1.6 - 0.6 = 1;
# --> price_difference = ((random number between 3 and 6) / 10) * 1
# --> In this case a price change between 30 cents and 60 cents would be possible
# --> The distance between the min and max price and the interval influence the price change
def change_price(drink, interval_start, price_change):
    if interval_start >= 0.7:
        print(f'Start of interval - {interval_start} - is too high; Should be less than 0.7')
    deviation = drink.maxPrice - drink.minPrice
    interval_end = interval_start + 0.3
    old_price = drink.price
    price_difference = (random.randint(interval_start * 10, interval_end * 10) / 10) * deviation
    if price_change == PriceChange.UP:
        drink.setPrice(old_price + price_difference)
    elif price_change == PriceChange.DOWN:
        drink.setPrice(old_price - price_difference)
    # price history is updated in function "setPrice";
    # Reason: calculated price could be lower or higher than allowed i.e. maxPrice, in that case it needs to be adjusted


def randomly_change_price(drink):
    draw = random.choices(population=[1, 2],
                          weights=[drink.price_change_prob, 1 - drink.price_change_prob],
                          k=1)
    if draw[0] == 1:
        drink.price_change_prob = 0.2
        return True
    else:
        drink.price_change_prob += 0.1
        return False


def get_total_sales():
    drinks = Drink.get_allDrinks()
    total_sales = 0
    for drink in drinks:
        total_sales += drink.newOrders()
    return total_sales


def get_random_direction():
    if random.randint(0, 1) == 0:
        return PriceChange.UP
    else:
        return PriceChange.DOWN


def update_price_history(drink, old_price):
    drink.price_history.append(round(old_price, 1))


def get_price_difference(drink):
    # import ipdb; ipdb.set_trace()
    return abs(drink.price - drink.price_history[-1])


def calc_relative_part(drink_sales, total_sales):
    if drink_sales == 0:
        return 0
    else:
        return drink_sales / total_sales  # can be between 0 and 1


def above_threshold(relative_part, threshold):
    return relative_part > threshold


def get_drink_threshold():
    return drink_threshold


drink_threshold = 0.25

