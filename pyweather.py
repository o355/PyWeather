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

# Verbosity works like this (for now)
# Turn on verbosity for, well, verbosity! Double verbosity outputs extra
# info, but for double verbosity, you need verbosity to be on.

verbosity = True
doubleverbosity = False
if verbosity == True:
    import logging
    logger = logging.getLogger('pyweather_0.1')
    logger.setLevel(logging.DEBUG)
    logformat = '%(asctime)s | %(levelname)s | %(message)s'
    logging.basicConfig(format=logformat)

import urllib.request
import sys
import json
from colorama import init, Fore, Style
import codecs
from geopy.geocoders import Nominatim
from datetime import datetime
import geocoder
geolocator = Nominatim()
if verbosity == True:
    logger.debug("Begin API keyload...")
apikey_load = open('storage//apikey.txt')
if verbosity == True:
    logger.debug("apikey_load = %s" % apikey_load)
apikey = apikey_load.read()
if verbosity == True:
    logger.debug("apikey = %s" % apikey)
print(datetime.now())

summaryHourlyIterations = 0

# This is the toggle for verbosity. Right now, it is. Also...
# the current implementation for verbosity sucks. It basically
# checks if verbosity is toggled, and does if verbosity, do
# this.

print("Welcome to PyWeather - Powered by Wunderground.")
print("Please enter a location to get weather information for.")
locinput = input("Input here: ")
print("Sweet! Getting your weather!")

# Error handling will come in the very near future. Because apparently geocoders are blocked in some places *cough* my school *cough*

if verbosity == True:
    logger.debug("Start geolocator...")
try:
    location = geolocator.geocode(locinput)
except:
    if verbosity == True:
        logger.error("No connection to the geolocator! Is the connection offline?")
    print("Can't connect to the geolocator. Make sure you " +
          "have an internet connection, and the geolocator is unblocked.")
    sys.exit()
if verbosity == True:
    logger.debug("location = %s" % location)
try:
    latstr = str(location.latitude)
except AttributeError:
    logger.error("No lat/long was provided by the geolocator! Invalid location?")
    print("The location you entered could not be understood properly. Please try again!")
    sys.exit()
try:
    lonstr = str(location.longitude)
except AttributeError:
    logger.error("No lat/long was provided by the geolocator! Invalid location?")
    print("The location you entered could not be understood properly. Please try again!")
    sys.exit()
if verbosity == True:
    logger.debug("Latstr: %s ; Lonstr: %s" % (latstr, lonstr))
loccoords = [latstr, lonstr]
if verbosity == True:
    logger.debug("Loccoords: %s" % loccoords)
    logger.info("End geolocator...")
    logger.info("Start API var declare...")
# Declare the API url, and use the workaround to get the JSON parsed
currenturl = 'http://api.wunderground.com/api/' + apikey + '/geolookup/conditions/q/' + latstr + "," + lonstr + '.json'
f3dayurl = 'http://api.wunderground.com/api/' + apikey + '/geolookup/forecast/q/' + latstr + "," + lonstr + '.json'
hourlyurl = 'http://api.wunderground.com/api/' + apikey + '/geolookup/hourly/q/' + latstr + "," + lonstr + '.json'
if verbosity == True:
    logger.debug("currenturl: %s" % currenturl)
    logger.debug("f3dayurl: %s" % currenturl)
    logger.debug("hourlyurl: %s" % currenturl)
    logger.info("End API var declare...")
    logger.info("Start codec change...")

# Due to Python, we have to get the UTF-8 reader to properly parse the JSON we got.
reader = codecs.getreader("utf-8")
if verbosity == True:
    logger.debug("reader: %s" % reader)
    logger.info("End codec change...")
    logger.info("Start API fetch...")
    
# We now fetch the JSON file to be parsed, using urllib.request
try:
    summaryJSON = urllib.request.urlopen(currenturl)
    if verbosity == True:
        logger.debug("Acquired summary JSON, end result: %s" % summaryJSON)
    forecastJSON = urllib.request.urlopen(f3dayurl)
    if verbosity == True:
        logger.debug("Acquired forecast 3day JSON, end result: %s" % forecastJSON)
    hourlyJSON = urllib.request.urlopen(hourlyurl)
    if verbosity == True:
        logger.debug("Acquired hourly JSON, end result: %s" % hourlyJSON)
except:
    if verbosity == True:
        logger.error("No connection to the API!! Is the connection offline?")
    print("Can't connect to the API. Make sure that Wunderground's API " +
          "is unblocked, and the internet is online.")
    sys.exit()
# And we parse the json using json.load, with the reader option (to use UTF-8)
if verbosity == True:
    logger.info("End API fetch...")
    logger.info("Start JSON load...")
current_json = json.load(reader(summaryJSON))
if doubleverbosity == True:
    logger.debug("current_json loaded with: %s" % current_json)
forecast3_json = json.load(reader(forecastJSON))
if doubleverbosity == True:
    logger.debug("forecast3_json loaded with: %s" % forecast3_json)
hourly_json = json.load(reader(hourlyJSON))
if doubleverbosity == True:
    logger.debug("hourly_json loaded with: %s" % hourly_json)
if verbosity == True:
    logger.info("3 JSONs loaded...")
    logger.info("Start 2nd geocoder...")


try:
    location2 = geocoder.google([latstr, lonstr], method='reverse')
except:
    if verbosity == True:
        logger.error("No connection to Google's Geolocator!! Is the connection offline?")
    print("Can't connect to Google's Geolocator. Make sure that Google's " +
          "Geolocator is unblocked, and your internet is online.")
    sys.exit()
        
if verbosity == True:
    logger.debug("location2: %s ; Location2.city: %s ; Location2.state: %s" % (location2, location2.city, location2.state))
    logger.info("End 2nd geolocator...")
    logger.info("Start parsing...")



# Parsing current weather conditions for the summary. Caching will come so the API is hit once for the summary/detailed debug.
# External parsing may be added once this list gets INSANELY long. Efficiency isn't too much of an issue.

summary_overall = current_json['current_observation']['weather']
summary_lastupdated = current_json['current_observation']['observation_time']
if verbosity == True:
    logger.debug("summary_overall: %s ; summary_lastupdated: %s" % (summary_overall, summary_lastupdated))
    
# While made for the US, metric units will also be tagged along.
summary_tempf = str(current_json['current_observation']['temp_f'])
summary_tempc = str(current_json['current_observation']['temp_c'])
# Since parsing the json spits out a float as the summary, a conversion to string is
# necessary to properly display it in the summary.
# summary_dewpointf = current_json['current_observation']
summary_humidity = str(current_json['current_observation']['relative_humidity'])
if verbosity == True:
    logger.debug("summary_tempf: %s ; summary_tempc: %s ; summary_humidity: %s" % (summary_tempf, summary_tempc, summary_humidity))
summary_winddir = current_json['current_observation']['wind_dir']
summary_windmph = current_json['current_observation']['wind_mph']
summary_windmphstr = str(summary_windmph)
if verbosity == True:
    logger.debug("summary_winddir: %s ; summary_windmph: %s ; summary_windmphstr: %s" % (summary_winddir, summary_windmph, summary_windmphstr))
summary_windkph = current_json['current_observation']['wind_kph']
summary_windkphstr = str(summary_windkph)
if verbosity == True:
    logger.debug("summary_windkph: %s ; summary_windkphstr: %s" % (summary_windkph, summary_windkphstr))
# Since some PWS stations on WU don't have a wind meter, this method will check if we should display wind data.
# WU lists the MPH at -9999 if there is no wind data.
# This method is probably reliable, but I need to see if it'll work by testing it work PWS stations around my area.
windcheck = float(summary_windmph)
windcheck2 = float(summary_windkph)
if verbosity == True:
    logger.debug("windcheck: %s ; windcheck2: %s" % (windcheck, windcheck2))
if windcheck == -9999:
    winddata = False
    if verbosity == True:
        logger.warn("No wind data available!")
elif windcheck2 == -9999:
    winddata = False
    if verbosity == True:
        logger.warn("No wind data available!")
else:
    winddata = True
    if verbosity == True:
        logger.info("Wind data is available.")
summary_heatindexf = current_json['current_observation']['heat_index_f']
summary_heatindexfstr = str(summary_heatindexf)
summary_heatindexc = current_json['current_observation']['heat_index_c']
summary_heatindexcstr = str(summary_heatindexc)
if verbosity == True:
    logger.debug("summary_heatindexf: %s ; summary_heatindexfstr: %s ; summary_heatindexc: %s ; summary_heatindexcstr: %s" % (summary_heatindexf, summary_heatindexfstr, summary_heatindexc, summary_heatindexcstr))
# Checking for a heat index is easier, Wunderground spits out "NA" if there isn't a head index/wind chill.
if summary_heatindexf == "NA":
    heatindexdata = False
    if verbosity == True:
        logger.warn("No heat index data available!")
else:
    heatindexdata = True
    if verbosity == True:
        logger.info("Heat index data is available.")
summary_windchillf = current_json['current_observation']['windchill_f']
summary_windchillfstr = str(summary_windchillf)
summary_windchillc = current_json['current_observation']['windchill_c']
summary_windchillcstr = str(summary_windchillc)
if verbosity == True:
    logger.debug("summary_windchillf: %s ; summary_windchillfstr: %s ; summary_windchillc: %s ; summary_windchillcstr: %s" % (summary_windchillf, summary_windchillfstr, summary_windchillc, summary_windchillcstr))
if summary_windchillf == "NA":
    windchilldata = False
    if verbosity == True:
        logger.warn("No wind chill data available!")
else:
    windchilldata = True
    if verbosity == True:
        logger.info("Wind chill data available.")


# Since normal users have the anvil developer plan, we can actually get a LOT of weather information.
if verbosity == True:
    logger.info("Initalize color...")
init()

if verbosity == True:
    logger.info("Printing current conditions...")
print(Style.BRIGHT + Fore.CYAN + "Here's the weather for: " + Fore.YELLOW + location2.city + ", " + location2.state)
print(Fore.YELLOW + summary_lastupdated)
print("")
print(Fore.YELLOW + "Currently:")
print(Fore.CYAN + "Current conditions: " + Fore.YELLOW + summary_overall)
print(Fore.CYAN + "Current temperature: " + Fore.YELLOW + summary_tempf + "°F (" + summary_tempc + "°C)")
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

for hour in hourly_json['hourly_forecast']:
    hourly_time = hour['FCTTIME']['civil']
    hourly_tempf = hour['temp']['english']
    hourly_tempc = hour['temp']['metric']
    hourly_condition = hour['condition']
    print(Fore.CYAN + hourly_time + ": " + Fore.YELLOW + hourly_condition + " with a temperature of " + hourly_tempf + "°F (" + hourly_tempc + "°C)")
    summaryHourlyIterations = summaryHourlyIterations + 1
    if summaryHourlyIterations == 6:
        break
print(Fore.YELLOW + "Input " + Fore.CYAN + "View more hourly " + Fore.YELLOW + "for more hourly weather info.")    
print("")
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

while True:
    print("")
    print("What would you like to do?")
    print("You can 'view more current data', 'view more hourly data'")
    print("You can also 'view the 10 day forecast', 'view weather for a different location'")
    print("Or you can 'close PyWeather'")
    moreoptions = input("Enter here: ").lower()
    if (moreoptions == "view more currently" or moreoptions == "view more current data" 
        or moreoptions == "view more current weather"):
        print("Loading...")
        print("")
        # I forgot to add Pressure and Dewpoints (rip)
        current_windDegrees = str(current_json['current_observation']['wind_degrees'])
        current_feelsLikeF = str(current_json['current_observation']['feelslike_f'])
        current_feelsLikeC = str(current_json['current_observation']['feelslike_c'])
        current_visibilityMi = str(current_json['current_observation']['visibility_mi'])
        current_visibilityKm = str(current_json['current_observation']['visibility_km'])
        current_UVIndex = str(current_json['current_observation']['UV'])
        current_precip1HrIn = str(current_json['current_observation']['precip_1hr_in'])
        current_precip1HrMm = str(current_json['current_observation']['precip_1hr_metric'])
        current_precipTodayIn = str(current_json['current_observation']['precip_today_in'])
        current_precipTodayMm = str(current_json['current_observation']['precip_today_metric'])
        print(Fore.CYAN + "Here's the detailed current weather for: " + Fore.YELLOW + location2.city + ", " + location2.state)
        print(Fore.CYAN + summary_lastupdated)
        print("")
        print(Fore.CYAN + "Current conditions: " + Fore.YELLOW + summary_overall)
        print(Fore.CYAN + "Current temperature: " + Fore.YELLOW + summary_tempf + "°F (" + summary_tempc + "°C)")
        print(Fore.CYAN + "And it feels like: " + Fore.YELLOW + current_feelsLikeF
              + "°F (" + current_feelsLikeC + "°C)")
        if winddata == True:
            print(Fore.CYAN + "Current wind: " + Fore.YELLOW + summary_windmphstr + 
                  " mph (" + summary_windkphstr + " kph), blowing " + summary_winddir 
                  + " (" + current_windDegrees + " degrees)")
        else:
            print(Fore.YELLOW + "Wind data is not available for this location.")
        print(Fore.CYAN + "Current humidity: " + Fore.YELLOW + summary_humidity)
        if heatindexdata == True:
            print(Fore.CYAN + "Current heat index: " + Fore.YELLOW + summary_heatindexfstr + "°F (" + summary_heatindexcstr + "°C)")
        if windchilldata == True:
            print(Fore.CYAN + "Current wind chill: " + Fore.YELLOW + summary_windchillfstr + "°F (" + summary_windchillcstr + "°C)")
        print(Fore.CYAN + "Current visibility: " + Fore.YELLOW + current_visibilityMi
              + " miles (" + current_visibilityKm + " km)")
        print(Fore.CYAN + "UV Index: " + Fore.YELLOW + current_UVIndex)
        print(Fore.CYAN + "Precipitation in the last hour: " + Fore.YELLOW
              + current_precip1HrIn + " inches (" + current_precip1HrMm
              + " mm)")
        print(Fore.CYAN + "Precipitation so far today: " + Fore.YELLOW
              + current_precipTodayIn + " inches (" + current_precipTodayMm
              + " mm)")
        continue
    elif (moreoptions == "view more hourly data" or
          moreoptions == "view more hourly" or
          moreoptions == "view hourly" or
          moreoptions == "hourly"):
        print("Loading...")
        print("")
        print(Fore.CYAN + "Here's the detailed hourly forecast for: " + Fore.YELLOW + location2.city + ", " + location2.state)
        print("")
        for hour in hourly_json['hourly_forecast']:
            hourly_time = hour['FCTTIME']['civil']
            hourly_month = str(hour['FCTTIME']['month_name'])
            hourly_day = str(hour['FCTTIME']['mday'])
            hourly_dewpointF = str(hour['dewpoint']['english'])
            hourly_dewpointC = str(hour['dewpoint']['metric'])
            hourly_windMPH = str(hour['wspd']['english'])
            hourly_windKPH = str(hour['wspd']['metric'])
            hourly_windDir = hour['wdir']['dir']
            hourly_windDegrees = str(hour['wdir']['degrees'])
            hourly_UVIndex = str(hour['uvi'])
            hourly_humidity = str(hour['humidity'])
            hourly_WCCheck = hour['windchill']['english']
            hourly_HICheck = hour['heatindex']['english']
            hourly_HIData = True
            if verbosity == True:
                logger.debug("hourly_WCCheck: %s" % hourly_WCCheck)
                logger.debug("hourly_HICheck: %s" % hourly_HICheck)
            if hourly_WCCheck == -9998:
                hourly_WCData = False
            else:
                hourly_WCData = True
                
            logger.debug("hourly_WCData: %s" % hourly_WCData)
            
            if hourly_HICheck == -9999:
                hourly_HIData = False
            
            
            logger.debug("hourly_HIData: %s" % hourly_HIData)
                
            hourly_windChillF = str(hourly_WCCheck)
            hourly_windchillC = str(hour['windchill']['metric'])
            hourly_HeatIndexF = str(hourly_HICheck)
            hourly_HeatIndexC = str(hour['heatindex']['metric'])
            hourly_feelsLikeF = str(hour['feelslike']['english'])
            hourly_feelsLikeC = str(hour['feelslike']['metric'])
            hourly_precipCheck = str(hour['qpf']['english'])
            hourly_snowCheck = str(hour['snow']['english'])
            if hourly_precipCheck == "":
                hourly_precipIn = "0.0"
                hourly_precipMm = "0.0"
            else:
                hourly_precipIn = str(hour['qpf']['english'])
                hourly_precipMm = str(hour['qpf']['metric'])
            if hourly_snowCheck == "":
                hourly_snowIn = "0.0"
                hourly_snowMm = "0.0"
            else:
                hourly_snowIn = str(hour['snow']['english'])
                hourly_snowMm = str(hour['snow']['metric'])
            hourly_precipChance = str(hour['pop'])
            hourly_pressureInHg = str(hour['mslp']['english'])
            hourly_pressureMb = str(hour['mslp']['metric'])
            print(Fore.CYAN + hourly_time + " on " + hourly_month + " " + hourly_day + ":")
            print(Fore.CYAN + "Conditions: " + Fore.YELLOW + hourly_condition)
            print(Fore.CYAN + "Temperature: " + Fore.YELLOW + hourly_tempf 
                  + "°F (" + hourly_tempc + "°C)")
            print(Fore.CYAN + "Dew Point: " + Fore.YELLOW + hourly_dewpointF
                  + "°F (" + hourly_dewpointC + "°C)")
            print(Fore.CYAN + "Wind: " + Fore.YELLOW + hourly_windMPH
                  + " mph (" + hourly_windKPH + " kph) blowing to the " +
                  hourly_windDir + " (" + hourly_windDegrees + "°)")
            print(Fore.CYAN + "Humidity: " + hourly_humidity + "%")
            if hourly_WCData == True:
                print(Fore.CYAN + "Wind chill: " + hourly_windChillF
                      + "°F (" + hourly_windchillC + "°C)")
            if hourly_HIData == False:
                print(Fore.CYAN + "Wind chill: " + Fore.YELLOW +
                      "No data available.")
            if hourly_HIData == True:
                print(Fore.CYAN + "Heat index: " + hourly_HeatIndexF
                      + "°F (" + hourly_HeatIndexF + "°C)")
            if hourly_HIData == False:
                print(Fore.CYAN + "Heat index: " + Fore.YELLOW + 
                      "No data available.")
            print(Fore.CYAN + "Feels like: " + Fore.YELLOW + hourly_feelsLikeF
                  + "°F (" + hourly_feelsLikeC + "°C)")
            # I may end up doing a check for precipitation data.
            print(Fore.CYAN + "Precipiation for the hour: " + Fore.YELLOW +
                  hourly_precipIn + " in (" + hourly_precipMm + " mm)")
            print(Fore.CYAN + "Snow for the next hour: " + Fore.YELLOW +
                  hourly_snowIn + " in (" + hourly_snowMm + " mm)")
            print(Fore.CYAN + "Precipitation chance: " + Fore.YELLOW + 
                  hourly_precipChance + "%")
            print(Fore.CYAN + "Barometric pressure: " + Fore.YELLOW +
                  hourly_pressureInHg + " inhg (" + hourly_pressureMb
                  + " mb)")
            
    elif (moreoptions == "close pyweather" or moreoptions == "close"):
        sys.exit()
    elif (moreoptions == "different location"
          or moreoptions == "view weather for a different location" or
          moreoptions == "view weather different location"):
        print("This feature has been temporarily removed.")
    