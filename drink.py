import time



class Drink:
    def __init__(self, name, init_price):  # array with one price - the starting price
        self.name = name
        self.price = init_price
        self.price_history = []  # former allPrices
        self.maxPrice = init_price * 1.4
        self.minPrice = init_price * 0.7
        self.orders = {}  # gives every order a time; size of dict is equal to amount of orders
        self.period_order_count = 0  # counter of orders in a period
        self.price_was_changed = 0  # counts the times the price is changed
        self.price_change_prob = 0.2
        self.drinkWasPurchased = 0


    def setPrice(self, price):
        newPrice = 0
        if price >= self.maxPrice:
            newPrice = self.maxPrice
        elif price <= self.minPrice:
            newPrice = self.minPrice
        else:
            newPrice = price
        self.price = round(newPrice, 1)
        self.price_history.append(newPrice)


    def update_recentlyChangedPrices(self):
        for drink in recentlyChangedPrices:
            if self == drink:
                recentlyChangedPrices.remove(drink)
                recentlyChangedPrices.append(drink)
                return
        # if price of drink wasnt changed yet
        recentlyChangedPrices.append(self)


    def newOrders(self):
        """ Looks a every order inside self.orders and looks for orders performed in the current period.
        
                returns self.period_order_count -> number of drinks purchased in the current period.
                
        """
        current_time = time.time()
        listOfItemsToRemove = []
        self.period_order_count = 0  # counts number of times this drink was bought in the period

        for element_time in self.orders:
            if current_time - element_time <= iteration_interval * 10:
                self.period_order_count += 1
                self.drinkWasPurchased += 1
        #     if current_time - element_time > iteration_interval * 10:
        #         # items from last period -- not important anymore
        #         listOfItemsToRemove.append(element_time)
        #     else:
        #         self.period_order_count = self.period_order_count + 1
        #         self.drinkWasPurchased += 1
        # for i in listOfItemsToRemove:
        #     del self.orders[i]  # cleanup orders (newDict) again
        return self.period_order_count

    @staticmethod
    def get_allDrinks():
        return allDrinks



iteration_interval = 90  # in seconds

allDrinks = [
    Drink("Bier", 0.7),
    Drink("Softdrink", 0.5),
    Drink("Amaretto", 0.3),
    Drink("Spezi", 0.2),
    Drink("Weißwein", 0.7),
    Drink("Rotwein", 0.6),
    Drink("Diesel", 0.5),
    Drink("ColaRum", 0.5),
    Drink("Kräuterlikör", 0.5),
    Drink("Wodka", 0.5),





]

recentlyChangedPrices = []


# customColorSet = ["#FF0000",
#                   "#FF8F00",
#                   "#4BF70B",
#                   "#0BF7C5",
#                   "#0B0FF7",
#                   "#C90BF7",
#                   "#F70B6F"
#                   ]


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