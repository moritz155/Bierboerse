from flask import Flask, render_template, request, jsonify
import time, json, random

class Drink:
    def __init__(self, name, init_price):  # array with one price - the starting price
        self.name = name
        self.price = init_price
        self.price_history = []  # former allPrices
        self.maxPrice = init_price * 1.4
        self.minPrice = init_price * 0.7
        self.newDict = {}  # gives every order a time; size of dict is equal to amount of orders
        self.newCounter = 0  # counter of orders in a period
        self.price_was_changed = 0  # counts the times the price is changed

    def get_allDrinks():
        return allDrinks

    #def addPrice(self, newPrice):
     #   self.price_history.append(newPrice)

    def update_recentlyChangedPrices(self):
        for drink in recentlyChangedPrices:
            if self == drink:
                recentlyChangedPrices.remove(drink)
                recentlyChangedPrices.append(drink)
                return
        recentlyChangedPrices.append(self)  # if price of drink wasnt changed yet

    # def addNewRandomPrice(self, price_increase, change_price):
    #     if change_price:
    #         self.price_was_changed = self.price_was_changed + 1
    #         multiplicator = random.randint(0, 5)  # max -50 cent
    #         oldPrice = self.price_history[-1]
    #         if price_increase:
    #             newPrice = oldPrice + (multiplicator * 0.1)  # get a random lower price
    #         elif not price_increase:
    #             newPrice = oldPrice - (multiplicator * 0.1)  # get a random higher price
    #         if self.minPrice < newPrice < self.maxPrice:
    #             self.addPrice(newPrice)
    #         else:
    #             self.addPrice(oldPrice)
    #         self.update_recentlyChangedPrices()
    #     else:
    #         self.addPrice(self.price_history[-1])

    def newOrders(self):
        current_time = time.time()
        listOfItemsToRemove = []
        self.newCounter = 0  # counts number of times this drink was bought in the period
        for element_time in self.newDict:
            if current_time - element_time > iteration_interval * 10:
                listOfItemsToRemove.append(element_time)  # items from last period -- not important anymore
            else:
                self.newCounter = self.newCounter + 1
        for i in listOfItemsToRemove:
            del self.newDict[i]  # cleanup newDict again
        return self.newCounter




# old_table_data = []
# updated_last_time = time.time()
# current_time: float = time.time()
# start_time = float(time.time())
iteration_interval = 5  # in seconds
# data = {}
# drink_threshold = 0.25
# customColorSet = ["#FF0000",
#                   "#FF8F00",
#                   "#4BF70B",
#                   "#0BF7C5",
#                   "#0B0FF7",
#                   "#C90BF7",
#                   "#F70B6F"
#                   ]

allDrinks = [
Drink("Gösser", 2.10), 
Drink("Gustl", 2.0), 
Drink("Radler", 2.3), 
Drink("Tyskie", 2.2),
Drink("Cola", 1.9),
Drink("Wein", 1.7),
Drink("Luft", 1.5)]
# beers_names = ["Gösser","Gustl","Radler","Tyskie","Cola","Wein","Luft"]
# clock_for_analysis = time.time()
recentlyChangedPrices = []
