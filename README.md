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

