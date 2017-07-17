# PyWeather - version 0.6.1 beta
# (c) 2017 o355, GNU GPL 3.0.
#
# ==============
# This is beta code. It's not pretty, and I'm not following PEP 8
# guidelines. There will be bugs in this code. I will be attempting to
# follow proper guidelines later down the road.

# <---- Preload starts here ---->

# Begin the import process.
import configparser
import subprocess
import traceback
import sys
try:
    import requests
except ImportEror:
    print("When attempting to import the library requests, we ran into an import error.",
          "Please make sure that requests is installed.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()
import json
import time
import shutil
try:
    from colorama import init, Fore, Style
except ImportError:
    print("When attempting to import the library colorama, we ran into an import error.",
          "Please make sure that colorama is installed.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()
import codecs
import os
from random import randint
try:
    from geopy import GoogleV3
except:
    print("When attempting to import the library geopy, we ran into an import error.",
          "Please make sure that geopy is installed.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()

try:
    from appJar import gui
except:
    print("When attempting to import the library appJar, we ran into an import error.",
          "Please make sure that appJar is installed.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()

# I had issues on OS X 10.12.5 with SSL certs, so HTTP is used instead.
geolocator = GoogleV3(scheme='http')

# Try loading the versioninfo.txt file. If it isn't around, create the file with
# the present version info.

try:
    versioninfo = open('updater//versioninfo.txt').close()
except:
    open('updater//versioninfo.txt', 'w').close()
    with open("updater//versioninfo.txt", 'a') as out:
        out.write("0.6.1 beta")
        out.close()


# Define configparser under config, and read the config.
config = configparser.ConfigParser()
config.read('storage//config.ini')

# See if the config is "provisioned". If it isn't, a KeyError will occur,
# because it's not created. Creative.
try:
    configprovisioned = config.getboolean('USER', 'configprovisioned')
except:
    print("We ran into an error. Full traceback below.")
    traceback.print_exc()
    # Not doing a separate script launch. Doing sys.exit in that script would just continue
    # PyWeather. We ask the user to run the script themselves.
    print("This isn't good. Your config file isn't provisioned.",
          "If you're new to PyWeather, you should run the setup script.",
          "Otherwise, try launching configsetup.py, which is available in the", 
          "storage folder. Press enter to exit.", sep="\n")
    input()
    sys.exit()
    
# Try to parse configuration options.    
try:
    sundata_summary = config.getboolean('SUMMARY', 'sundata_summary')
    almanac_summary = config.getboolean('SUMMARY', 'almanac_summary')
    checkforUpdates = config.getboolean('UPDATER', 'autocheckforupdates')
    verbosity = config.getboolean('VERBOSITY', 'verbosity')
    jsonVerbosity = config.getboolean('VERBOSITY', 'json_verbosity')
    tracebacksEnabled = config.getboolean('TRACEBACK', 'tracebacks')
    prefetch10Day_atStart = config.getboolean('HOURLY', '10dayfetch_atboot')
    user_loopIterations = config.getint('UI', 'detailedInfoLoops')
    user_enterToContinue = config.getboolean('UI', 'show_enterToContinue')
    user_showCompletedIterations = config.getboolean('UI', 
                                                     'show_completedIterations')
    user_forecastLoopIterations = config.getint('UI', 
                                                'forecast_detailedInfoLoops')
    user_showUpdaterReleaseTag = config.getboolean('UPDATER', 
                                                   'show_updaterReleaseTag')
    user_backupKeyDirectory = config.get('KEYBACKUP', 'savedirectory')
    validateAPIKey = config.getboolean('PYWEATHER BOOT', 'validateAPIKey')
    allowGitForUpdating = config.getboolean('UPDATER', 'allowGitForUpdating')
    showAlertsOnSummary = config.getboolean('SUMMARY', 'showAlertsOnSummary')
    showUpdaterReleaseNotes = config.getboolean('UPDATER', 'showReleaseNotes')
    showUpdaterReleaseNotes_uptodate = config.getboolean('UPDATER', 'showReleaseNotes_uptodate')
    showNewVersionReleaseDate = config.getboolean('UPDATER', 'showNewVersionReleaseDate')
    cache_enabled = config.getboolean('CACHE', 'enabled')
    cache_alertstime = config.getint('CACHE', 'alerts_cachedtime')
    cache_alertstime = cache_alertstime * 60
    cache_currenttime = config.getint('CACHE', 'current_cachedtime')
    cache_currenttime = cache_currenttime * 60
    cache_hourlytime = config.getint('CACHE', 'hourly_cachedtime')
    cache_hourlytime = cache_hourlytime * 60
    cache_forecasttime = config.getint('CACHE', 'forecast_cachedtime')
    cache_forecasttime = cache_forecasttime * 60
    cache_almanactime = config.getint('CACHE', 'almanac_cachedtime')
    cache_almanactime = cache_almanactime * 60
    cache_sundatatime = config.getint('CACHE', 'sundata_cachedtime')
    cache_sundatatime = cache_sundatatime * 60
    user_alertsUSiterations = config.getint('UI', 'alerts_usiterations')
    user_alertsEUiterations = config.getint('UI', 'alerts_euiterations')
    user_radarImageSize = config.get('RADAR GUI', 'radar_imagesize')
    radar_bypassconfirmation = config.getboolean('RADAR GUI', 'bypassconfirmation')
    
except:
    # If it fails (typo or code error), we set all options to default.
    print("When attempting to load your configuration file, an error",
          "occurred. This could of happened because of a typo, or an error",
          "in the code. Make sure there aren't any typos in the config file,",
          "and check the traceback below (report it to GitHub for extra internet",
          "points).", sep="\n")
    traceback.print_exc()
    sundata_summary = False
    almanac_summary = False
    verbosity = False
    jsonVerbosity = False
    checkforUpdates = False
    tracebacksEnabled = False
    prefetch10Day_atStart = False
    user_loopIterations = 6
    user_enterToContinue = False
    user_showCompletedIterations = False
    user_forecastLoopIterations = 5
    user_showUpdaterReleaseTag = False
    user_backupKeyDirectory = 'backup//'
    validateAPIKey = True
    allowGitForUpdating = False
    showAlertsOnSummary = True
    showUpdaterReleaseNotes = True
    showUpdaterReleaseNotes_uptodate = False
    showNewVersionReleaseDate = True
    cache_enabled = True
    cache_alertstime = 5
    cache_currenttime = 10
    cache_hourlytime = 60
    cache_forecasttime = 60
    cache_almanactime = 240
    cache_sundatatime = 480
    user_alertsEUiterations = 2
    user_alertsUSiterations = 1
    user_radarImageSize = "normal"
    radar_bypassconfirmation = False

# Import logging, and set up the logger.
import logging
logger = logging.getLogger(name='pyweather_0.6beta')
logformat = '%(asctime)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logformat)

# Set the logger levels by design. Critical works as a non-verbosity
# option, as I made sure not to have any critical messages.
if verbosity:
    logger.setLevel(logging.DEBUG)
elif tracebacksEnabled:
    logger.setLevel(logging.ERROR)
else:
    logger.setLevel(logging.CRITICAL)
    
# List config options for those who have verbosity enabled.    
logger.info("PyWeather 0.6 indev now starting.")
logger.info("Configuration options are as follows: ")
logger.debug("sundata_summary: %s ; almanac_summary: %s" %
             (sundata_summary, almanac_summary))
logger.debug("checkforUpdates: %s ; verbosity: %s" %
             (checkforUpdates, verbosity))
logger.debug("jsonVerbosity: %s ; tracebacksEnabled: %s" %
             (jsonVerbosity, tracebacksEnabled))
logger.debug("prefetch10Day_atStart: %s ; user_loopIterations: %s" 
             % (prefetch10Day_atStart, user_loopIterations))
logger.debug("user_enterToContinue: %s ; user_showCompletedIterations: %s"
             % (user_enterToContinue, user_showCompletedIterations))
logger.debug("user_forecastLoopIterations: %s ; user_showUpdaterReleaseTag: %s"
             % (user_forecastLoopIterations, user_showUpdaterReleaseTag))
logger.debug("user_backupKeyDirectory: %s ; validateAPIKey: %s"
             % (user_backupKeyDirectory, validateAPIKey))
logger.debug("allowGitForUpdating: %s ; showAlertsOnSummary: %s"
             % (allowGitForUpdating, showAlertsOnSummary))
logger.debug("showUpdaterReleaseNotes_uptodate: %s ; showNewVersionReleaseDate: %s"
             % (showUpdaterReleaseNotes_uptodate, showNewVersionReleaseDate))
logger.debug("showUpdaterReleaseNotes: %s ; cache_enabled: %s" %
             (showUpdaterReleaseNotes, cache_enabled))
logger.debug("cache_alertstime: %s ; cache_currenttime: %s" %
             (cache_alertstime, cache_currenttime))
logger.debug("cache_hourlytime: %s ; cache_forecasttime: %s" %
             (cache_hourlytime, cache_forecasttime))
logger.debug("cache_almanactime: %s ; cache_sundatatime: %s" %
             (cache_almanactime, cache_sundatatime))
logger.debug("user_alertsUSiterations: %s ; user_alertsEUiterations: %s" %
             (user_alertsUSiterations, user_alertsEUiterations))
logger.debug("user_radarImagesize: %s ; radar_bypassconfirmation: %s" %
             (user_radarImageSize, radar_bypassconfirmation))

logger.info("Setting gif x and y resolution for radar...")
# Set the size of the radar window.
if user_radarImageSize == "extrasmall":
    radar_gifx = "320"
    radar_gify = "240"
elif user_radarImageSize == "small":
    radar_gifx = "480"
    radar_gify = "360"
elif user_radarImageSize == "normal":
    radar_gifx = "640"
    radar_gify = "480"
elif user_radarImageSize == "large":
    radar_gifx = "960"
    radar_gify = "720"
elif user_radarImageSize == "extralarge":
    radar_gifx = "1280"
    radar_gify = "960"
else:
    radar_gifx = "640"
    radar_gify = "480"

logger.info("Defining custom functions...")

def printException():
    # We use tracebacksEnabled here, as it just worked.
    if tracebacksEnabled == True:
        print("Here's the full traceback (for bug reporting):")
        traceback.print_exc()
        
def printException_loggerwarn():
    # Same idea. If the print_exc was in just logger.warn, it'd print even
    # if verbosity was disabled.
    if verbosity == True:
        logger.warning("Snap! We hit a non-critical error. Here's the traceback.")
        traceback.print_exc()
        
def radar_clearImages():
    logger.debug("clearing temporary images...")
    logger.debug("removing r10.gif...")
    try:
        os.remove("temp//r10.gif")
    except:
        printException_loggerwarn()
    logger.debug("removing r20.gif...")   
    try:
        os.remove("temp//r20.gif")
    except:
        printException_loggerwarn()
    logger.debug("removing r40.gif...")
    try:
        os.remove("temp//r40.gif")
    except:
        printException_loggerwarn()
    logger.debug("removing r60.gif...")
    try:
        os.remove("temp//r60.gif")
    except:
        printException_loggerwarn()
    logger.debug("removing r80.gif...")
    try:
        os.remove("temp//r80.gif")
    except:
        printException_loggerwarn()
    logger.debug("removing r100.gif...")   
    try:
        os.remove("temp//r100.gif")
    except:
        printException_loggerwarn()


        
logger.info("Defining requests classes...")

urlheader = {'user-agent': 'pyweather-0.6.1beta/apifetcher'}

# Declare historical cache dictionary
historical_cache = {}
logger.debug("historical_cache: %s" % historical_cache)

logger.debug("Begin API keyload...")
# Load the API key.
try:
    apikey_load = open('storage//apikey.txt')
    logger.debug("apikey_load = %s" % apikey_load)
    apikey = apikey_load.read()
except FileNotFoundError:
    print("Your primary API key couldn't be loaded, as PyWeather ran into",
          "an error when attempting to access it. Make sure that your primary key",
          "file can be accessed (usually found at storage/apikey.txt. Make sure it has",
          "proper permissions, and that it exists). In the mean time, we're attempting",
          "to load your backup API key.", sep="\n")
    # If the key isn't found, try to find the second key.
    try:
        apikey2_load = open(user_backupKeyDirectory + "backkey.txt")
        logger.debug("apikey2_load: %s" % apikey2_load)
        apikey = apikey2_load.read()
        logger.debug("apikey: %s" % apikey)
        print("Loaded your backup key successfully!")
    except FileNotFoundError:
        print("When attempting to access your backup API key, PyWeather ran into",
              "an error. Make sure that your backup key file is accessible (wrong",
              "permissions and the file not existing are common issues).", sep="\n")
        logger.warning("Couldn't load the primary or backup key text file!" +
                    " Does it exist?")
        print("Press enter to continue.")
        input()
        sys.exit()
        
if validateAPIKey == True:
    # If the primary API key is valid, and got through the check,
    # this is here for those who validate their API key, and making sure
    # we can find their backup key.
    logger.info("Making sure the backup key can be found.")
    try:
        apikey2_load = open(user_backupKeyDirectory + "backkey.txt")
        logger.debug("apikey2_load: %s" % apikey2_load)
        apikey2 = apikey2_load.read()
        backupKeyLoaded = True
        logger.debug("apikey2: %s ; backupKeyLoaded: %s" %
                     (apikey2, backupKeyLoaded))
    except:
        logger.warn("Could not load the backup key for future validation.")
        # If we can't find it, a variable is set for future use.
        backupKeyLoaded = False
        logger.debug("backupKeyLoaded: %s" % backupKeyLoaded)
else:
    backupKeyLoaded = False

logger.debug("apikey = %s" % apikey)

# Version info gets defined here.

buildnumber = 61
buildversion = '0.6.1 beta'

# Refresh flag variables go here.
refresh_currentflagged = False
refresh_alertsflagged = False
refresh_hourly36flagged = False
refresh_hourly10flagged = False
refresh_forecastflagged = False
refresh_almanacflagged = False
refresh_sundataflagged = False

logger.debug("refresh_currentflagged: %s ; refresh_alertsflagged: %s" %
             (refresh_currentflagged, refresh_alertsflagged))
logger.debug("refresh_hourly36flagged: %s ; refresh_hourly10flagged: %s" %
             (refresh_hourly36flagged, refresh_hourly10flagged))
logger.debug("refresh_forecastflagged: %s ; refresh_almanacflagged: %s" %
             (refresh_forecastflagged, refresh_almanacflagged))
logger.debug("refresh_sundataflagged: %s" % refresh_sundataflagged)
 
if checkforUpdates == True:
    reader2 = codecs.getreader("utf-8")
    try:
        versioncheck = requests.get("https://raw.githubusercontent.com/o355/"
                                + "pyweater/master/updater/versioncheck.json")
    except:
        print("When attempting to check for updates, PyWeather couldn't",
              "fetch the .json for parsing. If you're on a network with a",
              "filter, try asking your IT admin to unblock:",
              "'https://raw.githubusercontent.com'. Otherwise, make",
              "sure you have a valid internet connection.", sep="\n")
        printException()
        print("Press enter to continue.")
        input()
        sys.exit()
    # Parse all the lovely .json info.
    versionJSON = json.loads(versioncheck.text)
    version_buildNumber = float(versionJSON['updater']['latestbuild'])
    logger.debug("reader2: %s ; versioncheck: %s" %
                 (reader2, versioncheck))
    if jsonVerbosity == True:
        logger.debug("versionJSON: %s" % versionJSON)
    logger.debug("version_buildNumber: %s" % version_buildNumber)
    version_latestVersion = versionJSON['updater']['latestversion']
    version_latestURL = versionJSON['updater']['latesturl']
    version_latestFileName = versionJSON['updater']['latestfilename']
    version_latestReleaseDate = versionJSON['updater']['releasedate']
    logger.debug("version_latestVersion: %s ; version_latestURL: %s"
                 % (version_latestVersion, version_latestURL))
    logger.debug("version_latestFileName: %s ; version_latestReleaseDate: %s"
                 % (version_latestFileName, version_latestReleaseDate))
    if buildnumber < version_buildNumber:
        # Print if we're out of date.
        logger.info("PyWeather is not up to date.")
        print("PyWeather is not up to date. You have version " + buildversion +
              ", and the latest version is " + version_latestVersion + ".")
        print("")

# Define about variables here.
logger.info("Defining about variables...")
about_buildnumber = "61"
about_version = "0.6.1 beta"
about_releasedate = "May 29, 2017"
about_maindevelopers = "o355"
logger.debug("about_buildnumber: %s ; about_version: %s" %
             (about_buildnumber, about_version))
logger.debug("about_releasedate: %s ; about_maindevelopers: %s" %
             (about_releasedate, about_maindevelopers))
about_contributors = "gsilvapt, ModoUnreal"
about_releasetype = "beta"
about_librariesinuse = "Colorama, Geopy, Requests"
logger.debug("about_contributors: %s ; about_releasetype: %s" %
             (about_contributors, about_releasetype))
logger.debug("about_librariesinuse: %s" % about_librariesinuse)
# I understand this goes against Wunderground's ToS for logo usage.
# Can't do much in a terminal.

print("Hey, welcome to PyWeather!")
print("Below, enter a location to check the weather for that location!")
locinput = input("Input here: ")
print("Checking the weather, it'll take a few seconds!")


# Start the geocoder. If we don't have a connection, exit nicely.
# After we get location data, store it in latstr and lonstr, and store
# it in the table called loccords.

firstfetch = time.time()
logger.info("Start geolocator...")
try:
    location = geolocator.geocode(locinput, language="en", timeout=20)
    # Since the loading bars interfere with true verbosity logging, we turn
    # them off if verbosity is enabled (it isn't needed)
    # :/
    if verbosity == False:
        print("[#---------] | 1% |", round(time.time() - firstfetch,1), 
              "seconds", end="\r")
except:
    logger.warn("No connection to Google's geocoder!")
    print("When attempting to access Google's geocoder, PyWeather ran into an error.",
          "A few things could of happened. If you're on a filter, make sure Google's",
          "geocoder is unblocked. Otherwise, Make sure your internet connection is online.",
          sep="\n")
    printException()
    print("Press enter to continue.")
    input()
    sys.exit()
logger.debug("location = %s" % location)

try:
    latstr = str(location.latitude)
    lonstr = str(location.longitude)
except AttributeError:
    logger.warning("No lat/long was provided by Google! Bad location?")
    print("When attempting to parse the location inputted, PyWeather",
          "ran into an error. Make sure that the location you entered is",
          "valid, and don't attempt to see the weather at Mark Watney's base.",
          sep="\n")
    printException()
    print("Press enter to continue.")
    input()
    sys.exit()
logger.debug("Latstr: %s ; Lonstr: %s" % (latstr, lonstr))
loccoords = [latstr, lonstr]
logger.debug("Loccoords: %s" % loccoords)
logger.info("End geolocator...")
logger.info("Start API var declare...")

# Declare the API URLs with the API key, and latitude/longitude strings from earlier.

currenturl = 'http://api.wunderground.com/api/' + apikey + '/conditions/q/' + latstr + ',' + lonstr + '.json'
f10dayurl = 'http://api.wunderground.com/api/' + apikey + '/forecast10day/q/' + latstr + ',' + lonstr + '.json'
hourlyurl = 'http://api.wunderground.com/api/' + apikey + '/hourly/q/' + latstr + ',' + lonstr + '.json'
tendayurl = 'http://api.wunderground.com/api/' + apikey + '/hourly10day/q/' + latstr + ',' + lonstr + '.json'
astronomyurl = 'http://api.wunderground.com/api/' + apikey + '/astronomy/q/' + latstr + ',' + lonstr + '.json'
almanacurl = 'http://api.wunderground.com/api/' + apikey + '/almanac/q/' + latstr + ',' + lonstr + '.json'
alertsurl = 'http://api.wunderground.com/api/' + apikey + '/alerts/q/' + latstr + ',' + lonstr + '.json'

if verbosity == False:
    print("[##--------] | 6% |", round(time.time() - firstfetch,1), "seconds", end="\r")
logger.debug("currenturl: %s" % currenturl)
logger.debug("f10dayurl: %s" % f10dayurl)
logger.debug("hourlyurl: %s" % hourlyurl)
logger.debug("tendayurl: %s" % tendayurl)
logger.debug("astronomyurl: %s" % astronomyurl)
logger.debug("almanacurl: %s" % almanacurl)
logger.info("End API var declare...")
logger.info("Start codec change...")

# Due to Python being Python, we have to get the UTF-8 reader 
# to properly parse the JSON we got.
reader = codecs.getreader("utf-8")
if verbosity == False:
    print("[##--------] | 8% |", round(time.time() - firstfetch,1), "seconds", end="\r")
logger.debug("reader: %s" % reader)
logger.info("End codec change...")
logger.info("Start API fetch...")

# If a user requested their API key to be validated, and the backup key
# can be loaded (as was checked earlier), we do it here.
if validateAPIKey == False and backupKeyLoaded == True:
    logger.info("Beginning API key validation.")
    testurl = 'http://api.wunderground.com/api/' + apikey + '/conditions/q/NY/New_York.json'
    logger.debug("testurl: %s" % testurl)
    try:
        testJSON = requests.get(testurl)
        logger.debug("Acquired test JSON, end result: %s" % testJSON)
    except:
        logger.warn("Cannot connect to the API! Is the internet down?")
        print("When attempting to validate your primary API key, PyWeather ran",
              "into an error when accessing Wunderground's API. If you're",
              "on a network with a filter, make sure that",
              "'api.wunderground.com' is unblocked. Otherwise, make sure you",
              "have an internet connection.", sep="\n")
        printException()
        print("Press enter to exit.")
        input()
        sys.exit()
    if verbosity == False:
        print("[##--------] | 9% |", round(time.time() - firstfetch,1), "seconds", end="\r")
    test_json = json.loads(testJSON.text)
    if jsonVerbosity == True:
        logger.debug("test_json: %s" % test_json)
    try:
        test_conditions = str(test_json['current_observation']['temp_f'])
        logger.debug("test_conditions: %s" % test_conditions)
        logger.info("API key is valid!")
    except:
        logger.warn("API key is NOT valid. Attempting to revalidate API key...")
        if backupKeyLoaded == True:
            logger.info("Beginning backup API key validation.")
            testurl = 'http://api.wunderground.com/api/' + apikey2 + '/conditions/q/NY/New_York.json'
            logger.debug("testurl: %s" % testurl)
            # What if the user's internet connection was alive during the 1st
            # validation, but not the 2nd? That's why this is here.
            try:
                testJSON = requests.get(testurl)
                logger.debug("Acquired test JSON, end result: %s" % testJSON)
            except:
                print("When attempting to validate your backup API key, PyWeather ran",
                      "into an error. If you're on a network with a filter, make sure",
                      "that 'api.wunderground.com' is unblocked. Otherwise, make sure you",
                      "have an internet conection, that that your internet connection's latency",
                      "isn't 1.59 days.", sep="\n")
                printException()
                print("Press enter to exit.")
                input()
                sys.exit()
            if verbosity == False:
                print("[##--------] | 12% |", round(time.time() - firstfetch,1), "seconds", end="\r")
            test_json = json.loads(testJSON.text)
            if jsonVerbosity == True:
                logger.debug("test_json: %s" % test_json)
            try:
                test_conditions = str(test_json['current_observation']['temp_f'])
                logger.debug("test_conditions: %s" % test_conditions)
                logger.info("Backup API key is valid!")
                apikey = apikey2
                logger.debug("apikey = apikey2. apikey: %s" % apikey)
                logger.debug("Redefining URL variables...")
                currenturl = 'http://api.wunderground.com/api/' + apikey + '/conditions/q/' + latstr + ',' + lonstr + '.json'
                f10dayurl = 'http://api.wunderground.com/api/' + apikey + '/forecast10day/q/' + latstr + ',' + lonstr + '.json'
                hourlyurl = 'http://api.wunderground.com/api/' + apikey + '/hourly/q/' + latstr + ',' + lonstr + '.json'
                tendayurl = 'http://api.wunderground.com/api/' + apikey + '/hourly10day/q/' + latstr + ',' + lonstr + '.json'
                astronomyurl = 'http://api.wunderground.com/api/' + apikey + '/astronomy/q/' + latstr + ',' + lonstr + '.json'
                almanacurl = 'http://api.wunderground.com/api/' + apikey + '/almanac/q/' + latstr + ',' + lonstr + '.json'
                logger.debug("currenturl: %s ; f10dayurl: %s" %
                             (currenturl, f10dayurl))
                logger.debug("hourlyurl: %s ; tendayurl: %s" %
                             (hourlyurl, tendayurl))
                logger.debug("astronomyurl: %s ; almanacurl: %s" %
                             (astronomyurl, almanacurl))
            except:
                logger.warn("Backup API key could not be validated!")
                print("Your primary and backup API key(s) could not be validated.",
                      "Make sure that your primary API key is valid, either because of a typo",
                      "or some other reason. Installing Gentoo may help with the validation",
                      "of your API key.", sep="\n")
                printException()
                print("Press enter to exit.")
                input()
                sys.exit()
        elif backupKeyLoaded == False:
            print("When attempting to validate your API key, your primary key",
                  "couldn't be validated, and your backup key wasn't able to",
                  "load at boot. Make sure that your primary API key is valid,",
                  "and that your backup API key can be accessed by PyWeather."
                  "Press enter to exit.", sep="\n")
            input()
            sys.exit()
        else:
            logger.warn("Backup key couldn't get loaded!")
            print("Your primary API key couldn't be validated, and your",
                  "backup key could not be loaded at startup.",
                  "Please make sure your primary API key is valid, and that",
                  "your backup API key can be accessed (common mistakes include",
                  "wrong permissions, and the file not existing).",
                  "Press enter to exit.", sep="\n")
            input()
            sys.exit()

# Fetch the JSON file using urllib.request, store it as a variable.
try:
    # For sanity's sake, refetching the current JSON is probably the better thing to do.
    summaryJSON = requests.get(currenturl)
    cachetime_current = time.time()
    if verbosity == False:
        print("[##--------] | 15% |", round(time.time() - firstfetch,1), "seconds", end="\r")
    logger.debug("Acquired summary JSON, end result: %s" % summaryJSON)
    forecast10JSON = requests.get(f10dayurl)
    cachetime_forecast = time.time()
    if verbosity == False:
        print("[###-------] | 24% |", round(time.time() - firstfetch,1), "seconds", end="\r")
    logger.debug("Acquired forecast 10day JSON, end result: %s" % forecast10JSON)
    if sundata_summary == True:
        cachetime_sundata = time.time()
        sundataJSON = requests.get(astronomyurl)
        if verbosity == False:
            print("[###-------] | 32% |", round(time.time() - firstfetch,1), "seconds", end="\r")
        logger.debug("Acquired astronomy JSON, end result: %s" % sundataJSON)
    if prefetch10Day_atStart == True:
        # Masking the JSON as hourlyJSON makes life a LOT easier.
        hourly10JSON = requests.get(tendayurl)
        # Special situation: We separate the 3-day/10-day hourly caches, but
        # they use the same cache timer. 
        cachetime_hourly10 = time.time()
        logger.info("Acquiring the 10 day hourly JSON, as specified.")
        tenday_prefetched = True
        logger.debug("tenday_prefetched: %s" % tenday_prefetched)
        logger.debug("Acquired 10 day hourly JSON, end result: %s" % hourly10JSON)
        hourly36JSON = requests.get(hourlyurl)
        cachetime_hourly36 = time.time()
        logger.debug("Acquired 36 hour hourly JSON, end result: %s" % hourly36JSON)
    else:   
        hourly36JSON = requests.get(hourlyurl)
        cachetime_hourly36 = time.time()
        tenday_prefetched = False
        logger.debug("tenday_prefetched: %s" % tenday_prefetched)
        logger.debug("Acquired 36 hour hourly JSON, end result: %s" % hourly36JSON)
    if verbosity == False:
        print("[####------] | 40% |", round(time.time() - firstfetch,1), "seconds", end="\r")
    if almanac_summary == True:
        almanacJSON = requests.get(almanacurl)
        cachetime_almanac = time.time()
        if verbosity == False:
            print("[#####-----] | 49% |", round(time.time() - firstfetch,1), "seconds", end="\r")
        logger.debug("Acquired almanac JSON, end result: %s" % almanacJSON)
    if showAlertsOnSummary == True:
        alertsJSON = requests.get(alertsurl)
        cachetime_alerts = time.time()
        alertsPrefetched = True
        if verbosity == False:
            print("[#####-----] | 52% |", round(time.time() - firstfetch,1), "seconds", end="\r")
        logger.debug("Acquired alerts JSON, end result: %s" % alertsJSON)
    else:
        alertsPrefetched = False
except:
    logger.warn("No connection to the API!! Is the connection offline?")
    print("When PyWeather attempted to fetch the .json files to show you the weather,",
          "PyWeather ran into an error. If you're on a network with a filter, make sure",
          "'api.wunderground.com' is unblocked. Otherwise, make sure you have an internet",
          "connection.", sep="\n")
    printException()
    print("Press enter to continue.")
    input()
    sys.exit()
    
# And we parse the json using json.load.
logger.info("End API fetch...")
logger.info("Start JSON load...")
if verbosity == False:
    print("[#####-----] | 55% |", round(time.time() - firstfetch,1), "seconds", end="\r")
current_json = json.loads(summaryJSON.text)
if jsonVerbosity == True:
    logger.debug("current_json loaded with: %s" % current_json)
if verbosity == False:
    print("[######----] | 63% |", round(time.time() - firstfetch,1), "seconds", end="\r")
forecast10_json = json.loads(forecast10JSON.text)
if jsonVerbosity == True:
    logger.debug("forecast10_json loaded with: %s" % forecast10_json)
if verbosity == False:
    print("[#######---] | 71% |", round(time.time() - firstfetch,1), "seconds", end="\r")
    

if prefetch10Day_atStart == True: 
    hourly10_json = json.loads(hourly10JSON.text)
    if jsonVerbosity == True:
        logger.debug("hourly10_json loaded with: %s" % hourly10_json)
    hourly36_json = json.loads(hourly36JSON.text)
    if jsonVerbosity == True:
        logger.debug("hourly36_json loaded with: %s" % hourly36_json)
else:
    hourly36_json = json.loads(hourly36JSON.text)
    if jsonVerbosity == True:
        logger.debug("hourly36_json loaded with: %s" % hourly36_json)
if sundata_summary == True:
    astronomy_json = json.loads(sundataJSON.text)
    if verbosity == False:
        print("[########--] | 81% |", round(time.time() - firstfetch,1), "seconds", end="\r")
    if jsonVerbosity == True:
        logger.debug("astronomy_json loaded with: %s" % astronomy_json)
if almanac_summary == True:
    almanac_json = json.loads(almanacJSON.text)
    if verbosity == False:
        print("[#########-] | 87% |", round(time.time() - firstfetch,1), "seconds", end="\r")
    if jsonVerbosity == True:
        logger.debug("almanac_json loaded with: %s" % almanac_json)
if showAlertsOnSummary == True:
    alerts_json = json.loads(alertsJSON.text)
    if verbosity == False:
        print("[#########-] | 90% |", round(time.time() - firstfetch,1), "seconds", end="\r")
    if jsonVerbosity == True:
        logger.debug("alerts_json loaded with: %s" % alerts_json)
logger.info("Some amount of JSONs loaded...")

# The 2nd geocoder was removed, as geopy can also do reverse information.



# Parse the current weather!

summary_overall = current_json['current_observation']['weather']
summary_lastupdated = current_json['current_observation']['observation_time']
    
# While made for the US, metric units will also be tagged along.
summary_tempf = str(current_json['current_observation']['temp_f'])
summary_tempc = str(current_json['current_observation']['temp_c'])
# Since parsing the json spits out a float as the summary, a conversion to string is
# necessary to properly display it in the summary.
# summary_dewpointf = current_json['current_observation']
summary_humidity = str(current_json['current_observation']['relative_humidity'])
logger.debug("summary_overall: %s ; summary_lastupdated: %s"
             % (summary_overall, summary_lastupdated))
logger.debug("summary_tempf: %s ; summary_tempc: %s"
             % (summary_tempf, summary_tempc))
summary_winddir = current_json['current_observation']['wind_dir']
summary_windmph = current_json['current_observation']['wind_mph']
summary_windmphstr = str(summary_windmph)
summary_windkph = current_json['current_observation']['wind_kph']
logger.debug("summary_winddir: %s ; summary_windmph: %s"
             % (summary_winddir, summary_windmph))
logger.debug("summary_windmphstr: %s ; summary_windkph: %s"
             % (summary_windmphstr, summary_windkph))
summary_windkphstr = str(summary_windkph)
logger.debug("summary_windkphstr: %s" % summary_windkphstr)
if verbosity == False:
    print("[##########] | 97% |", round(time.time() - firstfetch,1), "seconds", end="\r")
# Since some PWS stations on WU don't have a wind meter, this method will check if we should display wind data.
# WU lists the MPH at -9999 if there is no wind data.
# This method is probably reliable, but I need to see if it'll work by testing it work PWS stations around my area.
windcheck = float(summary_windmph)
windcheck2 = float(summary_windkph)
logger.debug("windcheck: %s ; windcheck2: %s" 
             % (windcheck, windcheck2))
if windcheck == -9999:
    winddata = False
    logger.warn("No wind data available!")
elif windcheck2 == -9999:
    winddata = False
    logger.warn("No wind data available!")
else:
    winddata = True
    logger.info("Wind data is available.")

summary_feelslikef = str(current_json['current_observation']['feelslike_f'])
summary_feelslikec = str(current_json['current_observation']['feelslike_c'])
summary_dewPointF = str(current_json['current_observation']['dewpoint_f'])
summary_dewPointC = str(current_json['current_observation']['dewpoint_c'])
logger.debug("summary_feelslikef: %s ; summary_feelslikec: %s"
             % (summary_feelslikef, summary_feelslikec))
logger.debug("summary_dewPointF: %s ; summary_dewPointC: %s"
             % (summary_dewPointF, summary_dewPointC))
    
sundata_prefetched = False
almanac_prefetched = False
logger.debug("sundata_prefetched: %s ; almanac_prefetched: %s"
             % (sundata_prefetched, almanac_prefetched))
# <--- Sun data gets parsed here, if the option for showing it in the summary
# is enabled in the config. --->

if sundata_summary == True:
    logger.info("Parsing sun information...")
    SR_minute = int(astronomy_json['moon_phase']['sunrise']['minute'])
    SR_hour = int(astronomy_json['moon_phase']['sunrise']['hour'])
    logger.debug("SR_minute: %s ; SR_hour: %s" %
                (SR_minute, SR_hour))
    if SR_hour == 0:
        logger.debug("Sunrise hour = 0. Prefixing AM, 12-hr correction...")
        SR_hour = "12"
        SR_minute = str(SR_minute).zfill(2)
        sunrise_time = SR_hour + ":" + SR_minute + " AM"
        logger.debug("SR_hour : %s ; SR_minute: %s" %
                    (SR_hour, SR_minute))
        logger.debug("sunrise_time: %s" % sunrise_time)
    elif SR_hour > 12:
        logger.info("Sunrise time > 12. Starting 12hr time conversion...")
        SR_hour = SR_hour - 12
        SR_hour = str(SR_hour)
        # For filling in extra zeros (when the minute is >10), I prefer using .zfill.
        # The code looks much nicer and more readable versus the %02d method.
        SR_minute = str(SR_minute).zfill(2)
        sunrise_time = SR_hour + ":" + SR_minute + " PM"
        logger.debug("SR_hour: %s ; SR_minute: %s"
                    % (SR_hour, SR_minute))
        logger.debug("sunrise_time: %s" % sunrise_time)
    elif SR_hour == 12:
        logger.info("Sunrise time = 12. Prefixing PM...")
        SR_hour = str(SR_hour)
        SR_minute = str(SR_minute).zfill(2)
        sunrise_time = SR_hour + ":" + SR_minute + " PM"
        logger.debug("SR_hour: %s ; SR_minute: %s" %
                    (SR_hour, SR_minute))
        logger.debug("sunrise_time: %s" % sunrise_time)
    else:
        logger.info("Sunrise time < 12. Prefixing AM...")
        SR_hour = str(SR_hour)
        SR_minute = str(SR_minute).zfill(2)
        sunrise_time = SR_hour + ":" + SR_minute + " AM"
        logger.debug("SR_hour: %s ; SR_minute: %s" %
                    (SR_hour, SR_minute))
        logger.debug("sunrise_time: %s" % sunrise_time)
            

    SS_minute = int(astronomy_json['moon_phase']['sunset']['minute'])
    SS_hour = int(astronomy_json['moon_phase']['sunset']['hour'])
    logger.debug("SS_minute: %s ; SS_hour: %s" %
                 (SS_minute, SS_hour))
    if SS_hour == 0:
        logger.debug("Sunset hour = 0. Prefixing AM, 12-hr correction...")
        SS_hour = "0"
        SS_minute = str(SS_minute).zfill(2)
        sunset_time = SS_hour + ":" + SS_minute + " AM"
        logger.debug("SS_hour: %s ; SS_minute: %s" %
                    (SS_hour, SS_minute))
        logger.debug("sunset_time: %s" % sunset_time)
    elif SS_hour > 12:
        logger.info("Sunset time > 12. Starting 12hr time conversion...")
        SS_hour = SS_hour - 12
        SS_hour = str(SS_hour)
        SS_minute = str(SS_minute).zfill(2)
        sunset_time = SS_hour + ":" + SS_minute + " PM"
        logger.debug("SS_hour: %s ; SS_minute: %s"
                     % (SS_hour, SS_minute))
        logger.debug("sunset_time: %s" % sunset_time)
    elif SS_hour == 12:
        logger.info("Sunset time = 12. Prefixing PM...")
        SS_hour = str(SS_hour)
        SS_minute = str(SS_minute).zfill(2)
        sunset_time = SS_hour + ":" + SS_minute + " PM"
        logger.debug("SS_hour: %s ; SS_minute: %s"
                    % (SS_hour, SS_minute))
        logger.debug("sunset_time: %s" % sunset_time)
    else:
        logger.info("Sunset time < 12. Prefixing AM...")
        SS_hour = str(SS_hour)
        SS_minute = str(SS_minute).zfill(2)
        sunset_time = SS_hour + ":" + SS_minute + " AM"
        logger.debug("SS_hour: %s ; SS_minute: %s" %
                     (SS_hour, SS_minute))
        logger.debug("sunset_time: %s" % sunset_time)
    sundata_prefetched = True
    logger.debug("sundata_prefetched: %s" % sundata_prefetched)

# <--- Almanac data gets parsed here, if showing almanac data is
# enabled in the config. --->

if almanac_summary == True:
    logger.debug("Parsing almanac data...")
    almanac_airportCode = almanac_json['almanac']['airport_code']
    almanac_normalHighF = str(almanac_json['almanac']['temp_high']['normal']['F'])
    almanac_normalHighC = str(almanac_json['almanac']['temp_high']['normal']['C'])
    almanac_recordHighF = str(almanac_json['almanac']['temp_high']['record']['F'])
    logger.debug("almanac_airportCode: %s ; almanac_normalHighF: %s"
                 % (almanac_airportCode, almanac_normalHighF))
    logger.debug("almanac_normalHighC: %s ; almanac_recordHighF: %s"
                 % (almanac_normalHighC, almanac_recordHighF))
    almanac_recordHighC = str(almanac_json['almanac']['temp_high']['record']['C'])
    almanac_recordHighYear = str(almanac_json['almanac']['temp_high']['recordyear'])
    almanac_normalLowF = str(almanac_json['almanac']['temp_low']['normal']['F'])
    almanac_normalLowC = str(almanac_json['almanac']['temp_low']['normal']['C'])
    logger.debug("almanac_recordHighC: %s ; almanac_recordHighYear: %s"
                 % (almanac_recordHighC, almanac_recordHighYear))
    logger.debug("almanac_normalLowF: %s ; almanac_normalLowC: %s"
                 % (almanac_normalLowF, almanac_normalLowC))
    almanac_recordLowF = str(almanac_json['almanac']['temp_low']['record']['F'])
    almanac_recordLowC = str(almanac_json['almanac']['temp_low']['record']['C'])
    almanac_recordLowYear = str(almanac_json['almanac']['temp_low']['recordyear'])
    almanac_prefetched = True
    logger.debug("almanac_recordLowF: %s ; almanac_recordLowC: %s"
                 % (almanac_recordLowF, almanac_recordLowC))
    logger.debug("almanac_recordLowYear: %s ; almanac_prefetched: %s"
                 % (almanac_recordLowYear, almanac_prefetched))

logger.info("Initalize color...")
init()
if verbosity == False:
    print("[##########] | 100% |", round(time.time() - firstfetch,1), "seconds", end="\r")
logger.info("Printing current conditions...")
    
# <--------------- This is where we end parsing, and begin printing. ---------->

summaryHourlyIterations = 0

print(Style.BRIGHT + Fore.YELLOW + "Here's the weather for: " + Fore.CYAN + str(location))
print(Fore.YELLOW + summary_lastupdated)
print("")

# Attempt to parse alerts here.
if showAlertsOnSummary == True:
    try:
        # We attempt to parse a Meteoalarm first, as it has unique
        # data names, or whatever they're called.
        for data in alerts_json['alerts']:
            # If the alert isn't an EU alert, a KeyError is issued, and
            # we then try to parse a US alert.
            logger.info("Attempting to parse EU alert first...")
            alerts_description = data['wtype_meteoalarm_name']
            alerts_expiretime = data['expires']
            # By now, if the alert wasn't an EU alert, the error would of been
            # caught. So, we add this. When a user wants detailed alert information,
            # instead of redoing this catching, the type is used for things to be easy.
            alerts_type = "EU"
            logger.debug("alerts_description: %s ; alerts_expiretime: %s"
                         % (alerts_description, alerts_expiretime))
            logger.debug("alerts_type: %s" % alerts_type)
            print(Fore.RED + "** A " + alerts_description + " Meteoalarm has been issued" +
                  " for " + str(location) + ",", 
                  "and is in effect until " + alerts_expiretime + ". **", sep="\n")
            print("")
    except:
        try:
            for data in alerts_json['alerts']:
                logger.info("Failed to parse EU alert data! Attempting to parse US alert data...")
                alerts_description = data['description']
                alerts_expiretime = data['expires']
                alerts_type = "US"
                logger.debug("alerts_description: %s ; alerts_expiretime: %s"
                             % (alerts_description, alerts_expiretime))
                logger.debug("alerts_type: %s" % alerts_type)
                print(Fore.RED + "** A " + alerts_description + " has been issued" + 
                      " for " + str(location) + ",",
                      "and is in effect until " + alerts_expiretime + ". **", sep="\n")
                print("")
        except:
            # I'll keep this here as a "just in case".
            logger.info("No alert information available!")
            alerts_type = "None"
            logger.debug("alerts_type: %s" % alerts_type)
    
print(Fore.YELLOW + "Currently:")
print(Fore.YELLOW + "Current conditions: " + Fore.CYAN + summary_overall)
print(Fore.YELLOW + "Current temperature: " + Fore.CYAN + summary_tempf + "°F (" + summary_tempc + "°C)")
print(Fore.YELLOW + "And it feels like: " + Fore.CYAN + summary_feelslikef
      + "°F (" + summary_feelslikec + "°C)")
print(Fore.YELLOW + "Current dew point: " + Fore.CYAN + summary_dewPointF
      + "°F (" + summary_dewPointC + "°C)")
if winddata == True:
    print(Fore.YELLOW + "Current wind: " + Fore.CYAN + summary_windmphstr + " mph (" + summary_windkphstr + " kph), blowing " + summary_winddir + ".")
else:
    print(Fore.YELLOW + "Wind data is not available for this location.")
print(Fore.YELLOW + "Current humidity: " + Fore.CYAN + summary_humidity)
print("")
if sundata_summary == True:
    print(Fore.YELLOW + "The sunrise and sunset:")
    print(Fore.YELLOW + "Sunrise: " + Fore.CYAN + sunrise_time)
    print(Fore.YELLOW + "Sunset: " + Fore.CYAN + sunset_time)
    print("")
print(Fore.YELLOW + "The hourly forecast:")

for hour in hourly36_json['hourly_forecast']:
    hourly_time = hour['FCTTIME']['civil']
    hourly_tempf = hour['temp']['english']
    hourly_tempc = hour['temp']['metric']
    hourly_condition = hour['condition']
    print(Fore.YELLOW + hourly_time + ": " + Fore.CYAN + hourly_condition + " with a temperature of " + hourly_tempf + "°F (" + hourly_tempc + "°C)")
    summaryHourlyIterations = summaryHourlyIterations + 1
    if summaryHourlyIterations == 6:
        break
print("")
print(Fore.YELLOW + "For the next few days:")

summary_forecastIterations = 0
# Iterations are what will have to happen for now...
for day in forecast10_json['forecast']['simpleforecast']['forecastday']:
    forecast10_weekday = day['date']['weekday']
    forecast10_month = str(day['date']['month'])
    forecast10_day = str(day['date']['day'])
    forecast10_highf = str(day['high']['fahrenheit'])
    forecast10_highc = str(day['high']['celsius'])
    forecast10_lowf = str(day['low']['fahrenheit'])
    forecast10_lowc = str(day['low']['celsius'])
    forecast10_conditions = day['conditions']
    print(Fore.YELLOW + forecast10_weekday + ", " + forecast10_month + "/" + forecast10_day + ": " + Fore.CYAN
          + forecast10_conditions + " with a high of " + forecast10_highf + "°F (" +
          forecast10_highc + "°C), and a low of " + forecast10_lowf + "°F (" +
          forecast10_lowc + "°C).")
    summary_forecastIterations = summary_forecastIterations + 1
    if summary_forecastIterations == 5:
        break
print("")
if almanac_summary == True:
    print(Fore.YELLOW + "The almanac:")
    print(Fore.YELLOW + "Data from: " + Fore.CYAN + almanac_airportCode
          + Fore.YELLOW + " (the nearest airport)")
    print(Fore.YELLOW + "Record high for today: " + Fore.CYAN + almanac_recordHighF
          + "°F (" + almanac_recordHighC + "°C)")
    print(Fore.YELLOW + "It was set in: " + Fore.CYAN + almanac_recordHighYear)
    print(Fore.YELLOW + "Record low for today: " + Fore.CYAN + almanac_recordLowF
          + "°F (" + almanac_recordLowC + "°C)")
    print(Fore.YELLOW + "It was set in: " + Fore.CYAN + almanac_recordLowYear)
# In this part of PyWeather, you'll find comments indicating where things end/begin.
# This is to help when coding, and knowing where things are.

while True:
    print("")
    print(Fore.YELLOW + "What would you like to do now?")
    print(Fore.YELLOW + "- View detailed current data - Enter " + Fore.CYAN + "0")
    print(Fore.YELLOW + "- View detailed alerts data - Enter " + Fore.CYAN + "1")
    print(Fore.YELLOW + "- View detailed hourly data - Enter " + Fore.CYAN + "2")
    print(Fore.YELLOW + "- View the 10 day hourly forecast - Enter " + Fore.CYAN + "3")
    print(Fore.YELLOW + "- View the 10 day forecast - Enter " + Fore.CYAN + "4")
    print(Fore.YELLOW + "- View the almanac for today - Enter " + Fore.CYAN + "5")
    print(Fore.YELLOW + "- View historical weather data - Enter " + Fore.CYAN + "6")
    print(Fore.YELLOW + "- View detailed sun/moon rise/set data - Enter " + Fore.CYAN + "7")
    print(Fore.YELLOW + "- Launch PyWeather's experimental radar - Enter " + Fore.CYAN + "8")
    print(Fore.YELLOW + "- Flag all data types to be refreshed - Enter " + Fore.CYAN + "9")
    print(Fore.YELLOW + "- Check for PyWeather updates - Enter " + Fore.CYAN + "10")
    print(Fore.YELLOW + "- View the about page for PyWeather - Enter " + Fore.CYAN + "11")
    print(Fore.YELLOW + "- Close PyWeather - Enter " + Fore.CYAN + "12" + Fore.YELLOW)
    moreoptions = input("Enter here: ").lower()
    logger.debug("moreoptions: %s" % moreoptions)
        
        
    if moreoptions == "0":
        print(Fore.RED + "Loading...")
        logger.info("Selected view more currently...")
        logger.debug("refresh_currentflagged: %s ; current cache time: %s" % 
                    (refresh_currentflagged, time.time() - cachetime_current))
        if (time.time() - cachetime_current >= cache_currenttime
            or refresh_currentflagged == True):
            print(Fore.RED + "Refreshing current data...")
            try:
                summaryJSON = requests.get(currenturl)
                logger.debug("summaryJSON acquired, end result: %s" % summaryJSON)
                cachetime_current = time.time()
                refresh_currentflagged = False
                logger.debug("refresh_currentflagged: %s ; current cache time: %s" % 
                             (refresh_currentflagged, time.time() - cachetime_current))
            except:
                print("Whoops! PyWeather ran into an error when refetching current",
                      "weather. Make sure that you have an internet connection, and",
                      "if you're on a filtered network, api.wunderground.com is unblocked.", 
                      "Press enter to exit to the main menu.", sep="\n")
                input()
                refresh_currentflagged = True
                logger.debug("refresh_currentflagged: %s" % refresh_currentflagged)
            current_json = json.loads(summaryJSON.text)
            if jsonVerbosity == True:
                logger.debug("current_json loaded with: %s" % current_json)
                   
        print("")
        current_pressureInHg = str(current_json['current_observation']['pressure_in'])
        current_pressureMb = str(current_json['current_observation']['pressure_mb'])
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
        logger.debug("current_pressureTrend: %s ; current_pressureTrend2: %s"
                    % (current_pressureTrend, current_pressureTrend2))
        current_windDegrees = str(current_json['current_observation']['wind_degrees'])
        current_feelsLikeF = str(current_json['current_observation']['feelslike_f'])
        current_feelsLikeC = str(current_json['current_observation']['feelslike_c'])
        current_visibilityMi = str(current_json['current_observation']['visibility_mi'])
        current_visibilityKm = str(current_json['current_observation']['visibility_km'])
        current_UVIndex = str(current_json['current_observation']['UV'])
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
        logger.debug("current_precip1HrIn: %s ; current_precip1HrMm: %s"
                    % (current_precip1HrIn, current_precip1HrMm))
        logger.debug("current_precipTodayIn: %s ; current_precipTodayMm: %s"
                     % (current_precipTodayIn, current_precipTodayMm))
        print(Fore.YELLOW + "Here's the detailed current weather for: " + Fore.CYAN + str(location))
        print(Fore.YELLOW + summary_lastupdated)
        print("")
        print(Fore.YELLOW + "Current conditions: " + Fore.CYAN + summary_overall)
        print(Fore.YELLOW + "Current temperature: " + Fore.CYAN + summary_tempf + "°F (" + summary_tempc + "°C)")
        print(Fore.YELLOW + "And it feels like: " + Fore.CYAN + current_feelsLikeF
              + "°F (" + current_feelsLikeC + "°C)")
        print(Fore.YELLOW + "Current dew point: " + Fore.CYAN + summary_dewPointF
              + "°F (" + summary_dewPointC + "°C)")
        if winddata == True:
            print(Fore.YELLOW + "Current wind: " + Fore.CYAN + summary_windmphstr + 
                  " mph (" + summary_windkphstr + " kph), blowing " + summary_winddir 
                  + " (" + current_windDegrees + " degrees)")
        else:
            print(Fore.YELLOW + "Wind data is not available for this location.")
        print(Fore.YELLOW + "Current humidity: " + Fore.CYAN + summary_humidity)
        print(Fore.YELLOW + "Current pressure: " + Fore.CYAN + current_pressureInHg
              + " inHg (" + current_pressureMb + " mb), " + current_pressureTrend2)
        print(Fore.YELLOW + "Current visibility: " + Fore.CYAN + current_visibilityMi
              + " miles (" + current_visibilityKm + " km)")
        print(Fore.YELLOW + "UV Index: " + Fore.CYAN + current_UVIndex)
        print(Fore.YELLOW + "Precipitation in the last hour: " + Fore.CYAN
              + current_precip1HrIn + " inches (" + current_precip1HrMm
              + " mm)")
        print(Fore.YELLOW + "Precipitation so far today: " + Fore.CYAN
              + current_precipTodayIn + " inches (" + current_precipTodayMm
              + " mm)")
        continue
    elif moreoptions == "1":
        # Or condition will sort out 3 potential conditions.
        logger.debug("alertsPrefetched: %s ; alerts cache time: %s" % 
                         (alertsPrefetched, time.time() - cachetime_alerts))
        if (alertsPrefetched == False or time.time() - cachetime_alerts >= cache_alertstime
            or refresh_alertsflagged == True):
            print(Fore.RED + "Alerts wasn't prefetched, the cache expired, or alerts was flagged", 
                  " for a refresh. Refreshing...", sep="\n")
            logger.debug("refresh_alertsflagged: %s" % refresh_alertsflagged)
            try:
                alertsJSON = requests.get(alertsurl)
                logger.debug("alertsJSON acquired, end result %s." % alertsJSON)
                alertsPrefetched = True
                cachetime_alerts = time.time()
                logger.debug("alertsPrefetched: %s ; alerts cache time: %s" %
                             (alertsPrefetched, time.time() - cachetime_alerts))
                refresh_alertsflagged = False
                logger.debug("alertsPrefetched: %s" % alertsPrefetched)
            except:
                print("When attempting to fetch the alerts JSON file to parse,",
                      "PyWeather ran into an error. If you're on a network with a",
                      "filter, make sure that 'api.wunderground.com' is unblocked.",
                      "Otherwise, make sure you have an internet connection.", sep="\n")
                printException()
                alertsPrefetched = False
                refresh_alertsflagged = True
                logger.debug("alertsPrefetched: %s ; refresh_alertsflagged: %s" % 
                             (alertsPrefetched, refresh_alertsflagged))
                print("Press enter to continue.")
                input()
                continue
            alerts_json = json.loads(alertsJSON.text)
            if jsonVerbosity == True:
                logger.debug("alerts_json: %s" % alerts_json)
            logger.info("Trying to parse alert type...")
            
            try:
                for data in alerts_json['alerts']:
                    alerts_testtype = data['wtype_meteoalarm']
                    alerts_type = "EU"
                    logger.debug("alerts_type: %s" % alerts_type)
            except:
                try:
                    for data in alerts_json['alerts']:
                        alerts_testtype = data['description']
                        alerts_type = "US"
                        logger.debug("alerts_type: %s" % alerts_type)
                except:
                    logger.info("No alert data available!")
                    alerts_type = "None"
                    logger.debug("alerts_type: %s" % alerts_type)
                    
        # Because of the oddities of locations with no alerts, we're doing a mini
        # catch the error here. An error would occur when going into the conditional.
        
        try:
            logger.debug("Attempting to see if alert type is declared...")
            if alerts_type == "US":
                logger.debug("Alert type is declared!")
            elif alerts_type == "EU":
                logger.debug("Alert type is declared!")
        except:
            logger.debug("Alert type isn't declared, so it must be none.")
            alerts_type = "None"
            logger.debug("alerts_type: %s" % alerts_type)
            
                    
        if alerts_type == "EU":
            logger.info("Showing detailed alerts info for EU.")
            alerts_totaliterations = 0
            alerts_completediterations = 0
            alerts_tempiterations = 0
            for data in alerts_json['alerts']:
                alerts_totaliterations = alerts_totaliterations + 1
                logger.debug("alerts_totaliterations: %s" % alerts_totaliterations)
            for data in alerts_json['alerts']:
                print("")
                alerts_completediterations = alerts_completediterations + 1
                logger.info("We're on iteration %s/%s" %
                            (alerts_completediterations, alerts_totaliterations))
                alerts_alertname = data['wtype_meteoalarm_name']
                alerts_alertlevel = data['level_meteoalarm_name']
                alerts_description = data['level_meteoalarm_description']
                logger.debug("alerts_alertname: %s ; alerts_alertlevel: %s"
                             % (alerts_alertname, alerts_alertlevel))
                logger.debug("alerts_alertlevel: %s ; alerts_description: %s"
                             % (alerts_alertlevel, alerts_description))
                alerts_issuedtime = data['date']
                alerts_expiretime = data['expires']
                logger.debug("alerts_issuedtime: %s ; alerts_expiretime: %s"
                             % (alerts_issuedtime, alerts_expiretime))
                print(Fore.YELLOW + "-----")
                print(Fore.RED + "Alert %s/%s:" % 
                      (alerts_completediterations, alerts_totaliterations))
                print("Alert Name: " + Fore.CYAN + alerts_alertname)
                print(Fore.RED + "Alert Level: " + Fore.CYAN + alerts_alertlevel)
                print(Fore.RED + "Alert issued at: " + Fore.CYAN + alerts_issuedtime)
                print(Fore.RED + "Alert expires at: " + Fore.CYAN + alerts_expiretime)
                print(Fore.RED + "Alert Description: " + Fore.CYAN + alerts_description
                      + Fore.RESET)
                alerts_tempiterations = alerts_tempiterations + 1
                if alerts_completediterations == alerts_totaliterations:
                    logger.debug("Completed iterations == total iterations. Breaking...")
                    break
                if alerts_tempiterations == user_alertsEUiterations:
                    print("")
                    try:
                        print(Fore.YELLOW + "Please press enter to view the next",
                              "%s alerts. To exit, press Control + C." % user_alertsEUiterations
                              ,sep="\n")
                        input()
                        alerts_tempiterations = 0
                    except KeyboardInterrupt:
                        logger.debug("User issued Keyboard Interrupt. Breaking...")
                        break
        elif alerts_type == "US":
            alerts_totaliterations = 0
            alerts_completediterations = 0
            alerts_tempiterations = 0
            for data in alerts_json['alerts']:
                alerts_totaliterations = alerts_totaliterations + 1
                logger.debug("alerts_totaliterations: %s" % alerts_totaliterations)
            for data in alerts_json['alerts']:
                print("")
                alerts_completediterations = alerts_completediterations + 1
                logger.info("We're on iteration %s/%s" %
                            (alerts_completediterations, alerts_totaliterations))
                alerts_alertname = data['description']
                alerts_alerttype = data['type']
                alerts_description = data['message']
                alerts_issuedtime = data['date']
                logger.debug('alerts_alertname: %s ; alerts_alerttype: %s' %
                             (alerts_alertname, alerts_alerttype))
                logger.debug("alerts_description: %s ; alerts_issuedtime: %s"
                             % (alerts_description, alerts_issuedtime))
                alerts_expiretime = data['expires']
                logger.debug("alerts_expiretime: %s" % alerts_expiretime)
                print(Fore.RED + "Alert %s/%s:" %
                      (alerts_completediterations, alerts_totaliterations))
                print(Fore.YELLOW + "-----")
                print(Fore.RED + "Alert Name: " + Fore.CYAN + alerts_alertname)
                print(Fore.RED + "Alert Type: " + Fore.CYAN + alerts_alerttype)
                print(Fore.RED + "Alert issued at: " + Fore.CYAN + alerts_issuedtime)
                print(Fore.RED + "Alert expires at: " + Fore.CYAN + alerts_expiretime)
                print(Fore.RED + "Alert Description: " + Fore.CYAN + alerts_description
                      + Fore.RESET)
                alerts_tempiterations = alerts_tempiterations + 1
                if alerts_completediterations == alerts_totaliterations:
                    logger.debug("Completed iterations equals total iterations. Breaking...")
                    break
                if alerts_tempiterations == user_alertsUSiterations:
                    try:
                        print(Fore.YELLOW + "Please press enter to view the next",
                              "%s alert(s). To exit, press Control + C." % user_alertsUSiterations,
                              sep="\n")
                        input()
                        alerts_tempiterations = 0
                    except KeyboardInterrupt:
                        logger.debug("User issued KeyboardInterrupt. Breaking...")
                        break
        elif alerts_type == "None":
            print(Fore.RED + "No data available! Either there are no alerts",
                  "at the location inputted, or Wunderground doesn't support alerts",
                  "for the location inputted.",
                  "As a quick note, Wunderground only supports alerts in the US/EU.", sep="\n")
        else:
            print(Fore.YELLOW + "Something went wrong when launching the correct conditional",
                  "for the alert data type involved.",
                  "For error reporting, this is what the variable 'alerts_type' is currently storing.",
                  "alerts_type: %s" % alerts_type, sep="\n" + Fore.RESET)  
# <----------- Detailed Currently is above, Detailed Hourly is below -------->
    
    elif moreoptions == "2":
        print(Fore.RED + "Loading...")
        print("")
        logger.debug("refresh_hourly36flagged: %s ; hourly36 cache time: %s" %
                    (refresh_hourly36flagged, time.time() - cachetime_hourly36))
        logger.info("Selected view more hourly...")
        if (refresh_hourly36flagged == True or time.time() - cachetime_hourly36 >= cache_hourlytime):
            print(Fore.RED + "Refreshing 3 day hourly data...")
            try:
                hourly36JSON = requests.get(hourlyurl)
                logger.debug("hourly36JSON acquired, end result: %s" % hourly36JSON)
                cachetime_hourly36 = time.time()
            except:
                print("Whoops! A problem occurred when trying to refresh 36 hour",
                      "hourly data. Make sure you have an internet connection, and if",
                      "you're on a network with a filter, make sure that api.wunderground.com",
                      "is unblocked.",
                      "Press enter to continue.", sep="\n")
                printException()
                input()
                refresh_hourly36flagged = False
                logger.debug("refresh_hourly36flagged: %s" % refresh_hourly36flagged)
                continue
            
            hourly36_json = json.loads(hourly36JSON.text)
            if jsonVerbosity == True:
                logger.debug("hourly36_json: %s" % hourly36_json)
            refresh_hourly36flagged = False
            logger.debug("refresh_hourly36flagged: %s" % refresh_hourly36flagged)
            
                
        detailedHourlyIterations = 0
        totaldetailedHourlyIterations = 0
        print(Fore.YELLOW + "Here's the detailed hourly forecast for: " + Fore.CYAN + str(location))
        for hour in hourly36_json['hourly_forecast']:
            logger.info("We're on iteration: %s" % detailedHourlyIterations)
            hourly_time = hour['FCTTIME']['civil']
            hourly_tempf = hour['temp']['english']
            hourly_tempc = hour['temp']['metric']
            hourly_month = str(hour['FCTTIME']['month_name'])
            hourly_day = str(hour['FCTTIME']['mday'])
            hourly_dewpointF = str(hour['dewpoint']['english'])
            logger.debug("hourly_time: %s ; hourly_month: %s"
                        % (hourly_time, hourly_month))
            logger.debug("hourly_day: %s ; hourly_dewpointF: %s"
                        % (hourly_day, hourly_dewpointF))
            hourly_dewpointC = str(hour['dewpoint']['metric'])
            hourly_windMPH = str(hour['wspd']['english'])
            hourly_windKPH = str(hour['wspd']['metric'])
            hourly_windDir = hour['wdir']['dir']
            logger.debug("hourly_dewpointC: %s ; hourly_windMPH: %s"
                        % (hourly_dewpointC, hourly_windMPH))
            logger.debug("hourly_windKPH: %s ; hourly_windDir: %s"
                        % (hourly_windKPH, hourly_windDir))
            hourly_windDegrees = str(hour['wdir']['degrees'])
            hourly_UVIndex = str(hour['uvi'])
            hourly_humidity = str(hour['humidity'])
            hourly_feelsLikeF = str(hour['feelslike']['english'])
            logger.debug("hourly_windDegrees: %s ; hourly_UVIndex: %s"
                        % (hourly_windDegrees, hourly_UVIndex))
            logger.debug("hourly_humidity: %s ; hourly_feelsLikeF: %s"
                        % (hourly_humidity, hourly_feelsLikeF))
            hourly_feelsLikeC = str(hour['feelslike']['metric'])
            hourly_precipIn = str(hour['qpf']['english'])
            hourly_precipMm = str(hour['qpf']['metric'])
            hourly_snowCheck = hour['snow']['english']
            logger.debug("hourly_feelsLikeC: %s ; hourly_precipIn: %s"
                        % (hourly_feelsLikeC, hourly_precipIn))
            logger.debug("hourly_precipMm: %s ; hourly_snowCheck: %s"
                        % (hourly_precipMm, hourly_snowCheck))
            logger.info("Starting snow check...")
            if hourly_snowCheck == "0.0":
                hourly_snowData = False
                logger.warn("No snow data! Maybe it's summer?")
            else:
                hourly_snowData = True
                logger.info("Lucky duck getting some snow.")
            
            hourly_snowIn = str(hourly_snowCheck)
            hourly_snowMm = str(hour['snow']['metric'])
            hourly_precipChance = str(hour['pop'])
            hourly_pressureInHg = str(hour['mslp']['english'])
            hourly_pressureMb = str(hour['mslp']['metric'])
            hourly_condition = hour['condition']
            logger.debug("hourly_snowIn: %s ; hourly_snowMm: %s"
                        % (hourly_snowIn, hourly_snowMm))
            logger.debug("hourly_precipChance: %s ; hourly_pressureInHg: %s"
                        % (hourly_precipChance, hourly_pressureInHg))
            logger.debug("hourly_pressureMb: %s ; hourly_condition: %s" 
                         % (hourly_pressureMb, hourly_condition))
            logger.info("Now printing weather data...")
            print("")
            # If you have verbosity on, there's a chance that the next
            # hourly iteration will start BEFORE the previous iteration
            # prints out. This is normal, and no issues are caused by such.
            print(Fore.YELLOW + hourly_time + " on " + hourly_month + " " + hourly_day + ":")
            print(Fore.YELLOW + "Conditions: " + Fore.CYAN + hourly_condition)
            print(Fore.YELLOW + "Temperature: " + Fore.CYAN + hourly_tempf 
                  + "°F (" + hourly_tempc + "°C)")
            print(Fore.YELLOW + "Feels like: " + Fore.CYAN + hourly_feelsLikeF
                  + "°F (" + hourly_feelsLikeC + "°C)")
            print(Fore.YELLOW + "Dew Point: " + Fore.CYAN + hourly_dewpointF
                  + "°F (" + hourly_dewpointC + "°C)")
            print(Fore.YELLOW + "Wind: " + Fore.CYAN + hourly_windMPH
                  + " mph (" + hourly_windKPH + " kph) blowing to the " +
                  hourly_windDir + " (" + hourly_windDegrees + "°)")
            print(Fore.YELLOW + "Humidity: " + Fore.CYAN + hourly_humidity + "%")
            if hourly_snowData == False:
                print(Fore.YELLOW + "Rain for the hour: " + Fore.CYAN +
                      hourly_precipIn + " in (" + hourly_precipMm + " mm)")
            if hourly_snowData == True:
                print(Fore.YELLOW + "Snow for the hour: " + Fore.CYAN +
                      hourly_snowIn + " in (" + hourly_snowMm + " mm)")
            print(Fore.YELLOW + "Precipitation chance: " + Fore.CYAN + 
                  hourly_precipChance + "%")
            print(Fore.YELLOW + "Barometric pressure: " + Fore.CYAN +
                  hourly_pressureInHg + " inHg (" + hourly_pressureMb
                  + " mb)")
            detailedHourlyIterations = detailedHourlyIterations + 1
            totaldetailedHourlyIterations = totaldetailedHourlyIterations + 1
            if user_showCompletedIterations == True:
                print(Fore.YELLOW + "Completed iterations: " + Fore.CYAN + "%s/36"
                      % totaldetailedHourlyIterations)
                print(Fore.RESET)
            if user_enterToContinue == True:
                if totaldetailedHourlyIterations == 36:
                    logger.debug("Total iterations is 36. Breaking...")
                    break
                if (detailedHourlyIterations == user_loopIterations):
                    logger.debug("detailedHourlyIterations: %s" % detailedHourlyIterations)
                    logger.debug("Asking user for continuation...")
                    try:
                        print("")
                        print(Fore.RED + "Please press enter to view the next %s hours of hourly data."
                              % user_loopIterations)
                        print("You can also press Control + C to head back to the input menu.")
                        input()
                        logger.debug("Iterating %s more times..." % user_loopIterations)
                        detailedHourlyIterations = 0
                    except KeyboardInterrupt:
                        logger.debug("Exiting to main menu...")
                        break
            elif user_enterToContinue == False:
                if totaldetailedHourlyIterations == 36:
                    logger.debug("totalDetailedHourlyIterations is 36. Breaking...")
                    break
                
    elif moreoptions == "3":
        print(Fore.RED + "Loading...")
        print("")
        logger.info("Selected view more 10 day hourly...")
        detailedHourly10Iterations = 0
        totaldetailedHourly10Iterations = 0
        logger.debug("tenday_prefetched: %s ; refresh_hourly10flagged: %s" %
                    (tenday_prefetched, refresh_hourly10flagged))
        try:
            logger.debug("hourly 10 cache time: %s" % time.time() - cachetime_hourly10)
        except:
            logger.debug("no hourly 10 cache time")
        if (tenday_prefetched == False or refresh_hourly10flagged == True or
            time.time() - cachetime_hourly10 >= cache_hourlytime):
            print(Fore.RED + "Refreshing (or fetching for the first time) 10 day hourly data...")
            try:
                tendayJSON = requests.get(tendayurl)
                logger.debug("Retrieved hourly 10 JSON with end result: %s" % tendayJSON)
                cachetime_hourly10 = time.time()
            except:
                print("When attempting to fetch the 10-day hourly forecast data, PyWeather ran",
                      "info an error. If you're on a network with a filter, make sure that",
                      "'api.wunderground.com' is unblocked. Otherwise, make sure that you have",
                      "an internet connection.", sep="\n")
                printException()
                tenday_prefetched = False
                refresh_hourly10flagged = False
                logger.debug("tenday_prefetched: %s ; refresh_hourly10flagged: %s" %
                             (tenday_prefetched, refresh_hourly10flagged))
                printException()
                print("Press enter to continue.")
                input()
                continue
            
            tenday_prefetched = True
            refresh_hourly10flagged = False
            logger.debug("tenday_prefetched: %s ; refresh_hourly10flagged: %s" %
                         (tenday_prefetched, refresh_hourly10flagged))
            tenday_json = json.loads(tendayJSON.text)
            if jsonVerbosity == True:
                logger.debug("tenday_json: %s" % tenday_json)
            logger.debug("tenday json loaded.")
            
        print(Fore.YELLOW + "Here's the detailed 10 day hourly forecast for: " + Fore.CYAN + str(location))  
        for hour in tenday_json['hourly_forecast']:
            logger.info("We're on iteration: %s/24. User iterations: %s." %
                        (detailedHourly10Iterations, user_loopIterations))
            hourly10_time = hour['FCTTIME']['civil']
            hourly10_tempf = hour['temp']['english']
            hourly10_tempc = hour['temp']['metric']
            hourly10_month = str(hour['FCTTIME']['month_name'])
            hourly10_day = str(hour['FCTTIME']['mday'])
            hourly10_dewpointF = str(hour['dewpoint']['english'])
            logger.debug("hourly10_time: %s ; hourly10_month: %s"
                        % (hourly10_time, hourly10_month))
            logger.debug("hourly10_day: %s ; hourly10_dewpointF: %s"
                        % (hourly10_day, hourly10_dewpointF))
            hourly10_dewpointC = str(hour['dewpoint']['metric'])
            hourly10_windMPH = str(hour['wspd']['english'])
            hourly10_windKPH = str(hour['wspd']['metric'])
            hourly10_windDir = hour['wdir']['dir']
            # the if verbosity == True will be left here
            # as a memorial. :)
            if verbosity == True:
                logger.debug("hourly10_dewpointC: %s ; hourly10_windMPH: %s"
                             % (hourly10_dewpointC, hourly10_windMPH))
                logger.debug("hourly_windKPH: %s ; hourly10_windDir: %s"
                             % (hourly10_windKPH, hourly10_windDir))
            hourly10_windDegrees = str(hour['wdir']['degrees'])
            hourly10_UVIndex = str(hour['uvi'])
            hourly10_humidity = str(hour['humidity'])
            hourly10_feelsLikeF = str(hour['feelslike']['english'])
            logger.debug("hourly10_windDegrees: %s ; hourly10_UVIndex: %s"
                        % (hourly10_windDegrees, hourly10_UVIndex))
            logger.debug("hourly10_humidity: %s ; hourly10_feelsLikeF: %s"
                        % (hourly10_humidity, hourly10_feelsLikeF))
            hourly10_feelsLikeC = str(hour['feelslike']['metric'])
            hourly10_precipIn = str(hour['qpf']['english'])
            hourly10_precipMm = str(hour['qpf']['metric'])
            hourly10_snowCheck = hour['snow']['english']
            logger.debug("hourly10_feelsLikeC: %s ; hourly10_precipIn: %s"
                        % (hourly10_feelsLikeC, hourly10_precipIn))
            logger.debug("hourly10_precipMm: %s ; hourly10_snowCheck: %s"
                        % (hourly10_precipMm, hourly10_snowCheck))
            logger.info("Starting snow check...")
            if hourly10_snowCheck == "0.0":
                hourly10_snowData = False
                logger.warn("No snow data! Maybe it's summer?")
            else:
                hourly10_snowData = True
                logger.info("Snow data is present.")
            
            hourly10_snowIn = str(hourly10_snowCheck)
            hourly10_snowMm = str(hour['snow']['metric'])
            hourly10_precipChance = str(hour['pop'])
            hourly10_pressureInHg = str(hour['mslp']['english'])
            hourly10_pressureMb = str(hour['mslp']['metric'])
            hourly10_condition = hour['condition']
            logger.debug("hourly10_snowIn: %s ; hourly10_snowMm: %s"
                        % (hourly10_snowIn, hourly10_snowMm))
            logger.debug("hourly10_precipChance: %s ; hourly10_pressureInHg: %s"
                        % (hourly10_precipChance, hourly10_pressureInHg))
            logger.debug("hourly10_pressureMb: %s ; hourly10_condition: %s" 
                         % (hourly10_pressureMb, hourly10_condition))
            logger.info("Now printing weather data...")
            # If you have verbosity on, there's a chance that the next
            # hourly iteration will start BEFORE the previous iteration
            # prints out. This is normal, and no issues are caused by such.
            print(Fore.YELLOW + hourly10_time + " on " + hourly10_month + " " 
                  + hourly10_day + ":")
            print(Fore.YELLOW + "Conditions: " + Fore.CYAN 
                  + hourly10_condition)
            print(Fore.YELLOW + "Temperature: " + Fore.CYAN + hourly10_tempf 
                  + "°F (" + hourly10_tempc + "°C)")
            print(Fore.YELLOW + "Feels like: " + Fore.CYAN + hourly10_feelsLikeF
                  + "°F (" + hourly10_feelsLikeC + "°C)")
            print(Fore.YELLOW + "Dew Point: " + Fore.CYAN + hourly10_dewpointF
                  + "°F (" + hourly10_dewpointC + "°C)")
            print(Fore.YELLOW + "Wind: " + Fore.CYAN + hourly10_windMPH
                  + " mph (" + hourly10_windKPH + " kph) blowing to the " +
                  hourly10_windDir + " (" + hourly10_windDegrees + "°)")
            print(Fore.YELLOW + "Humidity: " + Fore.CYAN + hourly10_humidity + "%")
            if hourly10_snowData == False:
                print(Fore.YELLOW + "Rain for the hour: " + Fore.CYAN +
                      hourly10_precipIn + " in (" + hourly10_precipMm + " mm)")
            if hourly10_snowData == True:
                print(Fore.YELLOW + "Snow for the hour: " + Fore.CYAN +
                      hourly10_snowIn + " in (" + hourly10_snowMm + " mm)")
            print(Fore.YELLOW + "Precipitation chance: " + Fore.CYAN + 
                  hourly10_precipChance + "%")
            print(Fore.YELLOW + "Barometric pressure: " + Fore.CYAN +
                  hourly10_pressureInHg + " inHg (" + hourly10_pressureMb
                  + " mb)")
            print("")
            detailedHourly10Iterations = detailedHourly10Iterations + 1
            totaldetailedHourly10Iterations = totaldetailedHourly10Iterations + 1
            if user_showCompletedIterations == True:
                print(Fore.YELLOW + "Completed iterations: " + Fore.CYAN + "%s/240"
                      % totaldetailedHourly10Iterations)
                print(Fore.RESET)
            if user_enterToContinue == True:
                if totaldetailedHourly10Iterations == 240:
                    logger.info("detailedHourly10Iterations is 240. Breaking...")
                    break
                if (detailedHourly10Iterations == user_loopIterations):
                    logger.debug("detailedHourly10Iterations: %s" % detailedHourly10Iterations)
                    logger.debug("Asking user for continuation...")
                    try:
                        print(Fore.RED + "Please press enter to view the next %s hours of hourly data."
                              % user_loopIterations)
                        print("You can also press Control + C to head back to the input menu.")
                        input()
                        logger.debug("Iterating %s more times...")
                        detailedHourly10Iterations = 0
                    except KeyboardInterrupt:
                        logger.debug("Exiting to main menu...")
                        break
            elif user_enterToContinue == False:
                if totaldetailedHourly10Iterations == 240:
                    logger.info("detailedhourly10Iterations is 240. Breaking...")
                    break
    elif moreoptions == "4":
        print(Fore.RED + "Loading, please wait a few seconds.")
        logger.info("Selected view more 10 day...")
        print("")
        logger.debug("refresh_forecastflagged: %s ; forecast cache time: %s" %
                    (refresh_forecastflagged, time.time() - cachetime_forecast))
        if (refresh_forecastflagged == True or time.time() - cachetime_forecast >= cache_hourlytime):
            print(Fore.RED + "Refreshing forecast data...")
            try:
                forecast10JSON = requests.get(f10dayurl)
                cachetime_forecast = time.time()
                logger.debug("forecast10JSON acquired, end result: %s" % forecast10JSON)
            except:
                print("PyWeather ran into an error when trying to refetch forecast",
                      "data. If you're on a filtered network, make sure that",
                      "api.wunderground.com is unblocked. Otherwise, make sure you have",
                      "an internet connection.", sep="\n")
                printException()
                refresh_forecastflagged = False
                logger.debug("refresh_forecastflagged: %s" % refresh_forecastflagged)
                print("Press enter to continue.")
                input()
                continue
            
            refresh_forecastflagged = False
            forecast10_json = json.loads(forecast10JSON.text)
            if jsonVerbosity == True:
                logger.debug("refresh_forecastflagged: %s" % refresh_forecastflagged)
                logger.debug("forecast10_json: %s" % forecast10_json)
            else:
                logger.debug("refresh_forecastflagged: %s" % refresh_forecastflagged)
                logger.debug("forecast10_json loaded.")
                
        detailedForecastIterations = 0
        totaldetailedForecastIterations = 0
        forecast10_precipDayData = True
        forecast10_snowDayData = True
        print(Fore.CYAN + "Here's the detailed 10 day forecast for: " + Fore.YELLOW + str(location))
        for day in forecast10_json['forecast']['simpleforecast']['forecastday']:
            print("")
            logger.info("We're on iteration: %s" % detailedForecastIterations)
            forecast10_weekday = day['date']['weekday']
            forecast10_month = str(day['date']['month'])
            forecast10_day = str(day['date']['day'])
            forecast10_highf = str(day['high']['fahrenheit'])
            forecast10_highfcheck = int(day['high']['fahrenheit'])
            logger.debug("forecast10_weekday: %s ; forecast10_month: %s"
                         % (forecast10_weekday, forecast10_month))
            logger.debug("forecast10_day: %s ; forecast10_highf: %s"
                        % (forecast10_day, forecast10_highf))
            forecast10_highc = str(day['high']['celsius'])
            forecast10_lowf = str(day['low']['fahrenheit'])
            forecast10_lowfcheck = int(day['low']['fahrenheit'])
            forecast10_lowc = str(day['low']['celsius'])
            forecast10_showsnowdatanight = False
            forecast10_showsnowdataday = False
            logger.debug("forecast10_highfcheck: %s ; forecast10_lowfcheck: %s" %
                         (forecast10_highfcheck, forecast10_lowfcheck))
            if forecast10_highfcheck > 32:
                forecast10_showsnowdataday = False
            else:
                forecast10_showsnowdataday = True
                
            if forecast10_lowfcheck > 32:
                forecat10_showsnowdatanight = False
            else:
                forecast10_showsnowdatanight = True
                
            logger.debug("forecast10_showsnowdataday: %s ; forecast10_showsnowdatanight: %s"
                         % (forecast10_showsnowdataday, forecast10_showsnowdatanight)) 
               
            if forecast10_highfcheck < 32 and forecast10_lowfcheck < 32:
                forecast10_showsnowdatatotal = True
                forecast10_showraindatatotal = False
            # It could happen!
            elif (forecast10_highfcheck > 32 and forecast10_lowfcheck < 32 or
                  forecast10_highfcheck < 32 and forecast10_lowfcheck > 32):
                forecast10_showsnowdatatotal = True
                forecast10_showraindatatotal = True
            elif forecast10_highfcheck > 32 and forecast10_lowfcheck > 32:
                forecast10_showsnowdatatotal = False
                forecast10_showraindatatotal = True
            else:
                forecast10_showsnowdatatotal = False
                forecast10_showraindatatotal = True
                
            logger.debug("forecast10_showsnowdatatotal: %s ; forecast10_showraindatatotal: %s" %
                         (forecast10_showsnowdatatotal, forecast10_showraindatatotal))
            forecast10_conditions = day['conditions']
            logger.debug("forecast10_highc: %s ; forecast10_lowf: %s"
                        % (forecast10_highc, forecast10_lowf))
            logger.debug("forecast10_lowc: %s ; forecast10_conditions: %s"
                        % (forecast10_lowc, forecast10_conditions))
            forecast10_precipTotalIn = str(day['qpf_allday']['in'])
            forecast10_precipTotalMm = str(day['qpf_allday']['mm'])
            forecast10_precipDayIn = str(day['qpf_day']['in'])
            forecast10_precipDayMm = str(day['qpf_day']['mm'])
            if forecast10_precipDayIn == "None":
                forecast10_precipDayData = False
                logger.debug("forecast10_precipDayData: %s" 
                             % forecast10_precipDayData)
            else:
                forecast10_precipDayData = True
                logger.debug("forecast10_precipDayData: %s"
                             % forecast10_precipDayData)
            logger.debug("forecast10_precipTotalIn: %s ; forecast10_precipTotalMm: %s"
                        % (forecast10_precipTotalIn, forecast10_precipTotalMm))
            logger.debug("forecast10_precipDayIn: %s ; forecast10_precipDayMm: %s"
                        % (forecast10_precipDayIn, forecast10_precipDayMm))
            forecast10_precipNightIn = str(day['qpf_night']['in'])
            forecast10_precipNightMm = str(day['qpf_night']['mm'])
            logger.debug("forecast10_precipNightIn: %s ; forecast10_precipNightMm: %s"
                        % (forecast10_precipNightIn, forecast10_precipNightMm))
            forecast10_snowTotalCheck = day['snow_allday']['in']
            logger.debug("forecast10_snowTotalCheck: %s" % forecast10_snowTotalCheck)
            forecast10_snowTotalIn = str(forecast10_snowTotalCheck)
            forecast10_snowTotalCm = str(day['snow_allday']['cm'])
            forecast10_snowDayCheck = day['snow_day']['in']
            logger.debug("forecast10_snowTotalIn: %s ; forecast10_snowTotalCm: %s"
                        % (forecast10_snowTotalIn, forecast10_snowTotalCm))
            logger.debug("forecast10_snowDayCheck: %s" % forecast10_snowDayCheck)
            forecast10_snowDayIn = str(forecast10_snowDayCheck)
            forecast10_snowDayCm = str(day['snow_day']['cm'])
            if forecast10_snowDayIn == "None":
                forecast10_snowDayData = False
                logger.debug("forecast10_snowDayData: %s" % 
                             forecast10_snowDayData)
            else:
                forecast10_snowDayData = True
                logger.debug("forecast10_snowDayData: %s" %
                             forecast10_snowDayData)
            forecast10_snowNightCheck = day['snow_night']['in']
            logger.debug("forecast10_snowDayIn: %s ; forecast10_snowDayCm: %s"
                         % (forecast10_snowDayIn, forecast10_snowDayCm))
            logger.debug("forecast10_snowNightCheck: %s" % forecast10_snowNightCheck)
            forecast10_snowNightIn = str(forecast10_snowNightCheck)
            forecast10_snowNightCm = str(day['snow_night']['cm'])
            forecast10_maxWindMPH = str(day['maxwind']['mph'])
            forecast10_maxWindKPH = str(day['maxwind']['kph'])
            forecast10_maxMPHcheck = int(forecast10_maxWindMPH)
            forecast10_maxKPHcheck = int(forecast10_maxWindKPH)
            logger.debug("forecast10_maxMPHcheck: %s ; forecast10_maxKPHcheck: %s"
                         % (forecast10_maxMPHcheck, forecast10_maxKPHcheck))
            if (forecast10_maxMPHcheck == -999 and forecast10_maxKPHcheck > -0.01):
                forecast10_maxWindMPH = forecast10_maxKPHcheck / 1.609344
                forecast10_maxWindMPH = str(round(forecast10_maxWindMPH, 0))
                forecast10_maxWindMPH = forecast10_maxWindMPH.strip(".0")
                logger.debug("forecast10_maxWindMPH: %s" 
                             % forecast10_maxWindMPH)
                
            elif (forecast10_maxMPHcheck == -999 and forecast10_maxKPHcheck < -0.01):
                forecast10_maxWindMPH = "N/A"
                forecast10_maxWindKPH = "N/A"
            logger.debug("forecast10_snowNightIn: %s ; forecast10_snowNightCm: %s"
                        % (forecast10_snowNightIn, forecast10_snowNightCm))
            logger.debug("forecast10_maxWindMPH: %s ; forecast10_maxWindKPH: %s"
                        % (forecast10_maxWindMPH, forecast10_maxWindKPH))
            forecast10_avgWindMPH = str(day['avewind']['mph'])
            forecast10_avgWindKPH = str(day['avewind']['kph'])
            forecast10_avgWindDir = day['avewind']['dir']
            forecast10_avgWindDegrees = str(day['avewind']['degrees'])
            forecast10_avgHumidity = str(day['avehumidity'])
            logger.debug("forecast10_avgWindMPH: %s ; forecast10_avgWindKPH: %s"
                        % (forecast10_avgWindMPH, forecast10_avgWindKPH))
            logger.debug("forecast10_avgWindDir: %s ; forecast10_avgWindDegrees: %s"
                        % (forecast10_avgWindDir, forecast10_avgWindDegrees))
            logger.debug("forecast10_avgHumidity: %s" % forecast10_avgHumidity)
            logger.info("Printing weather data...")
            print(Fore.YELLOW + forecast10_weekday + ", " + forecast10_month + "/" + forecast10_day + ":")
            print(Fore.CYAN + forecast10_conditions + Fore.YELLOW + " with a high of "
                  + Fore.CYAN + forecast10_highf + "°F (" + forecast10_highc + "°C)" +
                  Fore.YELLOW + " and a low of " + Fore.CYAN + forecast10_lowf + "°F (" +
                  forecast10_lowc + "°C)" + ".")
            if forecast10_showsnowdatatotal == True and forecast10_showraindatatotal == False:
                print(Fore.YELLOW + "Snow in total: " + Fore.CYAN + forecast10_snowTotalIn
                      + " in (" + forecast10_snowTotalCm + " cm)")
            elif forecast10_showsnowdatatotal == False and forecast10_showraindatatotal == True:
                print(Fore.YELLOW + "Rain in total: " + Fore.CYAN + forecast10_precipTotalIn
                      + " in (" + forecast10_precipTotalMm + " mm)")
            elif forecast10_showsnowdatatotal == True and forecast10_showraindatatotal == True:
                print(Fore.YELLOW + "Snow in total: " + Fore.CYAN + forecast10_snowTotalIn
                      + " in (" + forecast10_snowTotalCm + " cm)")
                print(Fore.YELLOW + "Rain in total: " + Fore.CYAN + forecast10_precipTotalIn
                      + " in (" + forecast10_precipTotalMm + " mm)")
            else:
                print(Fore.YELLOW + "Rain in total: " + Fore.CYAN + forecast10_precipTotalIn
                      + " in (" + forecast10_precipTotalMm + " mm)")
                
            if forecast10_showsnowdataday == False and forecast10_precipDayData == True:
                print(Fore.YELLOW + "Rain for the day: " + Fore.CYAN + forecast10_precipDayIn
                      + " in (" + forecast10_precipDayMm + " mm)")
            elif forecast10_showsnowdataday == True and forecast10_snowDayData == True:
                print(Fore.YELLOW + "Snow for the day: " + Fore.CYAN + forecast10_snowDayIn
                      + " in (" + forecast10_snowDayCm + " cm)")
            
            if forecast10_showsnowdatanight == False:
                print(Fore.YELLOW + "Rain for the night: " + Fore.CYAN + forecast10_precipNightIn
                      + " in (" + forecast10_precipNightMm + " mm)")
            elif forecast10_showsnowdatanight == True:
                print(Fore.YELLOW + "Snow for the night: " + Fore.CYAN + forecast10_snowNightIn
                      + " in (" + forecast10_snowNightCm + " cm)")
            else:
                print(Fore.YELLOW + "Rain for the night: " + Fore.CYAN + forecast10_precipNightIn
                      + " in (" + forecast10_precipNightMm + " mm)")
                
            print(Fore.YELLOW + "Winds: " + Fore.CYAN + 
                  forecast10_avgWindMPH + " mph (" + forecast10_avgWindKPH
                  + " kph), gusting to " + forecast10_maxWindMPH + " mph ("
                  + forecast10_maxWindKPH + " kph), "
                  + "and blowing " + forecast10_avgWindDir +
                  " (" + forecast10_avgWindDegrees + "°)")
            print(Fore.YELLOW + "Humidity: " + Fore.CYAN +
                  forecast10_avgHumidity + "%")
            detailedForecastIterations = detailedForecastIterations + 1
            totaldetailedForecastIterations = totaldetailedForecastIterations + 1
            if user_showCompletedIterations == True:
                print(Fore.YELLOW + "Completed iterations: " + Fore.CYAN + "%s/10"
                      % totaldetailedForecastIterations)
                print(Fore.RESET)
            if totaldetailedForecastIterations == 10:
                logger.debug("Total iterations is 10. Breaking...")
                break
            if user_enterToContinue == True:
                if detailedForecastIterations == user_forecastLoopIterations:
                    logger.debug("detailedForecastIterations: %s" % detailedForecastIterations)
                    try:
                        print("")
                        print(Fore.RED + "Press enter to view the next %s days of weather data."
                              % user_forecastLoopIterations)
                        print("You can also press Control + C to return to the input menu.")
                        input()
                        logger.info("Iterating %s more times..." 
                                    % user_forecastLoopIterations)
                    except KeyboardInterrupt:
                        break
                        logger.info("Exiting to the main menu.")


    elif moreoptions == "8":
        if radar_bypassconfirmation == False:
            print(Fore.RED + "The radar feature is experimental, and may not work properly.",
                  "PyWeather may crash when in this feature, and other unexpected",
                  "behavior may occur. Despite the radar feature being experimental,",
                  "would you like to use the radar?" + Fore.RESET, sep="\n")
            radar_confirmedusage = input("Input here: ").lower()
            if radar_confirmedusage == "yes":
                print("The radar is now launching.",
                      "If you want to bypass this confirmation message when",
                      "launching the radar feature, in config.ini, set bypassconfirmation",
                      "under the RADAR GUI section to True.", sep="\n")
            elif radar_confirmedusage == "no":
                print("Not launching the radar.")
                continue
            else:
                print("Could not understand your input. As such, the radar will not",
                      "be launched.", sep="\n")
                continue


        try:
            os.mkdir("temp")
        except:
            printException_loggerwarn()
            
        print(Fore.YELLOW + "Loading the GUI. This should take around 5 seconds.")
        radar_clearImages()
        try:
            frontend = gui()
        except:
            print(Fore.RED + "Cannot launch a GUI on this platform. If you don't have",
                  "a GUI on Linux, this is expected. Otherwise, investigate into why",
                  "tkinter won't launch.", sep="\n" + Fore.RESET)
            printException()
            continue
        print(Fore.YELLOW + "Defining variables...")
        # A quick note about cache variables.
        # The syntax goes like this:
        # (mode)(zoom)cached, where r = radar only, s = satellite only
        r10cached = False; r20cached = False; r40cached = False
        logger.debug("r10cached: %s ; r20cached: %s ; r40cached: %s" %
                     (r10cached, r20cached, r40cached))
        r60cached = False; r80cached = False; r100cached = False
        logger.debug("r60cached: %s ; r80cached: %s ; r100cached: %s" %
                     (r60cached, r80cached, r100cached))
        radar_zoomlevel = "None"
        r10url = 'http://api.wunderground.com/api/' + apikey + '/animatedradar/image.gif?centerlat=' + latstr + '&centerlon=' + lonstr + '&width=' + radar_gifx + '&height=' + radar_gify + '&newmaps=1&rainsnow=0&delay=25&num=10&timelabel=1&timelabel.y=10&radius=10&radunits=km'
        r20url = 'http://api.wunderground.com/api/' + apikey + '/animatedradar/image.gif?centerlat=' + latstr + '&centerlon=' + lonstr + '&width=' + radar_gifx + '&height=' + radar_gify + '&newmaps=1&rainsnow=0&delay=25&num=10&timelabel=1&timelabel.y=10&radius=20&radunits=km'
        logger.debug("r10url: %s ; r20url: %s" %
                     (r10url, r20url))
        r40url = 'http://api.wunderground.com/api/' + apikey + '/animatedradar/image.gif?centerlat=' + latstr + '&centerlon=' + lonstr + '&width=' + radar_gifx + '&height=' + radar_gify + '&newmaps=1&rainsnow=0&delay=25&num=10&timelabel=1&timelabel.y=10&radius=40&radunits=km'
        r60url = 'http://api.wunderground.com/api/' + apikey + '/animatedradar/image.gif?centerlat=' + latstr + '&centerlon=' + lonstr + '&width=' + radar_gifx + '&height=' + radar_gify + '&newmaps=1&rainsnow=0&delay=25&num=10&timelabel=1&timelabel.y=10&radius=60&radunits=km'
        logger.debug("r40url: %s ; r60url: %s" %
                     (r40url, r60url))
        r80url = 'http://api.wunderground.com/api/' + apikey + '/animatedradar/image.gif?centerlat=' + latstr + '&centerlon=' + lonstr + '&width=' + radar_gifx + '&height=' + radar_gify + '&newmaps=1&rainsnow=0&delay=25&num=10&timelabel=1&timelabel.y=10&radius=80&radunits=km'
        r100url = 'http://api.wunderground.com/api/' + apikey + '/animatedradar/image.gif?centerlat=' + latstr + '&centerlon=' + lonstr + '&width=' + radar_gifx + '&height=' + radar_gify + '&newmaps=1&rainsnow=0&delay=25&num=10&timelabel=1&timelabel.y=10&radius=100&radunits=km' 
        logger.debug("r80url: %s ; r100url: %s" %
                     (r80url, r100url))      
        
        
        print(Fore.YELLOW + "Defining functions...")
                
        def frontend_zoomswitch(btnName):
            global r10cached; global r20cached; global r40cached
            global r60cached; global r80cached; global r100cached
            global radar_zoomlevel
            logger.debug("btnName: %s" % btnName)
            if btnName == "10 km":
                logger.debug("r10cached: %s" % r10cached)
                if r10cached == False:
                    logger.debug("r10cached is false, fetching...")
                    frontend.setStatusbar("Zoom: 10 km", 0)
                    frontend.setStatusbar("Status: Fetching image...", 1)
                    try:
                        tempurl = requests.get(r10url, stream=True)
                    except:
                        frontend.setStatusbar("Zoom: Not selected", 0)
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather couldn't acquire radar data. Please make sure" + 
                                          " you have an internet connection, and that you can access Wunderground's API.")
                        printException()
                        return
                    logger.debug("10 km loop acquired, end result: %s" % tempurl)
                    with open('temp//r10.gif', 'wb') as fw:
                        logger.debug("saving file...")
                        for chunk in tempurl.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                    frontend.setStatusbar("Status: Loading image...", 1)
                    frontend.reloadImage("Viewer", "temp//r10.gif")
                    frontend.setStatusbar("Status: Idle", 1)
                    r10cached = True
                    radar_zoomlevel = "10 km"
                    logger.debug("r10cached: %s ; radar_zoomlevel: %s" %
                                 (r10cached, radar_zoomlevel))
                elif r10cached == True:
                    logger.debug("r10cached is true, fetching from cache...")
                    frontend.setStatusbar("Zoom: 10 km", 0)
                    frontend.setStatusbar("Status: Loading image...", 1)
                    try:
                        frontend.reloadImage("Viewer", "temp//r10.gif")
                    except:
                        frontend.setStatusbar("Zoom: " + radar_zoomlevel, 0)
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather could not acquire cached radar data. Please reselect a" +
                                          " 10 km zoom level again.")
                        printException()
                        r10cached = False
                        logger.debug("r10cached: %s" % r10cached)
                        return
                    frontend.setStatusbar("Status: Idle", 1)
                    radar_zoomlevel = "10 km"
                    logger.debug("radar_zoomlevel: %s" % radar_zoomlevel)
            elif btnName == "20 km":
                logger.debug("r20cached: %s" % r20cached)
                if r20cached == False:
                    logger.debug("r20cached is false, fetching...")
                    frontend.setStatusbar("Zoom: 20 km", 0)
                    frontend.setStatusbar("Status: Fetching image...", 1)
                    try:
                        tempurl = requests.get(r20url, stream=True)
                    except:
                        frontend.setStatusbar("Zoom: Not selected", 0)
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather couldn't acquire radar data. Please make sure" + 
                                          " you have an internet connection, and that you can access Wunderground's API.")
                        printException()
                        return
                    logger.debug("20 km loop acquired, end result: %s" % tempurl)
                    with open('temp//r20.gif', 'wb') as fw:
                        logger.debug("saving file...")
                        for chunk in tempurl.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                    frontend.setStatusbar("Status: Loading image...", 1)
                    frontend.reloadImage("Viewer", "temp//r20.gif")
                    frontend.setStatusbar("Status: Idle", 1)
                    r20cached = True
                    radar_zoomlevel = "20 km"
                    logger.debug("r20cached: %s ; radar_zoomlevel: %s" %
                                 (r20cached, radar_zoomlevel))
                elif r20cached == True:
                    logger.debug("r20cached is true, fetching from cache...")
                    frontend.setStatusbar("Zoom: 20 km", 0)
                    frontend.setStatusbar("Status: Loading image...", 1)
                    try:
                        frontend.reloadImage("Viewer", "temp//r20.gif")
                    except:
                        frontend.setStatusbar("Zoom: " + radar_zoomlevel, 0)
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather could not acquire cached radar data. Please reselect a" +
                                          " 20 km zoom level again.")
                        printException()
                        r20cached = False
                        logger.debug("r20cached: %s" % r20cached)
                        return
                    frontend.setStatusbar("Status: Idle", 1)
                    radar_zoomlevel = "20 km"
                    logger.debug("radar_zoomlevel: %s" % radar_zoomlevel)
            elif btnName == "40 km":
                logger.debug("r40cached: %s" % r40cached)
                if r40cached == False:
                    logger.debug("r40cached is false, fetching...")
                    frontend.setStatusbar("Zoom: 40 km", 0)
                    frontend.setStatusbar("Status: Fetching image...", 1)
                    try:
                        tempurl = requests.get(r40url, stream=True)
                    except:
                        frontend.setStatusbar("Zoom: Not selected", 0)
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather couldn't acquire radar data. Please make sure" + 
                                          " you have an internet connection, and that you can access Wunderground's API.")
                        printException()
                        return
                    logger.debug("40 km loop acquired, end result: %s" % tempurl)
                    with open('temp//r40.gif', 'wb') as fw:
                        logger.debug("saving file...")
                        for chunk in tempurl.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                    frontend.setStatusbar("Status: Loading image...", 1)
                    frontend.reloadImage("Viewer", "temp//r40.gif")
                    frontend.setStatusbar("Status: Idle", 1)
                    r40cached = True
                    radar_zoomlevel = "40 km"
                    logger.debug("r40cached: %s ; radar_zoomlevel: %s" %
                                 (r40cached, radar_zoomlevel))
                elif r40cached == True:
                    logger.debug("r40cached is true, fetching from cache...")
                    frontend.setStatusbar("Zoom: 40 km", 0)
                    frontend.setStatusbar("Status: Loading image...", 1)
                    try:
                        frontend.reloadImage("Viewer", "temp//r40.gif")
                    except:
                        frontend.setStatusbar("Zoom: " + radar_zoomlevel, 0)
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather could not acquire cached radar data. Please reselect a" +
                                          " 40 km zoom level again.")
                        printException()
                        r40cached = False
                        logger.debug("r40cached: %s" % r40cached)
                        return
                    frontend.setStatusbar("Status: Idle", 1)
                    radar_zoomlevel = "40 km"
                    logger.debug("radar_zoomlevel: %s" % radar_zoomlevel)
            elif btnName == "60 km":
                logger.debug("r60cached: %s" % r60cached)
                if r60cached == False:
                    logger.debug("r60cached is false, fetching...")
                    frontend.setStatusbar("Zoom: 60 km", 0)
                    frontend.setStatusbar("Status: Fetching image...", 1)
                    try:
                        tempurl = requests.get(r60url, stream=True)
                    except:
                        frontend.setStatusbar("Zoom: Not selected", 0)
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather couldn't acquire radar data. Please make sure" + 
                                          " you have an internet connection, and that you can access Wunderground's API.")
                        printException()
                        return
                    logger.debug("60 km loop acquired, end result: %s" % tempurl)
                    with open('temp//r60.gif', 'wb') as fw:
                        logger.debug("saving file...")
                        for chunk in tempurl.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                    frontend.setStatusbar("Status: Loading image...", 1)
                    frontend.reloadImage("Viewer", "temp//r60.gif")
                    frontend.setStatusbar("Status: Idle", 1)
                    r60cached = True
                    radar_zoomlevel = "60 km"
                    logger.debug("r60cached: %s ; radar_zoomlevel: %s" %
                                 (r60cached, radar_zoomlevel))
                elif r60cached == True:
                    logger.debug("r60cached is true, fetching from cache...")
                    frontend.setStatusbar("Zoom: 60 km", 0)
                    frontend.setStatusbar("Status: Loading image...", 1)
                    try:
                        frontend.reloadImage("Viewer", "temp//r60.gif")
                    except:
                        frontend.setStatusbar("Zoom: " + radar_zoomlevel, 0)
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather could not acquire cached radar data. Please reselect a" +
                                          " 60 km zoom level again.")
                        printException()
                        r60cached = False
                        logger.debug("r60cached: %s" % r60cached)
                        return
                    frontend.setStatusbar("Status: Idle", 1)
                    radar_zoomlevel = "60 km"
            elif btnName == "80 km":
                logger.debug("r80cached: %s" % r80cached)
                if r80cached == False:
                    logger.debug("r80cached is false, fetching...")
                    frontend.setStatusbar("Zoom: 80 km", 0)
                    frontend.setStatusbar("Status: Fetching image...", 1)
                    try:
                        tempurl = requests.get(r80url, stream=True)
                    except:
                        frontend.setStatusbar("Zoom: Not selected", 0)
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather couldn't acquire radar data. Please make sure" + 
                                          " you have an internet connection, and that you can access Wunderground's API.")
                        printException()
                        return
                    logger.debug("80 km loop acquired, end result: %s" % tempurl)
                    with open('temp//r80.gif', 'wb') as fw:
                        logger.debug("saving file...")
                        for chunk in tempurl.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                    frontend.setStatusbar("Status: Loading image...", 1)
                    frontend.reloadImage("Viewer", "temp//r80.gif")
                    frontend.setStatusbar("Status: Idle", 1)
                    r80cached = True
                    radar_zoomlevel = "80 km"
                    logger.debug("r80cached: %s ; radar_zoomlevel: %s" %
                                 (r80cached, radar_zoomlevel))
                elif r80cached == True:
                    logger.debug("r80cached is true, fetching from cache...")
                    frontend.setStatusbar("Zoom: 80 km", 0)
                    frontend.setStatusbar("Status: Loading image...", 1)
                    try:
                        frontend.reloadImage("Viewer", "temp//r80.gif")
                    except:
                        frontend.setStatusbar("Zoom: " + radar_zoomlevel, 0)
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather could not acquire cached radar data. Please reselect a" +
                                          " 80 km zoom level again.")
                        printException()
                        r80cached = False
                        logger.debug("r80cached: %s" % r80cached)
                        return
                    frontend.setStatusbar("Status: Idle", 1)
                    radar_zoomlevel = "80 km"
                    logger.debug("radar_zoomlevel: %s" % radar_zoomlevel)
            elif btnName == "100 km":
                logger.debug("r100cached: %s" % r100cached)
                if r100cached == False:
                    logger.debug("r100cached is false, fetching...")
                    frontend.setStatusbar("Zoom: 100 km", 0)
                    frontend.setStatusbar("Status: Fetching image...", 1)
                    try:
                        tempurl = requests.get(r100url, stream=True)
                    except:
                        frontend.setStatusbar("Zoom: Not selected", 0)
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather couldn't acquire radar data. Please make sure" + 
                                          " you have an internet connection, and that you can access Wunderground's API.")
                        printException()
                        return
                    logger.debug("100 km loop acquired, end result: %s" % tempurl)
                    with open('temp//r100.gif', 'wb') as fw:
                        logger.debug("saving file...")
                        for chunk in tempurl.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                    frontend.setStatusbar("Status: Loading image...", 1)
                    frontend.reloadImage("Viewer", "temp//r100.gif")
                    frontend.setStatusbar("Status: Idle", 1)
                    r100cached = True
                    radar_zoomlevel = "100 km"
                    logger.debug("r100cached: %s ; radar_zoomlevel: %s" %
                                 (r100cached, radar_zoomlevel))
                elif r100cached == True:
                    logger.debug("r100cached is true, fetching from cache...")
                    frontend.setStatusbar("Zoom: 100 km", 0)
                    frontend.setStatusbar("Status: Loading image...", 1)
                    try:
                        frontend.reloadImage("Viewer", "temp//r100.gif")
                    except:
                        frontend.setStatusbar("Zoom: " + radar_zoomlevel, 0)
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather could not acquire cached radar data. Please reselect a" +
                                          " 100 km zoom level again.")
                        printException()
                        r100cached = False
                        logger.debug("r100cached: %s" % r10cached)
                        return
                    frontend.setStatusbar("Status: Idle", 1)
                    radar_zoomlevel = "100 km"
                    logger.debug("radar_zoomlevel: %s" % radar_zoomlevel)
                    
        def frontend_extrabuttons(btnName):
            global radar_zoomlevel
            if btnName == "Refresh":
                logger.debug("refresh button pressed. zoom level: %s" % radar_zoomlevel)
                if radar_zoomlevel == "None":
                    frontend.warningBox("No zoom level selected!", "Please select a zoom level before using the Refresh button.")
                elif radar_zoomlevel == "10 km":
                    frontend.setStatusbar("Status: Fetching image...", 1)
                    try:
                        tempurl = requests.get(r10url, stream=True)
                    except:
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather couldn't acquire radar data. Please make sure" + 
                                          " you have an internet connection, and that you can access Wunderground's API.")
                        printException()
                        return
                    logger.debug("10 km loop acquired, end result: %s" % tempurl)
                    try:
                        os.remove("temp//r10.gif")
                    except:
                        printException_loggerwarn()
                        
                    with open('temp//r10.gif', 'wb') as fw:
                        logger.debug("saving file...")
                        for chunk in tempurl.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                    frontend.setStatusbar("Status: Loading image...", 1)
                    frontend.reloadImage("Viewer", "temp//r10.gif")
                    frontend.setStatusbar("Status: Idle", 1)
                elif radar_zoomlevel == "20 km":
                    frontend.setStatusbar("Status: Fetching image...", 1)
                    try:
                        tempurl = requests.get(r20url, stream=True)
                    except:
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather couldn't acquire radar data. Please make sure" + 
                                          " you have an internet connection, and that you can access Wunderground's API.")
                        printException()
                        return
                    
                    logger.debug("20 km loop acquired, end result: %s" % tempurl)
                    
                    try:
                        os.remove("temp//r20.gif")
                    except:
                        printException_loggerwarn()
                    
                    with open('temp//r20.gif', 'wb') as fw:
                        logger.debug("saving file...")
                        for chunk in tempurl.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                    frontend.setStatusbar("Status: Loading image...", 1)
                    frontend.reloadImage("Viewer", "temp//r20.gif")
                    frontend.setStatusbar("Status: Idle", 1)
                elif radar_zoomlevel == "40 km":
                    frontend.setStatusbar("Status: Fetching image...", 1)
                    try:
                        tempurl = requests.get(r40url, stream=True)
                    except:
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather couldn't acquire radar data. Please make sure" + 
                                          " you have an internet connection, and that you can access Wunderground's API.")
                        printException()
                        return
                    
                    logger.debug("40 km loop acquired, end result: %s" % tempurl)
                    
                    try:
                        os.remove("temp//r40.gif")
                    except:
                        printException_loggerwarn()
                        
                    with open('temp//r40.gif', 'wb') as fw:
                        logger.debug("saving file...")
                        for chunk in tempurl.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                    frontend.setStatusbar("Status: Loading image...", 1)
                    frontend.reloadImage("Viewer", "temp//r40.gif")
                    frontend.setStatusbar("Status: Idle", 1)
                elif radar_zoomlevel == "60 km":
                    frontend.setStatusbar("Status: Fetching image...", 1)
                    try:
                        tempurl = requests.get(r60url, stream=True)
                    except:
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather couldn't acquire radar data. Please make sure" + 
                                          " you have an internet connection, and that you can access Wunderground's API.")
                        printException()
                        return
                    
                    logger.debug("60 km loop acquired, end result: %s" % tempurl)
                    
                    try:
                        os.remove("temp//r60.gif")
                    except:
                        printException_loggerwarn()
                        
                    with open('temp//r60.gif', 'wb') as fw:
                        logger.debug("saving file...")
                        for chunk in tempurl.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                    frontend.setStatusbar("Status: Loading image...", 1)
                    frontend.reloadImage("Viewer", "temp//r60.gif")
                    frontend.setStatusbar("Status: Idle", 1)
                elif radar_zoomlevel == "80 km":
                    frontend.setStatusbar("Status: Fetching image...", 1)
                    try:
                        tempurl = requests.get(r80url, stream=True)
                    except:
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather couldn't acquire radar data. Please make sure" + 
                                          " you have an internet connection, and that you can access Wunderground's API.")
                        printException()
                        return
                    
                    logger.debug("80 km loop acquired, end result: %s" % tempurl)
                    
                    try:
                        os.remove("temp//r80.gif")
                    except:
                        printException_loggerwarn()
                        
                    with open('temp//r80.gif', 'wb') as fw:
                        logger.debug("saving file...")
                        for chunk in tempurl.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                    frontend.setStatusbar("Status: Loading image...", 1)
                    frontend.reloadImage("Viewer", "temp//r80.gif")
                    frontend.setStatusbar("Status: Idle", 1)
                elif radar_zoomlevel == "100 km":
                    frontend.setStatusbar("Status: Fetching image...", 1)
                    try:
                        tempurl = requests.get(r100url, stream=True)
                    except:
                        frontend.setStatusbar("Status: Idle", 1)
                        frontend.errorBox("Could not acquire radar data!", 
                                          "PyWeather couldn't acquire radar data. Please make sure" + 
                                          " you have an internet connection, and that you can access Wunderground's API.")
                        printException()
                        return
                    
                    logger.debug("100 km loop acquired, end result: %s" % tempurl)
                    
                    try:
                        os.remove("temp//r100.gif")
                    except:
                        printException_loggerwarn()
                        
                    with open('temp//r100.gif', 'wb') as fw:
                        logger.debug("saving file...")
                        for chunk in tempurl.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                    frontend.setStatusbar("Status: Loading image...", 1)
                    frontend.reloadImage("Viewer", "temp//r100.gif")
                    frontend.setStatusbar("Status: Idle", 1)
            elif btnName == "Empty Cache":
                radar_confirmation = frontend.yesNoBox("Empty the cache?", 
                                                       "Would you like to empty the cache? If you do" +
                                                       ", you'll need to reselect a zoom level.")
                if radar_confirmation == False:
                    logger.debug("not emptying cache.")
                elif radar_confirmation == True:
                    logger.debug("emptying cache.")
                    r10cached = False
                    r20cached = False
                    logger.debug("r10cached: %s ; r20cached: %s" %
                                 (r10cached, r20cached))
                    r40cached = False
                    r60cached = False
                    logger.debug("r40cached: %s ; r60cached: %s" %
                                 (r40cached, r60cached))
                    r80cached = False
                    r100cached = False
                    # We have to try each removal, or we may hit errors.
                    radar_clearImages()
                    frontend.clearImageCache()
                if user_radarImageSize == "extrasmall":
                    frontend.reloadImage("Viewer", "storage//320x240placeholder.gif")
                elif user_radarImageSize == "small":
                    frontend.reloadImage("Viewer", "storage//480x360placeholder.gif")
                elif user_radarImageSize == "normal":
                    frontend.reloadImage("Viewer", "storage//640x480placeholder.gif")
                elif user_radarImageSize == "large":
                    frontend.reloadImage("Viewer", "storage//960x720placeholder.gif")
                elif user_radarImageSize == "extralarge":
                    frontend.reloadImage("Viewer", "storage//1280x960placeholder.gif") 
                frontend.setStatusbar("Zoom: Not selected", 0)
                radar_zoomlevel = "None"
                logger.debug("radar_zoomlevel: %s" % radar_zoomlevel)
            elif btnName == "Return to PyWeather":
                frontend.stop()
                radar_clearImages()   
                
        def frontend_playerControls(btnName):
            if btnName == "Play":
                frontend.startAnimation("Viewer")
            elif btnName == "Pause":
                frontend.stopAnimation("Viewer")
        frontend.clearImageCache()       
        frontend.setTitle("PyWeather Radar Viewer - version 0.6.1 beta")
        frontend.setResizable(canResize=False)
        frontend.startLabelFrame("Viewer", column=0, row=0, colspan=3)
        # Placeholders are needed to start the viewer.
        if user_radarImageSize == "extrasmall":
            frontend.addImage("Viewer", "storage//320x240placeholder.gif")
        elif user_radarImageSize == "small":
            frontend.addImage("Viewer", "storage//480x360placeholder.gif")
        elif user_radarImageSize == "normal":
            frontend.addImage("Viewer", "storage//640x480placeholder.gif")
        elif user_radarImageSize == "large":
            frontend.addImage("Viewer", "storage//960x720placeholder.gif")
        elif user_radarImageSize == "extralarge":
            frontend.addImage("Viewer", "storage//1280x960placeholder.gif")
        frontend.stopLabelFrame()
        frontend.addLabel("mid2label", "Animation Control", column=0, row=2)
        frontend.addButtons(["Play", "Pause"], frontend_playerControls, column=0, row=3, colspan=3)
        frontend.addLabel("midlabel", "Zoom Control", column=0, row=4, colspan=3)
        frontend.addButtons(["10 km", "20 km", "40 km"], frontend_zoomswitch, column=0, row=5, colspan=3)
        frontend.addButtons(["60 km", "80 km", "100 km"], frontend_zoomswitch, row=6, column=0, colspan=3)
        frontend.addButtons(["Refresh", "Empty Cache", "Return to PyWeather"], frontend_extrabuttons, row=7, column=0, colspan=3)
        frontend.setInPadding([10, 10])
        frontend.addStatusbar(fields=2)
        frontend.setStatusbar("Zoom: Not selected", 0)
        frontend.setStatusbar("Status: Idle", 1)
        frontend.go()
    elif moreoptions == "12":
        sys.exit()
    elif moreoptions == "10":
        logger.info("Selected update.")
        logger.debug("buildnumber: %s ; buildversion: %s" %
                    (buildnumber, buildversion))
        print("Checking for updates. This should only take a few seconds.")
        try:
            versioncheck = requests.get("https://raw.githubusercontent.com/o355/pyweather/master/updater/versioncheck.json")
            releasenotes = requests.get("https://raw.githubusercontent.com/o355/pyweather/master/updater/releasenotes.txt")
            logger.debug("versioncheck: %s" % versioncheck)
        except:
            logger.warn("Couldn't check for updates! Is there an internet connection?")
            print("When attempting to fetch the update data file, PyWeather",
                  "ran into an error. If you're on a network with a filter,",
                  "make sure that 'raw.githubusercontent.com' is unblocked. Otherwise,",
                  "make sure that you have an internet connecction.", sep="\n")
            printException()
            continue
        versionJSON = json.loads(versioncheck.text)
        if jsonVerbosity == True:
            logger.debug("versionJSON: %s" % versionJSON)
        logger.debug("Loaded versionJSON with reader %s" % reader)
        version_buildNumber = float(versionJSON['updater']['latestbuild'])
        version_latestVersion = versionJSON['updater']['latestversion']
        version_latestURL = versionJSON['updater']['latesturl']
        version_latestFileName = versionJSON['updater']['latestfilename']
        version_latestReleaseTag = versionJSON['updater']['latestversiontag']
        version_newversionreleasedate = versionJSON['updater']['nextversionreleasedate']
        version_latestReleaseDate = versionJSON['updater']['releasedate']
        logger.debug("version_buildNumber: %s ; version_latestVersion: %s" %
                     (version_buildNumber, version_latestVersion))
        logger.debug("version_latestURL: %s ; version_latestFileName: %s" %
                     (version_latestURL, version_latestFileName))
        logger.debug("version_latestReleaseTag: %s" %
                     (version_latestReleaseTag))
        logger.debug("version_newversionreleasedate: %s ; version_latestReleaseDate: %s" %
                     (version_newversionreleasedate, version_latestReleaseDate))
        if buildnumber >= version_buildNumber:
            logger.info("PyWeather is up to date.")
            logger.info("local build (%s) >= latest build (%s)"
                        % (buildnumber, version_buildNumber))
            print("")
            print(Fore.GREEN + "PyWeather is up to date!")
            print("You have version: " + Fore.CYAN + buildversion)
            print(Fore.GREEN + "The latest version is: " + Fore.CYAN 
                  + version_latestVersion)
            if user_showUpdaterReleaseTag == True:
                print(Fore.GREEN + "The latest release tag is: " + Fore.CYAN 
                      + version_latestReleaseTag)
            if showNewVersionReleaseDate == True:
                print(Fore.GREEN + "Psst, a new version of PyWeather should get released on: "
                      + Fore.CYAN + version_newversionreleasedate)
            if showUpdaterReleaseNotes_uptodate == True:
                print(Fore.GREEN + "Here's the release notes for this release:",
                      Fore.CYAN + releasenotes.text, sep="\n")
        elif buildnumber < version_buildNumber:
            print("")
            logger.warn("PyWeather is NOT up to date.")
            logger.warn("local build (%s) < latest build (%s)"
                        % (buildnumber, version_buildNumber))
            print(Fore.RED + "PyWeather is not up to date! :(")
            print(Fore.RED + "You have version: " + Fore.CYAN + buildversion)
            print(Fore.RED + "The latest version is: " + Fore.CYAN + version_latestVersion)
            print(Fore.RED + "And it was released on: " + Fore.CYAN + version_latestReleaseDate)
            if user_showUpdaterReleaseTag == True:
                print(Fore.RED + "The latest release tag is: " + Fore.CYAN + version_latestReleaseTag)
            if showUpdaterReleaseNotes == True:
                print(Fore.RED + "Here's the release notes for the latest release:",
                      Fore.CYAN + releasenotes.text, sep="\n")
            print("")
            print(Fore.RED + "Would you like to download the latest version?" + Fore.YELLOW)
            downloadLatest = input("Yes or No: ").lower()
            logger.debug("downloadLatest: %s" % downloadLatest)
            if downloadLatest == "yes":
                if allowGitForUpdating == True:
                    print("Would you like to use Git to update PyWeather?",
                          "Yes or No.")
                    confirmUpdateWithGit = input("Input here: ").lower()
                    if confirmUpdateWithGit == "yes":
                        print("Now updating with Git.")
                        try:
                            subprocess.call(["git fetch"], shell=True)
                            subprocess.call(["git stash"], shell=True)
                            subprocess.call(["git checkout %s" % version_latestReleaseTag],
                                            shell=True)
                            print("Now updating your config file.")
                            exec(open("configupdate.py").read())
                            print("PyWeather has been updated to version %s." % version_latestReleaseTag,
                                  "To finish the update, PyWeather has to exit.",
                                  "Press enter to exit.", sep="\n")
                            input()
                            sys.exit()
                        except:
                            print("When attempting to update using git, either",
                                  "when doing `git fetch`, `git checkout`, or to",
                                  "execute the configupdate script, an error occurred."
                                  "We can try updating using the .zip method.",
                                  "Would you like to update PyWeather using the .zip method?",
                                  "Yes or No.", sep="\n")
                            printException()
                            confirmZipDownload = input("Input here: ").lower()
                            if confirmZipDownload == "yes":
                                print("Downloading using the .zip method.")
                            elif confirmZipDownload == "no":
                                print("Not downloading latest updates using the",
                                      ".zip method.", sep="\n")
                                continue
                            else:
                                print("Couldn't understand your input. Defaulting",
                                      "to downloading using a .zip.", sep="\n")
                    # The unnecessary amounts of confirms was to boost the line count to 2,000.
                    elif confirmUpdateWithGit == "no":
                        print("Not updating with Git. Would you like to update",
                              "PyWeather using the .zip download option?",
                              "Yes or No.", sep="\n")
                        confirmZipDownload = input("Input here: ").lower()
                        if confirmZipDownload == "yes":
                            print("Downloading the latest update with a .zip.")
                        elif confirmZipDownload == "no":
                            print("Not downloading the latest PyWeather updates.")
                            continue
                        else:
                            print("Couldn't understand your input. Defaulting to",
                                  "downloading the latest version with a .zip.", sep="\n")
                    else:
                        print("Couldn't understand your input. Defaulting to",
                              "downloading the latest version with a .zip.", sep="\n")        
                print("")
                logger.debug("Downloading latest version...")
                print(Fore.YELLOW + "Downloading the latest version of PyWeather...")
                try:
                    updatezip = requests.get(version_latestURL)
                    with open(version_latestFileName, 'wb') as fw:
                        for chunk in updatezip.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                except:
                    logger.warn("Couldn't download the latest version!")
                    logger.warn("Is the internet online?")
                    print("When attempting to download the latest .zip file",
                          "for PyWeather, an error occurred. If you're on a",
                          "network with a filter, make sure that",
                          "'raw.githubusercontent.com' is unblocked.",
                          "Otherwise, make sure you have an internet connection.",
                          sep="\n")
                    logger.error("Here's the full traceback (for bug reports):")
                    printException()
                    continue
                logger.debug("Latest version was saved, filename: %s"
                            % version_latestFileName)
                print(Fore.YELLOW + "The latest version of PyWeather was downloaded " +
                      "to the base directory of PyWeather, and saved as " +
                      Fore.CYAN + version_latestFileName + Fore.YELLOW + ".")
                continue
            elif downloadLatest == "no":
                logger.debug("Not downloading the latest version.")
                print(Fore.YELLOW + "Not downloading the latest version of PyWeather.")
                print("For reference, you can download the latest version of PyWeather at:")
                print(Fore.CYAN + version_latestURL)
                continue
            else:
                logger.warn("Input could not be understood!")
                print(Fore.GREEN + "Your input couldn't be understood.")
                continue
        else:
            logger.warn("PW updater failed. Variables corrupt, maybe?")
            print("When attempting to compare version variables, PyWeather ran",
                  "into an error. This error is extremely rare. Make sure you're",
                  "not trying to travel through a wormhole with Cooper, and report",
                  "the error on GitHub, while it's around.", sep='\n')
            continue
    elif moreoptions == "5":
        logger.info("Selected option: almanac")
        print(Fore.RED + "Loading, please wait...")
        print("")
        try:
            logger.debug("almanac_prefetched: %s ; almanac cache time: %s" %
                         (almanac_prefetched, time.time() - cachetime_almanac))
        except:
            logger.debug("almanac_prefetched: %s" % almanac_prefetched)
            
        logger.debug("refresh_almanacflagged: %s" % refresh_almanacflagged)
        if (almanac_prefetched == False or time.time() - cachetime_almanac >= cache_almanactime
            or refresh_almanacflagged == True):
            print(Fore.RED + "Fetching (or refreshing) almanac data...")
            try:
                almanacJSON = requests.get(almanacurl)
                logger.debug("almanacJSON fetched with end result: %s" % almanacJSON)
                cachetime_almanac = time.time()
            except:
                logger.warn("Couldn't contact Wunderground's API! Is the internet offline?")
                print("When fetching the almanac data from Wunderground, PyWeather ran into",
                      "an error. If you're on a network with a filter, make sure that",
                      "'api.wunderground.com' is unblocked. Otherwise, make sure you have",
                      "an internet connection, and that Wunderground's HAL9000 is online.")
                printException()
                print("Press enter to continue.")
                input()
                continue
            
            almanac_prefetched = True
            refresh_almanacflagged = False
            logger.debug("almanac_prefetched: %s ; refresh_almanacflagged: %s" %
                         (almanac_prefetched, refresh_almanacflagged))
            almanac_json = json.loads(almanacJSON.text)
            if jsonVerbosity == True:
                logger.debug("almanac_json: %s" % almanac_json)
            else:
                logger.debug("1 JSON loaded successfully.")
            
            almanac_airportCode = almanac_json['almanac']['airport_code']
            almanac_normalHighF = str(almanac_json['almanac']['temp_high']['normal']['F'])
            almanac_normalHighC = str(almanac_json['almanac']['temp_high']['normal']['C'])
            almanac_recordHighF = str(almanac_json['almanac']['temp_high']['record']['F'])
            logger.debug("almanac_airportCode: %s ; almanac_normalHighF: %s"
                         % (almanac_airportCode, almanac_normalHighF))
            logger.debug("almanac_normalHighC: %s ; almanac_recordHighF: %s"
                         % (almanac_normalHighC, almanac_recordHighF))
            almanac_recordHighC = str(almanac_json['almanac']['temp_high']['record']['C'])
            almanac_recordHighYear = str(almanac_json['almanac']['temp_high']['recordyear'])
            almanac_normalLowF = str(almanac_json['almanac']['temp_low']['normal']['F'])
            almanac_normalLowC = str(almanac_json['almanac']['temp_low']['normal']['C'])
            logger.debug("almanac_recordHighC: %s ; almanac_recordHighYear: %s"
                         % (almanac_recordHighC, almanac_recordHighYear))
            logger.debug("almanac_normalLowF: %s ; almanac_normalLowC: %s"
                         % (almanac_normalLowF, almanac_normalLowC))
            almanac_recordLowF = str(almanac_json['almanac']['temp_low']['record']['F'])
            almanac_recordLowC = str(almanac_json['almanac']['temp_low']['record']['C'])
            almanac_recordLowYear = str(almanac_json['almanac']['temp_low']['recordyear'])
            logger.debug("alamanac_recordLowF: %s ; almanac_recordLowC: %s"
                         % (almanac_recordLowF, almanac_recordLowC))
            logger.debug("almanac_recordLowYear: %s" % almanac_recordLowYear)
        
        print(Fore.YELLOW + "Here's the almanac for: " + Fore.CYAN +
              almanac_airportCode + Fore.YELLOW + " (the nearest airport)")
        print("")
        print(Fore.YELLOW + "Record High: " + Fore.CYAN + almanac_recordHighF + "°F ("
              + almanac_recordHighC + "°C)")
        print(Fore.YELLOW + "With the record being set in: " + Fore.CYAN
              + almanac_recordHighYear)
        print(Fore.YELLOW + "Normal High: " + Fore.CYAN + almanac_normalHighF
              + "°F (" + almanac_normalHighC + "°C)")
        print("")
        print(Fore.YELLOW + "Record Low: " + Fore.CYAN + almanac_recordLowF + "°F ("
              + almanac_recordLowC + "°C)")
        print(Fore.YELLOW + "With the record being set in: " + Fore.CYAN
              + almanac_recordLowYear)
        print(Fore.YELLOW + "Normal Low: " + Fore.CYAN + almanac_normalLowF + "°F ("
              + almanac_normalLowC + "°C)")
        print("")
    elif moreoptions == "7":
        print(Fore.RED + "Loading, please wait a few seconds...")
        print("")
        try:
            logger.debug("sundata_prefetched: %s ; sundata cache time: %s" %
                         (sundata_prefetched, time.time() - cachetime_sundata))
        except:
            logger.debug("sundata_prefetched: %s" % sundata_prefetched)
            
        logger.debug("refresh_sundataflagged: %s" % refresh_sundataflagged)
        logger.info("Selected option - Sun/moon data")
        if (sundata_prefetched == False or time.time() - cachetime_sundata >= cache_sundatatime
            or refresh_sundataflagged == True):
            print(Fore.RED + "Fetching (or refreshing) sun/moon data...")
            try:
                sundataJSON = requests.get(astronomyurl)
                logger.debug("Retrieved sundata JSON with response: %s" % sundataJSON)
                cachetime_sundata = time.time()
                
            except:
                print("When attempting to fetch the 'sundata' from Wunderground,",
                      "PyWeather ran into an error. If you're on a network with",
                      "a filter, make sure 'api.wunderground.com' is unblocked.",
                      "Otherwise, make sure you have an internet connection.", sep="\n")
                printException()
                print("Press enter to continue.")
                input()
                continue
            
            sundata_prefetched = True
            refresh_sundataflagged = False
            logger.debug("sundata_prefetched: %s ; refresh_sundataflagged: %s" %
                         (sundata_prefetched, refresh_sundataflagged))
            
            astronomy_json = json.loads(sundataJSON.text)
            if jsonVerbosity == True:
                logger.debug("astronomy_json: %s" % astronomy_json)
            else:
                logger.debug("astronomy json loaded.")
                
            SR_minute = int(astronomy_json['moon_phase']['sunrise']['minute'])
            SR_hour = int(astronomy_json['moon_phase']['sunrise']['hour'])
            logger.debug("SR_minute: %s ; SR_hour: %s" %
                        (SR_minute, SR_hour))
            if SR_hour == 0:
                logger.debug("Sunrise hour = 0. Prefixing AM, 12-hr correction...")
                SR_hour = "12"
                SR_minute = str(SR_minute).zfill(2)
                sunrise_time = SR_hour + ":" + SR_minute + " AM"
                logger.debug("SR_hour : %s ; SR_minute: %s" %
                             (SR_hour, SR_minute))
                logger.debug("sunrise_time: %s" % sunrise_time)
            elif SR_hour > 12:
                logger.debug("Sunrise Hour > 12. Prefixing PM, 12-hr correction...")
                SR_hour = SR_hour - 12
                SR_hour = str(SR_hour)
                SR_minute = str(SR_minute).zfill(2)
                sunrise_time = SR_hour + ":" + SR_minute + " PM"
                logger.debug("SR_hour: %s ; SR_minute: %s" %
                             (SR_hour, SR_minute))
                logger.debug("sunrise_time: %s" % sunrise_time)
            elif SR_hour == 12:
                logger.debug("Sunrise Hour = 12. Prefixing PM.")
                SR_hour = str(SR_hour)
                SR_minute = str(SR_minute).zfill(2)
                sunrise_time = SR_hour + ":" + SR_minute + " PM"
                logger.debug("SR_hour: %s ; SR_minute: %s" %
                             (SR_hour, SR_minute))
                logger.debug("SR_minute: %s" % SR_minute)
            else:
                logger.debug("Sunrise Hour < 12. Prefixing AM.")
                SR_hour = str(SR_hour)
                SR_minute = str(SR_minute).zfill(2)
                sunrise_time = SR_hour + ":" + SR_minute + " AM"
                logger.debug("SR_hour: %s ; SR_minute: %s" %
                             (SR_hour, SR_minute))
                logger.debug("sunrise_time: %s" % sunrise_time)

            SS_minute = int(astronomy_json['moon_phase']['sunset']['minute'])
            SS_hour = int(astronomy_json['moon_phase']['sunset']['hour'])
            logger.debug("SS_minute: %s ; SS_hour: %s" %
                         (SS_minute, SS_hour))
            
            if SS_hour == 0:
                logger.debug("Sunset hour = 0. Prefixing AM, 12-hr correction...")
                SS_hour = "0"
                SS_minute = str(SS_minute).zfill(2)
                sunset_time = SS_hour + ":" + SS_minute + " AM"
                logger.debug("SS_hour: %s ; SS_minute: %s" %
                             (SS_hour, SS_minute))
                logger.debug("sunset_time: %s" % sunset_time)
            elif SS_hour > 12:
                logger.debug("Sunset hour > 12. Prefixing PM, 12-hr correction...")
                SS_hour = SS_hour - 12
                SS_hour = str(SS_hour)
                SS_minute = str(SS_minute).zfill(2)
                sunset_time = SS_hour + ":" + SS_minute + " PM"
                logger.debug("SS_hour: %s ; SS_minute: %s"
                             % (SS_hour, SS_minute))
                logger.debug("sunset_time: %s" % sunset_time)
            elif SS_hour == 12:
                logger.debug("Sunset hour = 12. Prefixing PM...")
                SS_hour = str(SS_hour)
                SS_minute = str(SS_minute).zfill(2)
                sunset_time = SS_hour + ":" + SS_minute + " PM"
                logger.debug("SS_hour: %s ; SS_minute: %s"
                             % (SS_hour, SS_minute))
                logger.debug("sunset_time: %s" % sunset_time)
            else:
                logger.debug("Sunset hour < 12. Prefixing AM...")
                SS_hour = str(SS_hour)
                SS_minute = str(SS_minute).zfill(2)
                sunset_time = SS_hour + ":" + SS_minute + " AM"
                logger.debug("SS_hour: %s ; SS_minute: %s"
                             % (SS_hour, SS_minute))
                logger.debug("sunset_time: %s" % sunset_time)
            sundata_prefetched = True
            logger.debug("sundata_prefetched: %s" % sundata_prefetched)
                
        moon_percentIlluminated = str(astronomy_json['moon_phase']['percentIlluminated'])
        moon_age = str(astronomy_json['moon_phase']['ageOfMoon'])
        moon_phase = astronomy_json['moon_phase']['phaseofMoon']
        MR_minute = int(astronomy_json['moon_phase']['moonrise']['minute'])
        logger.debug("moon_percentIlluminated: %s ; moon_age: %s"
                     % (moon_percentIlluminated, moon_age))
        logger.debug("moon_phase: %s ; MR_minute: %s" %
                     (moon_phase, MR_minute))
        MR_hour = int(astronomy_json['moon_phase']['moonrise']['hour'])
        logger.debug("MR_minute: %s" % MR_minute)
           
        if MR_hour == 0:
            logger.debug("Moonrise hour is 0. Prefixing AM, and 12-hr correction...")
            MR_hour = "12"
            MR_minute = str(MR_minute).zfill(2)
            moonrise_time = MR_hour + ":" + MR_minute + " AM" 
            logger.debug("MR_hour: %s ; MR_minute: %s" %
                         (MR_hour, MR_minute))
            logger.debug("moonrise_time: %s" % moonrise_time)   
        elif MR_hour > 12:
            logger.debug("Moonrise hour > 12. Prefixing PM, 12-hr correction...")
            MR_hour = MR_hour - 12
            MR_hour = str(MR_hour)
            MR_minute = str(MR_minute).zfill(2)
            moonrise_time = MR_hour + ":" + MR_minute + " PM"
            logger.debug("MR_hour: %s ; MR_minute: %s"
                         % (MR_hour, MR_minute))
            logger.debug("moonrise_time: %s" % moonrise_time)
        elif MR_hour == 12:
            logger.debug("Moonrise hour = 12. Prefixing PM...")
            MR_hour = str(MR_hour)
            MR_minute = str(MR_minute).zfill(2)
            moonrise_time = MR_hour + ":" + MR_minute + " PM"
            logger.debug("MR_hour: %s ; MR_minute: %s" %
                         (MR_hour, MR_minute))
            logger.debug("moonrise_time: %s" % moonrise_time)
        else:
            logger.debug("Moonrise hour < 12. Prefixing AM...")
            MR_hour = str(MR_hour)
            MR_minute = str(MR_minute).zfill(2)
            moonrise_time = MR_hour + ":" + MR_minute + " AM"
            logger.debug("MR_hour: %s ; MR_minute: %s" %
                         (MR_hour, MR_minute))
            logger.debug("moonrise_time: %s" % moonrise_time)
        
        try:    
            MS_minute = int(astronomy_json['moon_phase']['moonset']['minute'])
            MS_hour = int(astronomy_json['moon_phase']['moonset']['hour'])
            MS_data = True
            logger.debug("MS_minute: %s ; MS_hour: %s" %
                         (MS_minute, MS_hour))
            logger.debug("MS_data: %s" % MS_data)
        except:
            logger.warn("Moonset data is not available!")
            printException_loggerwarn()
            MS_data = False
            moonset_time = "Unavailable"
            logger.debug("MS_data: %s ; moonset_time: %s"
                         % (MS_data, moonset_time))
        
        if MS_data == True:
            logger.debug("Moonset data is available. Preceding with checks...")
            
            if MS_hour == 0:
                logger.debug("Moonset hour is 0. Prefixing AM, 12-hr correction...")
                MS_hour = "12"
                MS_minute = str(MS_minute).zfill(2)
                moonset_time = MS_hour + ":" + MS_minute + " AM"
                logger.debug("MS_hour: %s ; MS_minute: %s"
                             % (MS_hour, MS_minute))
                logger.debug("moonset_time: %s" % moonset_time)
            elif MS_hour > 12:
                logger.debug("Moonset hour > 12. Prefixing PM, 12-hr correction...")
                MS_hour = MS_hour - 12
                MS_hour = str(MS_hour)
                MS_minute = str(MS_minute).zfill(2)
                moonset_time = MS_hour + ":" + MS_minute + " PM"
                logger.debug("MS_hour: %s ; MS_minute: %s"
                             % (MS_hour, MS_minute))
                logger.debug("moonset_time: %s" % moonset_time)
            elif MS_hour == 12:
                logger.debug("Moonset hour = 12. Prefixing PM...")
                MS_hour = str(MS_hour)
                MS_minute = str(MS_minute).zfill(2)
                moonset_time = MS_hour + ":" + MS_minute + " PM"
                logger.debug("MS_hour: %s ; MS_minute: %s"
                             % (MS_hour, MS_minute))
                logger.debug("moonset_time: %s" % moonset_time)
            elif MS_hour < 12 and MS_data == True:
                logger.debug("Moonset hour < 12. Prefixing AM...")
                MS_hour = str(MS_hour)
                MS_minute = str(MS_minute).zfill(2)
                moonset_time = MS_hour + ":" + MS_minute + " AM"
                logger.debug("MS_hour: %s ; MS_minute: %s"
                             % (MS_hour, MS_minute))
                logger.debug("moonset_time: %s")
            else:
                MS_data = False
                moonset_time = "Unavailable"
                logger.debug("MS_data: %s ; moonset_time: %s" %
                             (MS_data, moonset_time))
        
        logger.info("Printing data...")
        print(Fore.YELLOW + "Here's the detailed sun/moon data for: " +
              Fore.CYAN + str(location))
        print("")
        print(Fore.YELLOW + "Sunrise time: " + Fore.CYAN + sunrise_time)
        print(Fore.YELLOW + "Sunset time: " + Fore.CYAN + sunset_time)
        print(Fore.YELLOW + "Moonrise time: " + Fore.CYAN + moonrise_time)
        print(Fore.YELLOW + "Moonset time: " + Fore.CYAN + moonset_time)
        print("")
        print(Fore.YELLOW + "Percent of the moon illuminated: "
              + Fore.CYAN + moon_percentIlluminated + "%")
        print(Fore.YELLOW + "Age of the moon: " + Fore.CYAN +
              moon_age + " days")
        print(Fore.YELLOW + "Phase of the moon: " + Fore.CYAN +
              moon_phase)
    elif moreoptions == "6":
        print(Fore.RESET + "To show historical data for this location, please enter a date to show the data.")
        print("The date must be in the format YYYYMMDD.")
        print("E.g: If I wanted to see the weather for February 15, 2013, you'd enter 20130215.")
        print("Input the desired date below.")
        historical_input = input("Input here: ").lower()
        logger.debug("historical_input: %s" % historical_input)
        print(Fore.RED + "Loading...")
        print("")
        historical_loops = 0
        historical_totalloops = 0
        logger.debug("historical_loops: %s ; historical_totalloops: %s"
                     % (historical_loops, historical_totalloops))
        historicalurl = 'http://api.wunderground.com/api/' + apikey + '/history_' + historical_input +  '/q/' + latstr + "," + lonstr + '.json'
        logger.debug("historicalurl: %s" % historicalurl)
        
        historical_skipfetch = False
        logger.debug("historical_skipfetch: %s" % historical_skipfetch)
        
        for historical_cacheddate, payload in historical_cache.items():
            logger.debug("historical_cacheddate: %s")
            if historical_cacheddate == historical_input:
                print(Fore.RED + "Loading cached data...")
                historical_json = payload
                if jsonVerbosity == True:
                    logger.debug("historical_json: %s" % historical_json)
                historical_skipfetch = True
                logger.debug("historical_skipfetch: %s" % historical_skipfetch)
                break
            else:
                historical_skipfetch = False
                logger.debug("historical_skipfetch: %s" % historical_skipfetch)
                
                
        if historical_skipfetch == False:
            try:
                historicalJSON = requests.get(historicalurl)
                logger.debug("historicalJSON acquired, end response: %s" % historicalJSON)
            except:
                print("When attempting to fetch historical data, PyWeather ran into",
                      "an error. If you're on a network with a filter make sure that",
                      "'api.wunderground.com' is unblocked. Otherwise, make sure that",
                      "you have an internet connection, and that your DeLorean works.",
                      sep="\n")
                printException()
                print("Press enter to continue.")
                input()
                continue
        
        
            historical_json = json.loads(historicalJSON.text)
            historical_cache[historical_input] = historical_json
            logger.debug("Appended new key to historal cache: %s with value historical json"
                         % historical_input)
            if jsonVerbosity == True:
                logger.debug("historical_json: %s" % historical_json)
            else:
                logger.debug("Loaded 1 JSON.")
        historical_date = historical_json['history']['date']['pretty']
        print(Fore.YELLOW + "Here's the historical weather for " + Fore.CYAN + 
              str(location) + Fore.YELLOW + " on "
              + Fore.CYAN + historical_date)
        logger.debug("historical_date: %s" % historical_date)
        for data in historical_json['history']['dailysummary']:
            print("")
            # historicals: historical Summary
            #                         ^
            historicals_avgTempF = str(data['meantempi'])
            historicals_avgTempC = str(data['meantempm'])
            historicals_avgDewpointF = str(data['meandewpti'])
            historicals_avgDewpointC = str(data['meandewptm'])
            logger.debug("historicals_avgTempF: %s ; historicals_avgTempC: %s" %
                         (historicals_avgTempF, historicals_avgTempC))
            logger.debug("historicals_avgDewpointF: %s ; historicals_avgDewpointC: %s" %
                         (historicals_avgDewpointF, historicals_avgDewpointC))
            historicals_avgPressureMB = str(data['meanpressurem'])
            historicals_avgPressureInHg = str(data['meanpressurei'])
            historicals_avgWindSpeedMPH = str(data['meanwindspdi'])
            historicals_avgWindSpeedKPH = str(data['meanwindspdm'])
            logger.debug("historicals_avgPressureMB: %s ; historicals_avgPressureInHg: %s" %
                         (historicals_avgPressureMB, historicals_avgPressureInHg))
            logger.debug("historicals_avgWindSpeedMPH: %s ; historicals_avgWindSpeedKPH: %s" %
                         (historicals_avgWindSpeedMPH, historicals_avgWindSpeedKPH))
            historicals_avgWindDegrees = str(data['meanwdird'])
            historicals_avgWindDirection = data['meanwdire']
            historicals_avgVisibilityMI = str(data['meanvisi'])
            historicals_avgVisibilityKM = str(data['meanvism'])
            logger.debug("historicals_avgWindDegrees: %s ; historicals_avgWindDirection: %s" % 
                         (historicals_avgWindDegrees, historicals_avgWindDirection))
            logger.debug("historicals_avgVisibilityMI: %s ; historicals_avgVisibilityKM: %s" %
                         (historicals_avgVisibilityMI, historicals_avgVisibilityKM))
            historicals_maxHumidity = int(data['maxhumidity'])
            historicals_minHumidity = int(data['minhumidity'])
            logger.debug("historicals_maxHumidity: %s ; historicals_minHumidity: %s" %
                         (historicals_maxHumidity, historicals_minHumidity))
            # This is a really nieve way of calculating the average humidity. Sue me.
            # In reality, WU spits out nothing for average humidity.
            historicals_avgHumidity = (historicals_maxHumidity + 
                                       historicals_minHumidity)
            historicals_avgHumidity = (historicals_avgHumidity / 2)
            logger.debug("historicals_avgHumidity: %s" % historicals_avgHumidity)
            historicals_maxHumidity = str(data['maxhumidity'])
            historicals_minHumidity = str(data['minhumidity'])
            historicals_avgHumidity = str(historicals_avgHumidity)
            logger.info("Converted 3 vars to str.")
            historicals_maxTempF = str(data['maxtempi'])
            historicals_maxTempC = str(data['maxtempm'])
            historicals_minTempF = str(data['mintempi'])
            historicals_minTempC = str(data['mintempm'])
            logger.debug("historicals_maxTempF: %s ; historicals_maxTempC: %s" %
                         (historicals_maxTempF, historicals_maxTempC))
            logger.debug("historicals_minTempF: %s ; historicals_minTempC: %s" %
                         (historicals_minTempF, historicals_minTempC))
            historicals_maxDewpointF = str(data['maxdewpti'])
            historicals_maxDewpointC = str(data['maxdewptm'])
            historicals_minDewpointF = str(data['mindewpti'])
            historicals_minDewpointC = str(data['mindewptm'])
            logger.debug("historicals_maxDewpointF: %s ; historicals_maxDewpointC: %s" %
                         (historicals_maxDewpointF, historicals_maxDewpointC))
            logger.debug("historicals_minDewpointF: %s ; historicals_minDewpointC: %s" %
                         (historicals_minDewpointF, historicals_minDewpointC))
            historicals_maxPressureInHg = str(data['maxpressurei'])
            historicals_maxPressureMB = str(data['maxpressurem'])
            historicals_minPressureInHg = str(data['minpressurei'])
            historicals_minPressureMB = str(data['minpressurem'])
            logger.debug("historicals_maxPressureInHg: %s ; historicals_maxPressureMB: %s" %
                         (historicals_maxPressureInHg, historicals_maxPressureMB))
            logger.debug("historicals_minPressureInHg: %s ; historicals_minPressureMB: %s" %
                         (historicals_minPressureInHg, historicals_minPressureMB))
            historicals_maxWindMPH = str(data['maxwspdi'])
            historicals_maxWindKPH = str(data['maxwspdm'])
            historicals_minWindMPH = str(data['minwspdi'])
            historicals_minWindKPH = str(data['minwspdm'])
            logger.debug("historicals_maxWindMPH: %s ; historicals_maxWindKPH: %s" %
                         (historicals_maxWindMPH, historicals_maxWindMPH))
            logger.debug("historicals_minWindMPH: %s ; historicals_minWindKPH: %s" %
                         (historicals_minWindMPH, historicals_minWindKPH))
            historicals_maxVisibilityMI = str(data['maxvisi'])
            historicals_maxVisibilityKM = str(data['maxvism'])
            historicals_minVisibilityMI = str(data['minvisi'])
            historicals_minVisibilityKM = str(data['minvism'])
            logger.debug("historicals_maxVisibilityMI: %s ; historicals_maxVisibilityKM: %s" %
                         (historicals_maxVisibilityMI, historicals_maxVisibilityKM))
            logger.debug("historicals_minVisibilityMI: %s ; historicals_minVisibilityKM: %s" %
                         (historicals_minVisibilityMI, historicals_minVisibilityKM))
            historicals_precipMM = str(data['precipm'])
            historicals_precipIN = str(data['precipi'])
            logger.debug("historicals_precipMM: %s ; historicals_precipIN: %s" %
                         (historicals_precipMM, historicals_precipIN))
            print(Fore.YELLOW + "Here's the summary for the day.")
            print(Fore.YELLOW + "Minimum Temperature: " + Fore.CYAN + historicals_minTempF
                  + "°F (" + historicals_minTempC + "°C)")
            print(Fore.YELLOW + "Average Temperature: " + Fore.CYAN + historicals_avgTempF
                  + "°F (" + historicals_avgTempC + "°C)")
            print(Fore.YELLOW + "Maxmimum Temperature: " + Fore.CYAN + historicals_maxTempF
                  + "°F (" + historicals_maxTempC + "°C)")
            print(Fore.YELLOW + "Minimum Dew Point: " + Fore.CYAN + historicals_minDewpointF
                  + "°F (" + historicals_minDewpointC + "°C)")
            print(Fore.YELLOW + "Average Dew Point: " + Fore.CYAN + historicals_avgDewpointF
                  + "°F (" + historicals_avgDewpointC + "°C)")
            print(Fore.YELLOW + "Maximum Dew Point: " + Fore.CYAN + historicals_maxDewpointF
                  + "°F (" + historicals_maxDewpointC + "°C)")
            print(Fore.YELLOW + "Minimum Humidity: " + Fore.CYAN + historicals_minHumidity
                  + "%")
            print(Fore.YELLOW + "Average Humidity: " + Fore.CYAN + historicals_avgHumidity
                  + "%")
            print(Fore.YELLOW + "Maximum Humidity: " + Fore.CYAN + historicals_maxHumidity
                  + "%")
            print(Fore.YELLOW + "Minimum Wind Speed: " + Fore.CYAN + historicals_minWindMPH
                  + " mph (" + historicals_minWindKPH + " kph)")
            print(Fore.YELLOW + "Average Wind Speed: " + Fore.CYAN + historicals_avgWindSpeedMPH
                  + " mph (" + historicals_avgWindSpeedKPH + " kph)")
            print(Fore.YELLOW + "Maximum Wind Speed: " + Fore.CYAN + historicals_maxWindMPH
                  + " mph (" + historicals_maxWindKPH + " kph)")
            print(Fore.YELLOW + "Minimum Visibility: " + Fore.CYAN + historicals_minVisibilityMI
                  + " mi (" + historicals_minVisibilityKM + " kph)")
            print(Fore.YELLOW + "Average Visibility: " + Fore.CYAN + historicals_avgVisibilityMI
                  + " mi (" + historicals_avgVisibilityKM + " kph)")
            print(Fore.YELLOW + "Maximum Visibility: " + Fore.CYAN + historicals_maxVisibilityMI
                  + " mi (" + historicals_maxVisibilityKM + " kph)")
            print(Fore.YELLOW + "Minimum Pressure: " + Fore.CYAN + historicals_minPressureInHg
                  + " inHg (" + historicals_minPressureMB + " mb)")
            print(Fore.YELLOW + "Average Pressure: " + Fore.CYAN + historicals_avgPressureInHg
                  + " inHg (" + historicals_avgPressureMB + " mb)")
            print(Fore.YELLOW + "Maximum Pressure: " + Fore.CYAN + historicals_maxPressureInHg
                  + " inHg (" + historicals_maxPressureMB + " mb)")
            print(Fore.YELLOW + "Total Precipitation: " + Fore.CYAN + historicals_precipIN
                  + " in (" + historicals_precipMM + "mb)")
            try:
                print(Fore.RED + "To view hourly historical data, please press enter.")
                print(Fore.RED + "If you want to return to the main menu, press Control + C.")
                input()
            except KeyboardInterrupt:
                continue
        # Start the pre-loop to see how many times we're looping.
        historicalhourlyLoops = 0
        for data in historical_json['history']['observations']:
            historical_tempF = str(data['tempi'])
            historicalhourlyLoops = historicalhourlyLoops + 1
            
        for data in historical_json['history']['observations']:
            logger.info("We're on iteration %s/%s. User iteration limit: %s."
                        % (historical_totalloops, historicalhourlyLoops, user_loopIterations))
            historical_time = data['date']['pretty']
            historical_tempF = str(data['tempi'])
            historical_tempC = str(data['tempm'])
            historical_dewpointF = str(data['dewpti'])
            logger.debug("historical_time: %s ; historical_tempF: %s"
                         % (historical_time, historical_tempF))
            logger.debug("historical_tempC: %s ; historical_dewpointF: %s"
                         % (historical_tempC, historical_dewpointF))
            historical_dewpointC = str(data['dewptm'])
            historical_windspeedKPH = str(data['wspdm'])
            historical_windspeedMPH = str(data['wspdi'])
            try:
                historical_gustcheck = float(data['wgustm'])
            except ValueError:
                printException_loggerwarn()
                historical_gustcheck = -9999
            logger.debug("historical_dewpointC: %s ; historical_windspeedKPH: %s"
                         % (historical_dewpointC, historical_windspeedKPH))
            logger.debug("historical_windspeedMPH: %s ; historical_gustcheck: %s"
                         % (historical_windspeedMPH, historical_gustcheck))
            if historical_gustcheck == -9999:
                historical_windgustdata = False
                logger.warn("Wind gust data is not present! historical_windgustdata: %s"
                            % historical_windgustdata)
            else:
                historical_windgustdata = True
                historical_windgustKPH = str(data['wgustm'])
                historical_windgustMPH = str(data['wgusti'])
                logger.info("Wind gust data is present.")
                logger.debug("historical_windgustKPH: %s ; historical_windgustMPH: %s"
                             % (historical_windgustKPH, historical_windgustMPH))
            historical_windDegrees = str(data['wdird'])
            historical_windDirection = data['wdire']
            historical_visibilityKM = str(data['vism'])
            historical_visibilityMI = str(data['visi'])
            logger.debug("historical_windDegrees: %s ; historical_windDirection: %s"
                         % (historical_windDegrees, historical_windDirection))
            logger.debug("historical_visibilityKM: %s ; historical_visibilityMI: %s"
                         % (historical_visibilityKM, historical_visibilityMI))
            historical_pressureMB = str(data['pressurem'])
            historical_pressureInHg = str(data['pressurei'])
            historical_windchillcheck = float(data['windchillm'])
            logger.debug("historical_pressureMB: %s ; historical_pressureInHg: %s"
                         % (historical_pressureMB, historical_pressureInHg))
            logger.debug("historical_windchillcheck: %s" % historical_windchillcheck)
            if historical_windchillcheck == -999:
                historical_windchilldata = False
                logger.warn("Wind chill data is not present! historical_windchilldata: %s"
                            % historical_windchilldata)
            else:
                historical_windchilldata = True
                historical_windchillC = str(data['windchillm'])
                historical_windchillF = str(data['windchilli'])
                logger.info("Wind chill data is present.")
                logger.debug("historical_windchillC: %s ; historical_windchillF: %s"
                             % (historical_windchillC, historical_windchillF))
            historical_heatindexcheck = float(data['heatindexm'])
            logger.debug("historical_heatindexcheck: %s" % historical_heatindexcheck)
            if historical_heatindexcheck == -9999:
                historical_heatindexdata = False
                logger.warn("Heat index data is not present! historical_heatindexdata: %s"
                            % historical_heatindexdata)
            else:
                historical_heatindexdata = True
                historical_heatindexC = str(data['heatindexm'])
                historical_heatindexF = str(data['heatindexi'])
                logger.info("Heat index data is present.")
                logger.debug("historical_heatindexC: %s ; historical_heatindexF: %s"
                             % (historical_heatindexC, historical_heatindexF))
            try:
                historical_precipMM = float(data['precipm'])
                historical_precipIN = float(data['precipi'])
            except ValueError:
                printException_loggerwarn()
                historical_precipMM = -9999
                historical_precipIN = -9999
            logger.debug("historical_precipMM: %s ; historical_precipIN: %s"
                         % (historical_precipMM, historical_precipIN))
            if historical_precipMM == -9999:
                historical_precipMM = "0.0"
                logger.warn("historical_precipMM was -9999. It's now: %s"
                            % historical_precipMM)
            else:
                historical_precipMM = str(historical_precipMM)
                logger.info("historical_precipMM converted to str. It's now: %s"
                            % historical_precipMM)
            
            if historical_precipIN == -9999:
                historical_precipIN = "0.0"
                logger.warn("historical_precipIN was -9999. It's now: %s"
                            % historical_precipIN)
            else:
                historical_precipIN = str(historical_precipIN)
                logger.info("historical_precipIN converted to str. It's now: %s"
                            % historical_precipIN)
            
            historical_condition = str(data['conds'])
            logger.debug("historical_condition: %s" % historical_condition)
            logger.info("Now printing weather data...")
            print("")
            print(Fore.YELLOW + historical_time + ":")
            print(Fore.YELLOW + "Conditions: " + Fore.CYAN + historical_condition)
            print(Fore.YELLOW + "Temperature: " + Fore.CYAN + historical_tempF
                  + " °F (" + historical_tempC + " °C)")
            print(Fore.YELLOW + "Dew point: " + Fore.CYAN + historical_dewpointF
                  + " °F (" + historical_dewpointC + " °C)")
            print(Fore.YELLOW + "Wind speed: " + Fore.CYAN + historical_windspeedMPH
                  + " mph (" + historical_windspeedKPH + " kph)") 
            if historical_windgustdata == True:
                print(Fore.YELLOW + "Wind gusts: " + Fore.CYAN + historical_windgustMPH
                      + " mph (" + historical_windgustKPH + " kph)")
            if historical_windchilldata == True:
                print(Fore.YELLOW + "Wind chill: " + Fore.CYAN + historical_windchillF
                      + " °F (" + historical_windchillC + " kph)")
            if historical_heatindexdata == True:
                print(Fore.YELLOW + "Heat index: " + Fore.CYAN + historical_heatindexF
                      + " °F (" + historical_heatindexC + " °C)")
            print(Fore.YELLOW + "Precipitation: " + Fore.CYAN + historical_precipIN
                  + " in (" + historical_precipMM + " mm)")
            historical_loops = historical_loops + 1
            historical_totalloops = historical_totalloops + 1
            logger.debug("historical_loops: %s ; historical_totalloops: %s"
                         % (historical_loops, historical_totalloops))
                         
            if historical_totalloops == historicalhourlyLoops:
                logger.debug("Iterations now %s. Total iterations %s. Breaking..."
                             % (historical_totalloops, historicalhourlyLoops))
                             
            if user_showCompletedIterations == True:
                print(Fore.YELLOW + "Completed iterations: " + Fore.CYAN + "%s/%s"
                      % (historical_totalloops, historicalhourlyLoops))
                print(Fore.RESET)
                
            if user_enterToContinue == True:
                if historical_loops == user_loopIterations:
                    logger.info("Asking user to continue.")
                    try:
                        print(Fore.RED + "Press enter to view the next", user_loopIterations
                              , "iterations of historical weather information.")
                        print("Otherwise, press Control + C to get back to the main menu.")
                        input()
                        historical_loops = 0
                        logger.info("Printing more weather data. historical_loops is now: %s"
                                    % historical_loops)
                    except KeyboardInterrupt:
                        logger.info("Breaking to main menu, user issued KeyboardInterrupt")
                        break         
    elif moreoptions == "11":
        print("", Fore.YELLOW + "-=-=- " + Fore.CYAN + "PyWeather" + Fore.YELLOW + " -=-=-",
              Fore.CYAN + "version " + about_version, "",
              Fore.YELLOW + "Build Number: " + Fore.CYAN + about_buildnumber,
              Fore.YELLOW + "Release Date: " + Fore.CYAN + about_releasedate,
              Fore.YELLOW + "Release Type: " + Fore.CYAN + about_releasetype,
              "",
              Fore.YELLOW + "Created, and mostly coded by: " + Fore.CYAN + about_maindevelopers,
              Fore.YELLOW + "Contributors: " + Fore.CYAN + about_contributors,
              Fore.YELLOW + "A special thanks to the developers of these libraries",
              "that are used in PyWeather: " + Fore.CYAN,
              about_librariesinuse + Fore.RESET, sep="\n")        
    elif moreoptions == "tell me a joke":
        logger.debug("moreoptions: %s" % moreoptions)
        # Jokes from searching "weather jokes" on DuckDuckGo (the first option)
        # They're jokes for kids.
        jokenum = randint(0,12)
        logger.debug("jokenum: %s" % jokenum)
        print("")
        if jokenum == 0:
            print("How do hurricanes see?",
                  "With one eye!", sep="\n")
        elif jokenum == 1:
            print("What does a cloud wear under his raincoat?",
                  "Thunderwear!", sep="\n")
        elif jokenum == 2:
            print("What type of lightning likes to play sports?",
                  "Ball lightning!", sep="\n")
        elif jokenum == 3:
            print("What type of cloud is so lazy, because it will never get up?",
                  "Fog!", sep="\n")
        elif jokenum == 4:
            print("What did the lightning bolt say to the other lightning bolt?",
                  "You're shocking!", sep="\n")
        elif jokenum == 5:
            print("Whatever happened to the cow that was lifted into the tornado?",
                  "Udder disaster!", sep="\n")
        elif jokenum == 6:
            print("What did the one tornado say to the other?",
                  "Let's twist again like we did last summer.", sep="\n")
        elif jokenum == 7:
            print("What did the thermometer say to the other thermometer?",
                  "You make my temperature rise.", sep="\n")
        elif jokenum == 8:
            print("What's the difference between a horse and the weather?",
                  "One is reined up and the other rains down.", sep="\n")
        elif jokenum == 9:
            print("What did the one raindrop say to the other raindrop?",
                  "My plop is bigger than your plop.", sep="\n")
        elif jokenum == 10:
            print("Why did the woman go outdoors with her purse open?",
                  "Because she expected some change in the weather.", sep="\n")
        elif jokenum == 11:
            print("What's the different between weather and climate?",
                  "You can't weather a tree, but you can climate.", sep="\n")
        elif jokenum == 12:
            print("What did the hurricane say to the other hurricane?",
                  "I have my eye on you.", sep="\n")
    elif moreoptions == "12":
        print(Fore.RESET + "Attempting to relaunch PyWeather...")
        try:
            os.system("python3 pyweather.py")
            print("")
            sys.exit()
        except:
            try:
                os.system("python pyweather.py")
                print("")
                sys.exit()
            except:
                try:
                    os.system("pyweather.py")
                    print("")
                    sys.exit()
                except:
                    print("Can't relaunch PyWeather!")
    elif moreoptions == "9":
        print(Fore.RESET + "Flagging all data types to be refreshed when they are next",
              "launched.", sep="\n")
        refresh_alertsflagged = True
        refresh_almanacflagged = True
        logger.debug("refresh_alertsflagged: %s ; refresh_almanacflagged: %s" %
                     (refresh_alertsflagged, refresh_almanacflagged))
        refresh_currentflagged = True
        refresh_forecastflagged = True
        logger.debug("refresh_currentflagged: %s ; refresh_forecastflagged: %s" %
                     (refresh_currentflagged, refresh_forecastflagged))
        refresh_hourly10flagged = True
        refresh_hourly36flagged = True
        logger.debug("refresh_hourly10flagged: %s ; refresh_hourly36flagged: %s" %
                     (refresh_hourly10flagged, refresh_hourly36flagged))
        refresh_sundataflagged = True
        logger.debug("refresh_sundataflagged: %s" % refresh_sundataflagged)
    else:
        logger.warn("Input could not be understood!")
        print(Fore.RED + "Not a valid option.")
        print("")