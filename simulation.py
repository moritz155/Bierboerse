import random
from drink import Drink
from calculator import calculator


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
    for j in range(10):
        for i in range(0, 100):
            res = calculator()
            if i == 0:
                sort(res)
            drinks = Drink.get_allDrinks()
            for drink in drinks:
                rand_num = random.randint(0, 99)
                 # check if the random number is less than 20
                if rand_num < 1:
                    # drink is purchased
                    drink.newCounter += 1
                    print(f'{drink.name} was purchased.')
        #for drink in Drink.get_allDrinks():
            #print(f'{drink.name}\'s price history is: {drink.price_history}')
        sort(res)


def sort(drinks_dict):
    total_pct_change = 0
    for drink in drinks_dict:
        if 'history' in drinks_dict[drink]:
            avg_price = sum(drinks_dict[drink]['history']) / len(drinks_dict[drink]['history'])
            max_price = max(drinks_dict[drink]['history'])
            orig_price = drinks_dict[drink]['history'][0]
        else:
            avg_price = drinks_dict[drink]['price']
            max_price = drinks_dict[drink]['max']
            orig_price = drinks_dict[drink]['price']
        pct_change = (avg_price - orig_price) / orig_price * 100
        #print(f"{drink} had an average price of {avg_price:.2f}, a max price of {max_price:.2f} \t| ")
        #print(f"{pct_change:.2f}% price change.")
        total_pct_change += pct_change
    total_pct_change /= len(drinks_dict)
    print(f'The total average price change was: {total_pct_change:.2f} %')


no_purchases()
