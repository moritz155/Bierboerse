import time
import random
from unittest.mock import MagicMock
from drink import Drink
from calculator import calculator

# 1. Setup Mock Time
# We need to control time to make the filtering in drink.py work without waiting 15 minutes.
current_sim_time = 1000000.0 # Arbitrary start time
def mock_time():
    return current_sim_time

# Monkeypatch time.time
time.time = MagicMock(side_effect=mock_time)

def run_simulation():
    global current_sim_time
    print("--- STARTING PARTY SIMULATION ---")
    
    # Reset Drinks
    drinks = Drink.get_allDrinks()
    for d in drinks:
        d.price = 1.0 # Reset baseline
        d.price_history = [1.0]
        d.orders = {}
    
    target_drink = drinks[0] # "Sterni"
    print(f"Target Drink: {target_drink.name} (Starts at {target_drink.price}€)")

    # SIMULATION PARAMETERS
    ROUNDS = 30
    SECONDS_PER_ROUND = 90 # Match the 90s interval
    
    # SCENARIO:
    # Rounds 0-9:  Boring party (random sparse orders)
    # Rounds 10-12: RUSH HOUR! (Everyone buys Sterni)
    # Rounds 13-30: Cooldown
    
    history_log = []

    with open('sim_result.txt', 'w') as f:
        for r in range(ROUNDS):
            # 1. Advance Time
            current_sim_time += SECONDS_PER_ROUND
            
            # 2. Place Orders
            if 10 <= r <= 15:
                # EVEN DEMAND: Buy 1 of EACH drink per round to simulate busy but balanced bar
                # print(f"[Round {r}] !!! BUSY BAR (EVEN) !!!")
                for i, d in enumerate(drinks):
                    # Jitter the time unique to each drink/iteration
                    d.orders[current_sim_time + (i * 0.01)] = 1
            else:
                # Random background noise
                for d in drinks:
                    if random.random() < 0.3: # 30% chance someone buys a drink
                        d.orders[current_sim_time] = 1
            
            # 3. Calculate New Prices
            data = calculator()
            
            # 4. Log Result for ALL drinks
            log_entry = f"Round {r:02d}: "
            round_prices = {}
            for d in drinks:
                price = data[d.name]['price']
                round_prices[d.name] = price
                log_entry += f"[{d.name}: {price:.2f}] "
            
            history_log.append(round_prices)
            f.write(log_entry + "\n")

        f.write("\n--- SIMULATION FINISHED ---\n")
        f.write("Last Round Prices:\n")
        for name, price in history_log[-1].items():
            f.write(f"{name}: {price:.2f}\n")
            
        # change = history_log[-1] - history_log[0]
        # f.write(f"Final Change: {change:+.2f}\n")

if __name__ == "__main__":
    run_simulation()
