# Bierbörse

## Components: 
+ frontends (currently two)
+ a view function for the frontends to get the data 
+ calculator function 
    + calculates the current prices (and several other stuff) for each drink
+ backend 

## Interesting facts
+ the views update their data in an interval of `normal_interval` / 5
  + the `normal_interval` is the interval in which new data is calculated
  + by requesting new data five times more often than there actually is new data the time in which the views have different kinds of data is minimized

## Logic of Calculation
+ With help of `drink.newOrders()` the sum of all orders are calculated
+ relative of each drink in this period is calculated
+ if relative part > 25 % --> price is increased
+ price first drink that was not boùght in period is decreased
+ price of another drink is decreased (not totally true, needs to be checked again)


## Thoughts
+ Price generation overhaul
+ probability of direction of price change; amount of price change should relate to share in sales over the last iterations
+ have a random amount of drinks 5 - 30 % change each iteration
