# PyWeather Indev
# (c) 2017 o355, GNU GPL 3.0.
# Powered by Wunderground

# ===========================
#   A few quick notes:
# 1. The internal code is not organized, and it's meant to stay that way.
# I usually design programs with the fact that I'll clean up code, and use
# proper naming conventions/design conventions once the thing works.
# So, for now. Lines of code/comments will be 79+ characters long. Sorry. 
# 2. This program is 10% complete, meaning it's FAR from what it can do.
# 3. There is no setup.py file. Get the API key on your own, and download
# necessary modules through PIP.
# 4. Progress will be slow and steady with PyWeather. Trust me.

verbosity = True
if verbosity == True:
    import logging
    logger = logging.getLogger('pyweather_0.1')
    logger.setLevel(logging.INFO)
    logformat = '%(asctime)s | %(levelname)s | %(message)s'
    logging.basicConfig(format=logformat)

import urllib.request
import socket
import sys
import json
from colorama import init, Fore, Style
import codecs
from geopy.geocoders import Nominatim
from datetime import datetime
from datetime import timedelta
import geocoder
from distutils.log import set_verbosity
geolocator = Nominatim()
if verbosity == True:
    logger.info("Begin API keyload...")
apikey_load = open('storage//apikey.txt')
if verbosity == True:
    logger.info("apikey_load = %s" % apikey_load)
apikey = apikey_load.read()
if verbosity == True:
    logger.info("apikey = %s" % apikey)
print(datetime.now())

# This is the toggle for verbosity. Right now, it is. Also...
# the current implementation for verbosity sucks. It basically
# checks if verbosity is toggled, and does if verbosity, do
# this.

print("Welcome to PyWeather - Powered by Wunderground.")
print("Please enter a location to get weather information for.")
locinput = input("Input here: ")
print("Sweet! Getting your weather.")

# Error handling will come in the very near future. Because apparently geocoders are blocked in some places *cough* my school *cough*

if verbosity == True:
    logger.info("Start geolocator...")
try:
    location = geolocator.geocode(locinput)
except:
    if verbosity == True:
        logger.error("No connection to the geolocator!! Is the connection offline?")
    print("Can't connect to the geolocator. Make sure you " +
          "have an internet connection, and the geolocator is unblocked.")
    sys.exit()
if verbosity == True:
    logger.info("location = %s" % location)
try:
    latstr = str(location.latitude)
except AttributeError:
    logger.error("No lat/long was provided by the geolocator!!!")
    print("The location you entered could not be understood properly. Please try again!")
    sys.exit()
try:
    lonstr = str(location.longitude)
except AttributeError:
    logger.error("No lat/long was provided by the geolocator!!!")
    print("The location you entered could not be understood properly. Please try again!")
    sys.exit()
if verbosity == True:
    logger.info("Latstr: %s ; Lonstr: %s" % (latstr, lonstr))
loccoords = [latstr, lonstr]
if verbosity == True:
    logger.info("Loccoords: %s" % loccoords)
    logger.info("End geolocator...")
    logger.info("Start API fetch...")
# Declare the API url, and use the workaround to get the JSON parsed
currenturl = 'http://api.wunderground.com/api/' + apikey + '/geolookup/conditions/q/' + latstr + "," + lonstr + '.json'
f3dayurl = 'http://api.wunderground.com/api/' + apikey + '/geolookup/forecast/q/' + latstr + "," + lonstr + '.json'
hourlyurl = 'http://api.wunderground.com/api/' + apikey + '/geolookup/forecast/q' + latstr + "," + lonstr + '.json'
if verbosity == True:
    logger.info("currenturl: %s" % currenturl)
    logger.info("f3dayurl: %s" % currenturl)
    logger.info("hourlyurl: %s" % currenturl)
    logger.info("End API fetch...")
    logger.info("Start initial parse...")

# Due to Python, we have to get the UTF-8 reader to properly parse the JSON we got.
reader = codecs.getreader("utf-8")
if verbosity == True:
    logger.info("reader: %s" % reader)
# We now fetch the JSON file to be parsed, using urllib.request
try:
    summaryJSON = urllib.request.urlopen(currenturl)
    forecastJSON = urllib.request.urlopen(f3dayurl)
    hourlyJSON = urllib.request.urlopen(hourlyurl)
    if verbosity == True:
        logger.info("summaryJSON: %s ; forecastJSON: %s ; hourlyJSON: %s" % (summaryJSON, forecastJSON, hourlyJSON))
except:
    if verbosity == True:
        logger.error("No connection to the API!! Is the connection offline?")
    print("Can't connect to the API. Make sure that Wunderground's API " +
          "is unblocked, and the internet is online.")
    sys.exit()
# And we parse the json using json.load, with the reader option (to use UTF-8)
current_json = json.load(reader(summaryJSON))
if verbosity == True:
    logger.info("current_json: %s" % current_json)
forecast3_json = json.load(reader(forecastJSON))
if verbosity == True:
    logger.info("forecast3_json: %s" % forecast3_json)
hourly_json = json.load(reader(hourlyJSON))
if verbosity == True:
    logger.info("hourly_json: %s" % hourly_json)
    logger.info("End initial parse...")
    logger.info("Start 2nd geolocator...")
try:
    location2 = geocoder.google([latstr, lonstr], method='reverse')
except:
    if verbosity == True:
        logger.error("No connection to Google's Geolocator!! Is the connection offline?")
    print("Can't connect to Google's Geolocator. Make sure that Google's " +
          "Geolocator is unblocked, and your internet is online.")
    sys.exit()
        
if verbosity == True:
    logger.info("location2: %s ; Location2.city: %s ; Location2.state: %s" % (location2, location2.city, location2.state))
    logger.info("End 2nd geolocator...")



# Parsing current weather conditions for the summary. Caching will come so the API is hit once for the summary/detailed info.
# External parsing may be added once this list gets INSANELY long. Efficiency isn't too much of an issue.

summary_full = current_json['current_observation']['display_location']['full']
summary_overall = current_json['current_observation']['weather']
summary_lastupdated = current_json['current_observation']['observation_time']
# While made for the US, metric units will also be tagged along.
summary_tempf = str(current_json['current_observation']['temp_f'])
summary_tempc = str(current_json['current_observation']['temp_c'])
# Since parsing the json spits out a float as the summary, a conversion to string is
# necessary to properly display it in the summary.
summary_dewpointf = current_json['current_observation']
summary_humidity = str(current_json['current_observation']['relative_humidity'])
summary_winddir = current_json['current_observation']['wind_dir']
summary_winddirstr = str(summary_winddir)
summary_windmph = current_json['current_observation']['wind_mph']
summary_windmphstr = str(summary_windmph)
summary_windkph = current_json['current_observation']['wind_kph']
summary_windkphstr = str(summary_windkph)
# Since some PWS stations on WU don't have a wind meter, this method will check if we should display wind data.
# WU lists the MPH at -9999 if there is no wind data.
# This method is probably reliable, but I need to see if it'll work by testing it work PWS stations around my area.
windcheck = float(summary_windmph)
windcheck2 = float(summary_windkph)
if windcheck == -9999:
    winddata = False
elif windcheck2 == -9999:
    winddata = False
else:
    winddata = True
summary_heatindexf = current_json['current_observation']['heat_index_f']
summary_heatindexfstr = str(summary_heatindexf)
summary_heatindexc = current_json['current_observation']['heat_index_c']
summary_heatindexcstr = str(summary_heatindexc)
# Checking for a heat index is easier, Wunderground spits out "NA" if there isn't a head index/wind chill.
if summary_heatindexf == "NA":
    heatindexdata = False
else:
    heatindexdata = True
summary_windchillf = current_json['current_observation']['windchill_f']
summary_windchillfstr = str(summary_windchillf)
summary_windchillc = current_json['current_observation']['windchill_c']
summary_windchillcstr = str(summary_windchillc)
if summary_windchillf == "NA":
    windchilldata = False
else:
    windchilldata = True

# -- 10 Day Forecast Data --




# Since normal users have the anvil developer plan, we can actually get a LOT of weather information.
print("Reading the skies...")
init()
# We parse any alerts here.

# And the summary gets spitted out here!

# Entering city names that have odd characters will
print(Style.BRIGHT + Fore.CYAN + "Here's the weather for: " + Fore.YELLOW + location2.city + ", " + location2.state)
print(Fore.YELLOW + summary_lastupdated)
print("")
print(Fore.YELLOW + "Currently:")
print(Fore.CYAN + "Current conditions: " + Fore.YELLOW + summary_overall)
print(Fore.CYAN + "Current temperature: " + Fore.YELLOW + summary_tempf + "°F (" + summary_tempc + "°C)")
# We're using the winddata variable to check if we should give an error for wind data, or not at all print heat index/wind chill data.
if winddata == True:
    print(Fore.CYAN + "Current wind: " + Fore.YELLOW + summary_windmphstr + " mph (" + summary_windkphstr + " kph), blowing " + summary_winddir + ".")
else:
    print(Fore.YELLOW + "Wind data is not available for this location.")
print(Fore.CYAN + "Current humidity: " + Fore.YELLOW + summary_humidity)
if heatindexdata == True:
    print(Fore.CYAN + "Current heat index: " + Fore.YELLOW + summary_heatindexfstr + "°F (" + summary_heatindexcstr + "°C)")
if windchilldata == True:
    print(Fore.CYAN + "Current wind chill: " + Fore.YELLOW + summary_windchillfstr + "°F (" + summary_windchillcstr + "°C)")

print("")
print(Fore.YELLOW + "The hourly forecast:")

# for hour in hourly_json['hourly_forecast']['FCTTIME']['hour']:

print(Fore.YELLOW + "For the next few days:")

# Iterations are what will have to happen for now...
for day in forecast3_json['forecast']['simpleforecast']['forecastday']:
    forecast3_weekday = day['date']['weekday']
    forecast3_month = str(day['date']['month'])
    forecast3_day = str(day['date']['day'])
    forecast3_highf = str(day['high']['fahrenheit'])
    forecast3_highc = str(day['high']['celsius'])
    forecast3_lowf = str(day['low']['fahrenheit'])
    forecast3_lowc = str(day['low']['celsius'])
    forecast3_conditions = day['conditions']
    print(Fore.CYAN + forecast3_weekday + ", " + forecast3_month + "/" + forecast3_day + ": " + Fore.YELLOW 
          + forecast3_conditions + " with a high of " + forecast3_highf + "°F (" +
          forecast3_highc + "°C), and a low of " + forecast3_lowf + "°F (" +
          forecast3_lowc + "°C).")


                            
