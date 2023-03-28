import random
from drink import Drink
from calculator import calculator


def output():
    res = ''
    for i in range(0, 50):
        res = calculator()
        if i == 0:
            sort(res)
        drinks = Drink.get_allDrinks()
        # for drink in drinks:
        #     rand_num = random.randint(0, 99)
        #     # check if the random number is less than 20
        #     if rand_num < 1:
        #         # drink is purchased
        #         drink.newCounter += 1
        #         print(f'{drink.name} was purchased.')
    # for drink in Drink.get_allDrinks():
    #     print(f'{drink.name}\'s price history is: {drink.price_history}')
    sort(res)


def sort(drinks_dict):
    result = ''
    for drink in drinks_dict:
        if 'history' in drinks_dict[drink]:
            avg_price = sum(drinks_dict[drink]['history']) / len(drinks_dict[drink]['history'])
            max_price = max(drinks_dict[drink]['history'])
        else:
            avg_price = drinks_dict[drink]['price']
            max_price = drinks_dict[drink]['max']
        result += f'{drink} had an average price of {avg_price:.2f} and a max price of {max_price:.2f}.\n'

    print(result)


output()
