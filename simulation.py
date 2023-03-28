from flask import Flask
import requests
import json
import random
import time
from drink import Drink


class Simulation:  # a simulation consist of drinks
    def __init__(self, drink: Drink):  # array with one price - the starting price
        self.drink = drink
        self.maxReachedPrice = None
        self.minReachedPrice = None
        self.purchased = 0

    def simulate_purchase(self):
        # create json object
        data = {'name': self.drink.name}
        json_data = json.dumps(data)

        # increase purchased counter
        self.purchased += 1

        # send POST request
        requests.post('/ordered_Drink/', data=json_data)


def whatever():
    drinks = Drink.get_allDrinks()

