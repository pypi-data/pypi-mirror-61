Creates a Weather object getting an apikey as input
and either a city name or lat and lon coordinates.

Package use example:

# Create a weather object using a city name:
# The api key below is not guranateed to work.
# Get your own apikey from https://openweathermap.org
# And wait a couple of hours for the apikey to be activated

>>> weather1 = Weather(apikey = "26631f0f41b95fb9f5ac0df9a8f43c92", city = "Madrid")

# Using latitude and longitude coordinates
>>> weather2 = Weather(apikey = "26631f0f41b95fb9f5ac0df9a8f43c92", lat = 41.1, lon = -4.1)

# Get complete weather data for the next 12 hours:
>>> weather1.next_12h()

# Simplified data for the next 12 hours:
>>> weather1.next12h_simplified()