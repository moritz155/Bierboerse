import random
from drink import Drink
from calculator import calculator, get_increased_due_threshold
import time




def main():
    data_set = ''
    purchased_counter = 0
    drinks = Drink.get_allDrinks()

    # Let the simulation run for n -> 10 periods.
    for i in range(0, 10):
        data_set = calculator()
       
        for drink in drinks:
            # Randomly select a purchase number.
            rand_num = random.randint(0, 100)
            # Set to empty dict to simulate a new round
            drink.orders = {} 

            # Purchase a drink in 50% of the cases.
            if rand_num < 50:
                # Add 1..3 new drinks to the order list. 
                for i in range(0, random.randint(1, 3)):
                    drink.orders[time.time()] = 1
                    purchased_counter += 1
                    drink.drinkWasPurchased += 1

    # Provide a dictionary with the drinks and purchases. "{"Cola": 1, "Wein": 4 ...}"
    drinks_purchases = get_drinks_counter(Drink.get_allDrinks())

    # Print the analysis of the last period.
    print_results(data_set, drinks_purchases)



def print_results(data_set, drinks_purchases):
    total_pct_change = 0
    for drink in data_set:

        if 'history' in data_set[drink]:
            avg_price = sum(data_set[drink]['history']) / \
                len(data_set[drink]['history'])
            max_price = max(data_set[drink]['history'])
            orig_price = data_set[drink]['history'][0]
        else:
            avg_price = data_set[drink]['price']
            max_price = data_set[drink]['max']
            orig_price = data_set[drink]['price']

        pct_change = (avg_price - orig_price) / orig_price * 100
        total_pct_change += pct_change
     
        print(f"{drink} \t| purchased {drinks_purchases[drink]} times \t| average price of {avg_price:.2f}, a max price of {max_price:.2f} \t| {pct_change:.2f}% price change.")

    total_pct_change /= len(data_set)
    purchases_per_period = sum(drinks_purchases.values()) / 10

    print(f'The total average price change was: {total_pct_change:.2f} %')
    print(f'In total {purchases_per_period} were purchased per round')
    print(f'Prices were increased {get_increased_due_threshold()} times due to high purchase.')



def get_drinks_counter(drinks_list):
    counter_dict = {}
    for drink in drinks_list:
        counter_dict[drink.name] = drink.drinkWasPurchased
    return counter_dict




main()






##########################################################################################################################################



def no_purchases():
    res = ''
    for j in range(10):
        for i in range(0, 100):
            res = calculator()
            if i == 0:
                print_data_set(res)
        print_data_set(res)


def amount_of_purchases_per_drink():
    drinks = Drink.get_allDrinks()
    for drink in drinks:
        print(f'{drink.name}: was purchased: {drink.drinkWasPurchased} times.')


def print_data_set(data_set):
    total_pct_change = 0
    for drink in data_set:
        if 'history' in data_set[drink]:
            avg_price = sum(data_set[drink]['history']) / \
                len(data_set[drink]['history'])
            max_price = max(data_set[drink]['history'])
            orig_price = data_set[drink]['history'][0]
        else:
            avg_price = data_set[drink]['price']
            max_price = data_set[drink]['max']
            orig_price = data_set[drink]['price']
        pct_change = (avg_price - orig_price) / orig_price * 100
        # print(f"{drink} had an average price of {avg_price:.2f}, a max price of {max_price:.2f} \t| ")
        # print(f"{pct_change:.2f}% price change.")
        total_pct_change += pct_change
    total_pct_change /= len(data_set)
    print(f'The total average price change was: {total_pct_change:.2f} %')
