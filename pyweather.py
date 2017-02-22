# PyWeather 0.2 -> 0.2.1
# (c) 2017 o355, GNU GPL 3.0.
# Powered by Wunderground

# ===========================
#   A few quick notes:
# 1. The internal code is not organized, and it's meant to stay that way.
# I usually design programs with the fact that I'll clean up code, and use
# proper naming conventions/design conventions once the thing works.
# So, for now. Lines of code/comments will be 79+ characters long. Sorry. 
# 2. This program is 25% complete, meaning it's FAR from what it can do.
# 3. There is no setup.py file. Get the API key on your own, and download
# necessary modules through PIP.
# 4. Progress will be slow and steady with PyWeather. Trust me.

# Verbosity works like this (for now)
# Turn on verbosity for, well, verbosity! jsonVerbosity outputs
# the full JSON acquired (aka spams 50 lines of console), so it's
# a separate, and now, more obvious switch.

verbosity = True
jsonVerbosity = True
if verbosity == True:
    import logging
    logger = logging.getLogger('pyweather_0.2beta')
    logger.setLevel(logging.DEBUG)
    logformat = '%(asctime)s | %(levelname)s | %(message)s'
    logging.basicConfig(format=logformat)

import urllib.request
import sys
import json
import time
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
    location = geolocator.geocode(locinput)
    # Since the loading bars interfere with true verbosity logging, we turn
    # them off if verbosity is enabled (it isn't needed)
    if verbosity == False:
        print("[#---------] | 5% |", round(time.time() - firstfetch,1), "seconds", end="\r")
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
    location2 = geocoder.google([latstr, lonstr], method='reverse')
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

if verbosity == True:
    logger.info("Initalize color...")
init()
if verbosity == False:
    print("[##########] | 100% |", round(time.time() - firstfetch,1), "seconds", end="\r")
if verbosity == True:
    logger.info("Printing current conditions...")
    
# --------------- This is where we end parsing, and begin printing. ----------

summaryHourlyIterations = 0

print(Style.BRIGHT + Fore.CYAN + "Here's the weather for: " + Fore.YELLOW + location2.city + ", " + location2.state)
print(Fore.YELLOW + summary_lastupdated)
print("")
print(Fore.YELLOW + "Currently:")
# Currently should have the dew point (at the very least)
print(Fore.CYAN + "Current conditions: " + Fore.YELLOW + summary_overall)
print(Fore.CYAN + "Current temperature: " + Fore.YELLOW + summary_tempf + "°F (" + summary_tempc + "°C)")
print(Fore.CYAN + "And it feels like: " + Fore.YELLOW + summary_feelslikef
      + "°F (" + summary_tempc + "°C)")
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

while True:
    print("")
    print(Fore.GREEN + "What would you like to do?")
    print("You can 'view more current data' [0], 'view more hourly data' [1]")
    print("You can also 'view the 10 day forecast' [2], 'view weather for a different location' [3]")
    print("Or you can 'close PyWeather' [4]" + Fore.YELLOW)
    moreoptions = input("Enter here: ").lower()
    if verbosity == True:
        logger.debug("moreoptions: %s" % moreoptions)
    if (moreoptions == "view more current" or moreoptions == "view more current data" 
        or moreoptions == "view currently" or moreoptions == "view more currently"
        or moreoptions == "currently" or moreoptions == "current"):
        print(Fore.RED + "Loading...")
        print("")
        # I forgot to add Pressure and Dewpoints (rip)
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
        if winddata == True:
            print(Fore.CYAN + "Current wind: " + Fore.YELLOW + summary_windmphstr + 
                  " mph (" + summary_windkphstr + " kph), blowing " + summary_winddir 
                  + " (" + current_windDegrees + " degrees)")
        else:
            print(Fore.YELLOW + "Wind data is not available for this location.")
        print(Fore.CYAN + "Current humidity: " + Fore.YELLOW + summary_humidity)
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
        print(Fore.RED + "Loading...")
        detailedHourlyIterations = 0
        print(Fore.CYAN + "Here's the detailed hourly forecast for: " + Fore.YELLOW + location2.city + ", " + location2.state)
        for hour in hourly_json['hourly_forecast']:
            print("")
            logger.info("We're on iteration: %s" % detailedHourlyIterations)
            hourly_time = hour['FCTTIME']['civil']
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
                or detailedHourlyIterations == 18 or detailedHourlyIterations == 24):
                logger.debug("detailedHourlyIterations: %s" % detailedHourlyIterations)
                logger.debug("Asking user for continuation...")
                try:
                    print("")
                    print(Fore.RED + "Please press enter to view the next 6 hours of hourly data.")
                    print("You can also press Control + C to head back to the input menu.")
                    input()
                    logger.debug("Iterating 6 more times...")
                except KeyboardInterrupt:
                    logger.debug("Exiting to main menu...")
                    break
    elif (moreoptions == "view the 10 day weather forecast" or
          moreoptions == "view the 10 day" or moreoptions == "view 10 day"
          or moreoptions == "view the 10 day"
          or moreoptions == "10 day" or moreoptions == "10 day forecast"
          or moreoptions == "10 day weather forecast"):
        print(Fore.RED + "Loading...")
        print("")
        detailedForecastIterations = 0
        print(Fore.CYAN + "Here's the detailed 10 day forecast for: " + Fore.YELLOW + location2.city + ", " + location2.state)
        for day in forecast10_json['forecast']['simpleforecast']['forecastday']:
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
                logger.deug("forecast10_highc: %s ; forecast10_lowf: %s"
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
            if forecast10_snowTotalCheck == "0.0":
                forecast_snowTotalData = False
            else:
                forecast_snowTotalData = True
            forecast10_snowTotalIn = str(forecast10_snowTotalCheck)
            forecast10_snowTotalCm = str(day['snow_allday']['cm'])
            forecast10_snowDayCheck = day['snow_day']['in']
            if forecast10_snowDayCheck == "0.0":
                forecast_snowDayData = False
            else:
                forecast_snowDayData = True
            forecast10_snowDayIn = str(forecast10_snowDayCheck)
            forecast10_snowDayCm = str(day['snow_day']['cm'])
            forecast10_snowNightCheck = day['snow_night']['in']
            if forecast10_snowNightCheck == "0.0":
                forecast_snowNightData = False
            else:
                forecast_snowNightData = True
            forecast10_snowNightIn = str(day['snow_night']['in'])
            forecast10_snowNightCm = str(day['snow_night']['cm'])
            forecast10_maxWindMPH = str(day['maxwind']['mph'])
            forecast10_maxWindKPH = str(day['maxwind']['kph'])
            forecast10_avgWindMPH = str(day['avewind']['mph'])
            forecast10_avgWindKPH = str(day['avewind']['kph'])
            forecast10_avgWindDir = day['avewind']['dir']
            forecast10_avgWindDegrees = str(day['avewind']['degrees'])
            forecast10_avgHumidity = str(day['avehumidity'])
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
            print(Fore.CYAN + "Total snow: " + Fore.YELLOW +
                  forecast10_snowTotalIn + " in (" + forecast10_snowTotalCm
                  + " cm)")
            print(Fore.CYAN + "Snow during the day: " + Fore.YELLOW + 
                  forecast10_snowDayIn + " in (" + forecast10_snowDayCm
                  + " cm)")
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
                try:
                    print(Fore.RED + "Press enter to view the next 5 days of weather data.")
                    print("You can also press Control + C to return to the input menu.")
                    input()
                except KeyboardInterrupt:
                    break
    elif (moreoptions == "close pyweather" or moreoptions == "close"):
        sys.exit()
    elif (moreoptions == "different location"
          or moreoptions == "view weather for a different location" or
          moreoptions == "view weather different location"):
        print("This feature has been temporarily removed.")
    else:
        print(Fore.RED + "Not a valid option.")
        print("")
    