# PyWeather 0.3.1 -> 0.3.2 beta
# (c) 2017 o355, GNU GPL 3.0.
# Powered by Wunderground
# If there any random imports below here, blame Eclipse.
# Testing git within Eclipse.

# ===========================
#   A few quick notes:
# 1. The internal code is not organized, and it's meant to stay that way.
# I usually design programs with the fact that I'll clean up code, and use
# proper naming conventions/design conventions once the thing works.
# So, for now. Lines of code/comments will be 79+ characters long. Sorry. 
# 2. This program is 25% complete, meaning it's FAR from what it can do.
# 3. There is no setup.py file. Get the API key on your own, and download
# necessary modules through PIP.
# 4. Progress will be slow and steady with TermWeather. Trust me.


# Verbosity works like this (for now)
# Turn on verbosity for, well, verbosity! jsonVerbosity outputs
# the full JSON acquired (aka spams 50 lines of console), so it's
# a separate, and now, more obvious switch.

verbosity = True
jsonVerbosity = True
if verbosity == True:
    import logging
    logger = logging.getLogger('pyweather_0.3.2beta')
    logger.setLevel(logging.DEBUG)
    logformat = '%(asctime)s | %(levelname)s | %(message)s'
    logging.basicConfig(format=logformat)

import urllib.request
import sys
import json
import time
import shutil
from colorama import init, Fore, Style
import codecs
from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim
from datetime import datetime
import geocoder
geolocator = GoogleV3()
geolocator2 = Nominatim()

if verbosity == True:
    logger.debug("Begin API keyload...")
apikey_load = open('storage//apikey.txt')
if verbosity == True:
    logger.debug("apikey_load = %s" % apikey_load)
try:
    apikey = apikey_load.read()
except FileNotFoundError:
    print("The API key wasn't found. (Error 38, pyweather.py)")
    sys.exit()
if verbosity == True:
    logger.debug("apikey = %s" % apikey)

# I understand that this slightly goes against Wunderground's ToS
# for logo layout, but, seriously. This is a terminal. It's this
# or terminal logos.

# I think they more specifically target apps with the logo ToS,
# and not terminal scripts that a user needs to obtain an API
# key to use.

# Sorry WU. I still love you.

print("Welcome to PyWeather - Powered by Wunderground.")
print("Please enter a location to get weather information for.")
locinput = input("Input here: ")
print("Sweet! Getting your weather!")


# Start the geocoder. If we don't have a connection, exit nicely.
# After we get location data, store it in latstr and lonstr, and store
# it in the table called loccords.

firstfetch = time.time()
if verbosity == True:
    logger.debug("Start geolocator...")
try:
    location = geolocator.geocode(locinput, language="en", timeout=20)
    # Since the loading bars interfere with true verbosity logging, we turn
    # them off if verbosity is enabled (it isn't needed)
    if verbosity == False:
        print("[#---------] | 5% |", round(time.time() - firstfetch,1), "seconds", end="\r")
except:
    if verbosity == True:
        logger.error("No connection to Google's geocoder!")
    print("Could not connect to Google's geocoder.")
    print("Ensure you have an internet connection, and that Google's geocoder " +
          "is unblocked.")
    sys.exit()
if verbosity == True:
    logger.debug("location = %s" % location)

try:
    latstr = str(location.latitude)
    lonstr = str(location.longitude)
except AttributeError:
    if verbosity == True:
        logger.error("No lat/long was provided by Google! Bad location?")
    print("The location you inputted could not be understood.")
    print("Please try again.")
    sys.exit()
        
if verbosity == True:
    logger.debug("Latstr: %s ; Lonstr: %s" % (latstr, lonstr))
loccoords = [latstr, lonstr]
if verbosity == True:
    logger.debug("Loccoords: %s" % loccoords)
    logger.info("End geolocator...")
    logger.info("Start API var declare...")

# Declare the API URLs with the API key, and latitude/longitude strings from earlier.

currenturl = 'http://api.wunderground.com/api/' + apikey + '/conditions/q/' + latstr + "," + lonstr + '.json'
f3dayurl = 'http://api.wunderground.com/api/' + apikey + '/forecast/q/' + latstr + "," + lonstr + '.json'
f10dayurl = 'http://api.wunderground.com/api/' + apikey + '/forecast10day/q/' + latstr + "," + lonstr + '.json'
hourlyurl = 'http://api.wunderground.com/api/' + apikey + '/hourly/q/' + latstr + "," + lonstr + '.json'
if verbosity == False:
    print("[##--------] | 14% |", round(time.time() - firstfetch,1), "seconds", end="\r")
if verbosity == True:
    logger.debug("currenturl: %s" % currenturl)
    logger.debug("f3dayurl: %s" % currenturl)
    logger.debug("f10dayurl: %s" % currenturl)
    logger.debug("hourlyurl: %s" % currenturl)
    logger.info("End API var declare...")
    logger.info("Start codec change...")

# Due to Python, we have to get the UTF-8 reader to properly parse the JSON we got.
reader = codecs.getreader("utf-8")
if verbosity == False:
    print("[##--------] | 19% |", round(time.time() - firstfetch,1), "seconds", end="\r")
if verbosity == True:
    logger.debug("reader: %s" % reader)
    logger.info("End codec change...")
    logger.info("Start API fetch...")
    
# Fetch the JSON file using urllib.request, store it as a temporary file.
try:
    summaryJSON = urllib.request.urlopen(currenturl)
    if verbosity == False:
        print("[###-------] | 32% |", round(time.time() - firstfetch,1), "seconds", end="\r")
    if verbosity == True:
        logger.debug("Acquired summary JSON, end result: %s" % summaryJSON)
    forecastJSON = urllib.request.urlopen(f3dayurl)
    if verbosity == False:
        print("[####------] | 48% |", round(time.time() - firstfetch,1), "seconds", end="\r")
    if verbosity == True:
        logger.debug("Acquired forecast 3day JSON, end result: %s" % forecastJSON)
    forecast10JSON = urllib.request.urlopen(f10dayurl)
    if verbosity == False:
        print("[#####-----] | 58% |", round(time.time() - firstfetch,1), "seconds", end="\r")
    if verbosity == True:
        logger.debug("Acquired forecast 10day JSON, end result: %s" % forecast10JSON)
    hourlyJSON = urllib.request.urlopen(hourlyurl)
    if verbosity == False:
        print("[#######---] | 72% |", round(time.time() - firstfetch,1), "seconds", end="\r")
    if verbosity == True:
        logger.debug("Acquired hourly JSON, end result: %s" % hourlyJSON)
except:
    if verbosity == True:
        logger.error("No connection to the API!! Is the connection offline?")
    print("Can't connect to the API. Make sure that Wunderground's API " +
          "is unblocked, and the internet is online.")
    sys.exit()
# And we parse the json using json.load.
if verbosity == True:
    logger.info("End API fetch...")
    logger.info("Start JSON load...")
if verbosity == False:
    print("[#######---] | 74% |", round(time.time() - firstfetch,1), "seconds", end="\r")
current_json = json.load(reader(summaryJSON))
if jsonVerbosity == True:
    logger.debug("current_json loaded with: %s" % current_json)
if verbosity == False:
    print("[#######---] | 77% |", round(time.time() - firstfetch,1), "seconds", end="\r")
forecast3_json = json.load(reader(forecastJSON))
if jsonVerbosity == True:
    logger.debug("forecast3_json loaded with: %s" % forecast3_json)
if verbosity == False:
    print("[########--] | 81% |", round(time.time() - firstfetch,1), "seconds", end="\r")
forecast10_json = json.load(reader(forecast10JSON))
if jsonVerbosity == True:
    logger.debug("forecast10_json loaded with: %s" % forecast10_json)
if verbosity == False:
    print("[########--] | 85% |", round(time.time() - firstfetch,1), "seconds", end="\r")
hourly_json = json.load(reader(hourlyJSON))
if jsonVerbosity == True:
    logger.debug("hourly_json loaded with: %s" % hourly_json)
if verbosity == True:
    logger.info("4 JSONs loaded...")
    logger.info("Start 2nd geocoder...")

# Contact Google's reverse geocoder to give us a proper location
# of where we're getting the weather for.

try:
    location2 = geocoder.google([latstr, lonstr], method='reverse', timeout=20)
    if verbosity == False:
        print("[#########-] | 91% |", round(time.time() - firstfetch,1), "seconds", end="\r")
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



# Parse the current weather!

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
if verbosity == False:
    print("[##########] | 97% |", round(time.time() - firstfetch,1), "seconds", end="\r")
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

summary_feelslikef = str(current_json['current_observation']['feelslike_f'])
summary_feelslikec = str(current_json['current_observation']['feelslike_c'])
if verbosity == True:
    logger.info("summary_feelslikef: %s ; summary_feelslikec: %s"
                % (summary_feelslikef, summary_feelslikec))

summary_dewPointF = str(current_json['current_observation']['dewpoint_f'])
summary_dewPointC = str(current_json['current_observation']['dewpoint_c'])
if verbosity == True:
    logger.info("summary_dewPointF: %s ; summary_dewpointC: %s"
                % (summary_dewPointF, summary_dewPointC))
if verbosity == True:
    logger.info("Initalize color...")
init()
if verbosity == False:
    print("[##########] | 100% |", round(time.time() - firstfetch,1), "seconds", end="\r")
if verbosity == True:
    logger.info("Printing current conditions...")
    
# <--------------- This is where we end parsing, and begin printing. ---------->

summaryHourlyIterations = 0

print(Style.BRIGHT + Fore.CYAN + "Here's the weather for: " + Fore.YELLOW + location2.city + ", " + location2.state)
print(Fore.YELLOW + summary_lastupdated)
print("")
print(Fore.YELLOW + "Currently:")
print(Fore.CYAN + "Current conditions: " + Fore.YELLOW + summary_overall)
print(Fore.CYAN + "Current temperature: " + Fore.YELLOW + summary_tempf + "°F (" + summary_tempc + "°C)")
print(Fore.CYAN + "And it feels like: " + Fore.YELLOW + summary_feelslikef
      + "°F (" + summary_tempc + "°C)")
print(Fore.CYAN + "Current dew point: " + Fore.YELLOW + summary_dewPointF
      + "°F (" + summary_dewPointC + "°C)")
if winddata == True:
    print(Fore.CYAN + "Current wind: " + Fore.YELLOW + summary_windmphstr + " mph (" + summary_windkphstr + " kph), blowing " + summary_winddir + ".")
else:
    print(Fore.YELLOW + "Wind data is not available for this location.")
print(Fore.CYAN + "Current humidity: " + Fore.YELLOW + summary_humidity)
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

# In this part of PyWeather, you'll find comments indicating where things end/begin.
# This is to help when coding, and knowing where things are.

while True:
    print("")
    print(Fore.YELLOW + "What would you like to do now?")
    print("- View more current data (or press " + Fore.CYAN + "0" 
          + Fore.YELLOW + ")")
    print("- View more hourly data (or press " + Fore.CYAN + "1"
          + Fore.YELLOW + ")")
    print("- View more forecast data (or press " + Fore.CYAN + "2"
          + Fore.YELLOW + ")")
    print("- Check for PyWeather updates (or press " + Fore.CYAN + "3"
          + Fore.YELLOW + ")")
    print("- Close PyWeather (or press " + Fore.CYAN + "4" + Fore.YELLOW
          + ")")
    moreoptions = input("Enter here: ").lower()
    if verbosity == True:
        logger.debug("moreoptions: %s" % moreoptions)
        
        
    if (moreoptions == "view more current" or moreoptions == "view more current data" 
        or moreoptions == "view currently" or moreoptions == "view more currently"
        or moreoptions == "currently" or moreoptions == "current" or moreoptions == '0'):
        print(Fore.RED + "Loading...")
        if verbosity == True:
            logger.info("Selected view more currently...")
        print("")
        current_pressureInHg = str(current_json['current_observation']['pressure_in'])
        current_pressureMb = str(current_json['current_observation']['pressure_mb'])
        if verbosity == True:
            logger.debug("current_pressureInHg: %s ; current_pressureMb: %s"
                         % (current_pressureInHg, current_pressureMb))
        current_pressureTrend = current_json['current_observation']['pressure_trend']
        if current_pressureTrend == "+":
            current_pressureTrend2 = "and rising."
        elif current_pressureTrend == "0":
            current_pressureTrend2 = "and staying level."
        elif current_pressureTrend == "-":
            current_pressureTrend2 = "and dropping."
        else:
            current_pressureTrend2 = "with no trend available."
        if verbosity == True:
            logger.debug("current_pressureTrend: %s ; current_pressureTrend2: %s"
                         % (current_pressureTrend, current_pressureTrend2))
        current_windDegrees = str(current_json['current_observation']['wind_degrees'])
        current_feelsLikeF = str(current_json['current_observation']['feelslike_f'])
        current_feelsLikeC = str(current_json['current_observation']['feelslike_c'])
        current_visibilityMi = str(current_json['current_observation']['visibility_mi'])
        current_visibilityKm = str(current_json['current_observation']['visibility_km'])
        current_UVIndex = str(current_json['current_observation']['UV'])
        if verbosity == True:
            logger.debug("current_windDegrees: %s ; current_feelsLikeF: %s" 
                         % (current_windDegrees, current_feelsLikeF))
            logger.debug("current_feelsLikeC: %s ; current_visibilityMi: %s"
                         % (current_feelsLikeC, current_visibilityMi))
            logger.debug("current_visibilityKm: %s ; current_UVIndex: %s"
                         % (current_visibilityKm, current_UVIndex))
        current_precip1HrIn = str(current_json['current_observation']['precip_1hr_in'])
        current_precip1HrMm = str(current_json['current_observation']['precip_1hr_metric'])
        if current_precip1HrMm == "--":
            current_precip1HrMm = "0.0"
            current_precip1HrIn = "0.0"
        current_precipTodayIn = str(current_json['current_observation']['precip_today_in'])
        current_precipTodayMm = str(current_json['current_observation']['precip_today_metric'])
        if verbosity == True:
            logger.debug("current_precip1HrIn: %s ; current_precip1HrMm: %s"
                         % (current_precip1HrIn, current_precip1HrMm))
        if verbosity == True:
            logger.debug("current_precipTodayIn: %s ; current_precipTodayMm: %s"
                         % (current_precipTodayIn, current_precipTodayMm))
        print(Fore.CYAN + "Here's the detailed current weather for: " + Fore.YELLOW + location2.city + ", " + location2.state)
        print(Fore.CYAN + summary_lastupdated)
        print("")
        print(Fore.CYAN + "Current conditions: " + Fore.YELLOW + summary_overall)
        print(Fore.CYAN + "Current temperature: " + Fore.YELLOW + summary_tempf + "°F (" + summary_tempc + "°C)")
        print(Fore.CYAN + "And it feels like: " + Fore.YELLOW + current_feelsLikeF
              + "°F (" + current_feelsLikeC + "°C)")
        print(Fore.CYAN + "Current dew point: " + Fore.YELLOW + summary_dewPointF
              + "°F (" + summary_dewPointC + "°C)")
        if winddata == True:
            print(Fore.CYAN + "Current wind: " + Fore.YELLOW + summary_windmphstr + 
                  " mph (" + summary_windkphstr + " kph), blowing " + summary_winddir 
                  + " (" + current_windDegrees + " degrees)")
        else:
            print(Fore.YELLOW + "Wind data is not available for this location.")
        print(Fore.CYAN + "Current humidity: " + Fore.YELLOW + summary_humidity)
        print(Fore.CYAN + "Current pressure: " + Fore.YELLOW + current_pressureInHg
              + " inHg (" + current_pressureMb + " mb), " + current_pressureTrend2)
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
    
# <----------- Detailed Currently is above, Detailed Hourly is below -------->
    
    elif (moreoptions == "view more hourly data" or
          moreoptions == "view more hourly" or
          moreoptions == "view hourly" or
          moreoptions == "hourly" or
          moreoptions == "1"):
        print(Fore.RED + "Loading...")
        print("")
        if verbosity == True:
            logger.info("Selected view more hourly...")
        detailedHourlyIterations = 0
        print(Fore.CYAN + "Here's the detailed hourly forecast for: " + Fore.YELLOW + location2.city + ", " + location2.state)
        for hour in hourly_json['hourly_forecast']:
            if verbosity == True:
                logger.info("We're on iteration: %s" % detailedHourlyIterations)
            hourly_time = hour['FCTTIME']['civil']
            hourly_tempf = hour['temp']['english']
            hourly_tempc = hour['temp']['metric']
            hourly_month = str(hour['FCTTIME']['month_name'])
            hourly_day = str(hour['FCTTIME']['mday'])
            hourly_dewpointF = str(hour['dewpoint']['english'])
            if verbosity == True:
                logger.debug("hourly_time: %s ; hourly_month: %s"
                             % (hourly_time, hourly_month))
                logger.debug("hourly_day: %s ; hourly_dewpointF: %s"
                             % (hourly_day, hourly_dewpointF))
            hourly_dewpointC = str(hour['dewpoint']['metric'])
            hourly_windMPH = str(hour['wspd']['english'])
            hourly_windKPH = str(hour['wspd']['metric'])
            hourly_windDir = hour['wdir']['dir']
            if verbosity == True:
                logger.debug("hourly_dewpointC: %s ; hourly_windMPH: %s"
                             % (hourly_dewpointC, hourly_windMPH))
                logger.debug("hourly_windKPH: %s ; hourly_windDir: %s"
                             % (hourly_windKPH, hourly_windDir))
            hourly_windDegrees = str(hour['wdir']['degrees'])
            hourly_UVIndex = str(hour['uvi'])
            hourly_humidity = str(hour['humidity'])
            hourly_feelsLikeF = str(hour['feelslike']['english'])
            if verbosity == True:
                logger.debug("hourly_windDegrees: %s ; hourly_UVIndex: %s"
                             % (hourly_windDegrees, hourly_UVIndex))
                logger.debug("hourly_humidity: %s ; hourly_feelsLikeF: %s"
                             % (hourly_humidity, hourly_feelsLikeF))
            hourly_feelsLikeC = str(hour['feelslike']['metric'])
            hourly_precipIn = str(hour['qpf']['english'])
            hourly_precipMm = str(hour['qpf']['metric'])
            hourly_snowCheck = hour['snow']['english']
            if verbosity == True:
                logger.debug("hourly_feelsLikeC: %s ; hourly_precipIn: %s"
                             % (hourly_feelsLikeC, hourly_precipIn))
                logger.debug("hourly_precipMm: %s ; hourly_snowCheck: %s"
                             % (hourly_precipMm, hourly_snowCheck))
                logger.info("Starting snow check...")
            if hourly_snowCheck == "0.0":
                hourly_snowData = False
                if verbosity == True:
                    logger.warn("No snow data! Maybe it's summer?")
            else:
                hourly_snowData = True
                if verbosity == True:
                    logger.info("Lucky duck getting some snow.")
            
            hourly_snowIn = str(hourly_snowCheck)
            hourly_snowMm = str(hour['snow']['metric'])
            hourly_precipChance = str(hour['pop'])
            hourly_pressureInHg = str(hour['mslp']['english'])
            hourly_pressureMb = str(hour['mslp']['metric'])
            if verbosity == True:
                logger.debug("hourly_snowIn: %s ; hourly_snowMm: %s"
                             % (hourly_snowIn, hourly_snowMm))
                logger.debug("hourly_precipChance: %s ; hourly_pressureInHg: %s"
                             % (hourly_precipChance, hourly_pressureInHg))
                logger.debug("hourly_pressureMb: %s" % hourly_pressureMb)
                logger.info("Now printing weather data...")
            print("")
            # If you have verbosity on, there's a chance that the next
            # hourly iteration will start BEFORE the previous iteration
            # prints out. This is normal, and no issues are caused by such.
            print(Fore.YELLOW + hourly_time + " on " + hourly_month + " " + hourly_day + ":")
            print(Fore.CYAN + "Conditions: " + Fore.YELLOW + hourly_condition)
            print(Fore.CYAN + "Temperature: " + Fore.YELLOW + hourly_tempf 
                  + "°F (" + hourly_tempc + "°C)")
            print(Fore.CYAN + "Dew Point: " + Fore.YELLOW + hourly_dewpointF
                  + "°F (" + hourly_dewpointC + "°C)")
            print(Fore.CYAN + "Wind: " + Fore.YELLOW + hourly_windMPH
                  + " mph (" + hourly_windKPH + " kph) blowing to the " +
                  hourly_windDir + " (" + hourly_windDegrees + "°)")
            print(Fore.CYAN + "Humidity: " + Fore.YELLOW + hourly_humidity + "%")
            print(Fore.CYAN + "Feels like: " + Fore.YELLOW + hourly_feelsLikeF
                  + "°F (" + hourly_feelsLikeC + "°C)")
            print(Fore.CYAN + "Precipiation for the hour: " + Fore.YELLOW +
                  hourly_precipIn + " in (" + hourly_precipMm + " mm)")
            if hourly_snowData == True:
                print(Fore.CYAN + "Snow for the next hour: " + Fore.YELLOW +
                      hourly_snowIn + " in (" + hourly_snowMm + " mm)")
            print(Fore.CYAN + "Precipitation chance: " + Fore.YELLOW + 
                  hourly_precipChance + "%")
            print(Fore.CYAN + "Barometric pressure: " + Fore.YELLOW +
                  hourly_pressureInHg + " inHg (" + hourly_pressureMb
                  + " mb)")
            detailedHourlyIterations = detailedHourlyIterations + 1
            if (detailedHourlyIterations == 6 or detailedHourlyIterations == 12
                or detailedHourlyIterations == 18 or detailedHourlyIterations == 24
                or detailedHourlyIterations == 30):
                if verbosity == True:
                    logger.debug("detailedHourlyIterations: %s" % detailedHourlyIterations)
                    logger.debug("Asking user for continuation...")
                try:
                    print("")
                    print(Fore.RED + "Please press enter to view the next 6 hours of hourly data.")
                    print("You can also press Control + C to head back to the input menu.")
                    input()
                    if verbosity == True:
                        logger.debug("Iterating 6 more times...")
                except KeyboardInterrupt:
                    if verbosity == True:
                        logger.debug("Exiting to main menu...")
                    break
    elif (moreoptions == "view the 10 day weather forecast" or
          moreoptions == "view more forecast data" or
          moreoptions == "view the 10 day" or moreoptions == "view 10 day"
          or moreoptions == "view the 10 day"
          or moreoptions == "10 day" or moreoptions == "10 day forecast"
          or moreoptions == "10 day weather forecast"
          or moreoptions == "2"):
        print(Fore.RED + "Loading...")
        if verbosity == True:
            logger.info("Selected view more 10 day...")
        print("")
        detailedForecastIterations = 0
        print(Fore.CYAN + "Here's the detailed 10 day forecast for: " + Fore.YELLOW + location2.city + ", " + location2.state)
        for day in forecast10_json['forecast']['simpleforecast']['forecastday']:
            if verbosity == True:
                logger.info("We're on iteration: %s" % detailedForecastIterations)
            forecast10_weekday = day['date']['weekday']
            forecast10_month = str(day['date']['month'])
            forecast10_day = str(day['date']['day'])
            forecast10_highf = str(day['high']['fahrenheit'])
            if verbosity == True:
                logger.debug("forecast10_weekday: %s ; forecast10_month: %s"
                             % (forecast10_weekday, forecast10_month))
                logger.debug("forecast10_day: %s ; forecast10_highf: %s"
                             % (forecast10_day, forecast10_highf))
            forecast10_highc = str(day['high']['celsius'])
            forecast10_lowf = str(day['low']['fahrenheit'])
            forecast10_lowc = str(day['low']['celsius'])
            forecast10_conditions = day['conditions']
            if verbosity == True:
                logger.debug("forecast10_highc: %s ; forecast10_lowf: %s"
                            % (forecast10_highc, forecast10_lowf))
                logger.debug("forecast10_lowc: %s ; forecast10_conditions: %s"
                             % (forecast10_lowc, forecast10_conditions))
            forecast10_precipTotalIn = str(day['qpf_allday']['in'])
            forecast10_precipTotalMm = str(day['qpf_allday']['mm'])
            forecast10_precipDayIn = str(day['qpf_day']['in'])
            forecast10_precipDayMm = str(day['qpf_day']['mm'])
            if verbosity == True:
                logger.debug("forecast10_precipTotalIn: %s ; forecast10_precipTotalMm: %s"
                             % (forecast10_precipTotalIn, forecast10_precipTotalMm))
                logger.debug("forecast10_precipDayIn: %s ; forecast10_precipDayMm: %s"
                             % (forecast10_precipDayIn, forecast10_precipDayMm))
            forecast10_precipNightIn = str(day['qpf_night']['in'])
            forecast10_precipNightMm = str(day['qpf_night']['mm'])
            if verbosity == True:
                logger.debug("forecast10_precipNightIn: %s ; forecast10_precipNightMm: %s"
                             % (forecast10_precipNightIn, forecast10_precipNightMm))
            forecast10_snowTotalCheck = day['snow_allday']['in']
            if verbosity == True:
                logger.debug("forecast10_snowTotalCheck: %s" % forecast10_snowTotalCheck)
            if forecast10_snowTotalCheck == 0.0:
                forecast10_snowTotalData = False
                if verbosity == True:
                    logger.warn("Oh no! No snow data for the day. Is it too warm?")
            else:
                forecast10_snowTotalData = True
                if verbosity == True:
                    logger.info("Snow data for the day. Snow. I love snow.")
            forecast10_snowTotalIn = str(forecast10_snowTotalCheck)
            forecast10_snowTotalCm = str(day['snow_allday']['cm'])
            forecast10_snowDayCheck = day['snow_day']['in']
            if verbosity == True:
                logger.debug("forecast10_snowTotalIn: %s ; forecast10_snowTotalCm: %s"
                             % (forecast10_snowTotalIn, forecast10_snowTotalCm))
                logger.debug("forecast10_snowDayCheck: %s" % forecast10_snowDayCheck)
            if forecast10_snowDayCheck == 0.0:
                forecast10_snowDayData = False
                if verbosity == True:
                    logger.warn("Oh no! No snow data for the day. Is it too warm?")
            else:
                forecast10_snowDayData = True
                if verbosity == True:
                    logger.info("Snow data for the day is available.")
            forecast10_snowDayIn = str(forecast10_snowDayCheck)
            forecast10_snowDayCm = str(day['snow_day']['cm'])
            forecast10_snowNightCheck = day['snow_night']['in']
            if verbosity == True:
                logger.debug("forecast10_snowDayIn: %s ; forecast10_snowDayCm: %s"
                             % (forecast10_snowDayIn, forecast10_snowDayCm))
                logger.debug("forecast10_snowNightCheck: %s" % forecast10_snowNightCheck)
            if forecast10_snowNightCheck == 0.0:
                forecast10_snowNightData = False
                if verbosity == True:
                    logger.warn("Oh no! No snow data for the night. Is it too warm?")
            else:
                forecast10_snowNightData = True
                if verbosity == True:
                    logger.info("Snow data for the night is available. Snow day?")
            forecast10_snowNightIn = str(forecast10_snowNightCheck)
            forecast10_snowNightCm = str(day['snow_night']['cm'])
            forecast10_maxWindMPH = str(day['maxwind']['mph'])
            forecast10_maxWindKPH = str(day['maxwind']['kph'])
            if verbosity == True:
                logger.debug("forecast10_snowNightIn: %s ; forecast10_snowNightCm: %s"
                             % (forecast10_snowNightIn, forecast10_snowNightCm))
                logger.debug("forecast10_maxWindMPH: %s ; forecast10_maxWindKPH: %s"
                             % (forecast10_maxWindMPH, forecast10_maxWindKPH))
            forecast10_avgWindMPH = str(day['avewind']['mph'])
            forecast10_avgWindKPH = str(day['avewind']['kph'])
            forecast10_avgWindDir = day['avewind']['dir']
            forecast10_avgWindDegrees = str(day['avewind']['degrees'])
            forecast10_avgHumidity = str(day['avehumidity'])
            if verbosity == True:
                logger.debug("forecast10_avgWindMPH: %s ; forecast10_avgWindKPH: %s"
                             % (forecast10_avgWindMPH, forecast10_avgWindKPH))
                logger.debug("forecast10_avgWindDir: %s ; forecast10_avgWindDegrees: %s"
                             % (forecast10_avgWindDir, forecast10_avgWindDegrees))
                logger.debug("forecast10_avgHumidity: %s" % forecast10_avgHumidity)
                logger.info("Printing weather data...")
            print("")
            print(Fore.YELLOW + forecast10_weekday + ", " + forecast10_month + "/" + forecast10_day + ":")
            print(Fore.YELLOW + forecast10_conditions + Fore.CYAN + " with a high of "
                  + Fore.YELLOW + forecast10_highf + "°F (" + forecast10_highc + "°C)" +
                  Fore.CYAN + " and a low of " + Fore.YELLOW + forecast10_lowf + "°F (" +
                  forecast10_lowc + "°C)" + ".")
            print(Fore.CYAN + "Total Precip: " + Fore.YELLOW +
                  forecast10_precipTotalIn + " in (" + forecast10_precipTotalMm
                  + " mm)")
            print(Fore.CYAN + "Precip during the day: " + Fore.YELLOW +
                  forecast10_precipDayIn + " in (" + forecast10_precipDayMm
                  + " mm)")
            print(Fore.CYAN + "Precip during the night: " + Fore.YELLOW +
                  forecast10_precipNightIn + " in (" + forecast10_precipNightMm
                  + " mm)")
            if forecast10_snowTotalData == True:
                print(Fore.CYAN + "Total snow: " + Fore.YELLOW +
                      forecast10_snowTotalIn + " in (" + forecast10_snowTotalCm
                      + " cm)")
            if forecast10_snowDayData == True:
                print(Fore.CYAN + "Snow during the day: " + Fore.YELLOW + 
                      forecast10_snowDayIn + " in (" + forecast10_snowDayCm
                      + " cm)")
            if forecast10_snowNightData == True:
                print(Fore.CYAN + "Snow during the night: " + Fore.YELLOW +
                      forecast10_snowNightIn + " in (" + forecast10_snowNightCm
                      + " cm)")
            print(Fore.CYAN + "Winds: " + Fore.YELLOW +
                  forecast10_avgWindMPH + " mph (" + forecast10_avgWindKPH
                  + " kph), gusting to " + forecast10_maxWindMPH + " mph ("
                  + forecast10_maxWindKPH + " kph), "
                  + "and blowing " + forecast10_avgWindDir +
                  " (" + forecast10_avgWindDegrees + "°)")
            print(Fore.CYAN + "Humidity: " + Fore.YELLOW +
                  forecast10_avgHumidity + "%")
            detailedForecastIterations = detailedForecastIterations + 1
            if detailedForecastIterations == 5:
                if verbosity == True:
                    logger.debug("detailedForecastIterations: %s" % detailedForecastIterations)
                try:
                    print(Fore.RED + "Press enter to view the next 5 days of weather data.")
                    print("You can also press Control + C to return to the input menu.")
                    input()
                    if verbosity == True:
                        logger.info("Iterating 5 more times...")
                except KeyboardInterrupt:
                    break
                    if verbosity == True:
                        logger.info("Exiting to the main menu.")
    elif (moreoptions == "close pyweather" or moreoptions == "close"
          or moreoptions == "4" or moreoptions == "close pw"):
        sys.exit()
    elif (moreoptions == "update pyweather" or moreoptions == "update"
          or moreoptions == "update pw" or moreoptions == "3"
          or moreoptions == "check for pyweather updates"):
        if verbosity == True:
            logger.info("Selected update.")
        buildnumber = 31
        buildversion = "0.3.1 beta"
        if verbosity == True:
            logger.debug("buildnumber: %s ; buildversion" %
                         (buildnumber, buildversion))
        print("Checking for updates. This shouldn't take that long.")
        try:
            versioncheck = urllib.request.urlopen("https://raw.githubusercontent.com/o355/pyweather/master/updater/versioncheck.json")
            if verbosity == True:
                logger.debug("versioncheck: %s" % versioncheck)
        except:
            if verbosity == True:
                logger.warn("Couldn't check for updates! Is there an internet connection?")
            print(Fore.RED + "Couldn't check for updates.")
            print("Make sure GitHub user content is unblocked, and you have an internet connection.")
            print("Error 54, pyweather.py")
            continue
        versionJSON = json.load(reader(versioncheck))
        if jsonVerbosity == True:
            logger.debug("versionJSON: %s" % versionJSON)
        if verbosity == True:
            logger.debug("Loaded versionJSON with reader %s" % reader)
        version_buildNumber = float(versionJSON['updater']['latestbuild'])
        version_latestVersion = versionJSON['updater']['latestversion']
        version_latestURL = versionJSON['updater']['latesturl']
        version_latestFileName = versionJSON['updater']['latestfilename']
        if verbosity == True:
            logger.debug("version_buildNumber: %s ; version_latestVersion: %s"
                         % (version_buildNumber, version_latestVersion))
            logger.debug("version_latestURL: %s ; verion_latestFileName: %s"
                         % (version_latestURL, version_latestFileName))
        version_latestReleaseDate = versionJSON['updater']['releasedate']
        if verbosity == True:
            logger.debug("version_latestReleaseDate: %s" % version_latestReleaseDate)
        if buildnumber >= version_buildNumber:
            if verbosity == True:
                logger.info("PyWeather is up to date.")
                logger.info("local build (%s) >= latest build (%s)"
                            % (buildnumber, version_buildNumber))
            print("")
            print(Fore.GREEN + "PyWeather is up to date!")
            print("You have version: " + Fore.CYAN + buildversion)
            print(Fore.GREEN + "The latest version is: " + Fore.CYAN + version_latestVersion)
        elif buildnumber < version_buildNumber:
            print("")
            if verbosity == True:
                logger.warn("PyWeather is NOT up to date.")
                logger.warn("local build (%s) < latest build (%s)"
                            % (buildnumber, version_buildNumber))
            print(Fore.RED + "PyWeather is not up to date! :(")
            print(Fore.RED + "You have version: " + Fore.CYAN + buildversion)
            print(Fore.RED + "The latest version is: " + Fore.CYAN + version_latestVersion)
            print(Fore.RED + "And it was released on: " + Fore.CYAN + version_latestReleaseDate)
            print("")
            print(Fore.RED + "Would you like to download the latest version?" + Fore.YELLOW)
            downloadLatest = input("Yes or No: ").lower()
            if verbosity == True:
                logger.debug("downloadLatest: %s" % downloadLatest)
            if downloadLatest == "yes":
                print("")
                if verbosity == True:
                    logger.debug("Downloading latest version...")
                print(Fore.YELLOW + "Downloading the latest version of PyWeather...")
                try:
                    with urllib.request.urlopen(version_latestURL) as update_response, open(version_latestFileName, 'wb') as update_out_file:
                        if verbosity == True:
                            logger.debug("update_response: %s ; update_out_file: %s" %
                                         (update_response, update_out_file))
                        shutil.copyfileobj(update_response, update_out_file)
                except:
                    if verbosity == True:
                        logger.warn("Couldn't download the latest version!")
                        logger.warn("Is the internet online?")
                    print(Fore.RED + "Couldn't download the latest version.")
                    print("Make sure GitHub user content is unblocked, "
                          + "and you have an internet connection.")
                    print("Error 55, pyweather.py")
                    continue
                if verbosity == True:
                    logger.debug("Latest version was saved, filename: %s"
                                 % version_latestFileName)
                print(Fore.YELLOW + "The latest version of PyWeather was downloaded " +
                      "to the base directory of PyWeather, and saved as " +
                      Fore.CYAN + version_latestFileName + Fore.YELLOW + ".")
                continue
            elif downloadLatest == "no":
                if verbosity == True:
                    logger.debug("Not downloading the latest version.")
                print(Fore.YELLOW + "Not downloading the latest version of PyWeather.")
                print("For reference, you can download the latest version of PyWeather at:")
                print(Fore.CYAN + version_latestURL)
                continue
            else:
                if verbosity == True:
                    logger.warn("Input could not be understood!")
                print(Fore.GREEN + "Could not understand what you said.")
                continue
        else:
            if verbosity == True:
                logger.error("PW updater failed. Build comparison below.")
                try:
                    logger.error("local build: %s ; updater build: %s"
                                % (buildnumber, version_buildNumber))
                except:
                    logger.error("Variables are corrupted, or a typo was made.")
                    logger.error("Trying to list variables 1 more time...")
                    try:
                        logger.error("buildnumber: %s" % buildnumber)
                    except:
                        logger.error("Variable buildnumber is corrupt.")
            print(Fore.RED + "PyWeather Updater ran into an error, and couldn't compare versions.")
            print(Fore.RED + "Error 53, pyweather.py")
            continue
    else:
        if verbosity == True:
            logger.warn("Input could not be understood!")
        print(Fore.RED + "Not a valid option.")
        print("")