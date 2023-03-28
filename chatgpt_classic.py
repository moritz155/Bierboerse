import random

# Define the initial stock of beers
initial_stock = 1000

# Define the minimum and maximum prices for a beer
min_price = 1.0
max_price = 5.0

# Define a function to calculate the current price of a beer based on the current stock level
def get_price(stock):
    price_range = max_price - min_price
    price_per_unit = price_range / initial_stock
    price = max(min_price, max_price - (stock * price_per_unit))
    return round(price, 2)

# Define a function to simulate a user buying beers
def buy_beers(stock):
    num_beers = int(input("How many beers would you like to buy? "))
    if num_beers > stock:
        print("Sorry, we don't have enough beers in stock.")
    else:
        price_per_beer = get_price(stock)
        total_price = round(num_beers * price_per_beer, 2)
        print(f"That will be {total_price} dollars, please.")
        stock -= num_beers
        print(f"There are now {stock} beers left in stock.")
    return stock

# Define a function to display the current stock developments
def display_stock(stock):
    print(f"There are currently {stock} beers in stock.")
    price = get_price(stock)
    print(f"The current price of a beer is {price} dollars.")

# Define the main function to run the simulation
def main():
    stock = initial_stock
    while True:
        print("\nWelcome to the beer stock market!")
        print("1. Buy beers")
        print("2. Display current stock developments")
        print("3. Exit")
        choice = int(input("Please choose an option: "))
        if choice == 1:
            stock = buy_beers(stock)
        elif choice == 2:
            display_stock(stock)
        elif choice == 3:
            print("Thank you for using the beer stock market!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
