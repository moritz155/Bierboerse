import requests
import json
from drink import Drink
from calculator import calculator


class Simulation:  # a simulation consist of drinks

    def simulate_purchase(self):
        '''should simulate a user input'''
   
   
    
def output():
    for i in range(0,10):
        res = calculator()
        if i == 9:
            sort(res)


def sort(drinks_dict):
    '''This method receives a dictionary like 
    {'Gösser': {'name': 'Gösser', 'price': 2.0, 'price_diff': 0.0, 'min': '1.4', 'max': '2.900000003, 2.006, 2.0, 2.0, 2.0]}, 'Gustl': {'name': 'Gustl', 'price': 2.6, 'price_diff':99999999904, 'min': '1.6', 'max': '3.2', 'history': [2.3, 2.622, 2.6, 2.6, 2.6, 2.6, 3.083, 3.1, 3.1, 2.617]}, 'Tyskie': {'name': 'Tyskie', 'price': 2.2, 'price_diff': 0.0, 'min': '1.5', 'max': '3.0', 'history': [2.2, 2.8160000000000003, 2.8, 2.8, 2.8, 2.8, 2.1839999999999997, 2.2, 2.2, 2.2]}, 'Cola': {'name': 'Cola', 'price': 2.0, 'price_diff': 0.0, 'min': '1.3', 'max': '2.6', 'history': [1.501, 1.5, 1.5, 2.032, 2.0, 2.0, 2.532, 2.5, 1.968, 2.0]}, 'Wein': {'name': 'Wein', 'price': 1.8, 'price_diff': 0.0, 'min': '1.1', 'max': '2.3', 'history': [2.057, 2.1, 2.1, 1.624, 1.6, 1.6, 1.6, 1.6, 1.838, 1.8]}, 'Luft': {'name': 'Luft', 'price': 1.1, 'price_diff': 0.020000000000000018, 'min': '1.0', 'max': '2.0', 'history': [1.5, 1.5, 1.5, 1.5, 1.29, 1.3, 1.3, 1.3, 1.51, 1.08]}} 
    and should return a single string output like:
    Cola had an average price of x and a max price of Y. 
    '''
    result = ''
    for drink in drinks_dict:
        if 'history' in drinks_dict[drink]:
            avg_price = sum(drinks_dict[drink]['history']) / len(drinks_dict[drink]['history'])
            max_price = max(drinks_dict[drink]['history'])
        else:
            avg_price = drinks_dict[drink]['price']
            max_price = drinks_dict[drink]['max']
        result += f"{drink} had an average price of {avg_price:.2f} and a max price of {max_price:.2f}.\n"
    
    print(result)

output()