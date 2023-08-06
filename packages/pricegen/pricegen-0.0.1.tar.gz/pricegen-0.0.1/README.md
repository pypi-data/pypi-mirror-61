# pricegen

This utility helps simulate statistically randomized series of prices, based on the models below:

* Geometric Brownian motion
* Mean reversion (optional)

## Generating a next price

```
from pricegen import random_price

current_price = 100
next_price = random_price(current_price, sigma=0.20)
```

## Generating a series of prices

```
from pricegen import random_price, generate_prices

initial_price = 100

# Daily prices over a year (252 trading days)
price = initial_price
for _ in range(252):
    price = random_price(price, sigma=0.20, time=1.0/252)
    print(price)

# Or equivalently:
for price in generate_prices(252, initial_price, sigma=0.20, time=1.0/252):
    print(price)
```

## Volatility and time interval

```
# These two calls are roughly equivalent

# Case 1:
random_price(price, sigma=0.20, time=1.0/252)
# Annual volatility: 20%
# Time interval: (1.0 / 252) year

# Case 2:
random_price(price, sigma=0.20/math.sqrt(252)) # time == 1.0 by default
# Daily volatility: 20% / sqrt(252)
# Time interval: 1.0 day

# Note:
# "time" represents the time interval relative to 1.0.
# "sigma" is interpreted as volatility for time == 1.0.
# Internally, there is no assumption about the unit of time (year/month/day).
```

## Mean reversion

```
from pricegen import random_price

initial_price = 100

# Daily prices over a year (252 trading days)
price = initial_price
for _ in range(252):
    price = random_price(price, sigma=0.20, time=1.0/252, mean=initial_price)
    print(price)

# Mean reversion helps prevent the price from becoming too high or too low
# by attracting the price to a targe while maintaining a specific volatility.
```

## Using a custom Random class

```
from pricegen import PriceGenerator

generator = PriceGenerator(random=custom_random)
# custom_random needs to have .gauss() method

generator.random_price(100, 0.20)
```

## Ad-hoc random noise


```
from pricegen import random_price

random_price(100, 0.20, noise=custom_gauss(0.0, 1.0))
```
