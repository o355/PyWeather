# PyWeather Indev
# (c) 2017 o355, GNU GPL 3.0.
# Powered by Dark Sky (darksky.net)

import requests
from datetime import datetime
from time import strftime
from geopy.geocoders import Nominatim
geolocator = Nominatim()
from forecastiopy import *

# For the alphas, units default to US. Eventually a system will be introduced in which a setup is necessary/not necessary.

print("Welcome. Please enter the name of a city you'd like to view the current weather for.")
cityname = input("Input here: ")
print("Great! I'm baking your forecast! It's a piece of cake to bake a pretty forecast!")

locatecity = geolocator.geocode(cityname)
citycoord = [locatecity.latitude, locatecity.longitude]

f = ForecastIO.ForecastIO(apikey,
                          units=ForecastIO.ForecastIO.UNITS_US,
                          lang=ForecastIO.ForecastIO.LANG_ENGLISH,
                          latitude=citycoord[0],
                          longitude=citycoord[1])

if f.has_currently() is True:
    cfc = FIOCurrently.FIOCurrently(f)
    tempconv = datetime.fromtimestamp(int(cfc.time))
    print(cfc.time)
    ftime = tempconv.strftime('%B %e at %H:%M:%S')
    print("The latest forecast as of " + ftime)
    print(cfc.summary)
                                            
