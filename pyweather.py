# PyWeather 0.0 -> 0.1 Beta
# (c) 2017 o355, GNU GPL 3.0.
# Powered by Wunderground

# ===========================
#   A few quick notes:
# 1. The internal code is not organized, and it's meant to stay that way.
# I usually design programs with the fact that I'll clean up code, and use
# proper naming conventions/design conventions once the thing works.
# So, for now. Lines of code/comments will be 120+ characters long. Sorry. 
# 2. This program is 10% complete, meaning it's FAR from what it can do.
# 3. There is no setup.py file. Get the API key on your own, and download
# necessary modules through PIP.
# 4. 
import urllib.request
import json
from colorama import init, Fore, Style
import codecs
from geopy.geocoders import Nominatim
from datetime import datetime
from datetime import timedelta
import geocoder
geolocator = Nominatim()
apikey_load = open('apikey.txt')
apikey = apikey_load.read()
print(datetime.now())

print("Welcome to PyWeather - Powered by Wunderground.")
print("Please enter a location to get weather information for.")
locinput = input("Input here: ")
print("Sweet! Getting your weather.")

# Error handling will come in the very near future. Because apparently geocoders are blocked in some places *cough* my school *cough*
location = geolocator.geocode(locinput)
latstr = str(location.latitude)
lonstr = str(location.longitude)
loccoords = [latstr, lonstr]

# Declare the API url, and use the workaround to get the JSON parsed
currenturl = 'http://api.wunderground.com/api/' + apikey + '/geolookup/conditions/q/' + latstr + "," + lonstr + '.json'
f10dayurl = 'http://api.wunderground.com/api/' + apikey + '/geolookup/forecast10day/q/' + latstr + "," + lonstr + '.json'


# Due to Python, we have to get the UTF-8 reader to properly parse the JSON we got.
reader = codecs.getreader("utf-8")
# We now fetch the JSON file to be parsed, using urllib.request
summaryJSON = urllib.request.urlopen(currenturl)
forecastJSON = urllib.request.urlopen(f10dayurl)
# And we parse the json using json.load, with the reader option (to use UTF-8)
current_json = json.load(reader(summaryJSON))
forecast_json = json.load(reader(forecastJSON))

location2 = geocoder.google([latstr, lonstr], method='reverse')

forecast_Day1Temp = forecast_json['forecast']['forecastday'][1]['fahrenheit']
print(forecast_Day1Temp)


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
if heatindexdata == True:
    print(Fore.CYAN + "Current heat index: " + Fore.YELLOW + summary_heatindexfstr + "°F (" + summary_heatindexcstr + "°C)")
if windchilldata == True:
    print(Fore.CYAN + "Current wind chill: " + Fore.YELLOW + summary_windchillfstr + "°F (" + summary_windchillcstr + "°C)")

                            
