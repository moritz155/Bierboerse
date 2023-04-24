import random
from drink import Drink
from calculator import calculator, increased_due_threshold
import time


def no_purchases():
    res = ''
    for j in range(10):
        for i in range(0, 100):
            res = calculator()
            if i == 0:
                sort(res)
        sort(res)


def random_purchases():
    res = ''
    purchased_counter = 0
    for i in range(0, 1000):
        res = calculator()
        drinks = Drink.get_allDrinks()
        for drink in drinks:
            rand_num = random.randint(0, 100)
            drink.newDict = {}
            # check if the random number is less than 20
            if rand_num < 50:
                # drink is purchased
                for i in range(0, random.randint(1, 3)):
                    drink.newDict[time.time()] = 1
                    purchased_counter += 1
                    drink.drinkWasPurchased += 1

        # for drink in Drink.get_allDrinks():
            # print(f'{drink.name}\'s price history is: {drink.price_history}')
    sort(res)
    amount_of_purchases_per_drink()
    purchases_per_period = purchased_counter / 1000
    print(f'In total {purchases_per_period} were purchased per round')
    global increased_due_threshold
    print(
        f'Prices were increased {increased_due_threshold} times due to high purchase.')


def amount_of_purchases_per_drink():
    drinks = Drink.get_allDrinks()
    for drink in drinks:
        print(f'{drink.name}: was purchased: {drink.drinkWasPurchased} times.')


def sort(drinks_dict):
    total_pct_change = 0
    for drink in drinks_dict:
        if 'history' in drinks_dict[drink]:
            avg_price = sum(drinks_dict[drink]['history']) / \
                len(drinks_dict[drink]['history'])
            max_price = max(drinks_dict[drink]['history'])
            orig_price = drinks_dict[drink]['history'][0]
        else:
            avg_price = drinks_dict[drink]['price']
            max_price = drinks_dict[drink]['max']
            orig_price = drinks_dict[drink]['price']
        pct_change = (avg_price - orig_price) / orig_price * 100
        # print(f"{drink} had an average price of {avg_price:.2f}, a max price of {max_price:.2f} \t| ")
        # print(f"{pct_change:.2f}% price change.")
        total_pct_change += pct_change
    total_pct_change /= len(drinks_dict)
    print(f'The total average price change was: {total_pct_change:.2f} %')


random_purchases()
