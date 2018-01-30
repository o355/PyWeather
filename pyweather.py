'''
_______
|      \  \           /         @@@;
|       \  \         /        `#....@
|        |  \       /       ,;@.....;,;
|        |   \     /       @..@........@`           PyWeather
|        |    \   /        .............@           version 0.6.3 beta
|        /     \ /         .............@           (c) 2017-2018 - o355
|_______/       |          @...........#`
|               |           .+@@++++@#;
|               |             @ ;  ,
|               |             : ' .
|               |            @ # .`
|               |           @ # .`
'''

# The second part of the ASCII art you see was converted to ASCII from Wunderground's J icon set - the sleet icon.
# Some minor tweaking was done to straighten up the rain.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This line of code was typed in during the solar eclipse, in Eclipse.
#
# ==============
# This is beta code. It's not pretty, and I'm not following PEP 8
# guidelines. There will be bugs in this code. I will be attempting to
# follow proper guidelines later down the road.

# <---- Preload starts here ---->

# See if we're running Python 2. If so, exit out of the script.

# Begin the import process. - Section 1
import configparser
import subprocess
import traceback
import sys
try:
    import requests
except ImportError:
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
    import colorama
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
    import geopy
    from geopy import GoogleV3
except:
    print("When attempting to import the library geopy, we ran into an import error.",
          "Please make sure that geopy is installed.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()

try:
    from halo import Halo
except ImportError:
    print("When attempting to import the library halo, we ran into an import error.",
          "Please make sure that halo is installed.",
          "Press enter to exit.", sep="\n")


# Try loading the versioninfo.txt file. If it isn't around, create the file with
# the present version info. - Section 2

try:
    versioninfo = open('updater//versioninfo.txt').close()
except:
    open('updater//versioninfo.txt', 'w').close()
    with open("updater//versioninfo.txt", 'a') as out:
        out.write("0.6.3 beta")
        out.close()


# Define configparser under config, and read the config. - Section 3
config = configparser.ConfigParser()
config.read('storage//config.ini')

# See if the config is "provisioned". If it isn't, a KeyError will occur,
# because it's not created. Creative. - Section 4

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
    
# Try to parse configuration options. - Section 5

# Set a variable counting the config issues we run into. Display a message at the bottom
# of this code if we encounter 1 or more config errors.
configerrorcount = 0

try:
    sundata_summary = config.getboolean('SUMMARY', 'sundata_summary')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. SUMMARY/sundata_summary failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    sundata_summary = False
try:
    almanac_summary = config.getboolean('SUMMARY', 'almanac_summary')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. SUMMARY/almanac_summary failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    almanac_summary = False

try:
    checkforUpdates = config.getboolean('UPDATER', 'autocheckforupdates')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. UPDATER/autocheckforupdates failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    checkforUpdates = False
try:
    verbosity = config.getboolean('VERBOSITY', 'verbosity')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. VERBOSITY/verbosity failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    verbosity = False
try:
    jsonVerbosity = config.getboolean('VERBOSITY', 'json_verbosity')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. VERBOSITY/json_verbosity failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    jsonVerbosity = False
try:
    tracebacksEnabled = config.getboolean('TRACEBACK', 'tracebacks')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. TRACEBACK/tracebacks failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    tracebacksEnabled = False
try:
    prefetch10Day_atStart = config.getboolean('PREFETCH', '10dayfetch_atboot')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. PREFETCH/10dayfetch_atboot failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    prefetch10Day_atStart = False
try:
    user_loopIterations = config.getint('UI', 'detailedInfoLoops')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. UI/detailedInfoLoops failed to load. Defaulting to 6.", sep="\n")
    configerrorcount += 1
    user_loopIterations = 6
try:
    user_enterToContinue = config.getboolean('UI', 'show_enterToContinue')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. UI/show_enterToContinue failed to load. Defaulting to True.", sep="\n")
    configerrorcount += 1
    user_enterToContinue = True
try:
    user_showCompletedIterations = config.getboolean('UI', 'show_completedIterations')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. UI/show_completedIterations failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    user_showCompletedIterations = False
try:
    user_forecastLoopIterations = config.getint('UI', 'forecast_detailedInfoLoops')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. UI/forecast_detailedInfoLoops failed to load. Defaulting to 5.", sep="\n")
    configerrorcount += 1
    user_forecastLoopIterations = 5
try:
    user_showUpdaterReleaseTag = config.getboolean('UPDATER', 'show_updaterReleaseTag')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. UPDATER/show_updaterReleaseTag failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    user_showUpdaterReleaseTag = False
try:
    user_backupKeyDirectory = config.get('KEYBACKUP', 'savedirectory')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. KEYBACKUP/savedirectory failed to load. Defaulting to 'backup//'.", sep="\n")
    configerrorcount += 1
    user_backupKeyDirectory = 'backup//'
try:
    validateAPIKey = config.getboolean('PYWEATHER BOOT', 'validateAPIKey')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. PYWEATHER BOOT/validateAPIKey failed to load. Defaulting to True.", sep="\n")
    configerrorcount += 1
    validateAPIKey = True

try:
    showAlertsOnSummary = config.getboolean('SUMMARY', 'showAlertsOnSummary')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. SUMMARY/showAlertsOnSummary failed to load. Defaulting to True.", sep="\n")
    configerrorcount += 1
    showAlertsOnSummary = True
try:
    showyesterdayonsummary = config.getboolean('SUMMARY', 'showyesterdayonsummary')
except:
    print("Whnn attempting to load your configuration file, an error",
            "occurred. SUMMARY/showyesterdayonsummary failed to load. Defaulting to False", sep="\n")
    showyesterdayonsummary = False
try:
    showUpdaterReleaseNotes = config.getboolean('UPDATER', 'showReleaseNotes')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. UPDATER/showReleaseNotes failed to load. Defaulting to True.", sep="\n")
    configerrorcount += 1
    showUpdaterReleaseNotes = True
try:
    showUpdaterReleaseNotes_uptodate = config.getboolean('UPDATER', 'showReleaseNotes_uptodate')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. UPDATER/showReleaseNotes_uptodate failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    showUpdaterReleaseNotes_uptodate = False
try:
    showNewVersionReleaseDate = config.getboolean('UPDATER', 'showNewVersionReleaseDate')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. UPDATER/showNewVersionReleaseDate failed to load. Defaulting to True.", sep="\n")
    configerrorcount += 1
    showNewVersionReleaseDate = True
try:
    cache_enabled = config.getboolean('CACHE', 'enabled')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. CACHE/enabled failed to load. Defaulting to True.", sep="\n")
    configerrorcount += 1
    cache_enabled = True
try:
    cache_alertstime = config.getfloat('CACHE', 'alerts_cachedtime')
    cache_alertstime = cache_alertstime * 60
except:
    print("When attempting to load your configuration file, an error",
          "occurred. CACHE/alerts_cachedtime failed to load. Defaulting to 300.", sep="\n")
    configerrorcount += 1
    cache_alertstime = 300
try:
    cache_currenttime = config.getfloat('CACHE', 'current_cachedtime')
    cache_currenttime = cache_currenttime * 60
except:
    print("When attempting to load your configuration file, an error",
          "occurred. CACHE/current_cachedtime failed to load. Defaulting to 600.", sep="\n")
    configerrorcount += 1
    cache_currenttime = 600
try:
    cache_forecasttime = config.getfloat('CACHE', 'forecast_cachedtime')
    cache_forecasttime = cache_forecasttime * 60
except:
    print("When attempting to load your configuration file, an error",
          "occurred. CACHE/forecast_cachedtime failed to load. Defaulting to 3600.", sep="\n")
    configerrorcount += 1
    cache_forecasttime = 3600
try:
    cache_almanactime = config.getfloat('CACHE', 'almanac_cachedtime')
    cache_almanactime = cache_almanactime * 60
except:
    print("When attempting to load your configuration file, an error",
          "occurred. CACHE/almanac_cachedtime failed to load. Defaulting to 14400.", sep="\n")
    configerrorcount += 1
    cache_almanactime = 1440
try:
    cache_threedayhourly = config.getfloat('CACHE', 'threedayhourly_cachedtime')
    cache_threedayhourly = cache_threedayhourly * 60
except:
    print("When attempting to load your configuration file, an error",
          "occurred. CACHE/threedayhourly_cachedtime failed to load. Defaulting to 3600.", sep="\n")
    configerrorcount += 1
    cache_threedayhourly = 3600
try:
    cache_tendayhourly = config.getfloat('CACHE', 'tendayhourly_cachedtime')
    cache_tendayhourly = cache_tendayhourly * 60
except:
    print("When attempting to load your configuration file, an error",
          "occurred. CACHE/tendayhourly_cachedtime failed to load. Defaulting to 3600.", sep="\n")
    configerrorcount += 1
    cache_tendayhourly = 3600
try:
    cache_sundatatime = config.getfloat('CACHE', 'sundata_cachedtime')
    cache_sundatatime = cache_sundatatime * 60
except:
    print("When attempting to load your configuration file, an error",
          "occurred. CACHE/sundata_cachedtime failed to load. Defaulting to 28800.", sep="\n")
    configerrorcount += 1
    cache_sundatatime = 28800
try:
    cache_tidetime = config.getfloat('CACHE', 'tide_cachedtime')
    cache_tidetime = cache_tidetime * 60
except:
    print("When attempting to load your configuration file, an error",
          "occurred. CACHE/tide_cachedtime failed to load. Defaulting to 28800.", sep="\n")
    configerrorcount += 1
    cache_tidetime = 28800
try:
    cache_hurricanetime = config.getfloat('CACHE', 'hurricane_cachedtime')
    cache_hurricanetime = cache_hurricanetime * 60


except:
    print("When attempting to load your configuration file, an error",
          "occurred. CACHE/hurricane_cachedtime failed to load. Defaulting to 10800.", sep="\n")
    configerrorcount += 1
    cache_hurricanetime = 10800

try:
    cache_yesterdaytime = config.getfloat('CACHE', 'yesterday_cachedtime')
    cache_yesterdaytime = cache_yesterdaytime * 60
except:
    print("When attempting to load your configuration file, an error",
          "occurred. CACHE/yesterday_cachedtime failed to load. Defaulting to 10800.", sep="\n")
    configerrorcount += 1
    cache_yesterdaytime = 10800

try:
    user_alertsUSiterations = config.getint('UI', 'alerts_usiterations')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. UI/alerts_usiterations failed to load. Defaulting to 2.", sep="\n")
    configerrorcount += 1
    user_alertsEUiterations = 2
try:
    user_alertsEUiterations = config.getint('UI', 'alerts_euiterations')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. UI/alerts_euiterations failed to load. Defaulting to 1.", sep="\n")
    configerrorcount += 1
    user_alertsUSiterations = 1
try:
    user_radarImageSize = config.get('RADAR GUI', 'radar_imagesize')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. RADAR GUI/radar_imagesize failed to load. Defaulting to 'normal'.", sep="\n")
    configerrorcount += 1
    user_radarImageSize = "normal"
try:
    radar_bypassconfirmation = config.getboolean('RADAR GUI', 'bypassconfirmation')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. RADAR GUI/bypassconfirmation failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    radar_bypassconfirmation = False
try:
    showTideOnSummary = config.getboolean('SUMMARY', 'showtideonsummary')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. SUMMARY/showtideonsummary failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    showTideOnSummary = False
try:
    geopyScheme = config.get('GEOCODER', 'scheme')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. GEOCODER/scheme failed to load. Defaulting to 'https'.", sep="\n")
    configerrorcount += 1
    geopyScheme = 'https'
try:
    prefetchHurricane_atboot = config.getboolean('PREFETCH', 'hurricanedata_atboot')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. PREFETCH/hurricanedata_atboot failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    prefetchHurricane_atboot = False
try:
    geoip_enabled = config.getboolean('FIRSTINPUT', 'geoipservice_enabled')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FIRSTINPUT/geoipservice_enabled failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    geoip_enabled = False

try:
    pws_enabled = config.getboolean('FIRSTINPUT', 'allow_pwsqueries')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FIRSTINPUT/allow_pwsqueries failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    pws_enabled = False

try:
    hurricanenearestcity_enabled = config.getboolean('HURRICANE', 'enablenearestcity')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. HURRICANE/enablenearestcity failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    hurricanenearestcity_enabled = False

try:
    hurricanenearestcity_fenabled = config.getboolean('HURRICANE', 'enablenearestcity_forecast')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. HURRICANE/enablenearestcity_forecast failed to load. Defaulting to False", sep="\n")
    configerrorcount += 1
    hurricanenearestcity_fenabled = False
try:
    geonames_apiusername = config.get('HURRICANE', 'api_username')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. HURRICANE/api_username failed to load. Defaulting to 'pyweather_proj'", sep="\n")
    configerrorcount += 1
    geonames_apiusername = "pyweather_proj"
try:
    hurricane_nearestsize = config.get('HURRICANE', 'nearestcitysize')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. HURRICANE/nearestcitysize failed to load. Defaulting to 'medium'.", sep="\n")
    configerrorcount += 1
    hurricane_nearestsize = 'medium'
try:
    favoritelocation_enabled = config.getboolean('FAVORITE LOCATIONS', 'enabled')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FAVORITE LOCATIONS/enabled failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    favoritelocation_enabled = False
try:
    favoritelocation_1 = config.get('FAVORITE LOCATIONS', 'favloc1')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FAVORITE LOCATIONS/favloc1 failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    favoritelocation_1 = "None"

try:
    favoritelocation_2 = config.get('FAVORITE LOCATIONS', 'favloc2')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FAVORITE LOCATIONS/favloc2 failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    favoritelocation_2 = "None"

try:
    favoritelocation_3 = config.get('FAVORITE LOCATIONS', 'favloc3')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FAVORITE LOCATIONS/favloc3 failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    favoritelocation_3 = "None"

try:
    favoritelocation_4 = config.get('FAVORITE LOCATIONS', 'favloc4')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FAVORITE LOCATIONS/favloc4 failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    favoritelocation_4 = "None"

try:
    favoritelocation_5 = config.get('FAVORITE LOCATIONS', 'favloc5')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FAVORITE LOCATIONS/favloc5 failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    favoritelocation_5 = "None"

try:
    favoritelocation_1data = config.get('FAVORITE LOCATIONS', 'favloc1_data')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FAVORITE LOCATIONS/favloc1_data failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    favoritelocation_1data = "None"

try:
    favoritelocation_2data = config.get('FAVORITE LOCATIONS', 'favloc2_data')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FAVORITE LOCATIONS/favloc2_data failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    favoritelocation_2data = "None"

try:
    favoritelocation_3data = config.get('FAVORITE LOCATIONS', 'favloc3_data')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FAVORITE LOCATIONS/favloc3_data failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    favoritelocation_3data = "None"

try:
    favoritelocation_4data = config.get('FAVORITE LOCATIONS', 'favloc4_data')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FAVORITE LOCATIONS/favloc4_data failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    favoritelocation_4data = "None"

try:
    favoritelocation_5data = config.get('FAVORITE LOCATIONS', 'favloc5_data')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FAVORITE LOCATIONS/favloc5_data failed to load. Defaulting to 'None'.", sep="\n")
    favoritelocation_5data = "None"

try:
    previouslocation_enabled = config.get('PREVIOUS LOCATIONS', 'enabled')
except:
    print("When attempting to load your configuration file, an error",
          "occured. PREVIOUS LOCATIONS/enabled failed to load. Defaulting to True.", sep="\n")
    configerrorcount += 1
    previouslocation_enabled = True

try:
    previouslocation_1 = config.get('PREVIOUS LOCATIONS', 'prevloc1')
except:
    print("When attempting to load your configuration file, an error",
          "occured. PREVIOUS LOCATIONS/prevloc1 failed to load. Defaulting to None.", sep="\n")
    configerrorcount += 1
    previouslocation_1 = "None"

try:
    previouslocation_2 = config.get('PREVIOUS LOCATIONS', 'prevloc2')
except:
    print("When attempting to load your configuration file, an error",
          "occured. PREVIOUS LOCATIONS/prevloc2 failed to load. Defaulting to None.", sep="\n")
    configerrorcount += 1
    previouslocation_2 = "None"

try:
    previouslocation_3 = config.get('PREVIOUS LOCATIONS', 'prevloc3')
except:
    print("When attempting to load your configuration file, an error",
          "occured. PREVIOUS LOCATIONS/prevloc3 failed to load. Defaulting to None.", sep="\n")
    configerrorcount += 1
    previouslocation_3 = "None"

try:
    previouslocation_4 = config.get('PREVIOUS LOCATIONS', 'prevloc4')
except:
    print("When attempting to load your configuration file, an error",
          "occured. PREVIOUS LOCATIONS/prevloc4 failed to load. Defaulting to None.", sep="\n")
    configerrorcount += 1
    previouslocation_4 = "None"

try:
    previouslocation_5 = config.get('PREVIOUS LOCATIONS', 'prevloc5')
except:
    print("When attempting to load your configuration file, an error",
          "occured. PREVIOUS LOCATIONS/prevloc5 failed to load. Defaulting to None.", sep="\n")
    configerrorcount += 1
    previouslocation_5 = "None"

try:
    previouslocation_1data = config.get('PREVIOUS LOCATIONS', 'prevloc1_data')
except:
    print("When attempting to load your configuration file, an error",
          "occured. PREVIOUS LOCATIONS/prevloc1_data failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    previouslocation_1data = "None"

try:
    previouslocation_2data = config.get('PREVIOUS LOCATIONS', 'prevloc2_data')
except:
    print("When attempting to load your configuration file, an error",
          "occured. PREVIOUS LOCATIONS/prevloc2_data failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    previouslocation_2data = "None"

try:
    previouslocation_3data = config.get('PREVIOUS LOCATIONS', 'prevloc3_data')
except:
    print("When attempting to load your configuration file, an error",
          "occured. PREVIOUS LOCATIONS/prevloc3_data failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    previouslocation_3data = "None"

try:
    previouslocation_4data = config.get('PREVIOUS LOCATIONS', 'prevloc4_data')
except:
    print("When attempting to load your configuration file, an error",
          "occured. PREVIOUS LOCATIONS/prevloc4_data failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    previouslocation_4data = "None"

try:
    previouslocation_5data = config.get('PREVIOUS LOCATIONS', 'prevloc5_data')
except:
    print("When attempting to load your configuration file, an error",
          "occured. PREVIOUS LOCATIONS/prevloc5_data failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    previouslocation_5data = "None"

try:
    geocoder_customkeyEnabled = config.getboolean('GEOCODER API', 'customkey_enabled')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. GEOCODER API/customkey_enabled failed to load. Defaulting to False.", sep="\n")
    configerrorcount += 1
    geocoder_customkeyEnabled = False

try:
    geocoder_customkey = config.get('GEOCODER API', 'customkey')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. GEOCODER API/customkey failed to load. Defaulting to 'None'.", sep="\n")
    configerrorcount += 1
    geocoder_customkey = "None"

try:
    extratools_enabled = config.getboolean('UI', 'extratools_enabled')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. UI/extratools_enabled failed to load. Defaulting to 'False'.", sep="\n")
    configerrorcount += 1
    extratools_enabled = False

try:
    prefetch_yesterdaydata = config.getboolean('PREFETCH', 'yesterdaydata_atboot')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. PREFETCH/yesterdaydata_atboot failed to load. Defaulting to 'False'.", sep="\n")
    configerrorcount += 1
    prefetch_yesterdaydata = False

try:
    yesterdaydata_onsummary = config.getboolean('SUMMARY', 'showyesterdayonsummary')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. SUMMARY/showyesterdayonsummary failed to load. Defaulting to 'False'.", sep="\n")
    configerrorcount += 1
    yesterdaydata_onsummary = False

try:
    airports_enabled = config.getboolean('FIRSTINPUT', 'allow_airportqueries')
except:
    print("When attempting to load your configuration file, an error",
          "occurred. FIRSTINPUT/allow_airportqueries failed to load. Defaulting to 'True'.", sep="\n")
    configerrorcount += 1
    airports_enabled = True

if configerrorcount >= 1:
    print("", "When trying to load your configuration file, error(s) occurred.",
          "Try making sure that there are no typos in your config file, and try setting values",
          "in your config file to the default values as listed above. If all else fails, try using",
          "configsetup.py to set all config options to their defaults. If issues still occur,",
          "report the bug on GitHub.", sep="\n")

# Import logging, and set up the logger. - Section 6
import logging
logger = logging.getLogger(name='pyweather_0.6.3beta')
logformat = '%(asctime)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logformat)

# Set the logger levels by design. Critical works as a non-verbosity
# option, as I made sure not to have any critical messages. - Section 7
if verbosity:
    logger.setLevel(logging.DEBUG)
elif tracebacksEnabled:
    logger.setLevel(logging.ERROR)
else:
    logger.setLevel(logging.CRITICAL)

# Initialize the halo spinner - Section 8
spinner = Halo(text='Loading PyWeather...', spinner='line')
spinner.start()


from platform import python_version

headers = {'User-Agent': 'PyWeather 0.6.4 beta (Python %s)' % python_version()}

# List config options for those who have verbosity enabled. - Section 9
logger.info("PyWeather 0.6.3 beta now starting.")
logger.info("Configuration options are as follows: ")
logger.debug("sundata_summary: %s ; almanac_summary: %s" %
             (sundata_summary, almanac_summary))
logger.debug("showyesterdayonsummary: %s" % showyesterdayonsummary)
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
logger.debug("showAlertsOnSummary: %s" % showAlertsOnSummary)
logger.debug("showUpdaterReleaseNotes_uptodate: %s ; showNewVersionReleaseDate: %s"
             % (showUpdaterReleaseNotes_uptodate, showNewVersionReleaseDate))
logger.debug("showUpdaterReleaseNotes: %s ; cache_enabled: %s" %
             (showUpdaterReleaseNotes, cache_enabled))
logger.debug("cache_alertstime: %s ; cache_currenttime: %s" %
             (cache_alertstime, cache_currenttime))
logger.debug("cache_forecasttime: %s" %
             (cache_forecasttime))
logger.debug("cache_almanactime: %s ; cache_threedayhourly: %s" %
             (cache_almanactime, cache_threedayhourly))
logger.debug("cache_tendayhourly: %s ; cache_sundatatime: %s" %
             (cache_tendayhourly, cache_sundatatime))
# Coded during 70% totality of the 2017 eclipse, max for my location then
logger.debug("cache_tidetime: %s" % cache_tidetime)
# Please don't touch this line kthxbye
logger.debug("user_alertsUSiterations: %s ; user_alertsEUiterations: %s" %
             (user_alertsUSiterations, user_alertsEUiterations))
logger.debug("user_radarImagesize: %s ; radar_bypassconfirmation: %s" %
             (user_radarImageSize, radar_bypassconfirmation))
logger.debug("showTideOnSummary: %s ; geopyScheme: %s" %
             (showTideOnSummary, geopyScheme))
logger.debug("prefetchHurricane_atboot: %s ; cache_hurricanetime: %s" %
             (prefetchHurricane_atboot, cache_hurricanetime))
logger.debug("cache_yesterdaytime: %s" % (cache_yesterdaytime))

logger.debug("favoritelocation_enabled: %s ; favoritelocation_1: %s" %
             (favoritelocation_enabled, favoritelocation_1))
logger.debug("favoritelocation_2: %s ; favoritelocation_3: %s" %
             (favoritelocation_2, favoritelocation_3))
logger.debug("favoritelocation_4: %s ; favoritelocation_5: %s" %
             (favoritelocation_4, favoritelocation_5))

logger.debug("previouslocation_enabled: %s ; previouslocation_1 %s" %
             (previouslocation_enabled, previouslocation_1))

logger.debug("previouslocation_2: %s ; previouslocation_3 %s" %
             (previouslocation_2, previouslocation_3))

logger.debug("previouslocation_4: %s ; previouslocation_5 %s" %
             (previouslocation_4, previouslocation_5))

logger.debug("geocoder_customkeyEnabled: %s ; geocoder_customkey: %s" %
             (geocoder_customkeyEnabled, geocoder_customkey))
logger.debug("extratools_enabled: %s ; airports_enabled: %s" %
             (extratools_enabled, airports_enabled))
logger.debug("favoritelocation_1data: %s ; favoritelocation_2data: %s" %
             (favoritelocation_1data, favoritelocation_2data))
logger.debug("favoritelocation_3data: %s ; favoritelocation_4data: %s" %
             (favoritelocation_3data, favoritelocation_4data))
logger.debug("favoritelocation_5data: %s" % favoritelocation_5data)


logger.info("Setting gif x and y resolution for radar...")
# Set the size of the radar window. - Section 10
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

# Define custom functions - Section 11
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



logger.info("Declaring geocoder type...")
# Declare geocoder type - Section 12
if geopyScheme == "https" and geocoder_customkeyEnabled is False:
    geolocator = GoogleV3(scheme='https')
    logger.debug("geocoder scheme is now https, no custom key")
# If the user has a custom key enabled, do a geocode to validate the custom API key.
# The option to turn this off will be added in 0.6.4 beta.
elif geopyScheme == "https" and geocoder_customkeyEnabled is True:
    geolocator = GoogleV3(api_key=geocoder_customkey, scheme='https')
    spinner.stop()
    spinner.start(text="Validating geocoder API key...")
    logger.debug("geocoder scheme is now https, custom key. Validating...")
    # Do a warm-up geocode
    try:
        location = geolocator.geocode("123 5th Avenue, New York, NY")
    except:
        logger.debug("warmup geocode failed.")
    # Do the actual geocode
    try:
        location = geolocator.geocode("123 5th Avenue, New York, NY")
    except geopy.exc.GeocoderQueryError:
        spinner.fail(text="Geocoder API key is invalid!")
        print("")
        logger.debug("API key is invalid, falling back to no API key...")
        print("Your geocoder API key failed to validate, since it is wrong.",
              "Falling back to no API key...", sep="\n")
        printException()
        geolocator = GoogleV3(scheme='https')
        # Sleep the loading process for 100ms, this should give enough time to let the traceback get
        # printed, and let the loader continue
        time.sleep(0.1)
        spinner.start(text="Loading PyWeather...")
    except:
        spinner.fail(text="Failed to validate geocoder API key!")
        print("")
        print("When trying to validate your geocoder API key, something went wrong.",
              "Falling back to no API key...", sep="\n")
        printException()
        logger.debug("Failed to validate API key.")
        geolocator = GoogleV3(scheme='https')
        time.sleep(0.1)
        spinner.start(text="Loading PyWeather...")
elif geopyScheme == "http" and geocoder_customkeyEnabled is False:
    geolocator = GoogleV3(scheme='http')
    logger.debug("geocoder scheme is now http.")
elif geopyScheme == "http" and geocoder_customkeyEnabled is True:
    spinner.fail(text="A custom geocoder key on a HTTP scheme isn't allowed!")
    print("Sorry! Having a custom geocoder key on a HTTP scheme is not supported by",
          "Google. If you want to get rid of these error messages, please set GEOCODER API/",
          "customkeyenabled to False.", sep="\n")
    print("")
    geolocator = GoogleV3(scheme='http')
else:
    print("Geocoder scheme variable couldn't be understood.",
          "Defaulting to the https scheme.", sep="\n")
    geolocator = GoogleV3(scheme='https')
    logger.debug("geocoder scheme is now https.")

logger.info("Declaring hurricane nearest city population minimum...")
# Set hurricane nearest city size depending on the config option - Section 13
if hurricane_nearestsize == "small":
    hurricane_citiesamp = "&cities=cities1000"
elif hurricane_nearestsize == "medium":
    hurricane_citiesamp = "&cities=cities5000"
elif hurricane_nearestsize == "large":
    hurricane_citiesamp = "&cities=cities10000"

# Declare historical cache dictionary - Section 14
historical_cache = {}
logger.debug("historical_cache: %s" % historical_cache)

logger.debug("Begin API keyload...")
# Load the API key - Section 15
try:
    # Initially load the key - Section 15a
    apikey_load = open('storage//apikey.txt')
    logger.debug("apikey_load = %s" % apikey_load)
    apikey = apikey_load.read()
except FileNotFoundError:
    spinner.fail(text="Failed to access your primary API key!")
    print("")
    print("Your primary API key couldn't be loaded, as PyWeather ran into",
          "an error when attempting to access it. Make sure that your primary key",
          "file can be accessed (usually found at storage/apikey.txt. Make sure it has",
          "proper permissions, and that it exists). In the mean time, we're attempting",
          "to load your backup API key.", sep="\n")
    # If the key isn't found, try to find the second key. - Section 15b
    spinner.start(text="Loading PyWeather...")
    try:
        apikey2_load = open(user_backupKeyDirectory + "backkey.txt")
        logger.debug("apikey2_load: %s" % apikey2_load)
        apikey = apikey2_load.read()
        logger.debug("apikey: %s" % apikey)
        spinner.succeed(text="Successfully loaded your backup key!")
        spinner.start(text="Loading PyWeather...")
    except FileNotFoundError:
        spinner.fail(text="Failed to access a primary & backup key!")
        print("")
        print("When attempting to access your backup API key, PyWeather ran into",
              "an error. Make sure that your backup key file is accessible (wrong",
              "permissions and the file not existing are common issues).", sep="\n")
        logger.warning("Couldn't load the primary or backup key text file!" +
                    " Does it exist?")
        print("Press enter to continue.")
        input()
        sys.exit()

# Validate the user's API key for the full API key validation - Section 16
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

buildnumber = 63
buildversion = '0.6.3 beta'

# Refresh flag variables go here.
refresh_currentflagged = False
refresh_alertsflagged = False
refresh_hourly36flagged = False
refresh_hourly10flagged = False
refresh_forecastflagged = False
refresh_almanacflagged = False
refresh_sundataflagged = False
refresh_tidedataflagged = False
refresh_hurricanedataflagged = False
refresh_yesterdaydataflagged = False

logger.debug("refresh_currentflagged: %s ; refresh_alertsflagged: %s" %
             (refresh_currentflagged, refresh_alertsflagged))
logger.debug("refresh_hourly36flagged: %s ; refresh_hourly10flagged: %s" %
             (refresh_hourly36flagged, refresh_hourly10flagged))
logger.debug("refresh_forecastflagged: %s ; refresh_almanacflagged: %s" %
             (refresh_forecastflagged, refresh_almanacflagged))
logger.debug("refresh_sundataflagged: %s ; refresh_tidedataflagged: %s" %
             (refresh_sundataflagged, refresh_tidedataflagged))
logger.debug("refresh_hurricanedataflagged: %s ; refresh_yesterdaydataflagged: %s" %
             (refresh_hurricanedataflagged, refresh_yesterdaydataflagged))
 
if checkforUpdates == True:
    spinner.stop()
    spinner.start(text='Checking for updates...')
    reader2 = codecs.getreader("utf-8")
    try:
        versioncheck = requests.get("https://raw.githubusercontent.com/o355/"
                                + "pyweather/master/updater/versioncheck.json")
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
    except:
        spinner.fail(text="Couldn't check for PyWeather updates!")
        print("")
        spinner.start(text="Loading PyWeather...")
        print("Couldn't check for updates. Make sure raw.githubusercontent.com is unblocked on your network,",
              "and that you have a working internet connection.", sep="\n")


# Define about variables here.
logger.info("Defining about variables...")
about_buildnumber = "63"
about_version = "0.6.3 beta"
about_releasedate = "December 3, 2017"
about_maindevelopers = "o355" # Oh look, I'm also on TV, HI MOM!!!!!!!!!!!!
logger.debug("about_buildnumber: %s ; about_version: %s" %
             (about_buildnumber, about_version))
logger.debug("about_releasedate: %s ; about_maindevelopers: %s" %
             (about_releasedate, about_maindevelopers))
about_awesomecontributors = "ModoUnreal, TheLetterAndrew" # Oh look I'm on TV, HI MOM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# The winner of the explaination point contest for 0.6.3 beta:
# Oh boy guess I won!
#
#           ModoUnreal
#          ___________
#          |   1st    |   o355
#  Reddit  |          |___________
# ---------               2nd     |
# |  3rd                          |
# |_______________________________|
about_contributors = "gsilvapt, creepersbane"
about_releasetype = "beta"
about_librariesinuse = "Colorama, Geopy, appJar, Requests, Halo"
about_apisinuse = "freegeoip.net, GeoNames"
logger.debug("about_contributors: %s ; about_releasetype: %s" %
             (about_contributors, about_releasetype))
logger.debug("about_librariesinuse: %s ; about_awesomecontributors: %s" % 
            (about_librariesinuse, about_awesomecontributors))
logger.debug("about_apisinuse: %s" % about_apisinuse)
geoip_url = "https://freegeoip.net/json/"
logger.debug("geoip_url: %s" % geoip_url)

# Set up the initial variables that dictate availability, using PWS URLs,
# or using the geocoder.
geoip_available = False
pws_available = False
pws_urls = False
airport_available = False
airport_urls = False
useGeocoder = True
logger.debug("geoip_available: %s ; pws_available: %s" %
             (geoip_available, pws_available))
logger.debug("pws_urls: %s ; airport_available: %s" %
             (pws_urls, airport_available))
logger.debug("airport_urls: %s ; useGeocoder: %s" %
             (airport_urls, useGeocoder))

# Validate the API key before boot. It's now up here due to the new features at boot.
if validateAPIKey == True and backupKeyLoaded == True:
    spinner.stop()
    spinner.start(text="Validating API key...")
    logger.info("Beginning API key validation.")
    testurl = 'http://api.wunderground.com/api/' + apikey + '/conditions/q/NY/New_York.json'
    logger.debug("testurl: %s" % testurl)
    try:
        testJSON = requests.get(testurl)
        logger.debug("Acquired test JSON, end result: %s" % testJSON)
    except:
        spinner.fail(text="Failed to validate API key!")
        print("")
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
    test_json = json.loads(testJSON.text)
    if jsonVerbosity == True:
        logger.debug("test_json: %s" % test_json)
    try:
        test_conditions = str(test_json['current_observation']['temp_f'])
        logger.debug("test_conditions: %s" % test_conditions)
        logger.info("API key is valid!")
    except:
        spinner.fail(text="Primary API key is not valid!")
        logger.warn("API key is NOT valid. Attempting to revalidate API key...")
        if backupKeyLoaded == True:
            spinner.start(text="Validating backup API key...")
            logger.info("Beginning backup API key validation.")
            testurl = 'http://api.wunderground.com/api/' + apikey2 + '/conditions/q/NY/New_York.json'
            logger.debug("testurl: %s" % testurl)
            # What if the user's internet connection was alive during the 1st
            # validation, but not the 2nd? That's why this is here.
            try:
                testJSON = requests.get(testurl)
                logger.debug("Acquired test JSON, end result: %s" % testJSON)
            except:
                spinner.fail(text="Failed to validate backup API key!")
                print("")
                print("When attempting to validate your backup API key, PyWeather ran",
                      "into an error. If you're on a network with a filter, make sure",
                      "that 'api.wunderground.com' is unblocked. Otherwise, make sure you",
                      "have an internet conection, that that your internet connection's latency",
                      "isn't 1.59 days.", sep="\n")
                printException()
                print("Press enter to exit.")
                input()
                sys.exit()
            test_json = json.loads(testJSON.text)
            if jsonVerbosity == True:
                logger.debug("test_json: %s" % test_json)
            try:
                test_conditions = str(test_json['current_observation']['temp_f'])
                logger.debug("test_conditions: %s" % test_conditions)
                logger.info("Backup API key is valid!")
                apikey = apikey2
                logger.debug("apikey = apikey2. apikey: %s" % apikey)
                spinner.succeed(text="Backup API key is valid!")
                # We don't need to define new URLs here. The apikey variable is set before URL declaration.
            except:
                spinner.fail(text="Failed to valaidate backup API key!")
                print("")
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
            spinner.fail(text="Failed to validate API key!")
            print("")
            print("When attempting to validate your API key, your primary key",
                  "couldn't be validated, and your backup key wasn't able to",
                  "load at boot. Make sure that your primary API key is valid,",
                  "and that your backup API key can be accessed by PyWeather."
                  "Press enter to exit.", sep="\n")
            input()
            sys.exit()
        else:
            spinner.fail(text="Failed to validate API key!")
            print("")
            logger.warn("Backup key couldn't get loaded!")
            print("Your primary API key couldn't be validated, and your",
                  "backup key could not be loaded at startup.",
                  "Please make sure your primary API key is valid, and that",
                  "your backup API key can be accessed (common mistakes include",
                  "wrong permissions, and the file not existing).",
                  "Press enter to exit.", sep="\n")
            input()
            sys.exit()

spinner.stop()
spinner.start(text="Loading PyWeather...")
if geoip_enabled == True:
    spinner.stop()
    spinner.start(text="Fetching current location...")
    logger.info("geoip is enabled, attempting to fetch current location...")
    try:
        geoipJSON = requests.get(geoip_url)
        logger.debug("GeoIP JSON requsted with: %s" % geoipJSON)
        geoip_json = json.loads(geoipJSON.text)
        if jsonVerbosity is True:
            logger.debug("geoip_json: %s" % geoip_json)
        else:
            logger.debug("geoip_json is loaded.")
        geoip_city = geoip_json['city']
        geoip_state = geoip_json['region_code']
        logger.debug("geoip_city: %s ; geoip_state: %s" %
                     (geoip_city, geoip_state))
        currentlocation = geoip_city + ", " + geoip_state
        geoip_available = True
        logger.debug("currentlocation: %s ; geoip_available: %s" %
                     (currentlocation, geoip_available))
        latstr = str(geoip_json['latitude'])
        lonstr = str(geoip_json['longitude'])
        logger.debug("latstr: %s ; lonstr: %s" % (latstr, lonstr))
        logger.debug("useGeocoder: %s" % useGeocoder)
    except:
        spinner.fail(text="Failed to get current location! Current location is disabled.")
        print("")
        geoip_available = False
        logger.debug("geoip_available: %s" % geoip_available)
        spinner.start(text="Loading PyWeather...")

    # If geoip is available (the except block wasn't run), check for a bad geolocation (a straight up comma)
    if geoip_available == True:
        if geoip_city == "" or geoip_state == "":
            logger.warning("Bad geolocator data, geoip data is now not available.")
            geoip_available = False
            logger.debug("geoip_available: %s" % geoip_available)


# Check if we need to fully disable favorite location from having 5 "None" entries, if enabled
if favoritelocation_enabled is True:
    logger.debug("Checking favorite locations for invalid locations.")
    invalidlocations = 0
    for (key, val) in config.items("FAVORITE LOCATIONS"):
        logger.debug("key: %s ; val: %s" % (key, val))
        if val == "None":
            invalidlocations += 1
            logger.debug("invalidlocations: %s" % invalidlocations)

    if invalidlocations >= 10:
        logger.debug("invalidlocations is greater than or above 10. Favorite locations is disabled.")
        favoritelocation_available = False
    else:
        favoritelocation_available = True
else:
    favoritelocation_available = False

    logger.debug("favoritelocation_available: %s" % favoritelocation_available)

# Define favorite location display variables.
favoritelocation_1d = favoritelocation_1
favoritelocation_2d = favoritelocation_2
favoritelocation_3d = favoritelocation_3
favoritelocation_4d = favoritelocation_4
favoritelocation_5d = favoritelocation_5

logger.debug("favoritelocation_1d: %s ; favoritelocation_2d: %s" %
             (favoritelocation_1d, favoritelocation_2d))
logger.debug("favoritelocation_3d: %s ; favoritelocation_4d: %s" %
             (favoritelocation_3d, favoritelocation_4d))
logger.debug("favoritelocation_5d: %s" % favoritelocation_5d)

# Parse any favorite locations that contain PWS in their name. Set display variables.
# This is the same code for viewing favorite locations in the dedicated menu.

if favoritelocation_1d.find("pws:") == 0:
    # Delete pws: from the display string
    favoritelocation_1d = favoritelocation_1d[4:]
    favoritelocation_1d = "PWS " + favoritelocation_1d.upper()
    logger.debug("favoritelocation_1d: %s" % favoritelocation_1d)

if favoritelocation_2d.find("pws:") == 0:
    # Delete pws: from the display string
    favoritelocation_2d = favoritelocation_2d[4:]
    favoritelocation_2d = "PWS " + favoritelocation_2d.upper()
    logger.debug("favoritelocation_2d: %s" % favoritelocation_2d)

if favoritelocation_3d.find("pws:") == 0:
    # Delete pws: from the display string
    favoritelocation_3d = favoritelocation_3d[4:]
    favoritelocation_3d = "PWS " + favoritelocation_3d.upper()
    logger.debug("favoritelocation_3d: %s" % favoritelocation_3d)

if favoritelocation_4d.find("pws:") == 0:
    # Delete pws: from the display string
    favoritelocation_4d = favoritelocation_4d[4:]
    favoritelocation_4d = "PWS " + favoritelocation_4d.upper()
    logger.debug("favoritelocation_4d: %s" % favoritelocation_4d)

if favoritelocation_5d.find("pws:") == 0:
    # Delete pws: from the display string
    favoritelocation_5d = favoritelocation_5d[4:]
    favoritelocation_5d = "PWS " + favoritelocation_5d.upper()
    logger.debug("favoritelocation_5d: %s" % favoritelocation_5d)

# If we find arpt: or airport: in a favorite location, set the display variable to the extra data.
# The extra data variable contains the airport name to show to the user.

if favoritelocation_1d.find("arpt:") == 0 or favoritelocation_1d.find("airport:") == 0:
    # Set the display variable to extra data, only if the extra data isn't None.
    # If the extra data variable is None, show the airport code & "Airport"
    if favoritelocation_1data != "None":
        favoritelocation_1d = favoritelocation_1data
    else:
        favoritelocation_1d = favoritelocation_1.strip("airport:") + " Airport"

    logger.debug("favoritelocation_1d: %s" % favoritelocation_1d)

if favoritelocation_2d.find("arpt:") == 0 or favoritelocation_2d.find("airport:") == 0:
    # Set the display variable to extra data, only if the extra data isn't None.
    # If the extra data variable is None, show the airport code & "Airport"
    if favoritelocation_2data != "None":
        favoritelocation_2d = favoritelocation_2data
    else:
        favoritelocation_2d = favoritelocation_2.strip("airport:") + " Airport"

if favoritelocation_3d.find("arpt:") == 0 or favoritelocation_3d.find("airport:") == 0:
    # Set the display variable to extra data, only if the extra data isn't None.
    # If the extra data variable is None, show the airport code & "Airport"
    if favoritelocation_3data != "None":
        favoritelocation_3d = favoritelocation_3data
    else:
        favoritelocation_3d = favoritelocation_3.strip("airport:") + " Airport"

    logger.debug("favoritelocation_3d: %s" % favoritelocation_3d)

if favoritelocation_4d.find("arpt:") == 0 or favoritelocation_4d.find("airport:") == 0:
    # Set the display variable to extra data, only if the extra data isn't None.
    # If the extra data variable is None, show the airport code & "Airport"
    if favoritelocation_4data != "None":
        favoritelocation_4d = favoritelocation_4data
    else:
        favoritelocation_4d = favoritelocation_4.strip("airport:") + " Airport"

    logger.debug("favoritelocation_4d: %s" % favoritelocation_4d)

if favoritelocation_5d.find("arpt:") == 0 or favoritelocation_5d.find("airport:") == 0:
    # Set the display variable to extra data, only if the extra data isn't None.
    # If the extra data variable is None, show the airport code & "Airport"
    if favoritelocation_5data != "None":
        favoritelocation_5d = favoritelocation_5data
    else:
        favoritelocation_5d = favoritelocation_5.strip("airport:") + " Airport"

    logger.debug("favoritelocation_5d: %s" % favoritelocation_5d)

# I understand this goes against Wunderground's ToS for logo usage.
# Can't do much in a terminal.

spinner.stop()

print("Hey, welcome to PyWeather!")
print("Below, enter a location to check the weather for that location!")
if geoip_available is True:
    logger.debug("geoip is available. Showing option...")
    print("")
    print("You can also enter this to view weather for your current location:")
    print("currentlocation - " + currentlocation)
elif geoip_available is False and geoip_enabled is True:
    logger.debug("geoip isn't available, show an error message.")
    print("")
    print("The GeoIP service used for your current location gave an invalid location.")
    print("If this error continues, you can turn off the current location feature to avoid these error messages.")
if favoritelocation_available is True:
    logger.debug("favorite locations are enabled and available. showing option...")
    print("")
    print("You can also enter this to show weather for your favorite locations:")
    if favoritelocation_1 != "None":
        print("favoritelocation:1 - " + favoritelocation_1d)
    if favoritelocation_2 != "None":
        print("favoritelocation:2 - " + favoritelocation_2d)
    if favoritelocation_3 != "None":
        print("favoritelocation:3 - " + favoritelocation_3d)
    if favoritelocation_4 != "None":
        print("favoritelocation:4 - " + favoritelocation_4d)
    if favoritelocation_5 != "None":
        print("favoritelocation:5 - " + favoritelocation_5d)
if pws_enabled is True:
    logger.debug("pws queries have been enabled. Showing option...")
    print("")
    print("You can also query a Wunderground PWS by entering this:")
    print("pws:<PWS ID>")
if airports_enabled is True:
    logger.debug("Airport queries have been enabled. Showing option...")
    print("")
    print("You can also query airport weather information by entering this:")
    print("airport:<IATA or ICAO code>")

print("")
locinput = input("Input here: ")
locinput = str(locinput)

# Define previous location display variables
if previouslocation_enabled == "True":
    print("This piece of code is running")
    previouslocation_1d = locinput
    previouslocation_2d = previouslocation_1
    previouslocation_3d = previouslocation_2
    previouslocation_4d = previouslocation_3
    previouslocation_5d = previouslocation_4
    
    logger.debug("previouslocation_1d: %s ; previouslocation_2d: %s" %
                 (previouslocation_1d, previouslocation_2d))
    
    logger.debug("previouslocation_3d: %s ; previouslocation_4d: %s" %
                 (previouslocation_3d, previouslocation_4d))
    logger.debug("previouslocation_5d: %s" % previouslocation_5d)
    
    
    # Parse any previous locations that contain PWS in their, and set display variables.
    
    if previouslocation_1d.find("pws:") == 0:
        # The following code will delete pws: from the display string
        previouslocation_1d = previouslocation_1d[4:]
        previouslocation_1d = "PWS" + previouslocation_1d.upper()
        logger.debug("previouslocation_1d: %s" % previouslocation_1d)
    
    
    if previouslocation_2d.find("pws:") == 0:
        # The following code will delete pws: from the display string
        previouslocation_2d = previouslocation_2d[4:]
        previouslocation_2d = "PWS" + previouslocation_2d.upper()
        logger.debug("previouslocation_2d: %s" % previouslocation_2d)
    
    if previouslocation_3d.find("pws:") == 0:
        # The following code will delete pws: from the display string
        previouslocation_3d = previouslocation_3d[4:]
        previouslocation_3d = "PWS" + previouslocation_3d.upper()
        logger.debug("previouslocation_3d: %s" % previouslocation_3d)
    
    if previouslocation_4d.find("pws:") == 0:
        # The following code will delete pws: from the display string
        previouslocation_4d = previouslocation_4d[4:]
        previouslocation_4d = "PWS" + previouslocation_4d.upper()
        logger.debug("previouslocation_4d: %s" % previouslocation_4d)
    
    if previouslocation_5d.find("pws:") == 0:
        # The following code will delete pws: from the display string
        previouslocation_5d = previouslocation_5d[4:]
        previouslocation_5d = "PWS" + previouslocation_5d.upper()
        logger.debug("previouslocation_5d: %s" % previouslocation_5d)
    
    # Adds airport location to display variable and strips out the "airport bit"
    
    if previouslocation_1d.find("arpt:") == 0 or previouslocation_1d.find("airport") == 0:
        previouslocation_1d = previouslocation_1.strip("airport:") + "Airport"
        logger.debug("previouslocation_1d: %s" % previouslocation_1d)
    
    
    if previouslocation_2d.find("arpt:") == 0 or previouslocation_2d.find("airport") == 0:
        previouslocation_2d = previouslocation_2.strip("airport:") + "Airport"
        logger.debug("previouslocation_2d: %s" % previouslocation_2d)
    
    
    if previouslocation_3d.find("arpt:") == 0 or previouslocation_3d.find("airport") == 0:
        previouslocation_3d = previouslocation_3.strip("airport:") + "Airport"
        logger.debug("previouslocation_3d: %s" % previouslocation_3d)
    
    
    if previouslocation_4d.find("arpt:") == 0 or previouslocation_4d.find("airport") == 0:
        previouslocation_4d = previouslocation_4.strip("airport:") + "Airport"
        logger.debug("previouslocation_4d: %s" % previouslocation_4d)
    
    
    if previouslocation_5d.find("arpt:") == 0 or previouslocation_5d.find("airport") == 0:
        previouslocation_5d = previouslocation_5.strip("airport:") + "Airport"
        logger.debug("previouslocation_5d: %s" % previouslocation_5d)
    
    config['PREVIOUS LOCATIONS']['prevloc1'] = previouslocation_1d
    config['PREVIOUS LOCATIONS']['prevloc2'] = previouslocation_2d
    config['PREVIOUS LOCATIONS']['prevloc3'] = previouslocation_3d
    config['PREVIOUS LOCATIONS']['prevloc4'] = previouslocation_4d
    config['PREVIOUS LOCATIONS']['prevloc5'] = previouslocation_5d

    try:
        with open('storage//config.ini', 'w') as configfile:
            config.write(configfile)
        print(Fore.YELLOW + Style.BRIGHT + "Changes saved!")

    except:
        print(Fore.RED + Style.BRIGHT + "An issue occured when trying to write previous history to your config file.",
              "Please note that not changes were made to your config file.", sep="\n")

    test_thing = config.get('PREVIOUS LOCATIONS', 'prevloc1')
    print(previouslocation_1d)
    print(test_thing)
print("Checking the weather, it'll take a few seconds!")
print("")

# Define query types to false at the start. If a certain query type is found, it'll be marked as True later in the script.
pws_query = False
airport_query = False
logger.debug("pws_query: %s ; airport_query: %s" %
             (pws_query, airport_query))

# Tell users their query isn't supported nicely
# I understand that eggs.find("ham") isn't the most pythonic thing ever, but it's more reliable
# and easier to work with than if "ham" in eggs. Multiple conditions are needed to support the short
# shortcuts? Basically favloc: instead of favoritelocation:.
if (geoip_enabled is False and locinput.find("currentlocation") == 0 or
    geoip_enabled is False and locinput.find("curloc") == 0):
    spinner.fail(text="PyWeather query failed!")
    print("")
    print("Whoops! You entered the query to access your current location, but",
          "the current location feature is disabled. To enable the current location feature",
          "in your config file make FIRSTINPUT/geoipservice_enabled True. Press enter to exit.", sep="\n")
    input()
    sys.exit()
elif (geoip_available is False and locinput.find("currentlocation") == 0 or
      geoip_available is False and locinput.find("curloc") == 0):
    spinner.fail(text="PyWeather query failed!")
    print("")
    print("Whoops! You entered the query to access your current location, there isn't any current location",
          "data at this time. Press enter to exit.", sep="\n")
    input()
    sys.exit()
# Here we're just looking to see if favloc isn't enabled, and display an error message if it's off.
elif (favoritelocation_enabled is False and locinput.find("favoritelocation:") == 0 or
      favoritelocation_enabled is False and locinput.find("favloc:") == 0):
    spinner.fail(text="PyWeather query failed!")
    print("")
    print("Whoops! You entered the query to access a favorite location, but the favorite locations",
          "feature isn't on. If you'd like to enable favorite locations, you can do so by booting up",
          "PyWeather, and selecting the favorite locations option. Alternatively, you can go into",
          "your config file and set FAVORITE LOCATIONS/enabled to True. Press enter to exit.", sep="\n")
    input()
    sys.exit()
# If favorite locations is on, but there aren't any favorite locations, then throw an error.
elif (favoritelocation_available is False and locinput.find("favoritelocation:") == 0 or
        favoritelocation_available is False and locinput.find("favloc:") == 0):
    spinner.fail(text="PyWeather query failed!")
    print("")
    print("Whoops! You entered the query to access a favorite location, but you don't have any favorite",
          "locations at this time. Press enter to exit.", sep="\n")
    input()
    sys.exit()

if (favoritelocation_available is True and locinput.find("favoritelocation:") == 0 or
        favoritelocation_available is True and locinput.find("favloc:") == 0):
    haveFavoriteLocation = False
    logger.debug("haveFavoriteLocation: %s" % haveFavoriteLocation)
    if locinput == "favoritelocation:1" or locinput == "favloc:1" and favoritelocation_1 != "None":
        locinput = favoritelocation_1
        haveFavoriteLocation = True
        logger.debug("locinput: %s ; haveFavoriteLocation: %s" %
                     (locinput, haveFavoriteLocation))
    elif locinput == "favoritelocation:1" or locinput == "favloc:1" and favoritelocation_1 == "None":
        spinner.fail(text="PyWeather query failed!")
        print("")
        print("Whoops! You entered the query to access your first favorite location, but",
              "it's currently not set to anything. Press enter to exit.", sep="\n")
        input()
        sys.exit()

    if locinput == "favoritelocation:2" or locinput == "favloc:2" and favoritelocation_2 != "None" and haveFavoriteLocation is False:
        locinput = favoritelocation_2
        haveFavoriteLocation = True
        logger.debug("locinput: %s ; haveFavoriteLocation: %s" %
                     (locinput, haveFavoriteLocation))
    elif locinput == "favoritelocation:2" and favoritelocation_2 == "None":
        spinner.fail(text="PyWeather query failed!")
        print("")
        print("Whoops! You entered the query to access your second favorite location, but",
              "it's currently not set to anything. Press enter to exit.", sep="\n")
        input()
        sys.exit()

    if locinput == "favoritelocation:3" or locinput == "favloc:3" and favoritelocation_3 != "None" and haveFavoriteLocation is False:
        locinput = favoritelocation_3
        haveFavoriteLocation = True
        logger.debug("locinput: %s ; haveFavoriteLocation: %s" %
                     (locinput, haveFavoriteLocation))
    elif locinput == "favoritelocation:3" and favoritelocation_3 == "None":
        spinner.fail(text="PyWeather query failed!")
        print("")
        print("Whoops! You entered the query to access your third favorite location, but",
              "it's currently not set to anything. Press enter to exit.", sep="\n")
        input()
        sys.exit()

    if locinput == "favoritelocation:4" or locinput == "favloc:4" and favoritelocation_4 != "None" and haveFavoriteLocation is False:
        locinput = favoritelocation_4
        haveFavoriteLocation = True
        logger.debug("locinput: %s ; haveFavoriteLocation: %s" %
                     (locinput, haveFavoriteLocation))
    elif locinput == "favoritelocation:4" and favoritelocation_4 == "None":
        spinner.fail(text="PyWeather query failed!")
        print("")
        print("Whoops! You entered the query to access your fourth favorite location, but",
              "it's currently not set to anything. Press enter to exit.", sep="\n")
        input()
        sys.exit()

    if locinput == "favoritelocation:5" or locinput == "favloc:5" and favoritelocation_5 != "None" and haveFavoriteLocation is False:
        locinput = favoritelocation_5
        haveFavoriteLocation = True
        logger.debug("locinput: %s ; haveFavoriteLocation: %s" %
                     (locinput, haveFavoriteLocation))
    elif locinput == "favoritelocation:5" and favoritelocation_5 == "None":
        spinner.fail(text="PyWeather query failed!")
        print("")
        print("Whoops! You entered the query to access your fifth favorite location, but",
              "it's currently not set to anything. Press enter to exit.", sep="\n")
        input()
        sys.exit()

    if haveFavoriteLocation is False:
        spinner.fail(text="PyWeather query failed!")
        print("")
        print("Your input didn't match up to a favorite location (you likely entered an invalid character/number past the colon).",
              "Press enter to exit.", sep="\n")
        input()
        sys.exit()

    useGeocoder = True
    logger.debug("useGeocoder: %s" % useGeocoder)

if pws_enabled is False and locinput.find("pws:") == 0:
    spinner.fail(text="PyWeather query failed!")
    print("")
    print("Whoops! You entered the query to access a PWS, but PWS queries are currently",
          "disabled. Press enter to exit.", sep="\n")
    input()
    sys.exit()

# Check for an airport query and if airports aren't enabled.
if (airports_enabled is False and locinput.find("airport:") == 0 or
    airports_enabled is False and locinput.find("arpt:") == 0):
    spinner.fail(text="PyWeather query failed!")
    print("")
    print("Whoops! You entered the query to access an airport, but airport queries are currently",
          "disabled. Press enter to exit.", sep="\n")
    input()
    sys.exit()

if (geoip_available is True and locinput.find("currentlocation") == 0 or
    geoip_available is True and locinput.find("curloc") == 0):
    locinput = currentlocation
    useGeocoder = False
    location = currentlocation
    logger.debug("locinput: %s ; useGeocoder: %s" %
                 (locinput, useGeocoder))
    logger.debug("location: %s" % currentlocation)

if pws_enabled is True and locinput.find("pws:") == 0:
    # Just for safety, query Wunderground's geolocator to get the lat/lon of the PWS.
    # This also helps to validate the PWS.
    # Use a .lower() on the PWS query for safety. It works when in lower-case.
    pwsinfourl = 'http://api.wunderground.com/api/' + apikey + '/geolookup/q/' + locinput.lower() + ".json"
    logger.debug("pwsinfourl: %s" % pwsinfourl)
    spinner.start(text="Validating PWS query...")
    try:
        pwsinfoJSON = requests.get(pwsinfourl)
        logger.debug("pwsinfoJSON acquired with: %s" % pwsinfoJSON)
        pwsinfo_json = json.loads(pwsinfoJSON.text)
        if jsonVerbosity is True:
            logger.debug("pwsinfo_json: %s" % pwsinfo_json)
        else:
            logger.debug("pwsinfo_json has been loaded.")
    except:
        spinner.fail(text='Failed to validate PWS query!')
        print("")
        print("Couldn't query Wunderground to validate your inputted PWS. Make sure that you have",
              "an internet connection, and that api.wunderground.com is unblocked."
              "Press enter to exit.", sep="\n")
        printException()
        input()
        sys.exit()

    try:
        pws_invalid = pwsinfo_json['location']['lat']
        logger.debug("we have good pws data.")
    except:
        spinner.fail(text='Failed to validate PWS query!')
        print("")
        print("The PWS you entered isn't online, or is invalid. Please try entering an online",
              "or valid PWS next time you use PyWeather. Press enter to exit.", sep="\n")
        input()
        sys.exit()
    pws_available = True
    logger.debug("pws_available: %s" % pws_available)
    # Extract data about latitude and longitude, if needed in a float format.
    pws_lat = pwsinfo_json['location']['lat']
    pws_lon = pwsinfo_json['location']['lon']
    logger.debug("pws_lat: %s ; pws_lon: %s" % (pws_lat, pws_lon))
    # Use the standard latstr/lonstr variables for the PWS' lat/lon.
    latstr = str(pwsinfo_json['location']['lat'])
    lonstr = str(pwsinfo_json['location']['lon'])
    logger.debug("latstr: %s ; lonstr: %s" % (latstr, lonstr))
    # Extract data about the PWS location for outputting to user
    pws_city = pwsinfo_json['location']['city']
    pws_state = pwsinfo_json['location']['state']
    logger.debug("pws_city: %s ; pws_state: %s" %
                 (pws_city, pws_state))
    pws_location = pws_city + ", " + pws_state
    logger.debug("pws_location: %s" % pws_location)
    pws_id = pwsinfo_json['location']['nearby_weather_stations']['pws']['station'][0]['id']
    logger.debug("pws_id: %s" % pws_id)
    # Flag PWS enabled URLs, and not use the geocoder
    pws_urls = True
    useGeocoder = False
    logger.debug("pws_urls: %s ; useGeocoder: %s" % (pws_urls, useGeocoder))

if (airports_enabled is True and locinput.find("airport:") == 0
    or airports_enabled is True and locinput.find("arpt:") == 0):
    # In the location input trim off "airport:" or "arpt:", as we can't call the API with that being included
    spinner.start(text="Validating airport query...")
    if locinput.find("airport:") == 0:
        airport_locinput = locinput.strip("airport:").upper()
    elif locinput.find("arpt:") == 0:
        airport_locinput = locinput.strip("arpt:").upper()
    logger.debug("airport_locinput: %s" % airport_locinput)
    airportinfourl = 'http://api.wunderground.com/api/' + apikey + '/geolookup/q/' + airport_locinput.lower() + ".json"
    try:
        airportJSON = requests.get(airportinfourl)
        logger.debug("airport information JSON (airportJSON) acquired with end result: %s" % airportJSON)
        airportinfo_json = json.loads(airportJSON.text)
        if jsonVerbosity is True:
            logger.debug("airportinfo_json: %s" % airportinfo_json)
        else:
            logger.debug("airportinfo_json has been loaded.")
    except:
        spinner.fail(text='Failed to validate airport query!')
        print("")
        print("Couldn't query Wunderground to validate your inputted airport. Make sure that you have",
              "an internet connection, and that api.wunderground.com is unblocked."
              "Press enter to exit.", sep="\n")
        printException()
        input()
        sys.exit()

    try:
        airport_invalid = airportinfo_json['location']['lat']
        logger.debug("We have good airport data!")
    except:
        spinner.fail(text="Failed to validate airport query!")
        print("")
        print("The airport that you entered doesn't have an active weather service, or doesn't exist",
              "Please try entering an airport with an active weather service or one that exists next",
              "time you use PyWeather. Press enter to exit.", sep="\n")
        input()
        sys.exit()
    airport_available = True
    logger.debug("airport_available: %s" % airport_available)
    # Extract data about lat/lon. Use the airport_lat/airport_lon vars as raw data. latstr/lonstr are compatibility
    # strings.

    airport_lat = airportinfo_json['location']['lat']
    airport_lon = airportinfo_json['location']['lon']
    logger.debug("airport_lat: %s ; airport_lon: %s" % (airport_lat, airport_lon))
    # Standard lat/lon stuff here
    latstr = str(airportinfo_json['location']['lat'])
    lonstr = str(airportinfo_json['location']['lon'])
    logger.debug("latstr: %s ; lonstr: %s" % (latstr, lonstr))
    # Extract data about the airport location
    airport_city = airportinfo_json['location']['city']
    airport_state = airportinfo_json['location']['state']
    logger.debug("airport_city: %s ; airport_state: %s" %
                 (airport_city, airport_state))
    # Having this as the airport name works very well so far. The "city" that Wunderground
    # provides for airports is the name of an airport without "Airport" included.
    airport_name = airport_city + " Airport"
    airport_code = airportinfo_json['location']['nearby_weather_stations']['airport']['station'][0]['icao']
    logger.debug("airport_name: %s ; airport_code: %s" %
                 (airport_name, airport_code))
    airport_urls = True
    useGeocoder = False
    logger.debug("airport_urls: %s ; useGeocoder: %s" %
                 (airport_urls, useGeocoder))
    airport_query = True
    logger.debug("airport_query: %s" % airport_query)

# Start the geocoder. If we don't have a connection, exit nicely.
# After we get location data, store it in latstr and lonstr, and store
# it in the table called loccords.

firstfetch = time.time()
if useGeocoder is True:
    spinner.start(text='Locating input...')
    logger.info("Start geolocator...")
    try:
        location = geolocator.geocode(locinput, language="en", timeout=20)
        # Since the loading bars interfere with true verbosity logging, we turn
        # them off if verbosity is enabled (it isn't needed)
        # :/
    except geopy.exc.GeocoderQuotaExceeded:
        spinner.fail(text='Failed to locate input!')
        print("")
        logger.warning("Geocoder quota has been exceeded!")
        print("When attempting to access Google's geocoder, a quota error was hit. Please",
              "wait 1-2 minutes, then try using PyWeather again.", sep="\n")
        printException()
        print("Press enter to continue.")
        input()
        sys.exit()
    except geopy.exc.GeocoderServiceError:
        spinner.fail(text='Failed to locate input!')
        print("")
        logger.warning("Service error from geopy. SSL issue most likely?")
        print("When attempting to access Google's geocoder, a service error occurred.",
              "99% of the time, this is due to the geocoder operating in HTTPS mode,",
              "but not being able to properly operate on your OS in such mode. To fix this",
              "issue, in the configuration file, change the GEOCODER/scheme option to 'http'.", sep="\n")
        printException()
        print("Press enter to continue.")
        input()
        sys.exit()
    except:
        spinner.fail(text='Failed to locate input!')
        print("")
        logger.warning("No connection to Google's geocoder!")
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
        spinner.fail(text='Failed to locate input!')
        print("")
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

spinner.stop()
spinner.start(text='Declaring API variables...')

# Declare the API URLs with the API key, and latitude/longitude strings from earlier.
if pws_urls is False:
    currenturl = 'http://api.wunderground.com/api/' + apikey + '/conditions/q/' + latstr + ',' + lonstr + '.json'
    f10dayurl = 'http://api.wunderground.com/api/' + apikey + '/forecast10day/q/' + latstr + ',' + lonstr + '.json'
    hourlyurl = 'http://api.wunderground.com/api/' + apikey + '/hourly/q/' + latstr + ',' + lonstr + '.json'
    tendayurl = 'http://api.wunderground.com/api/' + apikey + '/hourly10day/q/' + latstr + ',' + lonstr + '.json'
    astronomyurl = 'http://api.wunderground.com/api/' + apikey + '/astronomy/q/' + latstr + ',' + lonstr + '.json'
    almanacurl = 'http://api.wunderground.com/api/' + apikey + '/almanac/q/' + latstr + ',' + lonstr + '.json'
    alertsurl = 'http://api.wunderground.com/api/' + apikey + '/alerts/q/' + latstr + ',' + lonstr + '.json'
    yesterdayurl = 'http://api.wunderground.com/api/' + apikey + '/yesterday/q/' + latstr + ',' + lonstr + '.json'
    tideurl = 'http://api.wunderground.com/api/' + apikey + '/tide/q/' + latstr + ',' + lonstr + '.json'
    hurricaneurl = 'http://api.wunderground.com/api/' + apikey + '/currenthurricane/view.json'
elif airport_urls is True:
    currenturl = 'http://api.wunderground.com/api/' + apikey + '/conditions/q/' + airport_locinput + '.json'
    f10dayurl = 'http://api.wunderground.com/api/' + apikey + '/forecast10day/q/' + airport_locinput + '.json'
    hourlyurl = 'http://api.wunderground.com/api/' + apikey + '/hourly/q/' + airport_locinput + '.json'
    tendayurl = 'http://api.wunderground.com/api/' + apikey + '/hourly10day/q/' + airport_locinput + '.json'
    astronomyurl = 'http://api.wunderground.com/api/' + apikey + '/astronomy/q/' + airport_locinput + '.json'
    almanacurl = 'http://api.wunderground.com/api/' + apikey + '/almanac/q/' + airport_locinput + '.json'
    alertsurl = 'http://api.wunderground.com/api/' + apikey + '/alerts/q/' + airport_locinput + '.json'
    yesterdayurl = 'http://api.wunderground.com/api/' + apikey + '/yesterday/q/' + airport_locinput + '.json'
    tideurl = 'http://api.wunderground.com/api/' + apikey + '/tide/q/' + airport_locinput + '.json'
    hurricaneurl = 'http://api.wunderground.com/api/' + apikey + '/currenthurricane/view.json'
elif pws_urls is True:
    currenturl = 'http://api.wunderground.com/api/' + apikey + '/conditions/q/' + locinput.lower() + '.json'
    f10dayurl = 'http://api.wunderground.com/api/' + apikey + '/forecast10day/q/' + locinput.lower() + '.json'
    hourlyurl = 'http://api.wunderground.com/api/' + apikey + '/hourly/q/' + locinput.lower() + '.json'
    tendayurl = 'http://api.wunderground.com/api/' + apikey + '/hourly10day/q/' + locinput.lower() + '.json'
    astronomyurl = 'http://api.wunderground.com/api/' + apikey + '/astronomy/q/' + locinput.lower() + '.json'
    almanacurl = 'http://api.wunderground.com/api/' + apikey + '/almanac/q/' + locinput.lower() + '.json'
    alertsurl = 'http://api.wunderground.com/api/' + apikey + '/alerts/q/' + locinput.lower() + '.json'
    yesterdayurl = 'http://api.wunderground.com/api/' + apikey + '/yesterday/q/' + locinput.lower() + '.json'
    tideurl = 'http://api.wunderground.com/api/' + apikey + '/tide/q/' + locinput.lower() + '.json'
    hurricaneurl = 'http://api.wunderground.com/api/' + apikey + '/currenthurricane/view.json'


logger.debug("currenturl: %s" % currenturl)
logger.debug("f10dayurl: %s" % f10dayurl)
logger.debug("hourlyurl: %s" % hourlyurl)
logger.debug("tendayurl: %s" % tendayurl)
logger.debug("astronomyurl: %s" % astronomyurl)
logger.debug("almanacurl: %s" % almanacurl)
logger.debug("yesterdayurl: %s" % yesterdayurl)
logger.debug("tideurl: %s" % tideurl)
logger.debug("hurricaneurl: %s" % hurricaneurl)
logger.debug("yesterdayurl: %s" % yesterdayurl)
logger.info("End API var declare...")

logger.info("Start API fetch...")

# If a user requested their API key to be validated, and the backup key
# can be loaded (as was checked earlier), we do it here.

# Fetch JSON files. Exit if a failure occurs.

spinner.stop()
spinner.start(text="Fetching current weather information...")

try:
    summaryJSON = requests.get(currenturl)
    cachetime_current = time.time()
    logger.debug("Acquired summary JSON, end result: %s" % summaryJSON)
except:
    spinner.fail("Failed to fetch current weather information!")
    print("")
    logger.warning("No connection to the API!! Is the connection offline?")
    print("When PyWeather attempted to fetch current weather information,",
          "PyWeather ran into an error. If you're on a network with a filter, make sure",
          "'api.wunderground.com' is unblocked. Otherwise, make sure you have an internet",
          "connection.", sep="\n")
    printException()
    print("Press enter to continue.")
    input()
    sys.exit()

if yesterdaydata_onsummary is True or prefetch_yesterdaydata is True:
    spinner.stop()
    spinner.start(text="Fetching yesterday's weather information...")
    # Tell PyWeather that yesterday's weather is prefetched
    yesterdaydata_prefetched = True
    logger.debug("yesterdaydata_prefetched: %s" % yesterdaydata_prefetched)
    try:
        yesterdayJSON = requests.get(yesterdayurl)
        cachetime_yesterday = time.time()
        logger.debug("Acquired yesterday JSON, end result: %s" % yesterdayJSON)
    except:
        spinner.fail("Failed to fetch yesterday weather information!")
        print("")
        logger.warning("No connection to the API!! Is the connection offline?")
        print("When PyWeather attempted to fetch yesterday's weather information,",
              "PyWeather ran into an error. If you're on a network with a filter, make sure",
              "'api.wunderground.com' is unblocked. Otherwise, make sure you have an internet",
              "connection.", sep="\n")
        printException()
        print("Press enter to continue.")
        input()
        sys.exit()
else:
    yesterdaydata_prefetched = False
    logger.debug("yesterdaydata_prefetched: %s" % yesterdaydata_prefetched)

spinner.stop()
spinner.start(text="Fetching forecast information...")
try:
    forecast10JSON = requests.get(f10dayurl)
    cachetime_forecast = time.time()
    logger.debug("Acquired forecast 10day JSON, end result: %s" % forecast10JSON)
except:
    spinner.fail(text="Failed to fetch forecast information!")
    print("")
    logger.warning("No connection to the API!! Is the connection offline?")
    print("When PyWeather attempted to fetch forecast information,",
          "PyWeather ran into an error. If you're on a network with a filter, make sure",
          "'api.wunderground.com' is unblocked. Otherwise, make sure you have an internet",
          "connection.", sep="\n")
    printException()
    print("Press enter to continue.")
    input()
    sys.exit()


if sundata_summary == True:
    spinner.stop()
    spinner.start(text="Fetching astronomy information...")
    try:
        cachetime_sundata = time.time()
        sundataJSON = requests.get(astronomyurl)
        logger.debug("Acquired astronomy JSON, end result: %s" % sundataJSON)
    except:
        spinner.fail(text="Failed to fetch astronomy information!")
        print("")
        logger.warning("No connection to the API!! Is the connection offline?")
        print("When PyWeather attempted to fetch astronomy information,",
              "PyWeather ran into an error. If you're on a network with a filter, make sure",
              "'api.wunderground.com' is unblocked. Otherwise, make sure you have an internet",
              "connection.", sep="\n")
        printException()
        print("Press enter to continue.")
        input()
        sys.exit()

if prefetch10Day_atStart == True:
    spinner.stop()
    spinner.start(text="Fetching 10 day/1.5 day hourly information...")
    try:
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
    except:
        spinner.fail(text="Failed to fetch 10 day/1.5 day hourly information!")
        print("")
        logger.warning("No connection to the API!! Is the connection offline?")
        print("When PyWeather attempted to fetch 10 day/1.5 day hourly information,",
              "PyWeather ran into an error. If you're on a network with a filter, make sure",
              "'api.wunderground.com' is unblocked. Otherwise, make sure you have an internet",
              "connection.", sep="\n")
        printException()
        print("Press enter to continue.")
        input()
        sys.exit()

else:
    spinner.stop()
    spinner.start(text="Fetching 1.5 day hourly information...")
    try:
        hourly36JSON = requests.get(hourlyurl)
        cachetime_hourly36 = time.time()
        tenday_prefetched = False
        logger.debug("tenday_prefetched: %s" % tenday_prefetched)
        logger.debug("Acquired 36 hour hourly JSON, end result: %s" % hourly36JSON)
    except:
        spinner.fail(text="Failed to fetch 1.5 day hourly information!")
        print("")
        logger.warning("No connection to the API!! Is the connection offline?")
        print("When PyWeather attempted to 1.5 day hourly information,",
              "PyWeather ran into an error. If you're on a network with a filter, make sure",
              "'api.wunderground.com' is unblocked. Otherwise, make sure you have an internet",
              "connection.", sep="\n")
        printException()
        print("Press enter to continue.")
        input()
        sys.exit()

if almanac_summary == True:
    spinner.stop()
    spinner.start(text="Fetching almanac information...")
    try:
        almanacJSON = requests.get(almanacurl)
        cachetime_almanac = time.time()
        logger.debug("Acquired almanac JSON, end result: %s" % almanacJSON)
    except:
        spinner.fail(text="Failed to fetch almanac information!")
        print("")
        logger.warning("No connection to the API!! Is the connection offline?")
        print("When PyWeather attempted to fetch almanac information,",
              "PyWeather ran into an error. If you're on a network with a filter, make sure",
              "'api.wunderground.com' is unblocked. Otherwise, make sure you have an internet",
              "connection.", sep="\n")
        printException()
        print("Press enter to continue.")
        input()
        sys.exit()

if showAlertsOnSummary == True:
    spinner.stop()
    spinner.start(text="Fetching alerts information...")
    try:
        alertsJSON = requests.get(alertsurl)
        cachetime_alerts = time.time()
        alertsPrefetched = True
        logger.debug("Acquired alerts JSON, end result: %s" % alertsJSON)
    except:
        spinner.fail(text="Failed to fetch alerts information!")
        print("")
        logger.warning("No connection to the API!! Is the connection offline?")
        print("When PyWeather attempted to fetch alerts information,",
              "PyWeather ran into an error. If you're on a network with a filter, make sure",
              "'api.wunderground.com' is unblocked. Otherwise, make sure you have an internet",
              "connection.", sep="\n")
        printException()
        print("Press enter to continue.")
        input()
        sys.exit()

else:
    alertsPrefetched = False
logger.debug("alertsPrefetched: %s" % alertsPrefetched)

if showTideOnSummary == True:
    spinner.stop()
    spinner.start(text="Fetching tide information...")
    try:
        tideJSON = requests.get(tideurl)
        cachetime_tide = time.time()
        tidePrefetched = True
        logger.debug("Acquired tide JSON, end result: %s" % tideJSON)
    except:
        spinner.fail(text="Failed to fetch tide information!")
        print("")
        logger.warning("No connection to the API!! Is the connection offline?")
        print("When PyWeather attempted to fetch tide information,",
              "PyWeather ran into an error. If you're on a network with a filter, make sure",
              "'api.wunderground.com' is unblocked. Otherwise, make sure you have an internet",
              "connection.", sep="\n")
        printException()
        print("Press enter to continue.")
        input()
        sys.exit()

else:
    tidePrefetched = False

logger.debug("tidePrefetched: %s" % tidePrefetched)

if prefetchHurricane_atboot == True:
    spinner.stop()
    spinner.start(text="Fetching hurricane information...")
    try:
        hurricaneJSON = requests.get(hurricaneurl)
        cachetime_hurricane = time.time()
        hurricanePrefetched = True
        logger.debug("Acquired hurricane JSON, end result: %s" % hurricaneJSON)
    except:
        spinner.fail(text="Failed to fetch hurricane information!")
        print("")
        logger.warning("No connection to the API!! Is the connection offline?")
        print("When PyWeather attempted to fetch hurricane information,",
              "PyWeather ran into an error. If you're on a network with a filter, make sure",
              "'api.wunderground.com' is unblocked. Otherwise, make sure you have an internet",
              "connection.", sep="\n")
        printException()
        print("Press enter to continue.")
        input()
        sys.exit()
else:
    hurricanePrefetched = False

logger.debug("hurricanePrefetched: %s" % hurricanePrefetched)


    
# And we parse the json using json.load.
logger.info("End API fetch...")
logger.info("Start JSON load...")
spinner.stop()
spinner.start(text="Parsing weather information...")
current_json = json.loads(summaryJSON.text)
if jsonVerbosity is True:
    logger.debug("current_json loaded with: %s" % current_json)
forecast10_json = json.loads(forecast10JSON.text)
if jsonVerbosity is True:
    logger.debug("forecast10_json loaded with: %s" % forecast10_json)
if prefetch10Day_atStart is True:
    tenday_json = json.loads(hourly10JSON.text)
    if jsonVerbosity is True:
        logger.debug("tenday_json loaded with: %s" % tenday_json)
    hourly36_json = json.loads(hourly36JSON.text)
    if jsonVerbosity is True:
        logger.debug("hourly36_json loaded with: %s" % hourly36_json)
else:
    hourly36_json = json.loads(hourly36JSON.text)
    if jsonVerbosity is True:
        logger.debug("hourly36_json loaded with: %s" % hourly36_json)
if sundata_summary is True:
    astronomy_json = json.loads(sundataJSON.text)
    if jsonVerbosity is True:
        logger.debug("astronomy_json loaded with: %s" % astronomy_json)

if yesterdaydata_prefetched is True:
    yesterday_json = json.loads(yesterdayJSON.text)
    if jsonVerbosity is True:
        logger.debug("yesterday_json: %s" % yesterday_json)

if almanac_summary is True:
    almanac_json = json.loads(almanacJSON.text)
    if jsonVerbosity is True:
        logger.debug("almanac_json loaded with: %s" % almanac_json)
if showAlertsOnSummary is True:
    alerts_json = json.loads(alertsJSON.text)
    if jsonVerbosity is True:
        logger.debug("alerts_json loaded with: %s" % alerts_json)
if showTideOnSummary is True:
    tide_json = json.loads(tideJSON.text)
    if jsonVerbosity is True:
        logger.debug("tide_json loaded with: %s" % tide_json)
if prefetchHurricane_atboot is True:
    hurricane_json = json.loads(hurricaneJSON.text)
    if jsonVerbosity is True:
        logger.debug("hurricane_json loaded with: %s" % hurricane_json)
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
logger.debug("summary_overall: %s ; summary_lastupdated: %s"
             % (summary_overall, summary_lastupdated))
logger.debug("summary_tempf: %s ; summary_tempc: %s"
             % (summary_tempf, summary_tempc))

summary_humidity = str(current_json['current_observation']['relative_humidity'])
logger.debug("summary_humidity: %s" % summary_humidity)
# Check for bad humidity data
currentcond_showHumidity = True
logger.debug("currentcond_showHumidity: %s" % currentcond_showHumidity)

if summary_humidity == "-999%":
    logger.info("summary_humidity is '-999%'.")
    currentcond_showHumidity = False
    logger.debug("currentcond_showHumidity: %s" % currentcond_showHumidity)

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
    almanac_prefetched = True
    almanac_data = True
    logger.debug("almanac_prefetched: %s ; almanac_data: %s" %
                 (almanac_prefetched, almanac_data))
    logger.debug("Parsing almanac data...")
    almanac_airportCode = almanac_json['almanac']['airport_code']
    if almanac_airportCode == "":
        almanac_data = False
    logger.debug("almanac_airportCode: %s" % almanac_airportCode)
    try:
        almanac_normalHighF = str(almanac_json['almanac']['temp_high']['normal']['F'])
        almanac_normalHighC = str(almanac_json['almanac']['temp_high']['normal']['C'])
        logger.debug("almanac_normalHighF: %s ; almanac_normalHighC: %s" %
                     (almanac_normalHighF, almanac_normalHighC))
        if almanac_normalHighF == "":
            almanac_normalHighdata = False
        else:
            almanac_normalHighdata = True
    except:
        almanac_normalHighdata = False
    logger.debug("almanac_normalHighdata: %s" % almanac_normalHighdata)
    try:
        almanac_recordHighF = str(almanac_json['almanac']['temp_high']['record']['F'])
        almanac_recordHighC = str(almanac_json['almanac']['temp_high']['record']['C'])
        logger.debug("almanac_recordHighF: %s ; almanac_recordHighC: %s" %
                     (almanac_recordHighF, almanac_recordHighC))
        almanac_recordHighdata = True
    except:
        printException_loggerwarn()
        almanac_recordHighdata = False
    logger.debug("almanac_recordHighdata: %s" % almanac_recordHighdata)
    try:
        almanac_recordHighYear = str(almanac_json['almanac']['temp_high']['recordyear'])
        logger.debug("almanac_recordHighYear: %s" % almanac_recordHighYear)
        almanac_recordHighYeardata = True
    except:
        almanac_recordHighYeardata = False
    logger.debug("almanac_recordHighYeardata: %s" % almanac_recordHighYeardata)
    try:
        almanac_normalLowF = str(almanac_json['almanac']['temp_low']['normal']['F'])
        almanac_normalLowC = str(almanac_json['almanac']['temp_low']['normal']['C'])
        logger.debug("almanac_normalLowF: %s ; almanac_normalLowC: %s" %
                     (almanac_normalLowF, almanac_normalLowC))
        if almanac_normalLowF == "":
            almanac_normalLowdata = False
        else:
            almanac_normalLowdata = True
    except:
        almanac_normalLowdata = False
    logger.debug("almanac_normalLowData: %s" % almanac_normalLowdata)
    try:
        almanac_recordLowF = str(almanac_json['almanac']['temp_low']['record']['F'])
        almanac_recordLowC = str(almanac_json['almanac']['temp_low']['record']['C'])
        logger.debug("almanac_recordLowF: %s ; almanac_recordLowC: %s" %
                     (almanac_recordLowF, almanac_recordLowC))
        almanac_recordLowdata = True
    except:
        almanac_recordLowdata = False
    logger.debug("almanac_recordLowdata: %s" % almanac_recordLowdata)
    try:
        almanac_recordLowYear = str(almanac_json['almanac']['temp_low']['recordyear'])
        logger.debug("almanac_recordLowYear: %s" % almanac_recordLowYear)
        almanac_recordLowYeardata = True
    except:
        almanac_recordLowYeardata = False
    logger.debug("almanac_recordLowYeardata: %s" % almanac_recordLowYeardata)

# <---- Tide data gets parsed here for the summary. ---->

if showTideOnSummary == True:
    tidedata_prefetched = True
    logger.debug("tidedata_prefetched: %s" % tidedata_prefetched)
    for data in tide_json['tide']['tideInfo']:
        tide_site = data['tideSite']

    if tide_site != "":
        tide_dataavailable = True
        tide_hightideacq = False
        tide_lowtideacq = False
        logger.debug("tide_dataavailable: %s ; tide_site: %s" %
                     (tide_dataavailable, tide_site))
        logger.debug("tide_hightideacq: %s ; tide_lowtideacq: %s" %
                     (tide_hightideacq, tide_lowtideacq))
        for data in tide_json['tide']['tideSummary']:
            if data['data']['type'] == "Low Tide" and tide_lowtideacq == False:
                tide_lowtidetime = data['date']['pretty']
                tide_lowtideheight = data['data']['height']
                tide_lowtideacq = True
                logger.debug("tide_lowtidetime: %s ; tide_lowtideheight: %s" %
                             (tide_lowtidetime, tide_lowtideheight))
                logger.debug("tide_lowtideacq: %s" % tide_lowtideacq)
            elif data['data']['type'] == "High Tide" and tide_hightideacq == False:
                tide_hightidetime = data['date']['pretty']
                tide_hightideheight = data['data']['height']
                tide_hightideacq = True
                logger.debug("tide_hightidetime: %s ; tide_hightideheight: %s" %
                             (tide_hightidetime, tide_hightideheight))
                logger.debug("tide_hightideacq: %s" % tide_hightideacq)

        if tide_hightideacq == False and tide_lowtideacq == False:
            tide_dataavailable = False
            logger.debug("tide_dataavailable: %s")
    else:
        tide_dataavailable = False
        logger.debug("tide_dataavailable: %s" % tide_dataavailable)
else:
    tidedata_prefetched = False
    logger.debug("tidedata_prefetched: %s" % tidedata_prefetched)

# Parse basic yesterday weather information.
if yesterdaydata_onsummary is True:
    # Parse the weather conditions, which is actually quite interesting to do.
    # For the day/night conditions, parse what the weather was at 12pm and 12am, and find the conditions given that '12:' and 'PM', etc are found.
    # If it matches, say the data was fetched, and move on.
    yesterdaysummary_dayconddata = True
    yesterdaysummary_nightconddata = True
    yesterdaysummary_daycondfetched = False
    yesterdaysummary_nightcondfetched = False
    logger.debug("yesterdaysummary_dayconddata: %s ; yesterdaysummary_nightconddata: %s" %
                 (yesterdaysummary_dayconddata, yesterdaysummary_nightconddata))
    logger.debug("yesterdaysummary_daycondfetched: %s ; yesterdaysummary_nightcondfetched: %s" %
                 (yesterdaysummary_daycondfetched, yesterdaysummary_nightcondfetched))
    for data in yesterday_json['history']['observations']:
        yesterdaysummary_hour = data['date']['hour']
        logger.debug("yesterdaysummary_hour: %s" % yesterdaysummary_hour)
        # Parse the weather given that we found '00' in the hour.
        if yesterdaysummary_hour.find("00") == 0 and yesterdaysummary_nightcondfetched is False:
            logger.info("'00' was found in yesterdaysummary_hour and yesterdaysummary_nightcondfetched is False.")
            yesterdaysummary_nightcondfetched = True
            logger.debug("yesterdaysummary_nightcondfetched: %s" % yesterdaysummary_nightcondfetched)

            try:
                yesterdaysummary_nightconditions = data['conds']
                logger.debug("yesterdaysummary_nightconditions: %s ; yesterdaysummary_nightconddata: %s" %
                             (yesterdaysummary_nightconditions, yesterdaysummary_nightconddata))

                if yesterdaysummary_nightconditions == "" or yesterdaysummary_nightconditions == "Unknown":
                    logger.info(
                        "yesterdaysumary_nightconditions is '' or yesterdaysummary_nightconditions is 'Unknown'.")
                    yesterdaysummary_nightconddata = False
                    logger.debug("yesterdaysummary_nightconddata: %s" % yesterdaysummary_nightconddata)

            except KeyError:
                printException_loggerwarn()
                yesterdaysummary_nightconddata = False
                logger.debug("yesterdaysummary_nightconddata: %s" % yesterdaysummary_nightconddata)


        if yesterdaysummary_hour.find("12") == 0 and yesterdaysummary_daycondfetched is False:
            logger.info("'12' was found in yesterdaysummary_hour and yesterdaysummary_daycondfetched is False.")
            yesterdaysummary_daycondfetched = True
            logger.debug("yesterdaysummary_daycondfetched: %s" % yesterdaysummary_daycondfetched)

            try:
                yesterdaysummary_dayconditions = data['conds']
                logger.debug("yesterdaysummary_dayconditions: %s ; yesterdaysummary_daycondfetched: %s" %
                             (yesterdaysummary_dayconditions, yesterdaysummary_daycondfetched))

                if yesterdaysummary_dayconditions == "" or yesterdaysummary_dayconditions == "Unknown":
                    logger.info("yesterdaysummary_dayconditions is '' or yesterdaysummary_dayconditions is 'Unknown'.")
                    yesterdaysummary_dayconddata = False
                    logger.debug("yesterdaysummary_dayconddata: %s" % yesterdaysummary_dayconddata)
            except KeyError:
                printException_loggerwarn()
                yesterdaysummary_dayconddata = False
                logger.debug("yesterdaysummary_dayconddata: %s" % yesterdaysummary_dayconddata)

        # We have data for both day/night conditions, break the loop.
        if yesterdaysummary_nightcondfetched is True and yesterdaysummary_daycondfetched is True:
            logger.info("yesterdaysummary_nightcondfetched is True & yesterdaysummary_daycondfetched is True.")
            break

    # Check from the for loop above if we have data for conditions. If we don't, put 'Not available' as the condition.

    if yesterdaysummary_nightcondfetched is False:
        logger.info("yesterdaysummary_nightcondfetched is False.")
        yesterdaysummary_nightconddata = False
        logger.debug("yesterdaysummary_nightconddata: %s" % yesterdaysummary_nightconddata)

    if yesterdaysummary_daycondfetched is False:
        logger.info("yesterdaysummary_daycondfetched is False.")
        yesterdaysummary_dayconddata = False
        logger.debug("yesterdaysummary_dayconddata: %s" % yesterdaysummary_dayconddata)

    # Set the display variables for yesterdaysummary
    yesterdaysummary_showHighTemp = True
    yesterdaysummary_showLowTemp = True
    yesterdaysummary_showHumidity = True
    yesterdaysummary_showWindSpeed = True
    yesterdaysummary_showWindGust = True
    logger.debug("yesterdaysummary_showHighTemp: %s ; yesterdaysummary_showLowTemp: %s" %
                 (yesterdaysummary_showHighTemp, yesterdaysummary_showLowTemp))
    logger.debug("yesterdaysummary_showHumidity: %s ; yesterdaysummary_showWindSpeed: %s" %
                 (yesterdaysummary_showHumidity, yesterdaysummary_showWindSpeed))
    logger.debug("yesterdaysummary_showWindGust: %s" % yesterdaysummary_showWindGust)

    # Get the high/low weather, the average wind/max wind, and average humidity for the previous day.

    for data in yesterday_json['history']['dailysummary']:
        yesterdaysummary_hightempf = str(data['maxtempi'])
        yesterdaysummary_hightempc = str(data['maxtempm'])
        logger.debug("yesterdaysummary_hightempf: %s ; yesterdaysummary_hightempc: %s" %
                     (yesterdaysummary_hightempf, yesterdaysummary_hightempc))
        if yesterdaysummary_hightempf == "" or yesterdaysummary_hightempc == "":
            logger.info("yesterdaysummary_hightempf is '' yesterdaysummary_hightempc is ''.")
            yesterdaysummary_showHighTemp = False
            logger.debug("yesterdaysummary_showHighTemp: %s" % yesterdaysummary_showHighTemp)
        yesterdaysummary_lowtempf = str(data['mintempi'])
        yesterdaysummary_lowtempc = str(data['mintempm'])
        logger.debug("yesterdaysummary_lowtempf: %s ; yesterdaysummary_lowtempc: %s" %
                     (yesterdaysummary_lowtempf, yesterdaysummary_lowtempc))
        if yesterdaysummary_lowtempf == "" or yesterdaysummary_lowtempc == "":
            logger.info("yesterdaysummary_lowtempf is '' or yesterdaysummary_lowtempc is ''.")
            yesterdaysummary_showLowTemp = False
            logger.debug("yesterdaysummary_showLowTemp: %s" % yesterdaysummary_showLowTemp)
        yesterdaysummary_windmph = str(data['meanwindspdi'])
        yesterdaysummary_windkph = str(data['meanwindspdm'])
        logger.debug("yesterdaysummary_windmph: %s ; yesterdaysummary_windkph: %s" %
                     (yesterdaysummary_windmph, yesterdaysummary_windkph))
        # Wunderground WHY DID YOU DO THIS?!?!! KEEP THINGS CONSTANT!
        yesterdaysummary_gustmph = str(data['maxwspdi'])
        yesterdaysummary_gustkph = str(data['maxwspdm'])
        logger.debug("yesterdaysummary_gustmph: %s ; yesterdaysummary_gustkph: %s" %
                     (yesterdaysummary_gustmph, yesterdaysummary_gustkph))

        # Check for bad wind data, since of course that's a thing!
        if yesterdaysummary_windmph == "" or yesterdaysummary_windkph == "":
            logger.info("yesterdaysummary_windmph is '' or yesterdaysummary_windkph is ''.")
            yesterdaysummary_showWindSpeed = False
            logger.debug("yesterdaysummary_showWindSpeed: %s" % yesterdaysummary_showWindSpeed)

        if yesterdaysummary_gustmph == "" or yesterdaysummary_gustkph == "":
            logger.info("yesterdaysumary_gustmph is '' or yesterdaysummary_gustkph is ''.")
            yesterdaysummary_showWindGust = False
            logger.debug("yesterdaysummary_showWindGust: %s" % yesterdaysummary_showWindGust)
        # Do what we do best - Guess the average humidity
        try:
            yesterdaysummary_maxhumidity = int(data['maxhumidity'])
            yesterdaysummary_minhumidity = int(data['minhumidity'])
            logger.debug("yesterdaysummary_maxhumidity: %s ; yesterdaysummary_minhumidity: %s" %
                         (yesterdaysummary_maxhumidity, yesterdaysummary_minhumidity))
        except ValueError:
            printException_loggerwarn()
            yesterdaysummary_showHumidity = False
            logger.debug("yesterdaysummary_showHumidity: %s" % yesterdaysummary_showHumidity)

        if yesterdaysummary_showHumidity is True:
            # Enter this block if we have valid humidity data, which basically means
            # yesterdaysummary_avghumidity isn't 'Not available'.
            logger.info("yesterdaysummary_avghumidity != 'Not available'")
            # Add the humidity, divide by 2
            yesterdaysummary_avghumidity = yesterdaysummary_maxhumidity + yesterdaysummary_minhumidity
            logger.debug("yesterdaysummary_avghumidity: %s" % yesterdaysummary_avghumidity)
            yesterdaysummary_avghumidity = yesterdaysummary_avghumidity / 2
            logger.debug("yesterdaysummary_avghumidity: %s" % yesterdaysummary_avghumidity)
            # Round to the 0th digit, then int it, and THEN str it. This removes the trailing zero.
            yesterdaysummary_avghumidity = str(int(round(yesterdaysummary_avghumidity, 0)))
            logger.debug("yesterdaysummary_avghumidity: %s" % yesterdaysummary_avghumidity)


logger.info("Initalize color...")
init()

spinner.stop()
logger.info("Printing current conditions...")
    
# <--------------- This is where we end parsing, and begin printing. ---------->

summaryHourlyIterations = 0

if pws_available is True:
    location = pws_id + " (located in " + pws_location + ")"
    location2 = "PWS " + pws_id
elif airport_available is True:
    location = airport_name
    location2 = airport_code
else:
    location2 = str(location)
logger.debug("location: %s" % location)
logger.debug("location2: %s" % location2)

print(Fore.YELLOW + Style.BRIGHT + "Here's the weather for: " + Fore.CYAN + Style.BRIGHT + str(location))
print(Fore.YELLOW + Style.BRIGHT + summary_lastupdated)
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
            print(Fore.RED + Style.BRIGHT + "** A " + alerts_description + " Meteoalarm has been issued" +
                  " for " + str(location) + ",", 
                  Fore.RED + Style.BRIGHT + "and is in effect until " + alerts_expiretime + ". **", sep="\n")
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
                print(Fore.RED + Style.BRIGHT + "** A " + alerts_description + " has been issued" +
                      " for " + str(location) + ",",
                      Fore.RED + Style.BRIGHT + "and is in effect until " + alerts_expiretime + ". **", sep="\n")
                print("")
        except:
            # I'll keep this here as a "just in case".
            logger.info("No alert information available!")
            alerts_type = "None"
            logger.debug("alerts_type: %s" % alerts_type)
    
print(Fore.YELLOW + Style.BRIGHT + "Currently:")
print(Fore.YELLOW + Style.BRIGHT + "Current conditions: " + Fore.CYAN + Style.BRIGHT + summary_overall)
print(Fore.YELLOW + Style.BRIGHT + "Current temperature: " + Fore.CYAN + Style.BRIGHT + summary_tempf + "°F (" + summary_tempc + "°C)")
print(Fore.YELLOW + Style.BRIGHT + "And it feels like: " + Fore.CYAN + Style.BRIGHT + summary_feelslikef
      + "°F (" + summary_feelslikec + "°C)")
print(Fore.YELLOW + Style.BRIGHT + "Current dew point: " + Fore.CYAN + Style.BRIGHT + summary_dewPointF
      + "°F (" + summary_dewPointC + "°C)")
if winddata == True:
    if summary_winddir == "Variable":
        print(Fore.YELLOW + Style.BRIGHT + "Current wind: " + Fore.CYAN + Style.BRIGHT + summary_windmphstr + " mph (" + summary_windkphstr + " kph), blowing in variable directions.")
    else:
        print(Fore.YELLOW + Style.BRIGHT + "Current wind: " + Fore.CYAN + Style.BRIGHT + summary_windmphstr + " mph (" + summary_windkphstr + " kph), blowing " + summary_winddir + ".")
else:
    print(Fore.YELLOW + Style.BRIGHT + "Wind data is not available for this location.")
if currentcond_showHumidity is True:
    print(Fore.YELLOW + Style.BRIGHT + "Current humidity: " + Fore.CYAN + Style.BRIGHT + summary_humidity)
print("")

if yesterdaydata_onsummary is True:
    print(Fore.YELLOW + Style.BRIGHT + "The weather that occurred yesterday: ")
    if yesterdaysummary_dayconddata is True:
        print(Fore.YELLOW + Style.BRIGHT + "The conditions during the day: " + Fore.CYAN + Style.BRIGHT + yesterdaysummary_dayconditions)
    if yesterdaysummary_nightconddata is True:
        print(Fore.YELLOW + Style.BRIGHT + "The conditions during the night: " + Fore.CYAN + Style.BRIGHT + yesterdaysummary_nightconditions)
    if yesterdaysummary_showHighTemp is True:
        print(Fore.YELLOW + Style.BRIGHT + "The high temperature: " + Fore.CYAN + Style.BRIGHT + yesterdaysummary_hightempf + "°F (" + yesterdaysummary_hightempc + "°C)")
    if yesterdaysummary_showLowTemp is True:
        print(Fore.YELLOW + Style.BRIGHT + "The low temperature: " + Fore.CYAN + Style.BRIGHT + yesterdaysummary_lowtempf + "°F (" + yesterdaysummary_lowtempc + "°C)")
    if yesterdaysummary_showWindSpeed is True:
        print(Fore.YELLOW + Style.BRIGHT + "The wind speed: " + Fore.CYAN + Style.BRIGHT + yesterdaysummary_windmph + " mph (" + yesterdaysummary_windkph + " kph)")
    if yesterdaysummary_showWindGust is True:
        print(Fore.YELLOW + Style.BRIGHT + "The wind gust: " + Fore.CYAN + Style.BRIGHT + yesterdaysummary_gustmph + " mph (" + yesterdaysummary_gustkph + " kph)")
    if yesterdaysummary_showHighTemp is True:
        print(Fore.YELLOW + Style.BRIGHT + "The humidity: " + Fore.CYAN + Style.BRIGHT + yesterdaysummary_avghumidity + "%")
    print("")

print(Fore.YELLOW + Style.BRIGHT + "The hourly forecast:")

for hour in hourly36_json['hourly_forecast']:
    hourly_time = hour['FCTTIME']['civil']
    hourly_tempf = hour['temp']['english']
    hourly_tempc = hour['temp']['metric']
    hourly_condition = hour['condition']
    print(Fore.YELLOW + Style.BRIGHT + hourly_time + ": " + Fore.CYAN + Style.BRIGHT + hourly_condition + " with a temperature of " + hourly_tempf + "°F (" + hourly_tempc + "°C)")
    summaryHourlyIterations = summaryHourlyIterations + 1
    if summaryHourlyIterations == 6:
        break
print("")
print(Fore.YELLOW + Style.BRIGHT + "For the next few days:")

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
    print(Fore.YELLOW + Style.BRIGHT + forecast10_weekday + ", " + forecast10_month + "/" + forecast10_day + ": " + Fore.CYAN + Style.BRIGHT +
          forecast10_conditions + " with a high of " + forecast10_highf + "°F (" +
          forecast10_highc + "°C), and a low of " + forecast10_lowf + "°F (" +
          forecast10_lowc + "°C).")
    summary_forecastIterations = summary_forecastIterations + 1
    if summary_forecastIterations == 5:
        break

if almanac_summary is True and almanac_data is True:
    print("")
    print(Fore.YELLOW + Style.BRIGHT + "The almanac:")
    print(Fore.YELLOW + Style.BRIGHT + "Data from: " + Fore.CYAN + Style.BRIGHT + almanac_airportCode
          + Fore.YELLOW + Style.BRIGHT + " (the nearest airport)")
    if almanac_recordHighdata is True:
        print(Fore.YELLOW + Style.BRIGHT + "Record high for today: " + Fore.CYAN + Style.BRIGHT + almanac_recordHighF
              + "°F (" + almanac_recordHighC + "°C)")
    else:
        print(Fore.YELLOW + Style.BRIGHT + "Record high data is not available for this location.")

    if almanac_recordHighYeardata is True:
        print(Fore.YELLOW + Style.BRIGHT + "It was set in: " + Fore.CYAN + Style.BRIGHT + almanac_recordHighYear)
    else:
        print(Fore.YELLOW + Style.BRIGHT + "Record high year data is not available for this location.")

    if almanac_recordLowdata is True:
        print(Fore.YELLOW + Style.BRIGHT + "Record low for today: " + Fore.CYAN + Style.BRIGHT + almanac_recordLowF
              + "°F (" + almanac_recordLowC + "°C)")
    else:
        print(Fore.YELLOW + Style.BRIGHT + "Record low data is not available for this location.")

    if almanac_recordLowYeardata is True:
        print(Fore.YELLOW + Style.BRIGHT + "It was set in: " + Fore.CYAN + Style.BRIGHT + almanac_recordLowYear)
    else:
        print(Fore.YELLOW + Style.BRIGHT + "Record low year data is not available for this location.")
elif almanac_summary is True and almanac_data is False:
    print("")
    print(Fore.YELLOW + Style.BRIGHT + "** Almanac data is not available for the location you entered. **")

if sundata_summary == True:
    print("")
    print(Fore.YELLOW + Style.BRIGHT + "The sunrise and sunset:")
    print(Fore.YELLOW + Style.BRIGHT + "Sunrise: " + Fore.CYAN + Style.BRIGHT + sunrise_time)
    print(Fore.YELLOW + Style.BRIGHT + "Sunset: " + Fore.CYAN + Style.BRIGHT + sunset_time)

if showTideOnSummary == True and tide_dataavailable == True:
    print("")
    print(Fore.YELLOW + Style.BRIGHT + "The tide for " + Fore.CYAN + Style.BRIGHT + tide_site + Fore.YELLOW + Style.BRIGHT + " (the closest site to you):")
    print("")
    print(Fore.YELLOW + Style.BRIGHT + "Low tide:")
    print(Fore.YELLOW + Style.BRIGHT + "Time: " + Fore.CYAN + Style.BRIGHT + tide_lowtidetime)
    print(Fore.YELLOW + Style.BRIGHT + "Height: " + Fore.CYAN + Style.BRIGHT + tide_lowtideheight)
    print("")
    print(Fore.YELLOW + Style.BRIGHT + "High tide:")
    print(Fore.YELLOW + Style.BRIGHT + "Time: " + Fore.CYAN + Style.BRIGHT + tide_hightidetime)
    print(Fore.YELLOW + Style.BRIGHT + "Height: " + Fore.CYAN + Style.BRIGHT + tide_hightideheight)
elif showTideOnSummary == True and tide_dataavailable == False:
    print("")
    print(Fore.YELLOW + Style.BRIGHT + "** Low/High tide data is not available for the location you entered. **" + Fore.RESET)

# In this part of PyWeather, you'll find comments indicating where things end/begin.
# This is to help when coding, and knowing where things are.

while True:
    print("")
    print(Fore.YELLOW + Style.BRIGHT + "What would you like to do now?")
    print(Fore.YELLOW + Style.BRIGHT + "- View detailed current data - Enter " + Fore.CYAN + Style.BRIGHT + "0")
    print(Fore.YELLOW + Style.BRIGHT + "- View detailed alerts data - Enter " + Fore.CYAN + Style.BRIGHT + "1")
    print(Fore.YELLOW + Style.BRIGHT + "- View detailed hourly data - Enter " + Fore.CYAN + Style.BRIGHT + "2")
    print(Fore.YELLOW + Style.BRIGHT + "- View the 10 day hourly forecast - Enter " + Fore.CYAN + Style.BRIGHT + "3")
    print(Fore.YELLOW + Style.BRIGHT + "- View the 10 day forecast - Enter " + Fore.CYAN + Style.BRIGHT + "4")
    print(Fore.YELLOW + Style.BRIGHT + "- View detailed hurricane data - Enter " + Fore.CYAN + Style.BRIGHT + "5")
    print(Fore.YELLOW + Style.BRIGHT + "- View detailed tide data - Enter " + Fore.CYAN + Style.BRIGHT + "6")
    print(Fore.YELLOW + Style.BRIGHT + "- View the almanac for today - Enter " + Fore.CYAN + Style.BRIGHT + "7")
    print(Fore.YELLOW + Style.BRIGHT + "- View historical weather data - Enter " + Fore.CYAN + Style.BRIGHT + "8")
    print(Fore.YELLOW + Style.BRIGHT + "- View yesterday's weather data - Enter " + Fore.CYAN + Style.BRIGHT + "9")
    print(Fore.YELLOW + Style.BRIGHT + "- View detailed sun/moon rise/set data - Enter " + Fore.CYAN + Style.BRIGHT + "10")
    print(Fore.YELLOW + Style.BRIGHT + "- Launch PyWeather's experimental radar - Enter " + Fore.CYAN + Style.BRIGHT + "11")
    print(Fore.YELLOW + Style.BRIGHT + "- Flag all data types to be refreshed - Enter " + Fore.CYAN + Style.BRIGHT + "12")
    print(Fore.YELLOW + Style.BRIGHT + "- Manage your favorite locations - Enter " + Fore.CYAN + Style.BRIGHT + "13")
    print(Fore.YELLOW + Style.BRIGHT + "- Manage your previous locations - Enter " + Fore.CYAN + Style.BRIGHT + "14")
    print(Fore.YELLOW + Style.BRIGHT + "- Check for PyWeather updates - Enter " + Fore.CYAN + Style.BRIGHT + "15")
    print(Fore.YELLOW + Style.BRIGHT + "- View the about page for PyWeather - Enter " + Fore.CYAN + Style.BRIGHT + "16")
    print(Fore.YELLOW + Style.BRIGHT + "- Close PyWeather - Enter " + Fore.CYAN + Style.BRIGHT + "17")
    if extratools_enabled is True:
        print(Fore.YELLOW + Style.BRIGHT + "- View cache timings - Enter " + Fore.CYAN + Style.BRIGHT + "extratools:1")
    moreoptions = input("Enter here: ").lower()
    logger.debug("moreoptions: %s" % moreoptions)
        
#<--- Menu is above | Current is below --->
    if moreoptions == "0":
        logger.info("Selected view more currently...")
        logger.debug("refresh_currentflagged: %s ; current cache time: %s" % 
                    (refresh_currentflagged, time.time() - cachetime_current))
        if (time.time() - cachetime_current >= cache_currenttime and cache_enabled == True
            or refresh_currentflagged == True):
            spinner.start("Refreshing current weather information...")
            try:
                summaryJSON = requests.get(currenturl)
                logger.debug("summaryJSON acquired, end result: %s" % summaryJSON)
                cachetime_current = time.time()
                refresh_currentflagged = False
                logger.debug("refresh_currentflagged: %s ; current cache time: %s" % 
                             (refresh_currentflagged, time.time() - cachetime_current))
            except:
                spinner.fail("Failed to refresh current information!")
                print("")
                print(Fore.YELLOW + Style.BRIGHT + "Whoops! PyWeather ran into an error when refetching current",
                      Fore.YELLOW + Style.BRIGHT + "weather. Make sure that you have an internet connection, and",
                      Fore.YELLOW + Style.BRIGHT + "if you're on a filtered network, api.wunderground.com is unblocked.",
                      Fore.YELLOW + Style.BRIGHT + "Press enter to exit to the main menu.", sep="\n")
                input()
                refresh_currentflagged = True
                logger.debug("refresh_currentflagged: %s" % refresh_currentflagged)
            current_json = json.loads(summaryJSON.text)
            if jsonVerbosity == True:
                logger.debug("current_json loaded with: %s" % current_json)
            spinner.stop()
        spinner.start("Loading current weather information...")
        # Parse extra stuff. Variable names are kept the same for the sake of sanity.
        # If the user hasn't refetched, this works out. Vars stay the same.
        summary_overall = current_json['current_observation']['weather']
        summary_lastupdated = current_json['current_observation']['observation_time']
        summary_tempf = str(current_json['current_observation']['temp_f'])
        summary_tempc = str(current_json['current_observation']['temp_c'])
        logger.debug("summary_overall: %s ; summary_lastupdated: %s"
                     % (summary_overall, summary_lastupdated))
        logger.debug("summary_tempf: %s ; summary_tempc: %s"
                     % (summary_tempf, summary_tempc))

        summary_humidity = str(current_json['current_observation']['relative_humidity'])
        logger.debug("summary_humidity: %s" % summary_humidity)
        # Check again for bad humidity data. The variable is already defined in any condition at the start
        # of PyWeather.
        if summary_humidity == "-999%":
            logger.info("summary_humidity is '-999%'.")
            currentcond_showHumidity = False
            logger.debug("currentcond_showHumidity: %s" % currentcond_showHumidity)

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
        current_precip1HrIn = float(current_json['current_observation']['precip_1hr_in'])
        if current_precip1HrIn == -999.00:
            current_precip1Hrdata = False
            current_precip1HrIn = str(current_precip1HrIn)
        else:
            current_precip1Hrdata = True
            current_precip1HrIn = str(current_precip1HrIn)
        logger.debug("current_precip1Hrdata: %s")
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
        # Check for bad visibility data
        current_showvisibilitydata = True
        logger.debug("current_showvisibilitydata: %s" % current_showvisibilitydata)
        if current_visibilityMi == "" or current_visibilityMi == "N/A":
            logger.info("current_visibilityMi is either '' or 'N/A'.")
            current_showvisibilitydata = False
            logger.debug("current_showvisibilitydata: %s" % current_showvisibilitydata)

        # Check for bad UV index data
        current_showuvindex = True
        logger.debug("current_showuvindex: %s" % current_showuvindex)
        if current_UVIndex == "-1" or current_UVIndex == "--":
            logger.info("current_UVindex is either '-1' or '--'.")
            current_showuvindex = False
            logger.debug("current_showuvindex: %s" % current_showuvindex)

        # Check for bad precip so far today data - "" for in and "--" for mm.
        current_showPrecipData = True
        logger.debug("current_showPrecipData: %s" % current_showPrecipData)
        if current_precipTodayIn == "" or current_precipTodayMm == "--":
            logger.info("current_precipTodayIn is '' or current_precipTodayMm is '--'.")
            current_showPrecipData = False
            logger.debug("current_showPrecipData: %s" % current_showPrecipData)

        spinner.stop()
        print("")
        print(Fore.YELLOW + Style.BRIGHT + "Here's the detailed current weather for: " + Fore.CYAN + Style.BRIGHT + str(location))
        print(Fore.YELLOW + Style.BRIGHT + summary_lastupdated)
        print("")
        print(Fore.YELLOW + Style.BRIGHT + "Current conditions: " + Fore.CYAN + Style.BRIGHT + summary_overall)
        print(Fore.YELLOW + Style.BRIGHT + "Current temperature: " + Fore.CYAN + Style.BRIGHT + summary_tempf + "°F (" + summary_tempc + "°C)")
        print(Fore.YELLOW + Style.BRIGHT + "And it feels like: " + Fore.CYAN + Style.BRIGHT + current_feelsLikeF
              + "°F (" + current_feelsLikeC + "°C)")
        print(Fore.YELLOW + Style.BRIGHT + "Current dew point: " + Fore.CYAN + Style.BRIGHT + summary_dewPointF
              + "°F (" + summary_dewPointC + "°C)")
        if winddata == True:
            if summary_winddir == "Variable":
                print(Fore.YELLOW + Style.BRIGHT + "Current wind: " + Fore.CYAN + Style.BRIGHT + summary_windmphstr +
                    " mph (" + summary_windkphstr + " kph), blowing in variable directions.")
            else:
                print(Fore.YELLOW + Style.BRIGHT + "Current wind: " + Fore.CYAN + Style.BRIGHT + summary_windmphstr +
                      " mph (" + summary_windkphstr + " kph), blowing " + summary_winddir
                      + " (" + current_windDegrees + " degrees)")
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Wind data is not available for this location.")
        if currentcond_showHumidity is True:
            print(Fore.YELLOW + Style.BRIGHT + "Current humidity: " + Fore.CYAN + Style.BRIGHT + summary_humidity)
        print(Fore.YELLOW + Style.BRIGHT + "Current pressure: " + Fore.CYAN + Style.BRIGHT + current_pressureInHg
              + " inHg (" + current_pressureMb + " mb), " + current_pressureTrend2)
        if current_showvisibilitydata is True:
            print(Fore.YELLOW + Style.BRIGHT + "Current visibility: " + Fore.CYAN + Style.BRIGHT + current_visibilityMi
                  + " miles (" + current_visibilityKm + " km)")
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Current visibility data is not available for this location.")

        if current_showuvindex is True:
            print(Fore.YELLOW + Style.BRIGHT + "UV Index: " + Fore.CYAN + Style.BRIGHT + current_UVIndex)
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Current UV index data is not available for this location.")

        if current_precip1Hrdata is True:
            print(Fore.YELLOW + Style.BRIGHT + "Precipitation in the last hour: " + Fore.CYAN + Style.BRIGHT
                  + current_precip1HrIn + " inches (" + current_precip1HrMm
                  + " mm)")
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Precipitation data in the last hour is not available.")

        if current_showPrecipData is True:
            print(Fore.YELLOW + Style.BRIGHT + "Precipitation so far today: " + Fore.CYAN + Style.BRIGHT
                  + current_precipTodayIn + " inches (" + current_precipTodayMm
                  + " mm)")
        continue

    elif moreoptions == "1":
        # Or condition will sort out 3 potential conditions.
        try:
            logger.debug("alertsPrefetched: %s ; alerts cache time: %s" %
                             (alertsPrefetched, time.time() - cachetime_alerts))
        except:
            logger.debug("alertsPrefetched: %s" % alertsPrefetched)

        if (alertsPrefetched is False or time.time() - cachetime_alerts >= cache_alertstime and cache_enabled == True
            or refresh_alertsflagged == True):
            spinner.start(text="Refreshing alerts info...")
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
                spinner.fail(text="Failed to refresh alerts information!")
                print("")
                print(Fore.YELLOW + Style.BRIGHT + "When attempting to fetch the alerts JSON file to parse,",
                      Fore.YELLOW + Style.BRIGHT + "PyWeather ran into an error. If you're on a network with a",
                      Fore.YELLOW + Style.BRIGHT + "filter, make sure that 'api.wunderground.com' is unblocked.",
                      Fore.YELLOW + Style.BRIGHT + "Otherwise, make sure you have an internet connection.", sep="\n")
                printException()
                alertsPrefetched = False
                refresh_alertsflagged = True
                logger.debug("alertsPrefetched: %s ; refresh_alertsflagged: %s" % 
                             (alertsPrefetched, refresh_alertsflagged))
                print(Fore.YELLOW + Style.BRIGHT + "Press enter to continue.")
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
            spinner.stop()
        # Because of the oddities of locations with no alerts, we're doing a mini
        # catch the error here. An error would occur when going into the conditional.
        spinner.start(text="Loading alerts data...")
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
            spinner.stop()
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
                spinner.stop()
                print(Fore.YELLOW + Style.BRIGHT + "-----")
                print(Fore.RED + Style.BRIGHT + "Alert %s/%s:" %
                      (alerts_completediterations, alerts_totaliterations))
                print(Fore.RED + Style.BRIGHT + "Alert Name: " + Fore.CYAN + Style.BRIGHT + alerts_alertname)
                print(Fore.RED + Style.BRIGHT + "Alert Level: " + Fore.CYAN + Style.BRIGHT + alerts_alertlevel)
                print(Fore.RED + Style.BRIGHT + "Alert issued at: " + Fore.CYAN + Style.BRIGHT + alerts_issuedtime)
                print(Fore.RED + Style.BRIGHT + "Alert expires at: " + Fore.CYAN + Style.BRIGHT + alerts_expiretime)
                print(Fore.RED + Style.BRIGHT + "Alert Description: " + Fore.CYAN + Style.BRIGHT + alerts_description
                      + Fore.RESET)
                alerts_tempiterations = alerts_tempiterations + 1
                if alerts_completediterations == alerts_totaliterations:
                    logger.debug("Completed iterations == total iterations. Breaking...")
                    break
                if alerts_tempiterations == user_alertsEUiterations:
                    print("")
                    try:
                        print(Fore.YELLOW + Style.BRIGHT + "Please press enter to view the next",
                              Fore.YELLOW + Style.BRIGHT + "%s alerts. To exit, press Control + C." % user_alertsEUiterations, sep="\n")
                        input()
                        alerts_tempiterations = 0
                    except KeyboardInterrupt:
                        logger.debug("User issued Keyboard Interrupt. Breaking...")
                        break
        elif alerts_type == "US":
            alerts_totaliterations = 0
            alerts_completediterations = 0
            alerts_tempiterations = 0
            spinner.stop()
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
                print(Fore.RED + Style.BRIGHT + "Alert %s/%s:" %
                      (alerts_completediterations, alerts_totaliterations))
                print(Fore.YELLOW + Style.BRIGHT + "-----")
                print(Fore.RED + Style.BRIGHT + "Alert Name: " + Fore.CYAN + Style.BRIGHT + alerts_alertname)
                print(Fore.RED + Style.BRIGHT + "Alert Type: " + Fore.CYAN + Style.BRIGHT + alerts_alerttype)
                print(Fore.RED + Style.BRIGHT + "Alert issued at: " + Fore.CYAN + Style.BRIGHT + alerts_issuedtime)
                print(Fore.RED + Style.BRIGHT + "Alert expires at: " + Fore.CYAN + Style.BRIGHT + alerts_expiretime)
                print(Fore.RED + Style.BRIGHT + "Alert Description: " + Fore.CYAN + Style.BRIGHT + alerts_description
                      + Fore.RESET)
                alerts_tempiterations = alerts_tempiterations + 1
                if alerts_completediterations == alerts_totaliterations:
                    logger.debug("Completed iterations equals total iterations. Breaking...")
                    break
                if alerts_tempiterations == user_alertsUSiterations:
                    try:
                        print(Fore.YELLOW + Style.BRIGHT + "Please press enter to view the next",
                              Fore.YELLOW + Style.BRIGHT + "%s alert(s). To exit, press Control + C." % user_alertsUSiterations, sep="\n")
                        input()
                        alerts_tempiterations = 0
                    except KeyboardInterrupt:
                        logger.debug("User issued KeyboardInterrupt. Breaking...")
                        break
        elif alerts_type == "None":
            spinner.fail(text="No alert data is available!")
            print("")
            print(Fore.RED + Style.BRIGHT + "No data available! Either there are no alerts",
                  Fore.RED + Style.BRIGHT + "at the location inputted, or Wunderground doesn't support alerts",
                  Fore.RED + Style.BRIGHT + "for the location inputted.",
                  Fore.RED + Style.BRIGHT + "As a quick note, Wunderground only supports alerts in the US/EU.", sep="\n")
        else:
            spinner.fail(text="No alert data is available!")
            print("")
            print(Fore.YELLOW + Style.BRIGHT + "Something went wrong when launching the correct conditional",
                  Fore.YELLOW + Style.BRIGHT + "for the alert data type involved.",
                  Fore.YELLOW + Style.BRIGHT + "For error reporting, this is what the variable 'alerts_type' is currently storing.",
                  Fore.YELLOW + Style.BRIGHT + "alerts_type: %s" % alerts_type, sep="\n" + Fore.RESET)

# <----- Alerts is above | 36-hour hourly is below ---->
    
    elif moreoptions == "2":
        logger.debug("refresh_hourly36flagged: %s ; hourly36 cache time: %s" %
                    (refresh_hourly36flagged, time.time() - cachetime_hourly36))
        logger.info("Selected view more hourly...")
        if (refresh_hourly36flagged == True or
                        time.time() - cachetime_hourly36 >= cache_threedayhourly and cache_enabled == True):
            spinner.start(text="Refreshing 36-hour hourly information...")
            try:
                hourly36JSON = requests.get(hourlyurl)
                logger.debug("hourly36JSON acquired, end result: %s" % hourly36JSON)
                cachetime_hourly36 = time.time()
            except:
                spinner.fail(text="Failed to refresh 36-hour hourly information!")
                print("")
                print(Fore.YELLOW + Style.BRIGHT + "Whoops! A problem occurred when trying to refresh 36 hour",
                      Fore.YELLOW + Style.BRIGHT + "hourly data. Make sure you have an internet connection, and if",
                      Fore.YELLOW + Style.BRIGHT + "you're on a network with a filter, make sure that api.wunderground.com",
                      Fore.YELLOW + Style.BRIGHT + "is unblocked.",
                      Fore.YELLOW + Style.BRIGHT + "Press enter to continue.", sep="\n")
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
            spinner.stop()
            
        spinner.start(text="Loading 36-hour hourly information...")
        detailedHourlyIterations = 0
        totaldetailedHourlyIterations = 0
        spinner.stop()
        print("")
        print(Fore.YELLOW + Style.BRIGHT + "Here's the detailed hourly forecast for: " + Fore.CYAN + Style.BRIGHT + str(location))
        for hour in hourly36_json['hourly_forecast']:
            print("")
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
            # If you have verbosity on, there's a chance that the next
            # hourly iteration will start BEFORE the previous iteration
            # prints out. This is normal, and no issues are caused by such.
            print(Fore.YELLOW + Style.BRIGHT + hourly_time + " on " + hourly_month + " " + hourly_day + ":")
            print(Fore.YELLOW + Style.BRIGHT + "Conditions: " + Fore.CYAN + Style.BRIGHT + hourly_condition)
            print(Fore.YELLOW + Style.BRIGHT + "Temperature: " + Fore.CYAN + Style.BRIGHT + hourly_tempf
                  + "°F (" + hourly_tempc + "°C)")
            print(Fore.YELLOW + Style.BRIGHT + "Feels like: " + Fore.CYAN + Style.BRIGHT + hourly_feelsLikeF
                  + "°F (" + hourly_feelsLikeC + "°C)")
            print(Fore.YELLOW + Style.BRIGHT + "Dew Point: " + Fore.CYAN + Style.BRIGHT + hourly_dewpointF
                  + "°F (" + hourly_dewpointC + "°C)")
            if hourly_windDir == "Variable":
                print(Fore.YELLOW + Style.BRIGHT + "Wind: " + Fore.CYAN + Style.BRIGHT + hourly_windMPH
                    + " mph (" + hourly_windKPH + " kph) blowing in " +
                    "variable directions.")
            else:
                print(Fore.YELLOW + Style.BRIGHT + "Wind: " + Fore.CYAN + Style.BRIGHT + hourly_windMPH
                      + " mph (" + hourly_windKPH + " kph) blowing to the " +
                      hourly_windDir + " (" + hourly_windDegrees + "°)")
            print(Fore.YELLOW + Style.BRIGHT + "Humidity: " + Fore.CYAN + Style.BRIGHT + hourly_humidity + "%")
            if hourly_snowData == False:
                print(Fore.YELLOW + Style.BRIGHT + "Rain for the hour: " + Fore.CYAN + Style.BRIGHT +
                      hourly_precipIn + " in (" + hourly_precipMm + " mm)")
            if hourly_snowData == True:
                print(Fore.YELLOW + Style.BRIGHT + "Snow for the hour: " + Fore.CYAN + Style.BRIGHT +
                      hourly_snowIn + " in (" + hourly_snowMm + " mm)")
            print(Fore.YELLOW + Style.BRIGHT + "Precipitation chance: " + Fore.CYAN + Style.BRIGHT +
                  hourly_precipChance + "%")
            print(Fore.YELLOW + Style.BRIGHT + "Barometric pressure: " + Fore.CYAN + Style.BRIGHT +
                  hourly_pressureInHg + " inHg (" + hourly_pressureMb
                  + " mb)")
            detailedHourlyIterations = detailedHourlyIterations + 1
            totaldetailedHourlyIterations = totaldetailedHourlyIterations + 1
            if user_showCompletedIterations == True:
                print(Fore.YELLOW + Style.BRIGHT + "Completed iterations: " + Fore.CYAN + Style.BRIGHT + "%s/36"
                      % totaldetailedHourlyIterations)
            if user_enterToContinue == True:
                if totaldetailedHourlyIterations == 36:
                    logger.debug("Total iterations is 36. Breaking...")
                    break
                if (detailedHourlyIterations == user_loopIterations):
                    logger.debug("detailedHourlyIterations: %s" % detailedHourlyIterations)
                    logger.debug("Asking user for continuation...")
                    try:
                        print("")
                        print(Fore.RED + Style.BRIGHT + "Please press enter to view the next %s hours of hourly data."
                              % user_loopIterations)
                        print(Fore.RED + Style.BRIGHT + "You can also press Control + C to head back to the input menu.")
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
#<-- 36 hour hourly is above | 10 day hourly is below --->
    elif moreoptions == "3":
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
            time.time() - cachetime_hourly10 >= cache_tendayhourly and cache_enabled == True):
            spinner.start(text="Refreshing ten-day hourly information...")
            try:
                tendayJSON = requests.get(tendayurl)
                logger.debug("Retrieved hourly 10 JSON with end result: %s" % tendayJSON)
                cachetime_hourly10 = time.time()
            except:
                spinner.fail(text="Failed to refresh ten-day hourly information!")
                print("")
                print(Fore.YELLOW + Style.BRIGHT + "When attempting to fetch the 10-day hourly forecast data, PyWeather ran",
                      Fore.YELLOW + Style.BRIGHT + "info an error. If you're on a network with a filter, make sure that",
                      Fore.YELLOW + Style.BRIGHT + "'api.wunderground.com' is unblocked. Otherwise, make sure that you have",
                      Fore.YELLOW + Style.BRIGHT + "an internet connection.", sep="\n")
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
            spinner.stop()
        # I get it, nothing gets loaded here. Just show the spinner anyways.
        spinner.start(text="Loading ten-day hourly information...")
        spinner.stop()
        print("")
        print(Fore.YELLOW + Style.BRIGHT + "Here's the detailed 10 day hourly forecast for: " + Fore.CYAN + Style.BRIGHT + str(location))
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
            print(Fore.YELLOW + Style.BRIGHT + hourly10_time + " on " + hourly10_month + " "
                  + hourly10_day + ":")
            print(Fore.YELLOW + Style.BRIGHT + "Conditions: " + Fore.CYAN + Style.BRIGHT
                  + hourly10_condition)
            print(Fore.YELLOW + Style.BRIGHT + "Temperature: " + Fore.CYAN + Style.BRIGHT + hourly10_tempf
                  + "°F (" + hourly10_tempc + "°C)")
            print(Fore.YELLOW + Style.BRIGHT + "Feels like: " + Fore.CYAN + Style.BRIGHT + hourly10_feelsLikeF
                  + "°F (" + hourly10_feelsLikeC + "°C)")
            print(Fore.YELLOW + Style.BRIGHT + "Dew Point: " + Fore.CYAN + Style.BRIGHT + hourly10_dewpointF
                  + "°F (" + hourly10_dewpointC + "°C)")
            if hourly10_windDir == "Variable":
                print(Fore.YELLOW + Style.BRIGHT + "Wind: " + Fore.CYAN + Style.BRIGHT + hourly10_windMPH
                    + " mph (" + hourly10_windKPH + " kph) blowing in " +
                    "variable directions.")
            else:
                print(Fore.YELLOW + Style.BRIGHT + "Wind: " + Fore.CYAN + Style.BRIGHT + hourly10_windMPH
                      + " mph (" + hourly10_windKPH + " kph) blowing to the " +
                      hourly10_windDir + " (" + hourly10_windDegrees + "°)")
            print(Fore.YELLOW + Style.BRIGHT + "Humidity: " + Fore.CYAN + Style.BRIGHT + hourly10_humidity + "%")
            if hourly10_snowData == False:
                print(Fore.YELLOW + Style.BRIGHT + "Rain for the hour: " + Fore.CYAN + Style.BRIGHT +
                      hourly10_precipIn + " in (" + hourly10_precipMm + " mm)")
            if hourly10_snowData == True:
                print(Fore.YELLOW + Style.BRIGHT + "Snow for the hour: " + Fore.CYAN + Style.BRIGHT +
                      hourly10_snowIn + " in (" + hourly10_snowMm + " mm)")
            print(Fore.YELLOW + Style.BRIGHT +"Precipitation chance: " + Fore.CYAN + Style.BRIGHT +
                  hourly10_precipChance + "%")
            print(Fore.YELLOW + Style.BRIGHT + "Barometric pressure: " + Fore.CYAN + Style.BRIGHT +
                  hourly10_pressureInHg + " inHg (" + hourly10_pressureMb
                  + " mb)")
            detailedHourly10Iterations = detailedHourly10Iterations + 1
            totaldetailedHourly10Iterations = totaldetailedHourly10Iterations + 1
            if user_showCompletedIterations == True:
                print(Fore.YELLOW + Style.BRIGHT + "Completed iterations: " + Fore.CYAN + Style.BRIGHT + "%s/240"
                      % totaldetailedHourly10Iterations)
            print("")
            if user_enterToContinue == True:
                if totaldetailedHourly10Iterations == 240:
                    logger.info("detailedHourly10Iterations is 240. Breaking...")
                    break
                if (detailedHourly10Iterations == user_loopIterations):
                    logger.debug("detailedHourly10Iterations: %s" % detailedHourly10Iterations)
                    logger.debug("Asking user for continuation...")
                    try:
                        print(Fore.RED + Style.BRIGHT + "Please press enter to view the next %s hours of hourly data."
                              % user_loopIterations)
                        print(Fore.RED + Style.BRIGHT + "You can also press Control + C to head back to the input menu.")
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
# <--- 10 day hourly is above | 10 day forecast is below --->
    elif moreoptions == "4":
        logger.info("Selected view more 10 day...")
        logger.debug("refresh_forecastflagged: %s ; forecast cache time: %s" %
                    (refresh_forecastflagged, time.time() - cachetime_forecast))
        if (refresh_forecastflagged == True 
            or time.time() - cachetime_forecast >= cache_forecasttime and cache_enabled == True):
            spinner.start(text="Refreshing forecast information...")
            try:
                forecast10JSON = requests.get(f10dayurl)
                cachetime_forecast = time.time()
                logger.debug("forecast10JSON acquired, end result: %s" % forecast10JSON)
            except:
                spinner.fail(text="Failed to refresh forecast data!")
                print("")
                print(Fore.YELLOW + Style.BRIGHT + "PyWeather ran into an error when trying to refetch forecast",
                      Fore.YELLOW + Style.BRIGHT + "data. If you're on a filtered network, make sure that",
                      Fore.YELLOW + Style.BRIGHT + "api.wunderground.com is unblocked. Otherwise, make sure you have",
                      Fore.YELLOW + Style.BRIGHT + "an internet connection.", sep="\n")
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
            spinner.stop()
        spinner.start(text="Loading forecast data...")
        detailedForecastIterations = 0
        totaldetailedForecastIterations = 0
        logger.debug("totaldetailedForecastIterations: %s" % totaldetailedForecastIterations)
        forecast10_precipDayData = True
        logger.debug("totaldetailedForecastIterations: %s ; forecast10_precipDayData: %s" %
                     (totaldetailedForecastIterations, forecast10_precipDayData))
        forecast10_snowDayData = True
        logger.debug("forecast10_snowDayData: %s" % forecast10_snowDayData)
        spinner.stop()
        print("")
        print(Fore.CYAN + Style.BRIGHT + "Here's the detailed 10 day forecast for: " + Fore.YELLOW + Style.BRIGHT + str(location))
        for day in forecast10_json['forecast']['simpleforecast']['forecastday']:
            print("")
            detailedForecastIterations = detailedForecastIterations + 1
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
            forecast10_conditions = day['conditions']
            logger.debug("forecast10_highc: %s ; forecast10_lowf: %s"
                        % (forecast10_highc, forecast10_lowf))
            logger.debug("forecast10_lowc: %s ; forecast10_conditions: %s"
                        % (forecast10_lowc, forecast10_conditions))
            forecast10_precipTotalIn = str(day['qpf_allday']['in'])
            forecast10_precipTotalMm = str(day['qpf_allday']['mm'])
            forecast10_precipDayIn = str(day['qpf_day']['in'])
            forecast10_precipDayMm = str(day['qpf_day']['mm'])
            logger.debug("forecast10_precipTotalIn: %s ; forecast10_precipTotalMm: %s"
                        % (forecast10_precipTotalIn, forecast10_precipTotalMm))
            logger.debug("forecast10_precipDayIn: %s ; forecast10_precipDayMm: %s"
                        % (forecast10_precipDayIn, forecast10_precipDayMm))
            forecast10_precipNightIn = str(day['qpf_night']['in'])
            forecast10_precipNightMm = str(day['qpf_night']['mm'])
            logger.debug("forecast10_precipNightIn: %s ; forecast10_precipNightMm: %s"
                        % (forecast10_precipNightIn, forecast10_precipNightMm))
            forecast10_snowTotalIn = str(day['snow_allday']['in'])
            forecast10_snowTotalCm = str(day['snow_allday']['cm'])
            logger.debug("forecast10_snowTotalIn: %s ; forecast10_snowTotalCm: %s"
                        % (forecast10_snowTotalIn, forecast10_snowTotalCm))
            forecast10_snowDayIn = str(day['snow_day']['in'])
            forecast10_snowDayCm = str(day['snow_day']['cm'])
            logger.debug("forecast10_snowDayIn: %s ; forecast10_snowDayCm: %s"
                         % (forecast10_snowDayIn, forecast10_snowDayCm))
            forecast10_snowNightIn = str(day['snow_night']['in'])
            forecast10_snowNightCm = str(day['snow_night']['cm'])
            # Set all display variables to true to begin with
            forecast10_showsnowdatatotal = True
            forecast10_showraindatatotal = True
            forecast10_showsnowdataday = True
            forecast10_showsnowdatanight = True
            forecast10_showraindataday = True
            forecast10_showraindatanight = True
            logger.debug("forecast10_showsnowdatatotal: %s ; forecast10_showraindatatotal: %s" %
                         (forecast10_showsnowdatatotal, forecast10_showraindatatotal))
            logger.debug("forecast10_showsnowdataday: %s ; forecast10_showsnowdatanight: %s" %
                         (forecast10_showsnowdataday, forecast10_showsnowdatanight))
            logger.debug("forecast10_showraindataday: %s ; forecast10_showraindatanight: %s" %
                         (forecast10_showraindataday, forecast10_showraindatanight))
            # Set the data available variables to true
            forecast10_snowtotalavail = True
            forecast10_raintotalavail = True
            forecast10_snowdayavail = True
            forecast10_snownightavail = True
            forecast10_raindayavail = True
            forecast10_rainnightavail = True
            logger.debug("forecast10_snowtotalavail: %s ; forecast10_raintotalavail: %s" %
                         (forecast10_snowtotalavail, forecast10_raintotalavail))
            logger.debug("forecast10_snowdayavail: %s ; forecast10_snownightavail: %s" %
                         (forecast10_snowdayavail, forecast10_snownightavail))
            logger.debug("forecast10_raindayavail: %s ; forecast10_rainnightavail: %s" %
                         (forecast10_raindayavail, forecast10_rainnightavail))
            # Begin checking for available data - Start with int conversions.
            # If a ValueError occurs, set the display variable to false.
            try:
                forecast10_snowtotalCheck = float(forecast10_snowTotalIn)
                logger.debug("forecast10_snowtotalCheck: %s" % forecast10_snowtotalCheck)
            except ValueError:
                logger.warning("Failed to convert total snow into float, not displaying...")
                printException_loggerwarn()
                forecast10_showsnowdatatotal = False
                forecast10_snowtotalavail = False
                logger.debug("forecast10_showsnowdatatotal: %s ; forecast10_snowtotalavail: %s" %
                             (forecast10_showsnowdatatotal, forecast10_snowtotalavail))

            try:
                forecast10_raintotalCheck = float(forecast10_precipTotalIn)
                logger.debug("forecast10_raintotalCheck: %s" % forecast10_raintotalCheck)
            except ValueError:
                logger.warning("Failed to convert total precip into float, not displaying...")
                printException_loggerwarn()
                forecast10_showraindatatotal = False
                forecast10_raintotalavail = False
                logger.debug("forecast10_showraindatatotal: %s ; forecast10_raintotalavail: %s" %
                             (forecast10_showraindatatotal, forecast10_raintotalavail))

            try:
                forecast10_snowdayCheck = float(forecast10_snowDayIn)
                logger.debug("forecast10_snowdayCheck: %s" % forecast10_snowdayCheck)
            except ValueError:
                logger.warning("Failed to convert day-only snow into float, not displaying...")
                printException_loggerwarn()
                forecast10_showsnowdataday = False
                forecast10_snowdayavail = False
                logger.debug("forecast10_showsnowdataday: %s ; forecast10_snowdayavail: %s" %
                             (forecast10_showsnowdataday, forecast10_snowdayavail))

            try:
                forecast10_snownightCheck = float(forecast10_snowNightIn)
                logger.debug("forecast10_snownightCheck: %s" % forecast10_snownightCheck)
            except ValueError:
                logger.warning("Failed to convert night-only snow into float, not displaying...")
                printException_loggerwarn()
                forecast10_showsnowdatanight = False
                forecast10_snownightavail = False
                logger.debug("forecast10_showsnowdatanight: %s ; forecast10_snownightavail: %s" %
                             (forecast10_showsnowdatanight, forecast10_snownightavail))


            try:
                forecast10_raindayCheck = float(forecast10_precipDayIn)
                logger.debug("forecast10_raindayCheck: %s" % forecast10_raindayCheck)
            except ValueError:
                logger.warning("Failed to convert day-only rain into float, not displaying...")
                printException_loggerwarn()
                forecast10_showraindataday = False
                forecast10_raindayavail = False
                logger.debug("forecast10_showraindataday: %s ; forecast10_raindayavail: %s" %
                             (forecast10_showraindataday, forecast10_raindayavail))


            try:
                forecast10_rainnightCheck = float(forecast10_precipNightIn)
                logger.debug("forecast10_rainnightCheck: %s" % forecast10_rainnightCheck)
            except ValueError:
                logger.warning("Failed to convert night-only rain into float, not displaying...")
                printException_loggerwarn()
                forecast10_showraindatanight = False
                forecast10_rainnightavail = False
                logger.debug("forecast10_showraindatanight: %s ; forecast10_rainnightavail: %s" %
                             (forecast10_showraindatanight, forecast10_rainnightavail))


            # Determine if we'll show total precip amounts

            # If snow total amount is above 0.01, show it regardless of temp
            if forecast10_snowtotalavail is True:
                if forecast10_snowtotalCheck >= 0.01:
                    logger.info("forecast10_snowtotalCheck is >= 0.01.")

            # Have a completely separate block of code for calculating displaying snow data
            if forecast10_snowtotalavail is True:
                if forecast10_snowtotalCheck == 0.00:
                    logger.info("forecast10_snowtotalCheck is 0.00")
                    if forecast10_highfcheck > 32 and forecast10_lowfcheck > 32:
                        forecast10_showsnowdatatotal = False
                    else:
                        # Every other possible combination will lead to showing snow data to be true.
                        # Put the else here as a way to keep things compact.
                        forecast10_showsnowdatatotal = True
                    logger.debug("forecast10_showsnowdatatotal: %s" % forecast10_showsnowdatatotal)

            if forecast10_raintotalavail is True:
                if forecast10_raintotalCheck >= 0.01:
                    logger.info("forecast10_raintotalCheck is >= 0.01.")

            if forecast10_raintotalavail is True:
                if forecast10_raintotalCheck == 0.00:
                    logger.info("forecast10_raintotalCheck is 0.00")
                    if forecast10_highfcheck <= 32 and forecast10_lowfcheck <= 32:
                        forecast10_showraindatatotal = False
                    else:
                        forecast10_showraindatatotal = True
                    logger.debug("forecast10_showraindatatotal: %s" % forecast10_showraindatatotal)

            if forecast10_snowdayavail is True:
                if forecast10_snowdayCheck >= 0.01:
                    logger.info("forecast10_snowdayCheck is >= 0.01.")

            if forecast10_snowdayavail is True:
                if forecast10_snowdayCheck == 0.00:
                    logger.info("forecast10_snowdayCheck is 0.00")
                    if forecast10_highfcheck >= 32:
                        forecast10_showsnowdataday = False
                    else:
                        forecast10_showsnowdataday = True
                    logger.debug("forecast10_showsnowdataday: %s" % forecast10_showsnowdataday)

            if forecast10_snownightavail is True:
                if forecast10_snownightCheck >= 0.01:
                    logger.info("forecast10_snownightCheck is >= 0.01.")
                    forecast10_showsnowdatanight = True

            if forecast10_snownightavail is True:
                if forecast10_snownightCheck == 0.00:
                    logger.info("forecast10_snownightCheck is 0.00")
                    if forecast10_lowfcheck >= 32:
                        forecast10_showsnowdatanight = False
                    else:
                        forecast10_showsnowdatanight = True
                    logger.debug("forecast10_showsnowdatanight: %s" % forecast10_showsnowdatanight)

            if forecast10_raindayavail is True:
                if forecast10_raindayCheck >= 0.01:
                    logger.info("forecast10_raindayCheck is >= 0.01")

            if forecast10_raindayavail is True:
                if forecast10_raindayCheck == 0.00:
                    logger.info("forecast10_raindayCheck is 0.00")
                    if forecast10_highfcheck < 32:
                        forecast10_showraindataday = False
                    else:
                        forecast10_showraindataday = True
                    logger.debug("forecast10_showraindataday: %s" % forecast10_showraindataday)

            if forecast10_rainnightavail is True:
                if forecast10_rainnightCheck >= 0.01:
                    logger.info("forecast10_rainnightCheck is >= 0.01")

            if forecast10_rainnightavail is True:
                if forecast10_rainnightCheck == 0.00:
                    logger.info("forecast10_rainnightCheck is 0.00")
                    if forecast10_lowfcheck < 32:
                        forecast10_showraindatanight = False
                    else:
                        forecast10_showraindatanight = True
                    logger.debug("forecast10_showraindatanight: %s" % forecast10_showraindatanight)


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
            forecast10_precipChance = str(day['pop'])
            logger.debug("forecast10_precipChance: %s" % forecast10_precipChance)
            logger.info("Printing weather data...")
            print(Fore.YELLOW + Style.BRIGHT + forecast10_weekday + ", " + forecast10_month + "/" + forecast10_day + ":")
            print(Fore.CYAN + Style.BRIGHT + forecast10_conditions + Fore.YELLOW + Style.BRIGHT + " with a high of "
                  + Fore.CYAN + Style.BRIGHT + forecast10_highf + "°F (" + forecast10_highc + "°C)" +
                  Fore.YELLOW + Style.BRIGHT + " and a low of " + Fore.CYAN + Style.BRIGHT + forecast10_lowf + "°F (" +
                  forecast10_lowc + "°C)" + ".")
            print(Fore.YELLOW + Style.BRIGHT + "Precipitation chance: " + Fore.CYAN + Style.BRIGHT + forecast10_precipChance + "%")
            if forecast10_showsnowdatatotal is True:
                print(Fore.YELLOW + Style.BRIGHT + "Snow in total: " + Fore.CYAN + Style.BRIGHT + forecast10_snowTotalIn
                      + " in (" + forecast10_snowTotalCm + " cm)")
            elif forecast10_snowtotalavail is False:
                print(Fore.YELLOW + Style.BRIGHT + "Total snow precipitation data is not available for this date.")

            if forecast10_showraindatatotal is True:
                print(Fore.YELLOW + Style.BRIGHT + "Rain in total: " + Fore.CYAN + Style.BRIGHT +  forecast10_precipTotalIn
                      + " in (" + forecast10_precipTotalMm + " mm)")
            elif forecast10_raintotalavail is False:
                print(Fore.YELLOW + Style.BRIGHT + "Total rain precipitation data is not available for this date.")
                
            if forecast10_showraindataday is True:
                print(Fore.YELLOW + Style.BRIGHT + "Rain for the day: " + Fore.CYAN + Style.BRIGHT + forecast10_precipDayIn
                      + " in (" + forecast10_precipDayMm + " mm)")
            elif forecast10_raindayavail is False:
                print(Fore.YELLOW + Style.BRIGHT + "Rain precipitation data during the day is not available for this date.")

            if forecast10_showsnowdataday is True:
                print(Fore.YELLOW + Style.BRIGHT + "Snow for the day: " + Fore.CYAN + Style.BRIGHT + forecast10_snowDayIn
                      + " in (" + forecast10_snowDayCm + " cm)")
            elif forecast10_snowdayavail is False:
                print(Fore.YELLOW + Style.BRIGHT + "Snow precipitation data during the day is not available for this date.")
            
            if forecast10_showraindatanight is True:
                print(Fore.YELLOW + Style.BRIGHT + "Rain for the night: " + Fore.CYAN + Style.BRIGHT + forecast10_precipNightIn
                      + " in (" + forecast10_precipNightMm + " mm)")
            elif forecast10_rainnightavail is False:
                print(Fore.YELLOW + Style.BRIGHT + "Rain precipitation data during the night is not available for this date.")

            if forecast10_showsnowdatanight is True:
                print(Fore.YELLOW + Style.BRIGHT + "Snow for the night: " + Fore.CYAN + Style.BRIGHT + forecast10_snowNightIn
                      + " in (" + forecast10_snowNightCm + " cm)")
            elif forecast10_snownightavail is False:
                print(Fore.YELLOW + Style.BRIGHT + "Snow precipitation data during the night is not available for this date.")

            if forecast10_avgWindDir == "Variable":
                print(Fore.YELLOW + Style.BRIGHT + "Winds: " + Fore.CYAN + Style.BRIGHT +
                    forecast10_avgWindMPH + " mph (" + forecast10_avgWindKPH
                    + " kph), gusting to " + forecast10_maxWindMPH + " mph ("
                    + forecast10_maxWindKPH + " kph), "
                    + "and blowing in variable directions.")
            else:
                print(Fore.YELLOW + Style.BRIGHT + "Winds: " + Fore.CYAN + Style.BRIGHT +
                      forecast10_avgWindMPH + " mph (" + forecast10_avgWindKPH
                      + " kph), gusting to " + forecast10_maxWindMPH + " mph ("
                      + forecast10_maxWindKPH + " kph), "
                      + "and blowing " + forecast10_avgWindDir +
                      " (" + forecast10_avgWindDegrees + "°)")
            print(Fore.YELLOW + Style.BRIGHT + "Humidity: " + Fore.CYAN + Style.BRIGHT +
                  forecast10_avgHumidity + "%")
            totaldetailedForecastIterations = totaldetailedForecastIterations + 1
            logger.debug("totaldetailedForecastIterations: %s" % totaldetailedForecastIterations)
            if user_showCompletedIterations == True:
                print(Fore.YELLOW + Style.BRIGHT + "Completed iterations: " + Fore.CYAN + Style.BRIGHT + "%s/10"
                      % totaldetailedForecastIterations)
            if totaldetailedForecastIterations == 10:
                logger.debug("Total iterations is 10. Breaking...")
                break
            if user_enterToContinue == True:
                if detailedForecastIterations == user_forecastLoopIterations:
                    logger.debug("detailedForecastIterations: %s" % detailedForecastIterations)
                    try:
                        print("")
                        print(Fore.RED + Style.BRIGHT + "Press enter to view the next %s days of weather data."
                              % user_forecastLoopIterations)
                        print(Fore.RED + Style.BRIGHT +"You can also press Control + C to return to the input menu.")
                        input()
                        logger.info("Iterating %s more times..." 
                                    % user_forecastLoopIterations)
                        detailedForecastIterations = 0
                    except KeyboardInterrupt:
                        break
                        logger.info("Exiting to the main menu.")

#<-- 10 day hourly is above | radar is below --->

    elif moreoptions == "11":
        if radar_bypassconfirmation == False:
            print(Fore.RED + Style.BRIGHT + "The radar feature is experimental, and may not work properly.",
                  Fore.RED + Style.BRIGHT + "PyWeather may crash when in this feature, and other unexpected",
                  Fore.RED + Style.BRIGHT + "behavior may occur. Despite the radar feature being experimental,",
                  Fore.RED + Style.BRIGHT + "would you like to use the radar?" + Fore.RESET, sep="\n")
            radar_confirmedusage = input("Input here: ").lower()
            if radar_confirmedusage == "yes":
                print("", "The radar is now launching.",
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

        spinner.start(text="Loading radar GUI...")
        try:
            os.mkdir("temp")
        except:
            printException_loggerwarn()

        radar_clearImages()
        try:
            from appJar import gui
            frontend = gui()
        except ImportError:
            spinner.fail(text="Failed to load radar GUI, an import error occurred!")
            print("")
            print(Fore.RED + Style.BRIGHT + "Cannot launch a GUI on this platform, as an import error occurred. If you don't have",
                  Fore.RED + Style.BRIGHT + "a GUI on Linux, this is expected. Otherwise, investigate into why",
                  Fore.RED + Style.BRIGHT + "tkinter won't launch.", sep="\n" + Fore.RESET)
            printException_loggerwarn()
            continue
        except:
            spinner.fail(text="Failed to load radar GUI!")
            print("")
            print(Fore.RED + Style.BRIGHT + "Cannot launch the GUI. This is probably occurring as a result of being in a terminal,",
                  Fore.RED + Style.BRIGHT + "and not having a display for the GUI to initialize on. If this is not the case, and you have a GUI,",
                  Fore.RED + Style.BRIGHT + "turn on tracebacks in the configuration file, and report the traceback on GitHub if the issue persists.",
                  Fore.RED + Style.BRIGHT + "Press enter to continue.")
            printException()
            input()
            continue

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
        

                
        def frontend_zoomswitch(btnName):
            # Globalize cache variables
            global r10cached; global r20cached; global r40cached
            global r60cached; global r80cached; global r100cached
            global radar_zoomlevel
            logger.debug("btnName: %s" % btnName)
            # If button name equals a zoom level enter this code
            if btnName == "10 km":
                logger.debug("r10cached: %s" % r10cached)
                if r10cached == False:
                    # If the radar image isn't cached fetch the image.
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
                    # If it is cached load the image. If it's not cached show the image failed to load.
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
                global r10cached
                global r20cached
                global r40cached
                global r60cached
                global r80cached
                global r100cached
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
        frontend.setTitle("PyWeather Radar Viewer")
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
        spinner.stop()
        frontend.go()
#<--- Radar is above | Exit PyWeather is below --->

    elif moreoptions == "17": # Changed
        sys.exit()

#<--- Exit PyWeather is above | Updater is below --->
    elif moreoptions == "15":  # Changed
        logger.info("Selected update.")
        logger.debug("buildnumber: %s ; buildversion: %s" %
                    (buildnumber, buildversion))
        spinner.start(text="Checking for updates...")
        try:
            versioncheck = requests.get("https://raw.githubusercontent.com/o355/pyweather/master/updater/versioncheck.json")
            releasenotes = requests.get("https://raw.githubusercontent.com/o355/pyweather/master/updater/releasenotes.txt")
            logger.debug("versioncheck: %s" % versioncheck)
        except:
            spinner.fail(text="Failed to check for updates!")
            print("")
            logger.warning("Couldn't check for updates! Is there an internet connection?")
            print(Fore.YELLOW + Style.BRIGHT + "When attempting to fetch the update data file, PyWeather",
                  Fore.YELLOW + Style.BRIGHT + "ran into an error. If you're on a network with a filter,",
                  Fore.YELLOW + Style.BRIGHT + "make sure that 'raw.githubusercontent.com' is unblocked. Otherwise,",
                  Fore.YELLOW + Style.BRIGHT + "make sure that you have an internet connecction.", sep="\n")
            printException()
            continue
        versionJSON = json.loads(versioncheck.text)
        if jsonVerbosity == True:
            logger.debug("versionJSON: %s" % versionJSON)
        else:
            logger.debug("versionJSON loaded.")
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
        spinner.stop()
        if buildnumber >= version_buildNumber:
            logger.info("PyWeather is up to date.")
            logger.info("local build (%s) >= latest build (%s)"
                        % (buildnumber, version_buildNumber))
            print("")
            print(Fore.GREEN + Style.BRIGHT + "Your PyWeather is up to date! :)")
            print(Fore.GREEN + Style.BRIGHT + "You have version: " + Fore.CYAN + Style.BRIGHT + buildversion)
            print(Fore.GREEN + Style.BRIGHT +"The latest version is: " + Fore.CYAN + Style.BRIGHT
                  + version_latestVersion)
            if user_showUpdaterReleaseTag == True:
                print(Fore.GREEN + Style.BRIGHT + "The latest release tag is: " + Fore.CYAN + Style.BRIGHT
                      + version_latestReleaseTag)
            if showNewVersionReleaseDate == True:
                print(Fore.GREEN + Style.BRIGHT + "Psst, a new version of PyWeather should get released on: "
                      + Fore.CYAN + Style.BRIGHT + version_newversionreleasedate)
            if showUpdaterReleaseNotes_uptodate == True:
                print(Fore.GREEN + Style.BRIGHT + "Here's the release notes for this release:",
                      Fore.CYAN + Style.BRIGHT + releasenotes.text, sep="\n")
        elif buildnumber < version_buildNumber:
            print("")
            logger.warn("PyWeather is NOT up to date.")
            logger.warn("local build (%s) < latest build (%s)"
                        % (buildnumber, version_buildNumber))
            print(Fore.RED + Style.BRIGHT + "Your PyWeather is not up to date! :(")
            print(Fore.RED + Style.BRIGHT + "You have version: " + Fore.CYAN + Style.BRIGHT + buildversion)
            print(Fore.RED + Style.BRIGHT + "The latest version is: " + Fore.CYAN + Style.BRIGHT + version_latestVersion)
            print(Fore.RED + Style.BRIGHT + "And it was released on: " + Fore.CYAN + Style.BRIGHT + version_latestReleaseDate)
            if user_showUpdaterReleaseTag == True:
                print(Fore.RED + Style.BRIGHT + "The latest release tag is: " + Fore.CYAN + Style.BRIGHT + version_latestReleaseTag)
            if showUpdaterReleaseNotes == True:
                print(Fore.RED + Style.BRIGHT + "Here's the release notes for the latest release:",
                      Fore.CYAN + Style.BRIGHT + releasenotes.text, sep="\n")
            print("")
            print(Fore.RED + Style.BRIGHT + "Would you like to download the latest version?")
            downloadLatest = input("Yes or No: ").lower()
            logger.debug("downloadLatest: %s" % downloadLatest)
            if downloadLatest == "yes":
                # Remove the Git updater - It is no longer needed.
                #if allowGitForUpdating == True:
                #    print(Fore.YELLOW + Style.BRIGHT + "Would you like to use Git to update PyWeather?",
                #          Fore.YELLOW + Style.BRIGHT + "Yes or No.")
                #    confirmUpdateWithGit = input("Input here: ").lower()
                #    if confirmUpdateWithGit == "yes":
                #        print(Fore.YELLOW + Style.BRIGHT + "Now updating with Git.")
                #        try:
                #            subprocess.call(["git fetch"], shell=True)
                #            subprocess.call(["git stash"], shell=True)
                #            subprocess.call(["git checkout %s" % version_latestReleaseTag],
                #                            shell=True)
                #            print(Fore.YELLOW + Style.BRIGHT + "Now updating your config file.")
                #            exec(open("configupdate.py").read())
                #            print(Fore.YELLOW + Style.BRIGHT + "PyWeather has been successfully updated. To finish updating,",
                #                  Fore.YELLOW + Style.BRIGHT + "please press enter to exit PyWeather.", sep="\n")
                #            input()
                #            sys.exit()
                #        except:
                #            print("When attempting to update using git, either",
                #                  "when doing `git fetch`, `git checkout`, or to",
                #                  "execute the configupdate script, an error occurred."
                #                  "We can try updating using the .zip method.",
                #                  "Would you like to update PyWeather using the .zip method?",
                #                  "Yes or No.", sep="\n")
                #            printException()
                #            confirmZipDownload = input("Input here: ").lower()
                #            if confirmZipDownload == "yes":
                #                print("Downloading using the .zip method.")
                #            elif confirmZipDownload == "no":
                #               print("Not downloading latest updates using the",
                #                     ".zip method.", sep="\n")
                #                continue
                #            else:
                #                print("Couldn't understand your input. Defaulting",
                #                      "to downloading using a .zip.", sep="\n")
                #    # The unnecessary amounts of confirms was to boost the line count to 2,000.
                #    elif confirmUpdateWithGit == "no":
                #        print("Not updating with Git. Would you like to update",
                #              "PyWeather using the .zip download option?",
                #              "Yes or No.", sep="\n")
                #        confirmZipDownload = input("Input here: ").lower()
                #        if confirmZipDownload == "yes":
                #            print("Downloading the latest update with a .zip.")
                #        elif confirmZipDownload == "no":
                #            print("Not downloading the latest PyWeather updates.")
                #            continue
                #        else:
                #            print("Couldn't understand your input. Defaulting to",
                #                  "downloading the latest version with a .zip.", sep="\n")
                #    else:
                #        print("Couldn't understand your input. Defaulting to",
                #              "downloading the latest version with a .zip.", sep="\n")
                print("")
                logger.debug("Downloading latest version...")
                # This will eventually get replaced with a real progress bar with size indicating and all that cool stuff.
                spinner.start(text="Downloading the latest version of PyWeather...")
                try:
                    updatezip = requests.get(version_latestURL)
                    with open(version_latestFileName, 'wb') as fw:
                        for chunk in updatezip.iter_content(chunk_size=128):
                            fw.write(chunk)
                        fw.close()
                except:
                    spinner.fail("Failed to download the latest version of PyWeather!")
                    print("")
                    logger.warning("Couldn't download the latest version!")
                    logger.warning("Is the internet online?")
                    print(Fore.RED + Style.BRIGHT + "When attempting to download the latest .zip file",
                          Fore.RED + Style.BRIGHT + "for PyWeather, an error occurred. If you're on a",
                          Fore.RED + Style.BRIGHT + "network with a filter, make sure that",
                          Fore.RED + Style.BRIGHT + "'raw.githubusercontent.com' is unblocked.",
                          Fore.RED + Style.BRIGHT + "Otherwise, make sure you have an internet connection.",
                          sep="\n")
                    logger.error("Here's the full traceback (for bug reports):")
                    printException()
                    continue
                logger.debug("Latest version was saved, filename: %s"
                            % version_latestFileName)
                spinner.stop()
                print(Fore.YELLOW + Style.BRIGHT + "The latest version of PyWeather was downloaded " +
                      "to the base directory of PyWeather, and saved as " +
                      Fore.CYAN + Style.BRIGHT + version_latestFileName + Fore.YELLOW + ".")
                continue
            elif downloadLatest == "no":
                logger.debug("Not downloading the latest version.")
                print(Fore.YELLOW + Style.BRIGHT + "Not downloading the latest version of PyWeather.")
                print(Fore.YELLOW + Style.BRIGHT + "For reference, you can download the latest version of PyWeather at:")
                print(Fore.CYAN + Style.BRIGHT + version_latestURL)
                continue
            else:
                logger.warn("Input could not be understood!")
                print(Fore.RED + Style.BRIGHT + "Your input couldn't be understood.")
                continue
        else:
            spinner.fail("Failed to check for updates!")
            print("")
            logger.warning("PW updater failed. Variables corrupt, maybe?")
            print(Fore.YELLOW + Style.BRIGHT + "When attempting to compare version variables, PyWeather ran",
                  Fore.YELLOW + Style.BRIGHT + "into an error. This error is extremely rare. Make sure you're",
                  Fore.YELLOW + Style.BRIGHT + "not trying to travel through a wormhole with Cooper, and report",
                  Fore.YELLOW + Style.BRIGHT + "the error on GitHub, while it's around. Make sure to turn on verbosity and report",
                  Fore.YELLOW + Style.BRIGHT + "variable data after selecting the updater option.", sep='\n')
            input()
            continue
# <--- Updater is above | Almanac is below --->
    elif moreoptions == "7":
        logger.info("Selected option: almanac")
        try:
            logger.debug("almanac_prefetched: %s ; almanac cache time: %s" %
                         (almanac_prefetched, time.time() - cachetime_almanac))
        except:
            logger.debug("almanac_prefetched: %s" % almanac_prefetched)
            
        logger.debug("refresh_almanacflagged: %s" % refresh_almanacflagged)
        if (almanac_prefetched == False or time.time() - cachetime_almanac >= cache_almanactime
            or refresh_almanacflagged == True):
            spinner.start(text="Refreshing almanac data...")
            try:
                almanacJSON = requests.get(almanacurl)
                logger.debug("almanacJSON fetched with end result: %s" % almanacJSON)
                cachetime_almanac = time.time()
            except:
                spinner.fail(text="Failed to load almanac data!")
                print("")
                logger.warn("Couldn't contact Wunderground's API! Is the internet offline?")
                print(Fore.RED + Style.BRIGHT + "When fetching the almanac data from Wunderground, PyWeather ran into",
                      Fore.RED + Style.BRIGHT + "an error. If you're on a network with a filter, make sure that",
                      Fore.RED + Style.BRIGHT + "'api.wunderground.com' is unblocked. Otherwise, make sure you have",
                      Fore.RED + Style.BRIGHT + "an internet connection, and that Wunderground's HAL9000 is online.")
                printException()
                print(Fore.RED + Style.BRIGHT + "Press enter to continue.")
                input()
                continue
            
            almanac_prefetched = True
            refresh_almanacflagged = False
            logger.debug("almanac_prefetched: %s ; refresh_almanacflagged: %s" %
                         (almanac_prefetched, refresh_almanacflagged))
            almanac_data = True
            logger.debug("almanac_data: %s" % almanac_data)
            almanac_json = json.loads(almanacJSON.text)
            if jsonVerbosity == True:
                logger.debug("almanac_json: %s" % almanac_json)
            else:
                logger.debug("1 JSON loaded successfully.")
            
            almanac_airportCode = almanac_json['almanac']['airport_code']
            if almanac_airportCode == "":
                almanac_data = False
                logger.debug("almanac_data: %s" % almanac_data)


            logger.debug("almanac_airportCode: %s" % almanac_airportCode)
            try:
                almanac_normalHighF = str(almanac_json['almanac']['temp_high']['normal']['F'])
                almanac_normalHighC = str(almanac_json['almanac']['temp_high']['normal']['C'])
                logger.debug("almanac_normalHighF: %s ; almanac_normalHighC: %s" %
                             (almanac_normalHighF, almanac_normalHighC))
                if almanac_normalHighF == "":
                    almanac_normalHighdata = False
                else:
                    almanac_normalHighdata = True
            except:
                almanac_normalHighdata = False
            logger.debug("almanac_normalHighdata: %s" % almanac_normalHighdata)
            try:
                almanac_recordHighF = str(almanac_json['almanac']['temp_high']['record']['F'])
                almanac_recordHighC = str(almanac_json['almanac']['temp_high']['record']['C'])
                logger.debug("almanac_recordHighF: %s ; almanac_recordHighC: %s" %
                             (almanac_recordHighF, almanac_recordHighC))
                almanac_recordHighdata = True
            except:
                printException_loggerwarn()
                almanac_recordHighdata = False
            logger.debug("almanac_recordHighdata: %s" % almanac_recordHighdata)
            try:
                almanac_recordHighYear = str(almanac_json['almanac']['temp_high']['recordyear'])
                logger.debug("almanac_recordHighYear: %s" % almanac_recordHighYear)
                almanac_recordHighYeardata = True
            except:
                almanac_recordHighYeardata = False
            logger.debug("almanac_recordHighYeardata: %s" % almanac_recordHighYeardata)
            try:
                almanac_normalLowF = str(almanac_json['almanac']['temp_low']['normal']['F'])
                almanac_normalLowC = str(almanac_json['almanac']['temp_low']['normal']['C'])
                logger.debug("almanac_normalLowF: %s ; almanac_normalLowC: %s" %
                             (almanac_normalLowF, almanac_normalLowC))
                if almanac_normalLowF == "":
                    almanac_normalLowdata = False
                else:
                    almanac_normalLowdata = True
            except:
                almanac_normalLowdata = False
            logger.debug("almanac_normalLowData: %s" % almanac_normalLowdata)
            try:
                almanac_recordLowF = str(almanac_json['almanac']['temp_low']['record']['F'])
                almanac_recordLowC = str(almanac_json['almanac']['temp_low']['record']['C'])
                logger.debug("almanac_recordLowF: %s ; almanac_recordLowC: %s" %
                             (almanac_recordLowF, almanac_recordLowC))
                almanac_recordLowdata = True
            except:
                almanac_recordLowdata = False
            logger.debug("almanac_recordLowdata: %s" % almanac_recordLowdata)
            try:
                almanac_recordLowYear = str(almanac_json['almanac']['temp_low']['recordyear'])
                logger.debug("almanac_recordLowYear: %s" % almanac_recordLowYear)
                almanac_recordLowYeardata = True
            except:
                almanac_recordLowYeardata = False
            logger.debug("almanac_recordLowYeardata: %s" % almanac_recordLowYeardata)
        spinner.start(text="Loading the almanac...")
        # If the airport code was "" (no data), exit almanac data.
        if almanac_data is False:
            spinner.fail(text="Almanac data is not available for this location.")
            continue

        spinner.stop()
        print(Fore.YELLOW + Style.BRIGHT + "Here's the almanac for: " + Fore.CYAN + Style.BRIGHT +
              almanac_airportCode + Fore.YELLOW + " (the nearest airport)")
        print("")
        if almanac_recordHighdata is True:
            print(Fore.YELLOW + Style.BRIGHT + "Record High: " + Fore.CYAN + Style.BRIGHT + almanac_recordHighF + "°F ("
                  + almanac_recordHighC + "°C)")
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Record high data is not available.")

        if almanac_recordHighYeardata is True:
            print(Fore.YELLOW + Style.BRIGHT + "With the record being set in: " + Fore.CYAN + Style.BRIGHT
                  + almanac_recordHighYear)
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Record high year data is not available.")

        if almanac_normalHighdata is True:
            print(Fore.YELLOW + Style.BRIGHT + "Normal High: " + Fore.CYAN + Style.BRIGHT + almanac_normalHighF
                  + "°F (" + almanac_normalHighC + "°C)")
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Normal high data is not available.")

        print("")

        if almanac_recordLowdata is True:
            print(Fore.YELLOW + Style.BRIGHT + "Record Low: " + Fore.CYAN + Style.BRIGHT + almanac_recordLowF + "°F ("
                  + almanac_recordLowC + "°C)")
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Record low data is not available.")

        if almanac_recordLowYeardata is True:
            print(Fore.YELLOW + Style.BRIGHT + "With the record being set in: " + Fore.CYAN + Style.BRIGHT
                  + almanac_recordLowYear)
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Record low year data is not available.")

        if almanac_normalLowdata is True:
            print(Fore.YELLOW + Style.BRIGHT + "Normal Low: " + Fore.CYAN + Style.BRIGHT + almanac_normalLowF + "°F ("
                  + almanac_normalLowC + "°C)")
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Normal low year data is not available.")
        print("")
#<--- Almanac is above | Sundata is below --->
    elif moreoptions == "10":
        try:
            logger.debug("sundata_prefetched: %s ; sundata cache time: %s" %
                         (sundata_prefetched, time.time() - cachetime_sundata))
        except:
            logger.debug("sundata_prefetched: %s" % sundata_prefetched)
            
        logger.debug("refresh_sundataflagged: %s" % refresh_sundataflagged)
        logger.info("Selected option - Sun/moon data")
        if (sundata_prefetched is False or
            time.time() - cachetime_sundata >= cache_sundatatime and cache_enabled == True or
                refresh_sundataflagged == True):
            spinner.start(text="Refreshing astronomy data...")
            try:
                sundataJSON = requests.get(astronomyurl)
                logger.debug("Retrieved sundata JSON with response: %s" % sundataJSON)
                cachetime_sundata = time.time()
                
            except:
                spinner.fail(text="Failed to load astronomy data!")
                print("")
                print(Fore.RED + Style.BRIGHT + "When attempting to fetch the 'sundata' from Wunderground,",
                      Fore.RED + Style.BRIGHT + "PyWeather ran into an error. If you're on a network with",
                      Fore.RED + Style.BRIGHT + "a filter, make sure 'api.wunderground.com' is unblocked.",
                      Fore.RED + Style.BRIGHT + "Otherwise, make sure you have an internet connection.", sep="\n")
                printException()
                print(Fore.RED + Style.BRIGHT + "Press enter to continue.")
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
            try:
                SR_minute = int(astronomy_json['moon_phase']['sunrise']['minute'])
                SR_hour = int(astronomy_json['moon_phase']['sunrise']['hour'])
                logger.debug("SR_minute: %s ; SR_hour: %s" %
                            (SR_minute, SR_hour))
                sunrisedata = True
            except:
                logger.warning("No sunrise data is available!")
                sunrisedata = False

            logger.debug("sunrisedata: %s" % sunrisedata)
            if sunrisedata == True:
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
            else:
                sunrise_time = "Unavailable"
                logger.debug("sunrise_time: %s" % sunrise_time)

            try:
                SS_minute = int(astronomy_json['moon_phase']['sunset']['minute'])
                SS_hour = int(astronomy_json['moon_phase']['sunset']['hour'])
                sunsetdata = True
                logger.debug("SS_minute: %s ; SS_hour: %s" %
                             (SS_minute, SS_hour))
            except:
                logger.warning("No sunset time is available!")
                sunsetdata = False
            logger.debug("sunsetdata: %s" % sunsetdata)

            if sunsetdata == True:
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
            else:
                sunset_time = "Unavailable"
                logger.debug("sunset_time: %s" % sunset_time)
        spinner.start(text="Loading astronomy data...")
        moon_percentIlluminated = str(astronomy_json['moon_phase']['percentIlluminated'])
        moon_age = str(astronomy_json['moon_phase']['ageOfMoon'])
        moon_phase = astronomy_json['moon_phase']['phaseofMoon']
        logger.debug("moon_percentIlluminated: %s ; moon_age: %s" %
                     (moon_percentIlluminated, moon_age))
        logger.debug("moon_phase: %s" % moon_phase)
        try:
            MR_minute = int(astronomy_json['moon_phase']['moonrise']['minute'])
            MR_hour = int(astronomy_json['moon_phase']['moonrise']['hour'])
            moonrisedata = True
            logger.debug("MR_minute: %s ; MR_hour: %s" % (MR_minute, MR_hour))
        except ValueError:
            logger.warning("Moonrise data is not available!")
            moonrisedata = False

        logger.debug("moonrisedata: %s" % moonrisedata)


        if moonrisedata == True:
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
            elif MR_hour < 12:
                logger.debug("Moonrise hour < 12. Prefixing AM...")
                MR_hour = str(MR_hour)
                MR_minute = str(MR_minute).zfill(2)
                moonrise_time = MR_hour + ":" + MR_minute + " AM"
                logger.debug("MR_hour: %s ; MR_minute: %s" %
                             (MR_hour, MR_minute))
                logger.debug("moonrise_time: %s" % moonrise_time)
        else:
            moonrise_time = "Unavailable"
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
            elif MS_hour < 12:
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
        else:
            moonset_time = "Unavailable"
            logger.debug("moonset_time: %s" % moonset_time)
        spinner.stop()
        logger.info("Printing data...")
        print("")
        print(Fore.YELLOW + Style.BRIGHT + "Here's the detailed sun/moon data for: " + Style.BRIGHT +
              Fore.CYAN + str(location))
        print("")
        print(Fore.YELLOW + Style.BRIGHT +  "Sunrise time: " + Fore.CYAN + Style.BRIGHT +  sunrise_time)
        print(Fore.YELLOW + Style.BRIGHT +  "Sunset time: " + Fore.CYAN + Style.BRIGHT +  sunset_time)
        print(Fore.YELLOW + Style.BRIGHT +  "Moonrise time: " + Fore.CYAN + Style.BRIGHT +  moonrise_time)
        print(Fore.YELLOW + Style.BRIGHT +  "Moonset time: " + Fore.CYAN + Style.BRIGHT +  moonset_time)
        print("")
        print(Fore.YELLOW + Style.BRIGHT +  "Percent of the moon illuminated: "
              + Fore.CYAN + Style.BRIGHT +  moon_percentIlluminated + "%")
        print(Fore.YELLOW + Style.BRIGHT +  "Age of the moon: " + Fore.CYAN + Style.BRIGHT +
              moon_age + " days")
        print(Fore.YELLOW + Style.BRIGHT +  "Phase of the moon: " + Fore.CYAN + Style.BRIGHT +
              moon_phase)
#<--- Sundata is above | Historical data is below --->
    elif moreoptions == "8":
        # Even with the improved data checking, Wunderground still entirely removes keys for invalid data for PWSes.
        if pws_query is True:
            print(Fore.YELLOW + Style.BRIGHT + "Sorry! Looking at historical data for PWS queries isn't supported yet.",
                  Fore.YELLOW + Style.BRIGHT + "You'll be able to look at historical data for PWS queries in PyWeather 0.6.4 beta.", sep="\n")
            continue
        print(Fore.YELLOW + Style.BRIGHT + "To show historical data for this location, please enter a date to show the data.")
        print(Fore.YELLOW + Style.BRIGHT + "The date must be in the format YYYYMMDD.")
        print(Fore.YELLOW + Style.BRIGHT + "E.g: If I wanted to see the weather for February 15, 2013, you'd enter 20130215.")
        print(Fore.YELLOW + Style.BRIGHT + "Input the desired date below.")
        historical_input = input("Input here: ").lower()
        logger.debug("historical_input: %s" % historical_input)
        spinner.start(text="Loading historical weather data...")
        historical_loops = 0
        historical_totalloops = 0
        logger.debug("historical_loops: %s ; historical_totalloops: %s"
                     % (historical_loops, historical_totalloops))
        if pws_available is False:
            historicalurl = 'http://api.wunderground.com/api/' + apikey + '/history_' + historical_input + '/q/' + latstr + "," + lonstr + '.json'
        elif pws_available is True:
            historicalurl = 'http://api.wunderground.com/api/' + apikey + '/history_' + historical_input + '/q/' + locinput.lower() + '.json'
        logger.debug("historicalurl: %s" % historicalurl)
        
        historical_skipfetch = False
        logger.debug("historical_skipfetch: %s" % historical_skipfetch)

        # Find out if we already have cached data for the date as inputted
        for historical_cacheddate, historical_data in historical_cache.items():
            logger.debug("historical_cacheddate: %s")
            # If we have a match, make the historical_json file equal "historical_data" as defined above.
            if historical_cacheddate == historical_input:
                print(Fore.RED + "Loading cached data...")
                historical_json = historical_data
                if jsonVerbosity == True:
                    logger.debug("historical_json: %s" % historical_json)
                historical_skipfetch = True
                logger.debug("historical_skipfetch: %s" % historical_skipfetch)
                break
            else:
                historical_skipfetch = False
                logger.debug("historical_skipfetch: %s" % historical_skipfetch)
                
        # No cached data, fetch the file.
        if historical_skipfetch == False:
            try:
                historicalJSON = requests.get(historicalurl)
                logger.debug("historicalJSON acquired, end response: %s" % historicalJSON)
            except:
                spinner.fail(text="Failed to load historical weather data!")
                print("")
                print(Fore.RED + Style.BRIGHT + "When attempting to fetch historical data, PyWeather ran into",
                      Fore.RED + Style.BRIGHT + "an error. If you're on a network with a filter make sure that",
                      Fore.RED + Style.BRIGHT + "'api.wunderground.com' is unblocked. Otherwise, make sure that",
                      Fore.RED + Style.BRIGHT + "you have an internet connection, and that your DeLorean works.",
                      sep="\n")
                printException()
                print(Fore.RED + Style.BRIGHT + "Press enter to continue.")
                input()
                continue
        
            try:
                historical_json = json.loads(historicalJSON.text)
            except json.decoder.JSONDecodeError:
                print(Fore.RED + Style.BRIGHT + "There was an issue parsing the data for the date requested. Try requesting another date."
                      + Fore.RESET)
                continue
            # Append the cache date into the historical cache (if it wasn't cached already). Set the data as the json.
            # Example: If we're getting the data for 1/1/2017 (20170101), historical_input is 20170101, and we're appending a 'section'
            # Called 20170101, the key being the entire historical json file.
            historical_cache[historical_input] = historical_json
            logger.debug("Appended new key to historal cache: %s with value historical json"
                         % historical_input)
            if jsonVerbosity == True:
                logger.debug("historical_json: %s" % historical_json)
            else:
                logger.debug("Loaded 1 JSON.")
        historical_date = historical_json['history']['date']['pretty']
        if historical_date == "":
            print(Fore.RED + Style.BRIGHT + "The date you entered was invalid. Please try selecting another date."
                  + Fore.RESET)
            continue
        spinner.stop()
        print("")
        print(Fore.YELLOW + Style.BRIGHT + "Here's the historical weather for " + Fore.CYAN + Style.BRIGHT +
              str(location) + Fore.YELLOW + Style.BRIGHT + " on "
              + Fore.CYAN + Style.BRIGHT + historical_date)
        logger.debug("historical_date: %s" % historical_date)
        for data in historical_json['history']['dailysummary']:
            print("")
            # historicals: historical Summary
            #                         ^

            # Declare show variables - we'll need 17 of them!
            historicals_showMinTemp = True
            historicals_showAvgTemp = True
            logger.debug("historicals_showMinTemp: %s ; historicals_showAvgTemp: %s" %
                         (historicals_showMinTemp, historicals_showAvgTemp))
            historicals_showMaxTemp = True
            historicals_showMinDewPoint = True
            logger.debug("historicals_showMaxTemp: %s ; historicals_showMinDewPoint: %s" %
                         (historicals_showMaxTemp, historicals_showMinDewPoint))
            historicals_showAvgDewPoint = True
            historicals_showMaxDewPoint = True
            logger.debug("historicals_showAvgDewPoint: %s ; historicals_showMaxDewPoint: %s" %
                         (historicals_showAvgDewPoint, historicals_showMaxDewPoint))
            historicals_showMinVis = True
            historicals_showAvgVis = True
            logger.debug("historicals_showMinVis: %s ; historicals_showAvgVis: %s" %
                         (historicals_showMinVis, historicals_showAvgVis))
            historicals_showMaxVis = True
            historicals_showMinPress = True
            logger.debug("historicals_showMaxVis: %s ; historicals_showMinPress: %s" %
                         (historicals_showMaxVis, historicals_showMinPress))
            historicals_showAvgPress = True
            historicals_showMaxPress = True
            logger.debug("historicals_showAvgPress: %s ; historicals_showMaxPress: %s" %
                         (historicals_showAvgPress, historicals_showMaxPress))
            historicals_showHumidity = True
            historicals_showMinWind = True
            logger.debug("historicals_showHumidity: %s ; historicals_showMinWind: %s" %
                         (historicals_showHumidity, historicals_showMinWind))
            historicals_showAvgWind = True
            historicals_showMaxWind = True
            logger.debug("historicals_showAvgWind: %s ; historicals_showMaxWind: %s" %
                         (historicals_showAvgWind, historicals_showMaxWind))
            historicals_showWindDir = True
            logger.debug("historicals_showWindDir: %s" % historicals_showWindDir)
            historicals_avgTempF = str(data['meantempi'])
            historicals_avgTempC = str(data['meantempm'])
            logger.debug("historicals_avgTempF: %s ; historicals_avgTempC: %s" %
                         (historicals_avgTempF, historicals_avgTempC))
            # With historical summary, Wunderground doesn't remove the key, but instead puts nothing ("") as the data.
            # Check for "" for each data type. If the data turns out to be "", don't show the data type.
            if historicals_avgTempF == "" or historicals_avgTempC == "":
                logger.info("historicals_avgTempF is '' or historicals_avgTempC is ''.")
                historicals_showAvgTemp = False
                logger.debug("historicals_showAvgTemp: %s" % historicals_showAvgTemp)

            historicals_avgDewpointF = str(data['meandewpti'])
            historicals_avgDewpointC = str(data['meandewptm'])
            logger.debug("historicals_avgDewpointF: %s ; historicals_avgDewpointC: %s" %
                         (historicals_avgDewpointF, historicals_avgDewpointC))
            if historicals_avgDewpointF == "" or historicals_avgDewpointC == "":
                logger.info("historicals_avgDewpointF is '' or historicals_avgDewpointC is ''.")
                historicals_showAvgDewPoint = False
                logger.debug("historicals_showAvgDewPoint: %s" % historicals_showAvgDewPoint)

            historicals_avgPressureMB = str(data['meanpressurem'])
            historicals_avgPressureInHg = str(data['meanpressurei'])
            logger.debug("historicals_avgPressureMB: %s ; historicals_avgPressureInHg: %s" %
                         (historicals_avgPressureMB, historicals_avgPressureInHg))
            if historicals_avgPressureMB == "" or historicals_avgPressureInHg == "":
                logger.info("historicals_avgPressureMB is '' or historicals_avgPressureInHg is ''.")
                historicals_showAvgPress = False
                logger.debug("historicals_showAvgPress: %s" % historicals_showAvgPress)

            historicals_avgWindSpeedMPH = str(data['meanwindspdi'])
            historicals_avgWindSpeedKPH = str(data['meanwindspdm'])
            logger.debug("historicals_avgWindSpeedMPH: %s ; historicals_avgWindSpeedKPH: %s" %
                         (historicals_avgWindSpeedMPH, historicals_avgWindSpeedKPH))
            if historicals_avgWindSpeedMPH == "" or historicals_avgWindSpeedKPH == "":
                logger.info("historicals_avgWindSpeedMPH is '' or historicals_avgWindSpeedKPH is ''.")
                historicals_showAvgWind = False
                logger.debug("historicals_showAvgWind: %s" % historicals_showAvgWind)

            historicals_avgWindDegrees = str(data['meanwdird'])
            historicals_avgWindDirection = data['meanwdire']
            logger.debug("historicals_avgWindDegrees: %s ; historicals_avgWindDirection: %s" %
                         (historicals_avgWindDegrees, historicals_avgWindDirection))
            if historicals_avgWindDegrees == "" or historicals_avgWindDirection == "":
                logger.info("historicals_avgWindDegrees is '' or historicals_avgWindDirection is ''.")
                historicals_showWindDir = False
                logger.debug("historicals_showWindDir: %s" % historicals_showWindDir)


            historicals_avgVisibilityMI = str(data['meanvisi'])
            historicals_avgVisibilityKM = str(data['meanvism'])
            logger.debug("historicals_avgVisibilityMI: %s ; historicals_avgVisibilityKM: %s" %
                         (historicals_avgVisibilityMI, historicals_avgVisibilityKM))
            if historicals_avgVisibilityMI == "" or historicals_avgVisibilityKM == "":
                logger.info("historicals_avgVisibilityMI is '' or historicals_avgVisibilityKM is ''.")
                historicals_showAvgVis = False
                logger.debug("historicals_showAvgVis: %s" % historicals_showAvgVis)

            # Check for good humidity data. if there is good humidity data, we then will do our
            # nieve way of finding the average humidity. If there is no good data, don't show humidity
            # during the summary screen, and don't do the average humidity code.


            try:
                historicals_maxHumidity = int(data['maxhumidity'])
                historicals_minHumidity = int(data['minhumidity'])
                logger.debug("historicals_maxHumidity: %s ; historicals_minHumidity: %s" %
                             (historicals_maxHumidity, historicals_minHumidity))
            except ValueError:
                historicals_showHumidity = False
                logger.debug("historicals_showHumidity: %s" % historicals_showHumidity)
            # This is a really nieve way of calculating the average humidity. Sue me.
            # In reality, WU spits out nothing for average humidity.
            if historicals_showHumidity is True:
                logger.info("historicals_showHumidity is True.")
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
            logger.debug("historicals_maxTempF: %s ; historicals_maxTempC: %s" %
                         (historicals_maxTempF, historicals_maxTempC))

            if historicals_maxTempF == "" or historicals_maxTempC == "":
                logger.info("historicals_maxTempF is '' or historicals_maxTempC is ''.")
                historicals_showMaxTemp = False
                logger.debug("historicals_showMaxTemp: %s" % historicals_showMaxTemp)

            historicals_minTempF = str(data['mintempi'])
            historicals_minTempC = str(data['mintempm'])
            logger.debug("historicals_minTempF: %s ; historicals_minTempC: %s" %
                         (historicals_minTempF, historicals_minTempC))

            if historicals_minTempF == "" or historicals_minTempC == "":
                logger.info("historicals_minTempF is '' or historicals_minTempC is ''.")
                historicals_showMinTemp = False
                logger.debug("historicals_showMinTemp: %s" % historicals_showMinTemp)

            historicals_maxDewpointF = str(data['maxdewpti'])
            historicals_maxDewpointC = str(data['maxdewptm'])
            logger.debug("historicals_maxDewpointF: %s ; historicals_maxDewpointC: %s" %
                         (historicals_maxDewpointF, historicals_maxDewpointC))

            if historicals_maxDewpointF == "" or historicals_maxDewpointC == "":
                logger.info("historicals_maxDewpointF is '' or historicals_maxDewpointC is ''.")
                historicals_showMaxDewPoint = False
                logger.debug("historicals_showMaxDewPoint: %s" % historicals_showMaxDewPoint)

            historicals_minDewpointF = str(data['mindewpti'])
            historicals_minDewpointC = str(data['mindewptm'])
            logger.debug("historicals_minDewpointF: %s ; historicals_minDewpointC: %s" %
                         (historicals_minDewpointF, historicals_minDewpointC))

            if historicals_minDewpointF == "" or historicals_minDewpointC == "":
                logger.info("historicals_minDewpointF is '' or historicals_minDewpointC is ''.")
                historicals_showMinDewPoint = False
                logger.debug("historicals_showMinDewPoint: %s" % historicals_showMinDewPoint)

            historicals_maxPressureInHg = str(data['maxpressurei'])
            historicals_maxPressureMB = str(data['maxpressurem'])
            logger.debug("historicals_maxPressureInHg: %s ; historicals_maxPressureMB: %s" %
                         (historicals_maxPressureInHg, historicals_maxPressureMB))

            if historicals_maxPressureInHg == "" or historicals_maxPressureMB == "":
                logger.info("historicals_maxPressureInHg is '' or historicals_maxPressureMB is ''.")
                historicals_showMaxPress = False
                logger.debug("historicals_showMaxPress: %s" % historicals_showMaxPress)

            historicals_minPressureInHg = str(data['minpressurei'])
            historicals_minPressureMB = str(data['minpressurem'])
            logger.debug("historicals_minPressureInHg: %s ; historicals_minPressureMB: %s" %
                         (historicals_minPressureInHg, historicals_minPressureMB))

            if historicals_minPressureInHg == "" or historicals_minPressureMB == "":
                logger.info("historicals_minPressureInHg is '' or historicals_minPressureMB is ''.")
                historicals_showMinPress = False
                logger.debug("historicals_showMinPress: %s" % historicals_showMinPress)

            historicals_maxWindMPH = str(data['maxwspdi'])
            historicals_maxWindKPH = str(data['maxwspdm'])
            logger.debug("historicals_maxWindMPH: %s ; historicals_maxWindKPH: %s" %
                         (historicals_maxWindMPH, historicals_maxWindMPH))

            if historicals_maxWindMPH == "" or historicals_maxWindKPH == "":
                logger.info("historicals_maxWindMPH is '' or historicals_maxWindKPH is ''.")
                historicals_showMaxWind = False
                logger.debug("historicals_showMaxWind: %s" % historicals_showMaxWind)

            historicals_minWindMPH = str(data['minwspdi'])
            historicals_minWindKPH = str(data['minwspdm'])
            logger.debug("historicals_minWindMPH: %s ; historicals_minWindKPH: %s" %
                         (historicals_minWindMPH, historicals_minWindKPH))

            if historicals_minWindMPH == "" or historicals_minWindKPH == "":
                logger.info("historicals_minWindMPH is '' or historicals_minWindKPH is ''.")
                historicals_showMinWind = False
                logger.debug("historicals_showMinWind: %s" % historicals_showMinWind)

            historicals_maxVisibilityMI = str(data['maxvisi'])
            historicals_maxVisibilityKM = str(data['maxvism'])
            logger.debug("historicals_maxVisibilityMI: %s ; historicals_maxVisibilityKM: %s" %
                         (historicals_maxVisibilityMI, historicals_maxVisibilityKM))

            if historicals_maxVisibilityMI == "" or historicals_maxVisibilityKM == "":
                logger.info("historicals_maxVisibilityMI is '' or historicals_maxVisibilityKM is ''.")
                historicals_showMaxVis = False
                logger.debug("historicals_showMaxVis: %s" % historicals_showMaxVis)

            historicals_minVisibilityMI = str(data['minvisi'])
            historicals_minVisibilityKM = str(data['minvism'])
            logger.debug("historicals_minVisibilityMI: %s ; historicals_minVisibilityKM: %s" %
                         (historicals_minVisibilityMI, historicals_minVisibilityKM))

            if historicals_minVisibilityMI == "" or historicals_minVisibilityKM == "":
                logger.info("historicals_minVisibilityMI is '' or historicals_minVisibilityKM is ''.")
                historicals_showMinVis = False
                logger.debug("historicals_showMinVis: %s" % historicals_showMinVis)

            historicals_precipMM = str(data['precipm'])
            historicals_precipIN = str(data['precipi'])
            logger.debug("historicals_precipMM: %s ; historicals_precipIN: %s" %
                         (historicals_precipMM, historicals_precipIN))


            # Check for invalid precip data - Don't show it if it equals "T".
            historicals_showPrecipData = True
            logger.debug("historicals_showPrecipData: %s" % historicals_showPrecipData)
            if historicals_precipIN == "T":
                logger.info("historicals_precipIN is 'T'.")
                historicals_showPrecipData = False
                logger.debug("historicals_showPrecipData: %s" % historicals_showPrecipData)


        print(Fore.YELLOW + Style.BRIGHT + "Here's the summary for the day.")
        if historicals_showMinTemp is True:
            print(Fore.YELLOW + Style.BRIGHT + "Minimum Temperature: " + Fore.CYAN + Style.BRIGHT + historicals_minTempF
                  + "°F (" + historicals_minTempC + "°C)")
        if historicals_showAvgTemp is True:
            print(Fore.YELLOW + Style.BRIGHT + "Average Temperature: " + Fore.CYAN + Style.BRIGHT + historicals_avgTempF
                  + "°F (" + historicals_avgTempC + "°C)")
        if historicals_showMaxTemp is True:
            print(Fore.YELLOW + Style.BRIGHT + "Maxmimum Temperature: " + Fore.CYAN + Style.BRIGHT + historicals_maxTempF
                  + "°F (" + historicals_maxTempC + "°C)")
        if historicals_showMinDewPoint is True:
            print(Fore.YELLOW + Style.BRIGHT + "Minimum Dew Point: " + Fore.CYAN + Style.BRIGHT + historicals_minDewpointF
                  + "°F (" + historicals_minDewpointC + "°C)")
        if historicals_showAvgDewPoint is True:
            print(Fore.YELLOW + Style.BRIGHT + "Average Dew Point: " + Fore.CYAN + Style.BRIGHT + historicals_avgDewpointF
                  + "°F (" + historicals_avgDewpointC + "°C)")
        if historicals_showMaxDewPoint is True:
            print(Fore.YELLOW + Style.BRIGHT + "Maximum Dew Point: " + Fore.CYAN + Style.BRIGHT + historicals_maxDewpointF
                  + "°F (" + historicals_maxDewpointC + "°C)")
        if historicals_showHumidity is True:
            print(Fore.YELLOW + Style.BRIGHT + "Minimum Humidity: " + Fore.CYAN + Style.BRIGHT + historicals_minHumidity
                  + "%")
            print(Fore.YELLOW + Style.BRIGHT + "Average Humidity: " + Fore.CYAN + Style.BRIGHT + historicals_avgHumidity
                  + "%")
            print(Fore.YELLOW + Style.BRIGHT + "Maximum Humidity: " + Fore.CYAN + Style.BRIGHT + historicals_maxHumidity
                  + "%")
        if historicals_showMinWind is True:
            print(Fore.YELLOW + Style.BRIGHT + "Minimum Wind Speed: " + Fore.CYAN + Style.BRIGHT + historicals_minWindMPH
                  + " mph (" + historicals_minWindKPH + " kph)")
        if historicals_showAvgWind is True:
            print(Fore.YELLOW + Style.BRIGHT + "Average Wind Speed: " + Fore.CYAN + Style.BRIGHT + historicals_avgWindSpeedMPH
                  + " mph (" + historicals_avgWindSpeedKPH + " kph)")
        if historicals_showMaxWind is True:
            print(Fore.YELLOW + Style.BRIGHT + "Maximum Wind Speed: " + Fore.CYAN + Style.BRIGHT + historicals_maxWindMPH
                  + " mph (" + historicals_maxWindKPH + " kph)")
        if historicals_showMinVis is True:
            print(Fore.YELLOW + Style.BRIGHT + "Minimum Visibility: " + Fore.CYAN + Style.BRIGHT + historicals_minVisibilityMI
                  + " mi (" + historicals_minVisibilityKM + " kph)")
        if historicals_showAvgVis is True:
            print(Fore.YELLOW + Style.BRIGHT + "Average Visibility: " + Fore.CYAN + Style.BRIGHT + historicals_avgVisibilityMI
                  + " mi (" + historicals_avgVisibilityKM + " kph)")
        if historicals_showMaxVis is True:
            print(Fore.YELLOW + Style.BRIGHT + "Maximum Visibility: " + Fore.CYAN + Style.BRIGHT + historicals_maxVisibilityMI
                  + " mi (" + historicals_maxVisibilityKM + " kph)")
        if historicals_showMinPress is True:
            print(Fore.YELLOW + Style.BRIGHT + "Minimum Pressure: " + Fore.CYAN + Style.BRIGHT + historicals_minPressureInHg
                  + " inHg (" + historicals_minPressureMB + " mb)")
        if historicals_showAvgPress is True:
            print(Fore.YELLOW + Style.BRIGHT + "Average Pressure: " + Fore.CYAN + Style.BRIGHT + historicals_avgPressureInHg
                  + " inHg (" + historicals_avgPressureMB + " mb)")
        if historicals_showMaxPress is True:
            print(Fore.YELLOW + Style.BRIGHT + "Maximum Pressure: " + Fore.CYAN + Style.BRIGHT + historicals_maxPressureInHg
                  + " inHg (" + historicals_maxPressureMB + " mb)")
        if historicals_showPrecipData is True:
            print(Fore.YELLOW + Style.BRIGHT + "Total Precipitation: " + Fore.CYAN + Style.BRIGHT + historicals_precipIN
                  + " in (" + historicals_precipMM + " mm)")
        print("")
        print(Fore.RED + Style.BRIGHT + "To view hourly historical data, please press enter.")
        print(Fore.RED + Style.BRIGHT + "If you want to return to the main menu, press Control + C.")
        try:
            historicalcontinue = input("Input here: ").lower()
        except KeyboardInterrupt:
            logger.debug("Continuing to the main menu...")
            print("")
            continue

        # Start the pre-loop to see how many times we're looping.
        historicalhourlyLoops = 0
        for data in historical_json['history']['observations']:
            historical_tempF = str(data['tempi'])
            historicalhourlyLoops = historicalhourlyLoops + 1
            
        for data in historical_json['history']['observations']:
            logger.info("We're on iteration %s/%s. User iteration limit: %s."
                        % (historical_totalloops, historicalhourlyLoops, user_loopIterations))
            # Define all the show variables up here.
            # Do note that some of these are here for future use.
            historical_showConditions = True
            historical_showTemp = True
            historical_showDewpoint = True
            historical_showWindSpeed = True
            historical_showWindGust = True
            historical_showWindDirection = True
            historical_showVis = True
            historical_showWindChill = True
            historical_showHeatIndex = True
            historical_showPressure = True
            historical_showPrecip = True
            logger.debug("historical_showConditions: %s ; historical_showTemp: %s" %
                         (historical_showConditions, historical_showTemp))
            logger.debug("historcial_showDewpoint: %s ; historical_showWindSpeed: %s" %
                         (historical_showDewpoint, historical_showWindSpeed))
            logger.debug("historical_showWindGust: %s ; historical_showWindDirection: %s" %
                         (historical_showWindGust, historical_showWindDirection))
            logger.debug("historical_showVis: %s ; historical_showWindChill: %s" %
                         (historical_showVis, historical_showWindChill))
            logger.debug("historical_showPressure: %s ; historical_showPrecip: %s" %
                         (historical_showPressure, historical_showPrecip))
            historical_time = data['date']['pretty']
            logger.debug("historical_time: %s" % historical_time)
            historical_tempF = str(data['tempi'])
            historical_tempC = str(data['tempm'])
            logger.debug("historical_tempF: %s ; historical_tempC: %s" %
                         (historical_tempF, historical_tempC))
            if historical_tempF == "-9999" or historical_tempC == "-9999" or historical_tempF == "" or historical_tempC == "":
                logger.info("historical_tempF is '-9999' or historical_tempC is '-9999' or historical_tempF is '' or historical_tempC is ''.")
                historical_showTemp = False
                logger.debug("historical_showTemp: %s" % historical_showTemp)

            historical_dewpointF = str(data['dewpti'])
            historical_dewpointC = str(data['dewptm'])
            logger.debug("historical_dewpointF: %s ; historical_dewpointC: %s" %
                         (historical_dewpointF, historical_dewpointC))

            if historical_dewpointF == "-9999" or historical_dewpointC == "-9999" or historical_dewpointF == "" or historical_dewpointC == "":
                logger.info("historical_dewpointF is '-9999' or historical_dewpointC is '-9999' or historical_dewpointF is '' or historical_dewpointC is ''.")
                historical_showDewpoint = False
                logger.debug("historical_showDewpoint: %s" % historical_showDewpoint)
            historical_windspeedKPH = str(data['wspdm'])
            historical_windspeedMPH = str(data['wspdi'])
            logger.debug("historical_windspeedKPH: %s ; historical_windspeedMPH: %s" %
                         (historical_windspeedKPH, historical_windspeedMPH))

            # Check for bad wind data in the hourly - it's "".

            if historical_windspeedKPH == "" or historical_windspeedKPH == "-9999.0" or historical_windspeedMPH == "" or historical_windspeedMPH == "-9999.0":
                logger.info("historical_windspeedKPH is '' or historical_windspeedKPH is '-9999.0' or historical_windspeedMPH is '' or historical_windspeedMPH is '-9999.0")
                historical_showWindSpeed = False
                logger.debug("historical_showWindSpeed: %s" % historical_showWindSpeed)

            try:
                historical_gustcheck = float(data['wgustm'])
            except ValueError:
                printException_loggerwarn()
                historical_showWindGust = False
                logger.debug("historical_showWindGust: %s" % historical_showWindGust)


            if historical_showWindGust is False:
                logger.warning("Wind gust data is not available!")
            else:
                historical_windgustKPH = str(data['wgustm'])
                historical_windgustMPH = str(data['wgusti'])
                logger.info("Wind gust data is present.")
                logger.debug("historical_windgustKPH: %s ; historical_windgustMPH: %s"
                             % (historical_windgustKPH, historical_windgustMPH))

            # Do yet ANOTHER check for data.
            if historical_showWindGust is True:
                logger.info("historical_showWindGust: %s" % historical_showWindGust)
                if historical_windgustMPH == "-9999.0" or historical_windgustKPH == "-9999.0":
                    logger.info("historical_windgustMPH is '-9999.0' or historical_windgustKPH is '-9999.0'.")
                    historical_showWindGust = False
                    logger.debug("historical_showWindGust")

            historical_windDegrees = str(data['wdird'])
            historical_windDirection = data['wdire']
            logger.debug("historical_windDegrees: %s ; historical_windDirection: %s"
                         % (historical_windDegrees, historical_windDirection))

            if historical_windDegrees == "" or historical_windDirection == "":
                logger.info("historical_windDegrees is '' or historical_windDirection is ''.")
                historical_showWindDirection = False
                logger.debug("historical_showWindDirection: %s" % historical_showWindDirection)

            historical_visibilityKM = str(data['vism'])
            historical_visibilityMI = str(data['visi'])
            logger.debug("historical_visibilityKM: %s ; historical_visibilityMI: %s"
                         % (historical_visibilityKM, historical_visibilityMI))

            if historical_visibilityMI == "-9999.0" or historical_visibilityKM == "-9999.0" or historical_visibilityKM == "" or historical_visibilityMI == "":
                logger.info("historical_visibilityMI is '-9999.0' or historical_visibilityKM is '-9999.0' or historical_visibilityKM is '' or historical_visibilityMI is ''.")
                historical_showVis = False
                logger.debug("historical_showVis: %s" % historical_showVis)

            historical_pressureMB = str(data['pressurem'])
            historical_pressureInHg = str(data['pressurei'])
            logger.debug("historical_pressureMB: %s ; historical_pressureInHg: %s"
                         % (historical_pressureMB, historical_pressureInHg))

            if historical_pressureMB == "-9999" or historical_pressureInHg == "-9999" or historical_pressureMB == "" or historical_pressureInHg == "":
                logger.info("historical_pressureMB is '-9999' or historical_pressureInHg is '-9999' or historical_pressureMB is '' or historical_pressureInHg is ''.")
                historical_showPressure = False
                logger.debug("historical_showPressure: %s" % historical_showPressure)
            historical_windchillcheck = float(data['windchillm'])
            logger.debug("historical_windchillcheck: %s" % historical_windchillcheck)
            if historical_windchillcheck == -999:
                logger.info("historical_windchillcheck is '-999'.")
                historical_showWindChill = False
                logger.debug("historical_showWindChill: %s" % historical_showWindChill)
            else:
                historical_showWindChill = True
                historical_windchillC = str(data['windchillm'])
                historical_windchillF = str(data['windchilli'])
                logger.info("Wind chill data is present. historical_showWindChill: %s" % historical_showWindChill)
                logger.debug("historical_windchillC: %s ; historical_windchillF: %s"
                             % (historical_windchillC, historical_windchillF))

            historical_heatindexcheck = float(data['heatindexm'])
            logger.debug("historical_heatindexcheck: %s" % historical_heatindexcheck)
            if historical_heatindexcheck == -9999:
                logger.info("historical_heatindexcheck is '-9999'.")
                historical_showHeatIndex = False
                logger.debug("historical_showHeatIndex: %s" % historical_showHeatIndex)
            else:
                historical_heatindexdata = True
                historical_heatindexC = str(data['heatindexm'])
                historical_heatindexF = str(data['heatindexi'])
                logger.info("Heat index data is present. historical_heatindexdata: %s" % historical_heatindexdata)
                logger.debug("historical_heatindexC: %s ; historical_heatindexF: %s"
                             % (historical_heatindexC, historical_heatindexF))

            try:
                historical_precipMM = float(data['precipm'])
                historical_precipIN = float(data['precipi'])
                logger.debug("historical_precipMM: %s ; historical_precipIN: %s"
                             % (historical_precipMM, historical_precipIN))
            except ValueError:
                printException_loggerwarn()
                historical_showPrecip = False
                logger.debug("historical_showPrecip: %s" % historical_showPrecip)

            if historical_showPrecip is False:
                logger.info("historical_showPrecip is False. We have no data.")
            else:
                # Convert into strings for the sake of easy checking & display
                historical_precipMM = str(historical_precipMM)
                historical_precipIN = str(historical_precipIN)
                logger.info("Converted 2 vars into strings.")
                logger.debug("historical_precipMM: %s ; historical_precipIN: %s" %
                             (historical_precipMM, historical_precipIN))

            # Data check for invalid precip data, given we didn't hit the traceback above.
            if historical_showPrecip is True:
                logger.info("historical_showPrecip is True.")
                if historical_precipIN == "-9999.0" or historical_precipMM == "-9999.0":
                    logger.info("historical_precipIN is '-9999.0' or historical_precipMM is '-9999.0'.")
                    historical_showPrecip = False
                    logger.debug("historical_showPrecip: %s" % historical_showPrecip)
            
            historical_condition = str(data['conds'])
            logger.debug("historical_condition: %s" % historical_condition)

            if historical_condition == "" or historical_condition == "Unknown":
                logger.info("historical_condition is '' or historical_condition is 'Unknown'.")
                historical_showConditions = False
                logger.debug("historical_showConditions: %s" % historical_showConditions)
            logger.info("Now printing weather data...")
            print("")
            print(Fore.YELLOW + Style.BRIGHT + historical_time + ":")
            if historical_showConditions is True:
                print(Fore.YELLOW + Style.BRIGHT + "Conditions: " + Fore.CYAN + Style.BRIGHT + historical_condition)
            if historical_showTemp is True:
                print(Fore.YELLOW + Style.BRIGHT + "Temperature: " + Fore.CYAN + Style.BRIGHT + historical_tempF
                      + "°F (" + historical_tempC + "°C)")
            if historical_showDewpoint is True:
                print(Fore.YELLOW + Style.BRIGHT + "Dew point: " + Fore.CYAN + Style.BRIGHT + historical_dewpointF
                      + "°F (" + historical_dewpointC + "°C)")
            if historical_showWindSpeed is True:
                print(Fore.YELLOW + Style.BRIGHT + "Wind speed: " + Fore.CYAN + Style.BRIGHT + historical_windspeedMPH
                      + " mph (" + historical_windspeedKPH + " kph)")
            if historical_showWindDirection is True:
                if historical_windDirection == "Variable":
                    print(Fore.YELLOW + Style.BRIGHT + "Wind direction: " + Fore.CYAN + Style.BRIGHT + "Variable directions")
                else:
                    print(Fore.YELLOW + Style.BRIGHT + "Wind direction: " + Fore.CYAN + Style.BRIGHT + historical_windDirection
                          + " (" + historical_windDegrees + "°)")
            if historical_showWindGust is True:
                print(Fore.YELLOW + Style.BRIGHT + "Wind gusts: " + Fore.CYAN + Style.BRIGHT + historical_windgustMPH
                      + " mph (" + historical_windgustKPH + " kph)")
            if historical_showWindChill is True:
                print(Fore.YELLOW + Style.BRIGHT + "Wind chill: " + Fore.CYAN + Style.BRIGHT + historical_windchillF
                      + "°F (" + historical_windchillC + "°C)")
            if historical_showHeatIndex is True:
                print(Fore.YELLOW + Style.BRIGHT + "Heat index: " + Fore.CYAN + Style.BRIGHT + historical_heatindexF
                      + "°F (" + historical_heatindexC + "°C)")
            if historical_showPrecip is True:
                print(Fore.YELLOW + Style.BRIGHT + "Precipitation: " + Fore.CYAN + Style.BRIGHT + historical_precipIN
                      + " in (" + historical_precipMM + " mm)")
            if historical_showPressure is True:
                print(Fore.YELLOW + Style.BRIGHT + "Barometric pressure: " + Fore.CYAN + Style.BRIGHT + historical_pressureInHg
                      + " inHg (" + historical_pressureMB + " mb)")
            if historical_showVis is True:
                print(Fore.YELLOW + Style.BRIGHT + "Visibility: " + Fore.CYAN + Style.BRIGHT + historical_visibilityMI + " mi ("
                      + historical_visibilityKM + " km)")
            historical_loops = historical_loops + 1
            historical_totalloops = historical_totalloops + 1
            logger.debug("historical_loops: %s ; historical_totalloops: %s"
                         % (historical_loops, historical_totalloops))
            if user_showCompletedIterations == True:
                print(Fore.YELLOW + Style.BRIGHT + "Completed iterations: " + Fore.CYAN + Style.BRIGHT + "%s/%s"
                      % (historical_totalloops, historicalhourlyLoops))
                         
            if historical_totalloops == historicalhourlyLoops:
                logger.debug("Iterations now %s. Total iterations %s. Breaking..."
                             % (historical_totalloops, historicalhourlyLoops))
                break
                
            if user_enterToContinue == True:
                if historical_loops == user_loopIterations:
                    logger.info("Asking user to continue.")
                    try:
                        print("")
                        print(Fore.RED + Style.BRIGHT + "Press enter to view the next " + str(user_loopIterations)
                              + " iterations of historical weather information.")
                        print(Fore.RED + Style.BRIGHT + "Otherwise, press Control + C to get back to the main menu.")
                        input()
                        historical_loops = 0
                        logger.info("Printing more weather data. historical_loops is now: %s"
                                    % historical_loops)
                    except KeyboardInterrupt:
                        logger.info("Breaking to main menu, user issued KeyboardInterrupt")
                        break
#<--- Historical is above | Tide is below --->
    elif moreoptions == "6":
        try:
            logger.debug("tidedata_prefetched: %s ; tide data cache time: %s" %
                         (tidedata_prefetched, time.time() - cachetime_tide))
        except:
            logger.debug("tidedata_prefetched: %s" % sundata_prefetched)

        logger.debug("refresh_tidedataflagged: %s" % refresh_tidedataflagged)
        if (tidedata_prefetched is False or
                            time.time() - cachetime_tide >= cache_tidetime and cache_enabled == True or
                    refresh_tidedataflagged == True):
            spinner.start(text="Refreshing tide data...")
            try:
                tideJSON = requests.get(tideurl)
                logger.debug("Retrieved tide JSON with response: %s" % tideJSON)
                cachetime_tide = time.time()

            except:
                spinner.fail(text="Failed to refresh tide data!")
                print("")
                print(Fore.RED + Style.BRIGHT + "When attempting to fetch tide data from Wunderground,",
                      Fore.RED + Style.BRIGHT + "PyWeather ran into an error. If you're on a network with",
                      Fore.RED + Style.BRIGHT + "a filter, make sure 'api.wunderground.com' is unblocked.",
                      Fore.RED + Style.BRIGHT + "Otherwise, make sure you have an internet connection.", sep="\n")
                printException()
                print(Fore.RED + Style.BRIGHT + "Press enter to continue.")
                input()
                continue

            tidedata_prefetched = True
            refresh_tidedataflagged = False
            logger.debug("tidedata_prefetched: %s ; refresh_tidedataflagged: %s" %
                         (tidedata_prefetched, refresh_tidedataflagged))

            tide_json = json.loads(tideJSON.text)
            if jsonVerbosity == True:
                logger.debug("tide_json: %s" % astronomy_json)
            else:
                logger.debug("tide json loaded.")
        spinner.start(text="Loading tide data...")
        for data in tide_json['tide']['tideInfo']:
            tide_site = data['tideSite']

        if tide_site == "":
            spinner.fail("Tide data is not available for this location.")
            continue


        # Get the iteration count
        # Total iterations is the actual number of iterations, completed is how many have been completed
        # Current is how many have been completed without interruption.
        tide_totaliterations = 0
        tide_completediterations = 0
        tide_currentiterations = 0
        logger.debug("tide_totaliterations: %s ; tide_currentiterations: %s" %
                     (tide_totaliterations, tide_currentiterations))

        for data in tide_json['tide']['tideSummary']:
            tide_totaliterations = tide_totaliterations + 1
        logger.debug("tide_totaliterations: %s" % tide_totaliterations)
        spinner.stop()

        print("")
        print(Fore.YELLOW + Style.BRIGHT + "Here's the tide data at " + Fore.CYAN + Style.BRIGHT + tide_site
              + Fore.YELLOW + Style.BRIGHT + " (the closest site to you)")
        for data in tide_json['tide']['tideSummary']:
            tide_date = data['date']['pretty']
            tide_type = data['data']['type']
            print("")
            logger.debug("tide_date: %s ; tide_type: %s" % (tide_date, tide_type))
            print(Fore.YELLOW + Style.BRIGHT + tide_date + ":")
            print(Fore.YELLOW + Style.BRIGHT + "Event: " + Fore.CYAN + Style.BRIGHT + tide_type)
            if tide_type == "Low Tide" or tide_type == "High Tide":
                tide_height = data['data']['height']
                logger.debug("tide_height: %s" % tide_height)
                print(Fore.YELLOW + Style.BRIGHT + "Height: " + Fore.CYAN + Style.BRIGHT + tide_height)
            tide_currentiterations = tide_currentiterations + 1
            tide_completediterations = tide_completediterations + 1
            if user_showCompletedIterations == True:
                print(Fore.YELLOW + Style.BRIGHT + "Completed iterations: " + Fore.CYAN + Style.BRIGHT + "%s/%s"
                      % (tide_completediterations, tide_totaliterations))
            logger.debug("tide_currentiterations: %s ; tide_completediterations: %s" %
                         (tide_currentiterations, tide_completediterations))
            if user_enterToContinue == True:
                if tide_completediterations == tide_totaliterations:
                    logger.debug("tide_completediterations is equal to tide_totaliterations. Breaking.")
                    break
                elif tide_currentiterations == user_loopIterations:
                    try:
                        print("")
                        print(Fore.RED + Style.BRIGHT + "Press enter to view the next %s iterations of tide data." % user_loopIterations,
                              Fore.RED + Style.BRIGHT + "Otherwise, press Control + C to head back to the main menu.", sep="\n")
                        input()
                        tide_currentiterations = 0
                        logger.debug("tide_currentiterations: %s" % tide_currentiterations)
                    except KeyboardInterrupt:
                        break
#<--- Tide data is above | Hurricane data is below --->
    elif moreoptions == "5":
        try:
            logger.debug("hurricane cache time: %s ; hurricane cache limit: %s" %
                         (time.time() - cachetime_hurricane, cache_hurricanetime))
        except:
            logger.debug("hurricane cache limit: %s" % cache_hurricanetime)
        # I get it, this part is poorly coded in. You know what? It works!
        if (hurricanePrefetched == False or refresh_hurricanedataflagged == True or time.time() - cachetime_hurricane >= cache_hurricanetime):
            spinner.start(text="Refreshing hurricane data...")
            try:
                hurricaneJSON = requests.get(hurricaneurl)
                cachetime_hurricane = time.time()
                hurricane_json = json.loads(hurricaneJSON.text)
                if jsonVerbosity == "True":
                    logger.debug("hurricane_json: %s" % hurricane_json)
                else:
                    logger.debug("hurricane_json loaded successfully.")
                hurricanePrefetched = True
                refresh_hurricanedataflagged = False
            except:
                spinner.fail(text="Failed to refresh hurricane data!")
                print("")
                print(Fore.RED + Style.BRIGHT + "When attempting to fetch hurricane data, PyWeather ran into an error.",
                      Fore.RED + Style.BRIGHT + "you have an internet connection, and that api.wunderground.com is unblocked",
                      Fore.RED + Style.BRIGHT + "on your network. Press enter to continue.", sep="\n")
                printException()
                input()
                continue

        spinner.start(text="Loading hurricane data!")
        activestorms = 0
        currentstormiterations = 0
        logger.debug("activestorms: %s ; currentstormiterations: %s" %
                     (activestorms, currentstormiterations))
        for data in hurricane_json['currenthurricane']:
            activestorms += 1
        logger.debug("activestorms: %s" % activestorms)

        if activestorms == 0:
            spinner.fail(text="There are no active tropical storms at this time.")
            continue
        spinner.stop()
        print(Fore.YELLOW + Style.BRIGHT + "Here are the active tropical systems around the world:")
        print("")
        # <--- Current data --->
        for data in hurricane_json['currenthurricane']:
            stormname = data['stormInfo']['stormName_Nice']
            logger.debug("stormname: %s" % stormname)
            stormlat = float(data['Current']['lat'])
            # Make a *url variable to store the raw lat/lon in str() format.
            stormlaturl = str(stormlat)
            logger.debug("stormlat: %s ; stormlaturl: %s" %
                         (stormlat, stormlaturl))
            stormlon = float(data['Current']['lon'])
            stormlonurl = str(stormlon)
            logger.debug("stormlon: %s ; stormlonurl: %s" %
                         (stormlon, stormlonurl))
            # Declare the URL for nearest city data
            nearesturl = 'http://api.geonames.org/findNearbyPlaceNameJSON?lat=' + stormlaturl + '&lng=' + stormlonurl + '&username=' + geonames_apiusername + '&radius=300&maxRows=1' + hurricane_citiesamp
            logger.debug("nearesturl: %s" % nearesturl)
            # Enter in here if the nearest city option is enabled
            if hurricanenearestcity_enabled is True:
                logger.info("hurricanenearestcity_enabled is True, loading up data...")
                try:
                    # Get the JSON file. If all goes well, set the nearest_data variable to true.
                    nearestJSON = requests.get(nearesturl)
                    logger.debug("nearestJSON fetched, result: %s" % nearestJSON)
                    nearest_json = json.loads(nearestJSON.text)
                    if jsonVerbosity == True:
                        logger.debug("nearest_json: %s" % nearest_json)
                    else:
                        logger.debug("nearest_json loaded.")
                    nearest_data = True
                    logger.debug("nearest_data: %s" % nearest_data)
                except:
                    # Have an issue, we have no data. Set the variable to false.
                    printException_loggerwarn()
                    nearest_data = False
                    logger.debug("nearest_data: %s" % nearest_data)

                if nearest_data is True:
                    try:
                        errorvalue = str(nearest_json['status']['value'])
                        if errorvalue == "10":
                            nearest_errortext = "The username for the API wasn't authorized."
                        elif errorvalue == "11":
                            nearest_errortext = "The record doesn't exist."
                        elif errorvalue == "12":
                            nearest_errortext = "An undefined error occurred."
                        elif errorvalue == "13":
                            nearest_errortext = "The database timed out."
                        elif errorvalue == "15":
                            nearest_errortext = "No result was found."
                        elif errorvalue == "18":
                            nearest_errortext = "The daily limit of lookups was exceeded. Please try again tomorrow."
                        elif errorvalue == "19":
                            nearest_errortext = "The hourly limit of lookups was exceeded. Please try again in an hour."
                        elif errorvalue == "20":
                            nearest_errortext = "The weekly limit of lookups was exceeded. Please try again at the start of next week."
                        elif errorvalue == "22":
                            nearest_errortext = "The geonames server was overloaded. Please try again in a bit."
                        else:
                            nearest_errortext = "A strange error occurred. That's strange!"
                        nearest_error = True
                        logger.debug("nearest_errortext: %s ; nearest_error: %s" %
                                     (nearest_errortext, nearest_error))
                        nearest_data = False
                        nearest_cityavailable = False
                        logger.debug("nearest_data: %s ; nearest_cityavailable: %s" %
                                     (nearest_data, nearest_cityavailable))

                    except:
                        logger.debug("No error.")
                        nearest_error = False
                        logger.debug("nearest_error: %s" % nearest_error)

                # If we have the raw data, start parsing.
                if nearest_data is True and nearest_error is False:
                    logger.debug("nearest_data is True, parsing data...")
                    try:
                        nearest_cityname = nearest_json['geonames'][0]['name']
                        nearest_citycountry = nearest_json['geonames'][0]['countryName']
                        logger.debug("nearest_cityname: %s ; nearest_citycountry: %s" %
                                     (nearest_cityname, nearest_citycountry))
                        nearest_kmdistance = float(nearest_json['geonames'][0]['distance'])
                        nearest_city = nearest_cityname + ", " + nearest_citycountry
                        logger.debug("nearest_kmdistance: %s ; nearest_city: %s" %
                                     (nearest_kmdistance, nearest_city))
                        nearest_cityavailable = True
                        logger.debug("nearest_cityavailable: %s" % nearest_cityavailable)
                    except:
                        # If we can't parse data, set the cityavailable variable to False. This shows a different
                        # error message to the user.
                        printException_loggerwarn()
                        nearest_cityavailable = False
                        logger.debug("nearest_cityavailable: %s" % nearest_cityavailable)

                # Final data parsing if the nearest city is available. 
                if nearest_cityavailable is True and nearest_error is False:
                    logger.debug("nearest_cityavailable is true. Doing some conversions...")
                    # Convert distance into imperial units for 3% of the world, round down to single digit
                    nearest_midistance = nearest_kmdistance * 0.621371
                    logger.debug("nearest_midistance: %s" % nearest_midistance)
                    nearest_kmdistance = round(nearest_kmdistance, 1)
                    nearest_midistance = round(nearest_midistance, 1)
                    logger.debug("nearest_kmdistance: %s ; nearest_midistance: %s" %
                                 (nearest_kmdistance, nearest_midistance))
                    nearest_kmdistance = str(nearest_kmdistance)
                    nearest_midistance = str(nearest_midistance)
                    logger.info("Converted nearest_kmdistance and nearest_midistance to str")
            else:
                logger.debug("closest city is disabled.")

            # Prefix direction cardinals to the lat/lon
            if stormlat >= 0:
                stormlat = str(stormlat) + "° N"
            elif stormlat <= 0:
                stormlat = abs(stormlat)
                stormlat = str(stormlat) + "° S"
            if stormlon >= 0:
                stormlon = str(stormlon) + "° E"
            elif stormlon <= 0:
                stormlon = abs(stormlon)
                stormlon = str(stormlon) + "° W"

            logger.debug("stormlat: %s ; stormlon: %s" %
                         (stormlat, stormlon))
            stormtype = data['Current']['Category']
            stormcat = data['Current']['SaffirSimpsonCategory']
            logger.debug("stormtype: %s ; stormcat: %s" %
                         (stormtype, stormcat))
            # Instead of the category being "Hurricane", make it "Category x hurricane"
            if stormtype == "Hurricane":
                logger.info("Storm type is 'Hurricane'. Making some modifications...")
                stormcat = int(stormcat)
                for x in range(1,6):
                    logger.debug("x: %s" % x)
                    if x == stormcat:
                        logger.info("We found a match. x equaled stormcat.")
                        stormtype = "Category " + str(x) + " Hurricane"
                        logger.debug("stormtype: %s" % stormtype)
            stormtime = data['Current']['Time']['pretty']
            stormwindspeedmph = str(data['Current']['WindSpeed']['Mph'])
            logger.debug("stormtime: %s ; stormwindspeedmph: %s" %
                         (stormtime, stormwindspeedmph))
            stormwindspeedkph = str(data['Current']['WindSpeed']['Kph'])
            stormwindspeedkts = str(data['Current']['WindSpeed']['Kts'])
            logger.debug("stormwindspeedkph: %s ; stormwindspeedkts: %s" %
                         (stormwindspeedkph, stormwindspeedkts))
            stormgustspeedmph = str(data['Current']['WindGust']['Mph'])
            stormgustspeedkph = str(data['Current']['WindGust']['Kph'])
            logger.debug("stormgustspeedmph: %s ; stormgustspeedkph: %s" %
                         (stormgustspeedmph, stormgustspeedkph))
            stormgustspeedkts = str(data['Current']['WindGust']['Kts'])
            stormdirectionmph = str(data['Current']['Fspeed']['Mph'])
            logger.debug("stormgustspeedkts: %s ; stormdirectionmph: %s" %
                         (stormgustspeedkts, stormdirectionmph))
            stormdirectionkph = str(data['Current']['Fspeed']['Kph'])
            stormdirectionkts = str(data['Current']['Fspeed']['Kts'])
            logger.debug("stormdirectionkph: %s ; stormdirectionkts: %s" %
                         (stormdirectionkph, stormdirectionkts))
            stormdirection = data['Current']['Movement']['Text']
            stormdirectiondegrees = str(data['Current']['Movement']['Degrees'])
            logger.debug("stormdirection: %s ; stormdirectiondegrees: %s" %
                         (stormdirection, stormdirectiondegrees))
            stormpressuremb = str(data['Current']['Pressure']['mb'])
            stormpressureinches = str(data['Current']['Pressure']['inches'])
            logger.debug("stormpressuremb: %s ; stormpressureinches: %s" %
                         (stormpressuremb, stormpressureinches))
            if stormpressuremb == "None":
                stormpressuredataavail = False
                logger.warning("No pressure data is available.")
            else:
                stormpressuredataavail = True
            logger.debug("stormpressuredataavail: %s" % stormpressuredataavail)
            print(Fore.YELLOW + Style.BRIGHT + stormname + ":")
            print(Fore.YELLOW + Style.BRIGHT + "Last updated: " + Fore.CYAN + Style.BRIGHT + stormtime)
            print(Fore.YELLOW + Style.BRIGHT + "Storm Type: " + Fore.CYAN + Style.BRIGHT + stormtype)
            print(Fore.YELLOW + Style.BRIGHT + "Wind speed: " + Fore.CYAN + Style.BRIGHT + stormwindspeedmph + " mph ("
                  + stormwindspeedkph + " kph, " + stormwindspeedkts + " kts)")
            print(Fore.YELLOW + Style.BRIGHT + "Wind Gust: " + Fore.CYAN + Style.BRIGHT + stormgustspeedmph + " mph ("
                  + stormgustspeedkph + " kph, " + stormgustspeedkts + " kts)")
            print(Fore.YELLOW + Style.BRIGHT + "Storm Movement: " + Fore.CYAN + Style.BRIGHT + "Moving to the " +
                  stormdirection + " (" + stormdirectiondegrees + "°) at " + stormdirectionmph + " mph ("
                  + stormdirectionkph + " kph, " + stormdirectionkts + " kts)")
            if stormpressuredataavail == True:
                print(Fore.YELLOW + Style.BRIGHT + "Pressure: " + Fore.CYAN + Style.BRIGHT + stormpressuremb + " mb ("
                      + stormpressureinches + " inHg)")
            print(Fore.YELLOW + Style.BRIGHT + "Location: " + Fore.CYAN + Style.BRIGHT + stormlat + ", " + stormlon)
            if hurricanenearestcity_enabled is True:
                if nearest_error is True and nearest_data is False:
                    print(Fore.RED + Style.BRIGHT + "Nearest city error: " + Fore.CYAN + Style.BRIGHT + nearest_errortext)
                elif nearest_data is False:
                    print(Fore.YELLOW + Style.BRIGHT + "No data is available for this tropical storm's nearest city.")
                elif nearest_data is True and nearest_cityavailable is False:
                    print(Fore.YELLOW + Style.BRIGHT + "This tropical system is further than 300 km (186.411 mi) from a city.")
                elif nearest_data is True and nearest_cityavailable is True:
                    print(Fore.YELLOW + Style.BRIGHT + "Nearest city: " + Fore.CYAN + Style.BRIGHT + nearest_midistance + " mi (" + nearest_kmdistance + " km)"
                          + " away from " + nearest_city + ".")
            currentstormiterations += 1
            logger.debug("currentstormiterations: %s" % currentstormiterations)
            if user_showCompletedIterations is True:
                print(Fore.YELLOW + Style.BRIGHT + "Completed iterations: " + Fore.CYAN + Style.BRIGHT + "%s/%s" %
                      (currentstormiterations, activestorms))

            # <--- Current storm data to forecast --->
            if activestorms > 1 and currentstormiterations != activestorms:
                logger.info("activestorms > 1 and currentstormiterations != activestorms.")
                print("")
                print(Fore.RED + Style.BRIGHT + "Press enter to view forecast data for " + stormname + ".",
                      Fore.RED + Style.BRIGHT + "Enter 'nextstorm' to view data for the next storm. Press Control + C to exit",
                      Fore.RED + Style.BRIGHT + "to the main menu.", sep="\n")
                try:
                    selection = input("Input here: ").lower()
                    print("")
                except KeyboardInterrupt:
                    logger.info("Breaking to main menu...")
                    print("")
                    break
                if selection == "nextstorm":
                    continue
                else:
                    if selection != "":
                        print(Fore.RED + Style.BRIGHT + "Couldn't understand your input. Listing forecast data...")
                        selection = ""
            elif activestorms == 1 or currentstormiterations == activestorms:
                logger.info("activestorms is 1 or currentstormiterations is activestorms.")
                print("")
                print(Fore.RED + Style.BRIGHT + "Press enter to view forecast data for " + stormname + ".",
                      Fore.RED + Style.BRIGHT + "Otherwise, enter 'exit' or press Control + C to exit to the main menu.", sep="\n")
                try:
                    selection = input("Input here: ").lower()
                    print("")
                except KeyboardInterrupt:
                    logger.info("Breaking to the main menu...")
                    print("")
                    break

                if selection == "exit":
                    break
                else:
                    if selection != "":
                        print(Fore.RED + Style.BRIGHT + "Couldn't understand your input. Listing forecast data...")
                        selection = ""

            # <--- Where the forecast is looped into --->
            if selection == "":
                # Do the classic "how many iterations?"
                hurricanetotaliterations = 0
                hurricanecurrentiterations = 0
                for loops in data['forecast']:
                    hurricanetotaliterations += 1
                logger.debug("hurricanetotaliterations: %s" % hurricanetotaliterations)
                if hurricanetotaliterations <= 5:
                    hurricane_hasExtDataInForecast = False
                elif hurricanetotaliterations >= 6:
                    hurricane_hasExtDataInForecast = True

                print(Fore.YELLOW + Style.BRIGHT + "Here's the forecast for " + stormname + ".")
                for forecast in data['forecast']:
                    print("")
                    hurricaneforecasttime = forecast['ForecastHour']
                    logger.debug("hurricaneforecasttime: %s" % hurricaneforecasttime)
                    # Properly parse the time
                    if hurricaneforecasttime == "12HR":
                        hurricaneforecasttime = "12 hours ahead"
                    elif hurricaneforecasttime == "24HR":
                        hurricaneforecasttime = "24 hours ahead"
                    elif hurricaneforecasttime == "36HR":
                        hurricaneforecasttime = "36 hours ahead"
                    elif hurricaneforecasttime == "48HR":
                        hurricaneforecasttime = "48 hours ahead"
                    elif hurricaneforecasttime == "72HR":
                        hurricaneforecasttime = "72 hours ahead"
                    elif hurricaneforecasttime == "4DAY":
                        hurricaneforecasttime = "4 days ahead"
                    elif hurricaneforecasttime == "5DAY":
                        hurricaneforecasttime = "5 days ahead"

                    logger.debug("hurricaneforecasttime: %s ; hurricane_hasExtDataInForecast: %s" %
                                 (hurricaneforecasttime, hurricane_hasExtDataInForecast))
                    hurricaneforecasttime_detail = forecast['Time']['pretty']
                    hurricaneforecast_lat = float(forecast['lat'])
                    logger.debug("hurricaneforecasttime_detail: %s ; hurricaneforecast_lat: %s" %
                                 (hurricaneforecasttime_detail, hurricaneforecast_lat))
                    hurricaneforecast_laturl = str(hurricaneforecast_lat)
                    hurricaneforecast_lon = float(forecast['lon'])
                    logger.debug("hurricaneforecast_laturl: %s ; hurricaneforecast_lon: %s" %
                                 (hurricaneforecast_laturl, hurricaneforecast_lon))
                    hurricaneforecast_lonurl = str(hurricaneforecast_lon)
                    logger.debug("hurricaneforecast_lonurl: %s" % hurricaneforecast_lonurl)
                    nearesturl = 'http://api.geonames.org/findNearbyPlaceNameJSON?lat=' + hurricaneforecast_laturl + '&lng=' + hurricaneforecast_lonurl + '&username=' + geonames_apiusername + '&radius=300&maxRows=1' + hurricane_citiesamp
                    logger.debug("nearesturl: %s" % nearesturl)

                    if hurricaneforecast_lat >= 0:
                        hurricaneforecast_lat = str(hurricaneforecast_lat) + "° N"
                    elif hurricaneforecast_lat <= 0:
                        hurricaneforecast_lat = abs(hurricaneforecast_lat)
                        hurricaneforecast_lat = str(hurricaneforecast_lat) + "° S"
                    if hurricaneforecast_lon >= 0:
                        hurricaneforecast_lon = str(hurricaneforecast_lon) + "° E"
                    elif hurricaneforecast_lon <= 0:
                        hurricaneforecast_lon = abs(hurricaneforecast_lon)
                        hurricaneforecast_lon = str(hurricaneforecast_lon) + "° W"

                    logger.debug("hurricaneforecast_lat: %s ; hurricaneforecast_lon: %s" %
                                 (hurricaneforecast_lat, hurricaneforecast_lon))
                    hurricaneforecast_category = int(forecast['SaffirSimpsonCategory'])
                    logger.debug("hurricaneforecast_category: %s" % hurricaneforecast_category)
                    if hurricaneforecast_category >= 1:
                        logger.info("Category is above 1. Making storm type pretty...")
                        # Totally unnecessary, but it works.
                        for x in range(1, 6):
                            logger.debug("x: %s" % x)
                            if x == hurricaneforecast_category:
                                logger.info("We found a match. x equaled stormcat.")
                                hurricaneforecast_type = "Category " + str(x) + " Hurricane"
                    elif hurricaneforecast_category == 0:
                        hurricaneforecast_type = "Tropical Storm"
                    elif hurricaneforecast_category == -1:
                        hurricaneforecast_type = "Subtropical Storm"
                    elif hurricaneforecast_category == -2:
                        hurricaneforecast_type = "Tropical Depression"
                    elif hurricaneforecast_category == -3:
                        hurricaneforecast_type = "Extratropical"
                    elif hurricaneforecast_category == -4:
                        hurricaneforecast_type = "Invest"
                    elif hurricaneforecast_category == -5:
                        hurricaneforecast_type = "Remnants"
                    logger.debug("hurricaneforecast_type: %s" % hurricaneforecast_type)

                    hurricaneforecast_windmph = str(forecast['WindSpeed']['Mph'])
                    hurricaneforecast_windkph = str(forecast['WindSpeed']['Kph'])
                    logger.debug("hurricaneforecast_windmph: %s ; hurricaneforecast_windkph: %s" %
                                 (hurricaneforecast_windmph, hurricaneforecast_windkph))
                    hurricaneforecast_windkts = str(forecast['WindSpeed']['Kts'])
                    hurricaneforecast_gustmph = str(forecast['WindGust']['Mph'])
                    logger.debug("hurricaneforecast_windkts: %s ; hurricaneforecast_gustmph: %s" %
                                 (hurricaneforecast_windkts, hurricaneforecast_gustmph))
                    hurricaneforecast_gustkph = str(forecast['WindGust']['Kph'])
                    hurricaneforecast_gustkts = str(forecast['WindGust']['Kts'])
                    logger.debug("hurricaneforecast_gustkph: %s ; hurricaneforecast_gustkts: %s" %
                                 (hurricaneforecast_gustkph, hurricaneforecast_gustkts))

                    if hurricanenearestcity_fenabled is True:
                        logger.info("hurricanenearestcity_fenabled is True, loading up data...")
                        try:
                            nearestJSON = requests.get(nearesturl)
                            logger.debug("nearestJSON fetched, result: %s" % nearestJSON)
                            nearest_json = json.loads(nearestJSON.text)
                            if jsonVerbosity == True:
                                logger.debug("nearest_json: %s" % nearest_json)
                            else:
                                logger.debug("nearest_json loaded.")
                            nearest_data = True
                            logger.debug("nearest_data: %s" % nearest_data)
                        except:
                            printException_loggerwarn()
                            nearest_data = False
                            logger.debug("nearest_data: %s" % nearest_data)

                        if nearest_data is True:
                            try:
                                errorvalue = str(nearest_json['status']['value'])
                                if errorvalue == "10":
                                    nearest_errortext = "The username for the API wasn't authorized."
                                elif errorvalue == "11":
                                    nearest_errortext = "The record doesn't exist."
                                elif errorvalue == "12":
                                    nearest_errortext = "An undefined error occurred."
                                elif errorvalue == "13":
                                    nearest_errortext = "The database timed out."
                                elif errorvalue == "15":
                                    nearest_errortext = "No result was found."
                                elif errorvalue == "18":
                                    nearest_errortext = "The daily limit of lookups was exceeded. Please try again tomorrow."
                                elif errorvalue == "19":
                                    nearest_errortext = "The hourly limit of lookups was exceeded. Please try again in an hour."
                                elif errorvalue == "20":
                                    nearest_errortext = "The weekly limit of lookups was exceeded. Please try again at the start of next week."
                                elif errorvalue == "22":
                                    nearest_errortext = "The geonames server was overloaded. Please try again in a bit."
                                else:
                                    nearest_errortext = "A strange error occurred. That's strange!"
                                nearest_error = True
                                logger.debug("nearest_errortext: %s ; nearest_error: %s" %
                                             (nearest_errortext, nearest_error))
                                nearest_data = False
                                logger.debug("nearest_data: %s" % nearest_data)
                            except:
                                logger.debug("No error.")
                                nearest_error = False
                                logger.debug("nearest_error: %s" % nearest_error)

                        if nearest_data is True:
                            logger.debug("nearest_data is True, parsing data...")
                            try:
                                nearest_cityname = nearest_json['geonames'][0]['name']
                                nearest_citycountry = nearest_json['geonames'][0]['countryName']
                                logger.debug("nearest_cityname: %s ; nearest_citycountry: %s" %
                                             (nearest_cityname, nearest_citycountry))
                                nearest_kmdistance = float(nearest_json['geonames'][0]['distance'])
                                nearest_city = nearest_cityname + ", " + nearest_citycountry
                                logger.debug("nearest_kmdistance: %s ; nearest_city: %s" %
                                             (nearest_kmdistance, nearest_city))
                                nearest_cityavailable = True
                                logger.debug("nearest_cityavailable: %s" % nearest_cityavailable)
                            except:
                                printException_loggerwarn()
                                nearest_cityavailable = False
                                logger.debug("nearest_cityavailable: %s" % nearest_cityavailable)

                        if nearest_cityavailable is True:
                            logger.debug("nearest_cityavailable is true. Doing some conversions...")
                            # Convert distance into imperial units for 3% of the world, round down to single digit
                            nearest_midistance = nearest_kmdistance * 0.621371
                            logger.debug("nearest_midistance: %s" % nearest_midistance)
                            nearest_kmdistance = round(nearest_kmdistance, 1)
                            nearest_midistance = round(nearest_midistance, 1)
                            logger.debug("nearest_kmdistance: %s ; nearest_midistance: %s" %
                                         (nearest_kmdistance, nearest_midistance))
                            nearest_kmdistance = str(nearest_kmdistance)
                            nearest_midistance = str(nearest_midistance)
                            logger.info("Converted nearest_kmdistance and nearest_midistance to str")
                    else:
                        logger.debug("closest city is disabled.")

                    print(Fore.YELLOW + Style.BRIGHT + hurricaneforecasttime_detail + " (" + hurricaneforecasttime + ")")
                    print(Fore.YELLOW + Style.BRIGHT + "Storm Type: " + Fore.CYAN + Style.BRIGHT + hurricaneforecast_type)
                    print(Fore.YELLOW + Style.BRIGHT + "Wind Speed: " + Fore.CYAN + Style.BRIGHT + hurricaneforecast_windmph + " mph (" + hurricaneforecast_windkph + " kph, "
                          + hurricaneforecast_windkts + " kts)")
                    print(Fore.YELLOW + Style.BRIGHT + "Wind Gusts: " + Fore.CYAN + Style.BRIGHT + hurricaneforecast_gustmph + " mph (" + hurricaneforecast_gustkph + " kph, "
                          + hurricaneforecast_gustkts + " kts)")
                    print(Fore.YELLOW + Style.BRIGHT + "Location: " + Fore.CYAN + Style.BRIGHT + hurricaneforecast_lat + ", " + hurricaneforecast_lon)
                    if hurricanenearestcity_fenabled is True:
                        if nearest_error is True and nearest_data is False:
                            print(Fore.RED + Style.BRIGHT + "Nearest city error: " + Fore.CYAN + Style.BRIGHT + nearest_errortext)
                        elif nearest_data is False:
                            print(Fore.YELLOW + Style.BRIGHT + "No data is available for this tropical storm's nearest city.")
                        elif nearest_data is True and nearest_cityavailable is False:
                            print(
                                Fore.YELLOW + Style.BRIGHT + "This tropical system is further than 300 km (186.411 mi) from a city.")
                        elif nearest_data is True and nearest_cityavailable is True:
                            print(
                                Fore.YELLOW + Style.BRIGHT + "Nearest city: " + Fore.CYAN + Style.BRIGHT + nearest_midistance + " mi (" + nearest_kmdistance + " km)"
                                + " away from " + nearest_city + ".")
                    hurricanecurrentiterations += 1
                    logger.debug("hurricanecurrentiterations: %s" % hurricanecurrentiterations)
                    if user_showCompletedIterations is True:
                        print(Fore.YELLOW + Style.BRIGHT + "Completed iterations: " + Fore.CYAN + Style.BRIGHT + "%s/%s" %
                              (hurricanecurrentiterations, hurricanetotaliterations))

                    # <--- Forecast data ends, loop into extended forecast data --->
                    # Have a detection for if extended data is available here.

                    # Basically says if activestorms are two and above, and we're not on the last iteration, and we've gone through all
                    # loops, and 4/5 day forecast data was not before the extended forecast enter this dialogue.
                    if (activestorms > 1 and currentstormiterations != activestorms and hurricanecurrentiterations == hurricanetotaliterations):
                        logger.debug("activestorms > 1, currentstormiterations != activestorms, hurricanecurrentiterations == hurricanetotaliterations")
                        if hurricane_hasExtDataInForecast == False:
                            logger.debug("hurricane_hasExtDataInForecast = False")
                            print("")
                            print(Fore.RED + Style.BRIGHT + "Press enter to view the extended forecast for " + stormname + ".",
                                  Fore.RED + Style.BRIGHT + "Enter 'nextstorm' to view details about the next storm.",
                                  Fore.RED + Style.BRIGHT + "Otherwise, press Control + C twice to exit to the main menu.", sep="\n")

                            try:
                                forecastselection = input("Input here: ").lower()
                                logger.debug("forecastselection: %s" % forecastselection)
                                print("")
                            except KeyboardInterrupt:
                                logger.debug("Breaking to the main menu.")
                                print("")
                                break

                            if forecastselection == "nextstorm":
                                continue
                            else:
                                if forecastselection != "":
                                    print(Fore.RED + Style.BRIGHT + "Your input couldn't be understood. Listing extended forecast data.")
                                    forecastselection = ""
                        elif hurricane_hasExtDataInForecast == True:
                            logger.debug("hurricane_hasExtDataInForecast - True")
                            print("")
                            print(Fore.RED + Style.BRIGHT + "Press enter to view data for the next storm.",
                                  Fore.RED + Style.BRIGHT + "Otherwise, press Control + C to exit to the main menu.", sep="\n")

                            try:
                                forecastselection = input("Input here: ").lower()
                                logger.debug("forecastselection: %s" % forecastselection)
                                print("")
                            except KeyboardInterrupt:
                                logger.debug("Breaking to the main menu.")
                                print("")
                                break

                            if forecastselection != "":
                                print(Fore.RED + Style.BRIGHT + "Your input could not be understood. Listing data for the next storm...")
                            continue

                    # This says if activestorms are just one, or if we're on the last storm, and we've gone through all loops, and 4/5 day
                    # forecast data was not before the extended forecast, enter this dialogue.
                    elif (currentstormiterations == activestorms and hurricanecurrentiterations == hurricanetotaliterations):
                        logger.debug("activestorms is 1, or currentstormiterations == activestorms and hurricanecurrentiterations == hurricanetotaliterations")
                        print("")
                        if hurricane_hasExtDataInForecast == False:
                            logger.debug("hurricane_hasExtDataInForecast is False")
                            print(Fore.RED + Style.BRIGHT + "Press enter to see extended forecast for " + stormname + ".",
                            Fore.RED + Style.BRIGHT + "Otherwise, enter 'exit' or press Control + C to exit to the main menu.", sep='\n')
                            try:
                                forecastselection = input("Input here: ").lower()
                                logger.debug("forecastselection: %s" % forecastselection)
                            except:
                                logger.debug("Breaking to the main menu.")
                                print("")
                                break

                            if forecastselection != "":
                                print(Fore.RED + Style.BRIGHT + "Your input could not be understood. Listing extended forecast data.")

                        elif hurricane_hasExtDataInForecast == True:
                            logger.debug("hurricane_hasExtDataInForecast is True.")
                            break
                    else:
                        # This has to be none for this entire thing to work.
                        forecastselection = "none"


                    if forecastselection == "":
                        extendedforecastloops = 0
                        extendedcurrentloops = 0
                        logger.debug("extendedforecastloops: %s ; extendedcurrentloops: %s" %
                                     (extendedforecastloops, extendedcurrentloops))
                        for extforecast in data['ExtendedForecast']:
                            extendedforecastloops += 1

                        if extendedforecastloops == 0 and currentstormiterations == activestorms:
                            print(Fore.RED + Style.BRIGHT + "Extended forecast data is not available for " + stormname + ".",
                                  Fore.RED + Style.BRIGHT + "Since this is the last storm, press enter to exit.", sep='\n')
                            input()
                            break

                        elif extendedforecastloops == 0:
                            print(Fore.RED + Style.BRIGHT + "Extended forecast data is not available for " + stormname + ".",
                                  Fore.RED + Style.BRIGHT + "Press enter to view data for the next storm. Press Control + C to exit to the main menu.", sep="\n")
                            try:
                                extnodata = input("Input here: ").lower()
                                print("")
                                logger.debug("extnodata: %s" % extnodata)
                            except KeyboardInterrupt:
                                logger.debug("Breaking to main menu.")
                                print("")
                                break
                        # If we're on the last storm, and there isn't an extended forecast, press enter to exit.

                        for extforecast in data['ExtendedForecast']:
                            print("")
                            hurricaneextforecasttime = extforecast['ForecastHour']
                            logger.debug("hurricaneextforecasttime: %s" % hurricaneextforecasttime)
                            # Properly parse the time
                            if hurricaneextforecasttime == "4DAY":
                                hurricaneextforecasttime = "4 days ahead"
                            elif hurricaneextforecasttime == "5DAY":
                                hurricaneextforecasttime = "5 days ahead"

                            logger.debug("hurricaneextforecasttime: %s" % hurricaneextforecasttime)
                            hurricaneextforecasttime_detail = extforecast['Time']['pretty']
                            hurricaneextforecast_lat = float(extforecast['lat'])
                            hurricaneextforecast_urllat = str(hurricaneextforecast_lat)
                            hurricaneextforecast_lon = float(extforecast['lon'])
                            hurricaneextforecast_urllon = str(hurricaneextforecast_lon)
                            logger.debug("hurricaneextforecasttime_detail: %s ; hurricaneextforecast_lat: %s" %
                                         (hurricaneextforecasttime_detail, hurricaneextforecast_lat))
                            logger.debug("hurricaneextforecast_lon: %s" % hurricaneextforecast_lon)
                            nearesturl = 'http://api.geonames.org/findNearbyPlaceNameJSON?lat=' + hurricaneextforecast_urllat + '&lng=' + hurricaneextforecast_urllon + '&username=' + geonames_apiusername + '&radius=300&maxRows=1' + hurricane_citiesamp

                            if hurricaneextforecast_lat >= 0:
                                hurricaneextforecast_lat = str(hurricaneextforecast_lat) + "° N"
                            elif hurricaneextforecast_lat <= 0:
                                hurricaneextforecast_lat = abs(hurricaneextforecast_lat)
                                hurricaneextforecast_lat = str(hurricaneextforecast_lat) + "° S"
                            if hurricaneextforecast_lon >= 0:
                                hurricaneextforecast_lon = str(hurricaneextforecast_lon) + "° E"
                            elif hurricaneextforecast_lon <= 0:
                                hurricaneextforecast_lon = abs(hurricaneextforecast_lon)
                                hurricaneextforecast_lon = str(hurricaneextforecast_lon) + "° W"

                            logger.debug("hurricaneextforecast_lat: %s ; hurricaneextforecast_lon: %s" %
                                         (hurricaneextforecast_lat, hurricaneextforecast_lon))
                            hurricaneextforecast_category = int(extforecast['SaffirSimpsonCategory'])
                            logger.debug("hurricaneextforecast_category: %s" % hurricaneextforecast_category)
                            if hurricaneextforecast_category >= 1:
                                logger.info("Category is above 1. Making storm type pretty...")
                                # Totally unnecessary, but it works.
                                for x in range(1, 6):
                                    logger.debug("x: %s" % x)
                                    if x == hurricaneextforecast_category:
                                        logger.info("We found a match. x equaled stormcat.")
                                        hurricaneextforecast_type = "Category " + str(x) + " Hurricane"
                            elif hurricaneextforecast_category == 0:
                                hurricaneextforecast_type = "Tropical Storm"
                            elif hurricaneextforecast_category == -1:
                                hurricaneextforecast_type = "Subtropical Storm"
                            elif hurricaneextforecast_category == -2:
                                hurricaneextforecast_type = "Tropical Depression"
                            elif hurricaneextforecast_category == -3:
                                hurricaneextforecast_type = "Extratropical"
                            elif hurricaneextforecast_category == -4:
                                hurricaneextforecast_type = "Invest"
                            elif hurricaneextforecast_category == -5:
                                hurricaneextforecast_type = "Remnants"

                            hurricaneextforecast_windmph = str(extforecast['WindSpeed']['Mph'])
                            hurricaneextforecast_windkph = str(extforecast['WindSpeed']['Kph'])
                            logger.debug("hurricaneextforecast_windmph: %s ; hurricaneextforecast_windkph: %s" %
                                         (hurricaneextforecast_windmph, hurricaneextforecast_windkph))
                            hurricaneextforecast_windkts = str(extforecast['WindSpeed']['Kts'])
                            hurricaneextforecast_gustmph = str(extforecast['WindGust']['Mph'])
                            logger.debug("hurricaneextforecast_windkts: %s ; hurricaneextforecast_gustmph: %s" %
                                         (hurricaneextforecast_windkts, hurricaneextforecast_gustmph))
                            hurricaneextforecast_gustkph = str(extforecast['WindGust']['Kph'])
                            hurricaneextforecast_gustkts = str(extforecast['WindGust']['Kts'])
                            logger.debug("hurricaneextforecast_gustkph: %s ; hurricaneextforecast_gustkts: %s" %
                                         (hurricaneextforecast_gustkph, hurricaneextforecast_gustkts))

                            if hurricanenearestcity_fenabled is True:
                                logger.info("hurricanenearestcity_fenabled is True, loading up data...")
                                try:
                                    nearestJSON = requests.get(nearesturl)
                                    logger.debug("nearestJSON fetched, result: %s" % nearestJSON)
                                    nearest_json = json.loads(nearestJSON.text)
                                    if jsonVerbosity == True:
                                        logger.debug("nearest_json: %s" % nearest_json)
                                    else:
                                        logger.debug("nearest_json loaded.")
                                    nearest_data = True
                                    logger.debug("nearest_data: %s" % nearest_data)
                                except:
                                    printException_loggerwarn()
                                    nearest_data = False
                                    logger.debug("nearest_data: %s" % nearest_data)

                                if nearest_data is True:
                                    try:
                                        errorvalue = str(nearest_json['status']['value'])
                                        if errorvalue == "10":
                                            nearest_errortext = "The username for the API wasn't authorized."
                                        elif errorvalue == "11":
                                            nearest_errortext = "The record doesn't exist."
                                        elif errorvalue == "12":
                                            nearest_errortext = "An undefined error occurred."
                                        elif errorvalue == "13":
                                            nearest_errortext = "The database timed out."
                                        elif errorvalue == "15":
                                            nearest_errortext = "No result was found."
                                        elif errorvalue == "18":
                                            nearest_errortext = "The daily limit of lookups was exceeded. Please try again tomorrow."
                                        elif errorvalue == "19":
                                            nearest_errortext = "The hourly limit of lookups was exceeded. Please try again in an hour."
                                        elif errorvalue == "20":
                                            nearest_errortext = "The weekly limit of lookups was exceeded. Please try again at the start of next week."
                                        elif errorvalue == "22":
                                            nearest_errortext = "The geonames server was overloaded. Please try again in a bit."
                                        else:
                                            nearest_errortext = "A strange error occurred. That's strange!"
                                        nearest_error = True
                                        logger.debug("nearest_errortext: %s ; nearest_error: %s" %
                                                     (nearest_errortext, nearest_error))
                                        nearest_data = False
                                        logger.debug("nearest_data: %s" % nearest_data)
                                    except:
                                        logger.debug("No error.")
                                        nearest_error = False
                                        logger.debug("nearest_error: %s" % nearest_error)

                                if nearest_data is True:
                                    logger.debug("nearest_data is True, parsing data...")
                                    try:
                                        nearest_cityname = nearest_json['geonames'][0]['name']
                                        nearest_citycountry = nearest_json['geonames'][0]['countryName']
                                        logger.debug("nearest_cityname: %s ; nearest_citycountry: %s" %
                                                     (nearest_cityname, nearest_citycountry))
                                        nearest_kmdistance = float(nearest_json['geonames'][0]['distance'])
                                        nearest_city = nearest_cityname + ", " + nearest_citycountry
                                        logger.debug("nearest_kmdistance: %s ; nearest_city: %s" %
                                                     (nearest_kmdistance, nearest_city))
                                        nearest_cityavailable = True
                                        logger.debug("nearest_cityavailable: %s" % nearest_cityavailable)
                                    except:
                                        printException_loggerwarn()
                                        nearest_cityavailable = False
                                        logger.debug("nearest_cityavailable: %s" % nearest_cityavailable)

                                if nearest_cityavailable is True:
                                    logger.debug("nearest_cityavailable is true. Doing some conversions...")
                                    # Convert distance into imperial units for 3% of the world, round down to single digit
                                    nearest_midistance = nearest_kmdistance * 0.621371
                                    logger.debug("nearest_midistance: %s" % nearest_midistance)
                                    nearest_kmdistance = round(nearest_kmdistance, 1)
                                    nearest_midistance = round(nearest_midistance, 1)
                                    logger.debug("nearest_kmdistance: %s ; nearest_midistance: %s" %
                                                 (nearest_kmdistance, nearest_midistance))
                                    nearest_kmdistance = str(nearest_kmdistance)
                                    nearest_midistance = str(nearest_midistance)
                                    logger.info("Converted nearest_kmdistance and nearest_midistance to str")
                            else:
                                logger.debug("closest city is disabled.")

                            print(Fore.YELLOW + Style.BRIGHT + hurricaneextforecasttime_detail + " (" + hurricaneextforecasttime + ")")
                            print(Fore.YELLOW + Style.BRIGHT + "Storm Type: " + Fore.CYAN + Style.BRIGHT + hurricaneextforecast_type)
                            print(
                                Fore.YELLOW + Style.BRIGHT + "Wind Speed: " + Fore.CYAN + Style.BRIGHT + hurricaneextforecast_windmph + " mph (" + hurricaneextforecast_windkph + " kph, "
                                + hurricaneextforecast_windkts + " kts)")
                            print(
                                Fore.YELLOW + Style.BRIGHT + "Wind Gusts: " + Fore.CYAN + Style.BRIGHT + hurricaneextforecast_gustmph + " mph (" + hurricaneextforecast_gustkph + " kph, "
                                + hurricaneextforecast_gustkts + " kts)")
                            print(Fore.YELLOW + Style.BRIGHT + "Location: " + Fore.CYAN + Style.BRIGHT + hurricaneextforecast_lat + ", " + hurricaneextforecast_lon)
                            if hurricanenearestcity_fenabled is True:
                                if nearest_error is True and nearest_data is False:
                                    print(Fore.RED + Style.BRIGHT + "Nearest city error: " + Fore.CYAN + Style.BRIGHT + nearest_errortext)
                                elif nearest_data is False:
                                    print(Fore.YELLOW + Style.BRIGHT + "No data is available for this tropical storm's nearest city.")
                                elif nearest_data is True and nearest_cityavailable is False:
                                    print(
                                        Fore.YELLOW + Style.BRIGHT + "This tropical system is further than 300 km (186.411 mi) from a city.")
                                elif nearest_data is True and nearest_cityavailable is True:
                                    print(
                                        Fore.YELLOW + Style.BRIGHT + "Nearest city: " + Fore.CYAN + Style.BRIGHT + nearest_midistance + " mi (" + nearest_kmdistance + " km)"
                                        + " away from " + nearest_city + ".")
                            extendedcurrentloops += 1
                            logger.debug("extendedcurrentloops: %s" % extendedcurrentloops)
                            if user_showCompletedIterations == True:
                                print(Fore.YELLOW + Style.BRIGHT + "Completed iterations: " + Fore.CYAN + Style.BRIGHT + "%s/%s" %
                                      (extendedcurrentloops, extendedforecastloops))

                            if extendedcurrentloops == extendedforecastloops:
                                logger.debug("extendedcurrentloops == extendedforecastloops")
                                print("")
                                if currentstormiterations != activestorms:
                                    logger.debug("currentstormiterations != activestorms")
                                    print(Fore.RED + Style.BRIGHT + "Press enter to view data for the next storm.",
                                          Fore.RED + Style.BRIGHT + "Otherwise, enter 'exit' or press Control + C to exit to the main menu.", sep='\n')

                                    try:
                                        extforecastinput = input("Input here: ").lower()
                                    except KeyboardInterrupt:
                                        logger.debug("Breaking to main menu...")
                                        print("")
                                        break

                                    if extforecastinput == "exit":
                                        print(Fore.RED + "Exiting to the main menu...")
                                        break
                                    else:
                                        if extforecastinput != "":
                                            print(Fore.RED + Style.BRIGHT + "Your input could not be understood. Viewing data for the next storm...")
                                        print("")
                                        continue
                                elif currentstormiterations == activestorms:
                                    logger.debug("currentstormiterations == activestorms")
                                    break
                        else:
                            continue


    elif moreoptions == "13":
        if favoritelocation_enabled is False:
            print("", Fore.RED + Style.BRIGHT + "To manage favorite locations, you'll need to enable the favorite locations feature.",
                  Fore.RED + Style.BRIGHT + "Would you like me to enable favorite locations for you?", sep="\n")
            enablefavoritelocations = input("Input here: ").lower()
            logger.debug("enablefavoritelocations: %s" % enablefavoritelocations)
            if enablefavoritelocations == "yes":
                config['FAVORITE LOCATIONS']['enabled'] = 'True'
                logger.info("FAVORITE LOCATIONS/enabled is now 'True'.")
                try:
                    with open('storage//config.ini', 'w') as configfile:
                        config.write(configfile)
                    print(Fore.YELLOW + Style.BRIGHT + "Favorite locations is now enabled, and will be operational when you next boot up PyWeather.")
                    continue
                except:
                    print(Fore.RED + Style.BRIGHT + "An issue occurred when trying to save new configuration options.",
                          Fore.RED + Style.BRIGHT + "Please enable favorite locations in the config file. In the FAVORITE LOCATIONS",
                          Fore.RED + Style.BRIGHT + "section, change enabled to True.")
                    continue
            elif enablefavoritelocations == "no":
                print(Fore.YELLOW + Style.BRIGHT + "Not enabling favorite locations. Returning to the main menu.",
                      "You can come back to this menu to reenable favorite locations, or go into your config file and",
                      "enable FAVORITE LOCATIONS/enabled (set it to True).", sep="\n")
                continue
            else:
                print(Fore.YELLOW + Style.BRIGHT + "Your input wasn't understood, and as such favorite locations will not be enabled.",
                      "You can come back to this menu to reenable favorite locations, or go into your config file and",
                      "enable FAVORITE LOCATIONS/enabled (set it to True).")

        while True:
            # Get up-to-date configuration information about favorite locations.
            spinner.start(text="Loading your favorite locations...")
            try:
                favoritelocation_1 = config.get('FAVORITE LOCATIONS', 'favloc1')
                favoritelocation_1d = favoritelocation_1
                favoritelocation_2 = config.get('FAVORITE LOCATIONS', 'favloc2')
                favoritelocation_2d = favoritelocation_2
                favoritelocation_3 = config.get('FAVORITE LOCATIONS', 'favloc3')
                favoritelocation_3d = favoritelocation_3
                favoritelocation_4 = config.get('FAVORITE LOCATIONS', 'favloc4')
                favoritelocation_4d = favoritelocation_4
                favoritelocation_5 = config.get('FAVORITE LOCATIONS', 'favloc5')
                favoritelocation_5d = favoritelocation_5

                favoritelocation_1data = config.get('FAVORITE LOCATIONS', 'favloc1_data')
                favoritelocation_2data = config.get('FAVORITE LOCATIONS', 'favloc2_data')
                favoritelocation_3data = config.get('FAVORITE LOCATIONS', 'favloc3_data')
                favoritelocation_4data = config.get('FAVORITE LOCATIONS', 'favloc4_data')
                favoritelocation_5data = config.get('FAVORITE LOCATIONS', 'favloc5_data')

            except:
                spinner.fail(text="Failed to load your favorite locations!")
                print("")
                print(Fore.RED + Style.BRIGHT + "An error with your configuration file occurred when",
                      Fore.RED + Style.BRIGHT + "we tried to refresh current location information. For safety,",
                      Fore.RED + Style.BRIGHT +"the favorite location configurator will be exited out of.")
                printException()
                break

            logger.debug("favoritelocation_1: %s ; favoritelocation_1d: %s" %
                         (favoritelocation_1, favoritelocation_1d))
            logger.debug("favoritelocation_2: %s ; favoritelocation_2d: %s" %
                         (favoritelocation_2, favoritelocation_2d))
            logger.debug("favoritelocation_3: %s ; favoritelocation_3d: %s" %
                         (favoritelocation_3, favoritelocation_3d))
            logger.debug("favoritelocation_4: %s ; favoritelocation_4d: %s" %
                         (favoritelocation_4, favoritelocation_4d))
            logger.debug("favoritelocation_5: %s ; favoritelocation_5d: %s" %
                         (favoritelocation_5, favoritelocation_5d))

            logger.debug("favoritelocation_1data: %s ; favoritelocation_2data: %s" %
                         (favoritelocation_1data, favoritelocation_2data))
            logger.debug("favoritelocation_3data: %s ; favoritelocation_4data: %s" %
                         (favoritelocation_3data, favoritelocation_4data))
            logger.debug("favoritelocation_5data: %s" % favoritelocation_5data)

            if "pws:" in favoritelocation_1d:
                # Delete pws: from the display string
                favoritelocation_1d = favoritelocation_1d[4:]
                favoritelocation_1d = "PWS " + favoritelocation_1d.upper()
                logger.debug("favoritelocation_1d: %s" % favoritelocation_1d)

            if "pws:" in favoritelocation_2d:
                # Delete pws: from the display string
                favoritelocation_2d = favoritelocation_2d[4:]
                favoritelocation_2d = "PWS " + favoritelocation_2d.upper()
                logger.debug("favoritelocation_2d: %s" % favoritelocation_2d)

            if "pws:" in favoritelocation_3d:
                # Delete pws: from the display string
                favoritelocation_3d = favoritelocation_3d[4:]
                favoritelocation_3d = "PWS " + favoritelocation_3d.upper()
                logger.debug("favoritelocation_3d: %s" % favoritelocation_3d)

            if "pws:" in favoritelocation_4d:
                # Delete pws: from the display string
                favoritelocation_4d = favoritelocation_4d[4:]
                favoritelocation_4d = "PWS " + favoritelocation_4d.upper()
                logger.debug("favoritelocation_4d: %s" % favoritelocation_4d)

            if "pws:" in favoritelocation_5d:
                # Delete pws: from the display string
                favoritelocation_5d = favoritelocation_5d[4:]
                favoritelocation_5d = "PWS " + favoritelocation_5d.upper()
                logger.debug("favoritelocation_5d: %s" % favoritelocation_5d)

            if favoritelocation_1d.find("arpt:") == 0 or favoritelocation_1d.find("airport:") == 0:
                # Do that same ol' thing at boot. See if the data text is not None, and show
                # the display location as that additional data if so.
                if favoritelocation_1data != "None":
                    favoritelocation_1d = favoritelocation_1data
                else:
                    favoritelocation_1d = favoritelocation_1.strip("airport:") + " Airport"

                logger.debug("favoritelocation_1d: %s" % favoritelocation_1d)

            if favoritelocation_2d.find("arpt:") == 0 or favoritelocation_2d.find("airport:") == 0:
                # Do that same ol' thing at boot. See if the data text is not None, and show
                # the display location as that additional data if so.
                if favoritelocation_2data != "None":
                    favoritelocation_2d = favoritelocation_2data
                else:
                    favoritelocation_2d = favoritelocation_2.strip("airport:") + " Airport"

                logger.debug("favoritelocation_2d: %s" % favoritelocation_2d)

            if favoritelocation_3d.find("arpt:") == 0 or favoritelocation_3d.find("airport:") == 0:
                # Do that same ol' thing at boot. See if the data text is not None, and show
                # the display location as that additional data if so.
                if favoritelocation_3data != "None":
                    favoritelocation_3d = favoritelocation_3data
                else:
                    favoritelocation_3d = favoritelocation_3.strip("airport:") + " Airport"

                logger.debug("favoritelocation_3d: %s" % favoritelocation_3d)

            if favoritelocation_4d.find("arpt:") == 0 or favoritelocation_4d.find("airport:") == 0:
                # Do that same ol' thing at boot. See if the data text is not None, and show
                # the display location as that additional data if so.
                if favoritelocation_4data != "None":
                    favoritelocation_4d = favoritelocation_4data
                else:
                    favoritelocation_4d = favoritelocation_4.strip("airport:") + " Airport"

                logger.debug("favoritelocation_4d: %s" % favoritelocation_4d)

            if favoritelocation_5d.find("arpt:") == 0 or favoritelocation_5d.find("airport:") == 0:
                # Do that same ol' thing at boot. See if the data text is not None, and show
                # the display location as that additional data if so.
                if favoritelocation_5data != "None":
                    favoritelocation_5d = favoritelocation_5data
                else:
                    favoritelocation_5d = favoritelocation_5.strip("airport:") + " Airport"

                logger.debug("favoritelocation_1d: %s" % favoritelocation_5d)



            spinner.stop()
            print("")
            print(Fore.YELLOW + Style.BRIGHT + "Your current favorite locations configuration:")
            print(Fore.YELLOW + Style.BRIGHT + "Favorite Location 1 - " + Fore.CYAN + Style.BRIGHT + favoritelocation_1d)
            print(Fore.YELLOW + Style.BRIGHT + "Favorite Location 2 - " + Fore.CYAN + Style.BRIGHT + favoritelocation_2d)
            print(Fore.YELLOW + Style.BRIGHT + "Favorite Location 3 - " + Fore.CYAN + Style.BRIGHT + favoritelocation_3d)
            print(Fore.YELLOW + Style.BRIGHT + "Favorite Location 4 - " + Fore.CYAN + Style.BRIGHT + favoritelocation_4d)
            print(Fore.YELLOW + Style.BRIGHT + "Favorite Location 5 - " + Fore.CYAN + Style.BRIGHT + favoritelocation_5d)
            print("")
            print(Fore.YELLOW + Style.BRIGHT + "What would you like to do with your favorite locations?")
            print(Fore.YELLOW + Style.BRIGHT + "- Add this location (" + Fore.CYAN + Style.BRIGHT + str(location) + Fore.YELLOW
                  + Style.BRIGHT + ") as a favorite location - Enter " + Fore.CYAN + "1")
            print(Fore.YELLOW + Style.BRIGHT + "- Add a location as a favorite location - Enter " + Fore.CYAN + Style.BRIGHT + "2")
            print(Fore.YELLOW + Style.BRIGHT + "- Edit a favorite location - Enter " + Fore.CYAN + Style.BRIGHT + "3")
            print(Fore.YELLOW + Style.BRIGHT + "- Remove a favorite location - Enter " + Fore.CYAN + Style.BRIGHT + "4")
            print(Fore.YELLOW + Style.BRIGHT + "- Return to PyWeather - Enter " + Fore.CYAN + Style.BRIGHT + "5")
            favconfig_menuinput = input("Input here: ").lower()
            logger.debug("favconfig_menuinput: %s" % favconfig_menuinput)
            if favconfig_menuinput == "1":
                # Code for adding current location as a favorite location
                print(Fore.YELLOW + Style.BRIGHT + "Would you like to add " + Fore.CYAN + Style.BRIGHT + location + Fore.YELLOW
                      + Style.BRIGHT + " as a favorite location? Yes or No.", sep="\n")
                favconfig_confirmadd = input("Input here: ").lower()
                logger.debug("favconfig_confirmadd: %s" % favconfig_confirmadd)
                if favconfig_confirmadd != "yes":
                    if favconfig_confirmadd != "no":
                        print("", Fore.YELLOW + Style.BRIGHT + "Couldn't understand your input. Not adding " + Fore.CYAN + Style.BRIGHT + location2 +
                              Fore.YELLOW + Style.BRIGHT + " to your location list.", sep="\n")
                    else:
                        print("", Fore.YELLOW + Style.BRIGHT + "Not adding " + Fore.CYAN + Style.BRIGHT +
                              str(location) + Fore.YELLOW + Style.BRIGHT + " to your location list.", sep="\n")
                    continue

                # Add location to favorite locations
                config['FAVORITE LOCATIONS']['favloc2'] = favoritelocation_1
                logger.debug("FAVORITE LOCATIONS/favloc2 is now: %s" % favoritelocation_1)
                config['FAVORITE LOCATIONS']['favloc3'] = favoritelocation_2
                logger.debug("FAVORITE LOCATIONS/favloc3 is now: %s" % favoritelocation_2)
                config['FAVORITE LOCATIONS']['favloc4'] = favoritelocation_3
                logger.debug("FAVORITE LOCATIONS/favloc4 is now: %s" % favoritelocation_3)
                config['FAVORITE LOCATIONS']['favloc5'] = favoritelocation_4
                logger.debug("FAVORITE LOCATIONS/favloc5 is now: %s" % favoritelocation_4)
                config['FAVORITE LOCATIONS']['favloc2_data'] = favoritelocation_1data
                logger.debug("FAVORITE LOCATIONS/favloc2_data is now: %s" % favoritelocation_1data)
                config['FAVORITE LOCATIONS']['favloc3_data'] = favoritelocation_2data
                logger.debug("FAVORITE LOCATIONS/favloc3_data is now: %s" % favoritelocation_2data)
                config['FAVORITE LOCATIONS']['favloc4_data'] = favoritelocation_3data
                logger.debug("FAVORITE LOCATIONS/favloc4_data is now: %s" % favoritelocation_3data)
                config['FAVORITE LOCATIONS']['favloc5_data'] = favoritelocation_4data
                logger.debug("FAVORITE LOCATIONS/favloc5_data is now: %s" % favoritelocation_4data)
                # Use location if the location isn't a PWS, use locinput for PWS. Use extra data for airport queries.
                if pws_query is False and airport_query is False:
                    logger.info("pws_query is False and airport_query is False")
                    config['FAVORITE LOCATIONS']['favloc1'] = str(location)
                    config['FAVORITE LOCATIONS']['favloc1_data'] = "None"
                    logger.debug("FAVORITE LOCATIONS/favloc1 is now: %s" % location)
                    logger.debug("FAVORITE LOCATIONS/favloc1_data is now: 'None'")
                elif pws_query is True:
                    logger.debug("pws_query is True")
                    config['FAVORITE LOCATIONS']['favloc1'] = locinput
                    config['FAVORITE LOCATIONS']['favloc1_data'] = "None"
                    logger.debug("FAVORITE LOCATIONS/favloc1 is now: %s" % locinput)
                    logger.debug("FAVORITE LOCATIONS/favloc1_data is now: 'None'")
                elif airport_query is True:
                    logger.debug("airport_query is True")
                    config['FAVORITE LOCATIONS']['favloc1'] = locinput.lower()
                    config['FAVORITE LOCATIONS']['favloc1_data'] = location
                    logger.debug("FAVORITE LOCATIONS/favloc1 is now: %s" % locinput)
                    logger.debug("FAVORITE LOCATIONS/favloc1_data is now: %s" % location)



                try:
                    with open('storage//config.ini', 'w') as configfile:
                        config.write(configfile)
                    print(Fore.YELLOW + Style.BRIGHT + "Changes saved!")
                    continue
                except:
                    print(Fore.RED + Style.BRIGHT + "An issue occurred when trying to write new options to your config file.",
                          "Please note that no changes were made to your config file.", sep="\n")
                    continue
            elif favconfig_menuinput == "2":
                # Code for adding a separate current location as a favorite location
                print(Fore.YELLOW + Style.BRIGHT + "Please enter the location that you'd like to add as a favorite location.",
                      Fore.YELLOW + Style.BRIGHT + "For a PWS, you'd enter pws:<PWS ID>, where <PWS ID> is the ID of the PWS.",
                      Fore.YELLOW + Style.BRIGHT + "For an airport, you'd enter airport:<IATA or ICAO code>, where <IATA or ICAO>",
                      Fore.YELLOW + Style.BRIGHT + "is the IATA or ICAO code of the airport you're adding.",
                      Fore.YELLOW + Style.BRIGHT + "Queries for favoritelocation:, currentlocation, and previouslocation: are not supported.",
                      Fore.YELLOW + Style.BRIGHT + "Please note that if you want to want to add an airport as a favorite location, we will",
                      Fore.YELLOW + Style.BRIGHT + "need to grab extra data for proper formatting.", sep="\n")
                try:
                    favloc_manualinput = input("Input here: ")
                except KeyboardInterrupt:
                    print(Fore.YELLOW + Style.BRIGHT + "Going back to the main menu.")
                    continue

                # Set the query type to "Default" here, as to help with adding the extra data variable.
                # If we have a PWS/airport query it will change.
                favloc_add_querytype = "Default"
                logger.debug("favloc_add_querytype: %s" % favloc_add_querytype)

                favloc_manualinputLower = favloc_manualinput.lower()
                logger.debug("favloc_manualinput: %s ; favloc_manualinputLower: %s" %
                             (favloc_manualinput, favloc_manualinputLower))

                if favloc_manualinputLower.find("pws:") == 0:
                    print(Fore.YELLOW + Style.BRIGHT + "Please note: For PWS queries to work as a favorite location, you'll need to have",
                          Fore.YELLOW + Style.BRIGHT + "PWS queries enabled in the config file. (FIRSTINPUT/allow_pwsqueries should be True).", sep="\n")
                    favloc_add_querytype = "PWS"
                    logger.debug("favloc_add_querytype: %s" % favloc_add_querytype)

                elif favloc_manualinputLower.find("airport:") == 0 or favloc_manualinputLower.find("arpt:") == 0:
                    logger.debug("Airport query detected.")
                    favloc_add_querytype = "Airport"
                    logger.debug("favloc_add_querytype: %s" % favloc_add_querytype)
                    print(Fore.YELLOW + Style.BRIGHT + "Please note: For airport queries to work as a favorite location, you'll need to have",
                          Fore.YELLOW + Style.BRIGHT + "airport queries enabled in the config file. (FIRSTINPUT/allow_airportqueries should be True).", sep="\n")
                    print("")
                    print(Fore.YELLOW + Style.BRIGHT + "For proper formatting of an airport as a favorite location, we need to grab extra data",
                          Fore.YELLOW + Style.BRIGHT + "about it's actual name. This process can be skipped entirely, but will result in improper",
                          Fore.YELLOW + Style.BRIGHT + "formatting of the favorite location. Would you like to get extra data about the airport?",
                          Fore.YELLOW + Style.BRIGHT + "Yes or No.", sep="\n")
                    airportvalidate_input = input("Input here: ").lower()
                    if airportvalidate_input == "yes":
                        print(Fore.YELLOW + Style.BRIGHT + "Now getting extra data about the airport that you inputted. This should only take a moment.")
                        spinner.start(text="Validating favorite location...")
                        airport_locinput = favloc_manualinput.strip("airport:")
                        logger.debug("airport_locinput: %s" % airport_locinput)
                        airportvalidate_url = 'http://api.wunderground.com/api/' + apikey + '/geolookup/q/' + airport_locinput.lower() + ".json"
                        logger.debug("airportvalidate_url: %s" % airportvalidate_url)
                        try:
                            airportvalidateJSON = requests.get(airportvalidate_url)
                            logger.debug("airportvalidateJSON acquired with end result: %s" % airportvalidateJSON)
                            airportvalidate_json = json.loads(airportvalidateJSON.text)
                            if jsonVerbosity is True:
                                logger.debug("airportvalidate_json: %s" % airportvalidate_json)
                            else:
                                logger.debug("airportvalidate_json has been loaded.")
                            airportvalidate_data = True
                            logger.debug("airportvalidate_data: %s" % airportvalidate_data)
                        except:
                            airportvalidate_data = False
                            logger.debug("airportvalidate_data: %s" % airportvalidate_data)
                            spinner.fail(text="Failed to validate favorite location!")
                            print("")
                            print(Fore.YELLOW + Style.BRIGHT + "Sorry, we couldn't query Wunderground to get extra data about the airport.",
                                  Fore.YELLOW + Style.BRIGHT + "you inputted. Would you still like to add this airport as a favorite",
                                  Fore.YELLOW + Style.BRIGHT + "location anyways? Yes or No.", sep="\n")
                            airportvalidate_invalidinput = input("Input here: ").lower()
                            if airportvalidate_invalidinput == "yes":
                                print(Fore.YELLOW + Style.BRIGHT + "Still adding the airport as a favorite location.")
                            elif airportvalidate_invalidinput == "no":
                                print(Fore.YELLOW + Style.BRIGHT + "Not adding the airport as a favorite location.")
                                continue
                            else:
                                print(Fore.YELLOW + Style.BRIGHT + "Could not understand your input, but still adding the airport as",
                                      Fore.YELLOW + Style.BRIGHT + "as a favorite location.", sep="\n")

                        if airportvalidate_data is True:
                            logger.info("airportvalidate_data is True.")

                            try:
                                airport_name = airportvalidate_json['location']['city'] + " Airport"
                                logger.debug("airport_name: %s" % airport_name)
                                spinner.succeed(text="Airport location is valid!")
                                print("")
                                print(Fore.YELLOW + Style.BRIGHT + "The airport you entered is valid, and we have good extra data.",
                                      Fore.YELLOW + Style.BRIGHT + "Proceeding with adding it to your favorite locations.", sep="\n")
                            except:
                                spinner.fail(text="Failed to validate favorite location.")
                                # Set the airport name to none, as that's the data that will get added.
                                airportvalidate_data = False
                                logger.debug("airportvalidate_data: %s" % airportvalidate_data)
                                print("")
                                print(Fore.YELLOW + Style.BRIGHT + "The airport that you entered is invalid, or doesn't have proper",
                                      Fore.YELLOW + Style.BRIGHT + "extra data. Would you still like to add the airport as a favorite location? Yes or No.", sep="\n")
                                airportvalidate_invalidinput = input("Input here: ").lower()
                                if airportvalidate_invalidinput == "yes":
                                    print(Fore.YELLOW + Style.BRIGHT + "Proceeding with adding the airport as a favorite location.")
                                elif airportvalidate_invalidinput == "no":
                                    print(Fore.YELLOW + Style.BRIGHT + "Not adding the airport as a favorite location, and returning to the main menu.")
                                    continue
                                else:
                                    print(Fore.YELLOW + Style.BRIGHT + "Could not understand your input, but the airport will be added",
                                          Fore.YELLOW + Style.BRIGHT + "as a favorite location anyways.", sep="\n")
                    elif airportvalidate_input == "no":
                        print(Fore.YELLOW + Style.BRIGHT + "Not validating the airport you inputted, and proceeding with adding it as a favorite location.")
                    else:
                        print(Fore.YELLOW + Style.BRIGHT + "Could not understand your input. Defaulting to adding the airport you inputted.")

                if favloc_manualinputLower.find("favoritelocation:") == 0 or favloc_manualinputLower.find("favloc:") == 0:
                    logger.debug("Invalid query detected - favorite location")
                    print("", Fore.RED + Style.BRIGHT + "Whoops! You can't use a favorite location query as a favorite location.",
                          Fore.RED + Style.BRIGHT + "Makes sense, right? Returning to main menu.", sep="\n")
                    continue
                if favloc_manualinputLower.find("currentlocation") == 0 or favloc_manualinputLower.find("curloc") == 0:
                    logger.debug("Invalid query detected - current location")
                    print("", Fore.RED + Style.BRIGHT + "Whoops! You can't use a current location query as a favorite location.",
                          Fore.RED + Style.BRIGHT + "If you'd like to use your current location at boot, make sure that the",
                          Fore.RED + Style.BRIGHT + "current location feature is enabled (FIRSTINPUT/geoipservice_enabled should be True).",
                          Fore.RED + Style.BRIGHT + "Returning to main menu.", sep="\n")
                    continue

                # Bump down the favloc data variables. It doesn't matter what query type we're working with.

                config['FAVORITE LOCATIONS']['favloc2'] = favoritelocation_1
                logger.debug("FAVORITE LOCATIONS/favloc2 is now: %s" % favoritelocation_1)
                config['FAVORITE LOCATIONS']['favloc3'] = favoritelocation_2
                logger.debug("FAVORITE LOCATIONS/favloc3 is now: %s" % favoritelocation_2)
                config['FAVORITE LOCATIONS']['favloc4'] = favoritelocation_3
                logger.debug("FAVORITE LOCATIONS/favloc4 is now: %s" % favoritelocation_3)
                config['FAVORITE LOCATIONS']['favloc5'] = favoritelocation_4
                logger.debug("FAVORITE LOCATIONS/favloc5 is now: %s" % favoritelocation_4)
                # Use the non-lowercased variable as the favorite location here.

                # Shift down the data variables.
                config['FAVORITE LOCATIONS']['favloc2_data'] = favoritelocation_1data
                logger.debug("FAVORITE LOCATIONS/favloc2_data is now: %s" % favoritelocation_1data)
                config['FAVORITE LOCATIONS']['favloc3_data'] = favoritelocation_2data
                logger.debug("FAVORITE LOCATIONS/favloc3_data is now: %s" % favoritelocation_2data)
                config['FAVORITE LOCATIONS']['favloc4_data'] = favoritelocation_3data
                logger.debug("FAVORITE LOCATIONS/favloc4_data is now: %s" % favoritelocation_3data)
                config['FAVORITE LOCATIONS']['favloc5_data'] = favoritelocation_4data
                logger.debug("FAVORITE LOCATIONS/favloc5_data is now: %s" % favoritelocation_4data)

                # Depending on the query type we either add the favloc input in lowercase form, or the way it was in the input.
                if favloc_add_querytype == "Default":
                    config['FAVORITE LOCATIONS']['favloc1'] = favloc_manualinput
                    logger.debug("FAVORITE LOCATIONS/favloc1 is now: %s" % favloc_manualinput)
                elif favloc_add_querytype == "PWS":
                    config['FAVORITE LOCATIONS']['favloc1'] = favloc_manualinputLower
                    logger.debug("FAVORITE LOCATIONS/favloc1 is now: %s" % favloc_manualinputLower)
                elif favloc_add_querytype == "Airport":
                    config['FAVORITE LOCATIONS']['favloc1'] = favloc_manualinputLower
                    logger.debug("FAVORITE LOCATIONS/favloc1 is now: %s" % favloc_manualinputLower)
                else:
                    # In the event that somehow the query type isn't set, just put in the lower manual input for safety.
                    logger.warn("Query type wasn't set! Defaulting to adding the lowercase input var.")
                    config['FAVORITE LOCATIONS']['favloc1'] = favloc_manualinputLower
                    logger.debug("FAVORITE LOCATIONS/favloc1 is now: %s" % favloc_manualinputLower)

                # Do the same thing as we did above, adding the data variable depending on query type.
                if favloc_add_querytype == "Default":
                    config['FAVORITE LOCATIONS']['favloc1_data'] = "None"
                    logger.debug("FAVORITE LOCATIONS/favloc1_data is now 'None'.")
                elif favloc_add_querytype == "PWS":
                    config['FAVORITE LOCATIONS']['favloc1_data'] = "None"
                    logger.debug("FAVORITE LOCATIONS/favloc1_data is now 'None'.")
                elif favloc_add_querytype == "Airport":
                    # We can have two scenarios where we have data or not.
                    if airportvalidate_data is True:
                        logger.info("airportvalidate_data is True.")
                        config['FAVORITE LOCATIONS']['favloc1_data'] = airport_name
                        logger.debug("FAVORITE LOCATIONS/favloc1_data is now: %s" % airport_name)
                    elif airportvalidate_data is False:
                        logger.info("airportvalidate_data is False.")
                        config['FAVORITE LOCATIONS']['favloc1_data'] = "None"
                        logger.debug("FAVORITE LOCATIONS/favloc1_data is now 'None'.")
                    else:
                        logger.warning("airportvalidate_data isn't True or False! Defaulting to no extra data.")
                        config['FAVORITE LOCATIONS']['favloc1_data'] = "None"
                        logger.debug("FAVORITE LOCATIONS/favloc1_data is now 'None'.")
                else:
                    logger.warning("Query type wasn't set! Defaulting to adding no extra data.")
                    config['FAVORITE LOCATIONS']['favloc1_data'] = "None"
                    logger.debug("FAVORITE LOCATIONS/favloc1_data is now 'None'.")

                try:
                    with open('storage//config.ini', 'w') as configfile:
                        config.write(configfile)
                    print(Fore.YELLOW + Style.BRIGHT + "Changes saved!")
                    continue
                except:
                    print(Fore.RED + Style.BRIGHT + "An issue occurred when trying to write new options to your config file.",
                          Fore.RED + Style.BRIGHT + "Please note that no changes were made to your config file.", sep="\n")
                    continue
            elif favconfig_menuinput == "3":
                print(Fore.YELLOW + Style.BRIGHT + "Which favorite location would you like to modify? Enter a number 1-5 representing",
                      Fore.YELLOW + Style.BRIGHT + "the favorite locations 1-5.", sep="\n")
                favloc_editinputnum = input("Input here: ").lower()
                logger.debug("favloc_editinputnum: %s" % favloc_editinputnum)
                # Convert the number to an integer to see if the user entered a number. If a ValueError is catched,
                # return to the main menu. Floats will be rounded down to the first number.

                try:
                    favloc_editinputnum = int(favloc_editinputnum)
                except ValueError:
                    print("", Fore.RED + Style.BRIGHT + "Whoops! Your input didn't seem to be a number. Returning to the",
                          Fore.RED + Style.BRIGHT + "main menu.", sep="\n")
                    continue

                # Validate the number is between 1-5
                if favloc_editinputnum < 1 or favloc_editinputnum > 5:
                    print(Fore.RED + Style.BRIGHT + "Whoops! You entered a favorite location to input that was not between 1-5.",
                          Fore.RED + Style.BRIGHT + "Returning to the main menu...", sep="\n")
                    continue

                # Confirm to the user which favorite location we're editing.
                if favloc_editinputnum is 1:
                    favloc_editdisplay = favoritelocation_1d
                elif favloc_editinputnum is 2:
                    favloc_editdisplay = favoritelocation_2d
                elif favloc_editinputnum is 3:
                    favloc_editdisplay = favoritelocation_3d
                elif favloc_editinputnum is 4:
                    favloc_editdisplay = favoritelocation_4d
                elif favloc_editinputnum is 5:
                    favloc_editdisplay = favoritelocation_5d
                logger.debug("favloc_editdisplay: %s" % favloc_editdisplay)

                print(Fore.YELLOW + Style.BRIGHT + "Just to confirm, you're editing favorite location " + Fore.CYAN + Style.BRIGHT + str(favloc_editinputnum)
                      + Fore.YELLOW + Style.BRIGHT + ".",
                      Fore.YELLOW + Style.BRIGHT + "This favorite location is currently: " + Fore.CYAN + Style.BRIGHT + favloc_editdisplay +
                      Fore.YELLOW + Style.BRIGHT + ".",
                      Fore.YELLOW + Style.BRIGHT + "Would you like to edit this favorite location? Yes or No.", sep="\n")
                favloc_editconfirm = input("Input here: ").lower()
                logger.debug("favloc_editconfirm: %s" % favloc_editconfirm)
                if favloc_editconfirm == "yes":
                    logger.debug("moving to the final input...")
                elif favloc_editconfirm == "no":
                    print(Fore.YELLOW + Style.BRIGHT + "", "Not editing favorite location " + Fore.CYAN + Style.BRIGHT + str(favloc_editinputnum)
                          + Fore.YELLOW + Style.BRIGHT + ".",
                          Fore.YELLOW + Style.BRIGHT + "Returning to the main menu.", sep="\n")
                    continue
                else:
                    print("", Fore.RED + Style.BRIGHT + "Could not understand your input. Returning to the main menu.", sep="\n")
                    continue


                # User input for the change goes here.
                print(Fore.YELLOW + Style.BRIGHT + "What would you like to change favorite location " + Fore.CYAN + Style.BRIGHT + str(favloc_editdisplay) + Fore.YELLOW + Style.BRIGHT + " to?",
                      Fore.YELLOW + Style.BRIGHT + "For a PWS, you'd enter pws:<PWS ID>, where <PWS ID> is the ID of the PWS.",
                      Fore.YELLOW + Style.BRIGHT + "For an airport, you'd enter airport:<IATA or ICAO code>, where <IATA or ICAO>",
                      Fore.YELLOW + Style.BRIGHT + "Queries for favoritelocation:, currentlocation, and previouslocation: are not supported.",
                      Fore.YELLOW + Style.BRIGHT + "Please note that if you want to want to add an airport as a favorite location, we will",
                      Fore.YELLOW + Style.BRIGHT + "need to grab extra data for proper formatting.", sep="\n")
                favloc_editinput = input("Input here: ")
                favloc_editinputLower = favloc_editinput.lower()
                logger.debug("favloc_editinput: %s ; favloc_editinputLower: %s" %
                             (favloc_editinput, favloc_editinputLower))

                # Validate the user input, do special conversions for PWSes.
                if favloc_editinputLower == "exit":
                    print("", Fore.YELLOW + Style.BRIGHT + "Exiting to the main menu.", sep="\n")

                if favloc_editinputLower.find("airport:") == 0 or favloc_editinputLower.find("arpt:") == 0:
                    logger.debug("Airport query detected.")
                    print(Fore.YELLOW + Style.BRIGHT + "Please note: For airport queries to work as a favorite location, you'll need to have",
                          Fore.YELLOW + Style.BRIGHT + "airport queries enabled in the config file. (FIRSTINPUT/allow_airportqueries should be True).", sep="\n")
                    print("")
                    print(Fore.YELLOW + Style.BRIGHT + "For proper formatting of an airport as a favorite location, we need to grab extra data",
                          Fore.YELLOW + Style.BRIGHT + "about it's actual name. This process can be skipped entirely, but will result in improper",
                          Fore.YELLOW + Style.BRIGHT + "formatting of the favorite location. Would you like to get extra data about the airport?",
                          Fore.YELLOW + Style.BRIGHT + "Yes or No.", sep="\n")
                    airportvalidate_input = input("Input here: ").lower()
                    if airportvalidate_input == "yes":
                        print(Fore.YELLOW + Style.BRIGHT + "Now getting extra data about the airport that you inputted. This should only take a moment.")
                        spinner.start(text="Validating favorite location...")
                        favloc_editinput = favloc_editinput.strip("airport:")
                        airportvalidate_url = 'http://api.wunderground.com/api/' + apikey + '/geolookup/q/' + favloc_editinput.lower() + ".json"
                        logger.debug("airportvalidate_url: %s" % airportvalidate_url)
                        try:
                            airportvalidateJSON = requests.get(airportvalidate_url)
                            logger.debug("airportvalidateJSON acquired with end result: %s" % airportvalidateJSON)
                            airportvalidate_json = json.loads(airportvalidateJSON.text)
                            if jsonVerbosity is True:
                                logger.debug("airportvalidate_json: %s" % airportvalidate_json)
                            else:
                                logger.debug("airportvalidate_json has been loaded.")
                            airportvalidate_data = True
                            logger.debug("airportvalidate_data: %s" % airportvalidate_data)
                        except:
                            airportvalidate_data = False
                            logger.debug("airportvalidate_data: %s" % airportvalidate_data)
                            spinner.fail(text="Failed to validate favorite location!")
                            print("")
                            print(Fore.YELLOW + Style.BRIGHT + "Sorry, we couldn't query Wunderground to get extra data about the airport.",
                                  Fore.YELLOW + Style.BRIGHT + "you inputted. Would you still like to add this airport as a favorite",
                                  Fore.YELLOW + Style.BRIGHT + "location anyways? Yes or No.", sep="\n")
                            airportvalidate_invalidinput = input("Input here: ").lower()
                            if airportvalidate_invalidinput == "yes":
                                print(Fore.YELLOW + Style.BRIGHT + "Still adding the airport as a favorite location.")
                            elif airportvalidate_invalidinput == "no":
                                print(Fore.YELLOW + Style.BRIGHT + "Not adding the airport as a favorite location.")
                                continue
                            else:
                                print(Fore.YELLOW + Style.BRIGHT + "Could not understand your input, but still adding the airport as",
                                      Fore.YELLOW + Style.BRIGHT + "as a favorite location.", sep="\n")

                        if airportvalidate_data is True:
                            logger.info("airportvalidate_data is True.")

                            try:
                                airport_name = airportvalidate_json['location']['city'] + " Airport"
                                logger.debug("airport_name: %s" % airport_name)
                                spinner.succeed(text="Airport location is valid!")
                                print("")
                                print(Fore.YELLOW + Style.BRIGHT + "The airport you entered is valid, and we have good extra data.",
                                      Fore.YELLOW + Style.BRIGHT + "Proceeding with adding it to your favorite locations.", sep="\n")
                            except:
                                spinner.fail(text="Failed to validate favorite location.")
                                # Set the airport name to none, as that's the data that will get added.
                                airportvalidate_data = False
                                logger.debug("airportvalidate_data: %s" % airportvalidate_data)
                                print("")
                                print(Fore.YELLOW + Style.BRIGHT + "The airport that you entered is invalid, or doesn't have proper",
                                      Fore.YELLOW + Style.BRIGHT + "extra data. Would you still like to add the airport as a favorite location? Yes or No.", sep="\n")
                                airportvalidate_invalidinput = input("Input here: ").lower()
                                if airportvalidate_invalidinput == "yes":
                                    print(Fore.YELLOW + Style.BRIGHT + "Proceeding with adding the airport as a favorite location.")
                                elif airportvalidate_invalidinput == "no":
                                    print(Fore.YELLOW + Style.BRIGHT + "Not adding the airport as a favorite location, and returning to the main menu.")
                                    continue
                                else:
                                    print(Fore.YELLOW + Style.BRIGHT + "Could not understand your input, but the airport will be added",
                                          Fore.YELLOW + Style.BRIGHT + "as a favorite location anyways.", sep="\n")
                    elif airportvalidate_input == "no":
                        print(Fore.YELLOW + Style.BRIGHT + "Not validating the airport you inputted, and proceeding with adding it as a favorite location.")
                        continue
                    else:
                        print(Fore.YELLOW + Style.BRIGHT + "Could not understand your input. Defaulting to adding the airport you inputted.")

                    # At this point we add the favorite location. Lower input as with PWSes & the extra data var set to the airport name.

                    if favloc_editinputnum == 1:
                        config['FAVORITE LOCATIONS']['favloc1'] = favloc_editinputLower
                        logger.debug("FAVORITE LOCATIONS/favloc1 is now: %s" % favloc_editinputLower)
                        config['FAVORITE LOCATIONS']['favloc1_data'] = airport_name
                        logger.debug("FAVORITE LOCATIONS/favloc1_data is now: %s" % airport_name)
                    elif favloc_editinputnum == 2:
                        config['FAVORITE LOCATIONS']['favloc2'] = favloc_editinputLower
                        logger.debug("FAVORITE LOCATIONS/favloc2 is now: %s" % favloc_editinputLower)
                        config['FAVORITE LOCATIONS']['favloc2_data'] = airport_name
                        logger.debug("FAVORITE LOCATIONS/favloc2_data is now: %s" % airport_name)
                    elif favloc_editinputnum == 3:
                        config['FAVORITE LOCATIONS']['favloc3'] = favloc_editinputLower
                        logger.debug("FAVORITE LOCATIONS/favloc3 is now: %s" % favloc_editinputLower)
                        config['FAVORITE LOCATIONS']['favloc3_data'] = airport_name
                        logger.debug("FAVORITE LOCATIONS/favloc3_data is now: %s" % airport_name)
                    elif favloc_editinputnum == 4:
                        config['FAVORITE LOCATIONS']['favloc4'] = favloc_editinputLower
                        logger.debug("FAVORITE LOCATIONS/favloc4 is now: %s" % favloc_editinputLower)
                        config['FAVORITE LOCATIONS']['favloc4_data'] = airport_name
                        logger.debug("FAVORITE LOCATIONS/favloc4_data is now: %s" % airport_name)
                    elif favloc_editinputnum == 5:
                        config['FAVORITE LOCATIONS']['favloc5'] = favloc_editinputLower
                        logger.debug("FAVORITE LOCATIONS/favloc5 is now: %s" % favloc_editinputLower)
                        config['FAVORITE LOCATIONS']['favloc5_data'] = airport_name
                        logger.debug("FAVORITE LOCATIONS/favloc5_data is now: %s" % airport_name)

                    try:
                        with open('storage//config.ini', 'w') as configfile:
                            config.write(configfile)
                        print(Fore.YELLOW + Style.BRIGHT + "Changes saved!")
                        continue
                    except:
                        print(Fore.RED + Style.BRIGHT + "An issue occurred when trying to write new options to your config file.",
                              Fore.RED + Style.BRIGHT + "Please note that no changes were made to your config file.", sep="\n")
                        continue


                if favloc_editinputLower.find("pws:") == 0:
                    logger.debug("PWS query has been detected.")
                    print("", Fore.YELLOW + Style.BRIGHT + "Please note: For PWS queries to work as a favorite location, you'll need to enable PWS queries",
                          Fore.YELLOW + Style.BRIGHT + "in the config file. (FIRSTINPUT/allow_pwsqueries should be True.)", sep="\n")

                    # PWS query means no extra data. Use the lower input as it doesn't matter.

                    if favloc_editinputnum == 1:
                        config['FAVORITE LOCATIONS']['favloc1'] = favloc_editinputLower
                        logger.debug("FAVORITE LOCATIONS/favloc1 is now: %s" % favloc_editinputLower)
                        config['FAVORITE LOCATIONS']['favloc1_data'] = "None"
                        logger.debug("FAVORITE LOCATIONS/favloc1_data is now: 'None'")
                    elif favloc_editinputnum == 2:
                        config['FAVORITE LOCATIONS']['favloc2'] = favloc_editinputLower
                        logger.debug("FAVORITE LOCATIONS/favloc2 is now: %s" % favloc_editinputLower)
                        config['FAVORITE LOCATIONS']['favloc2_data'] = "None"
                        logger.debug("FAVORITE LOCATIONS/favloc2_data is now: 'None'")
                    elif favloc_editinputnum == 3:
                        config['FAVORITE LOCATIONS']['favloc3'] = favloc_editinputLower
                        logger.debug("FAVORITE LOCATIONS/favloc3 is now: %s" % favloc_editinputLower)
                        config['FAVORITE LOCATIONS']['favloc3_data'] = "None"
                        logger.debug("FAVORITE LOCATIONS/favloc3_data is now: 'None'")
                    elif favloc_editinputnum == 4:
                        config['FAVORITE LOCATIONS']['favloc4'] = favloc_editinputLower
                        logger.debug("FAVORITE LOCATIONS/favloc4 is now: %s" % favloc_editinputLower)
                        config['FAVORITE LOCATIONS']['favloc4_data'] = "None"
                        logger.debug("FAVORITE LOCATIONS/favloc4_data is now: 'None'")
                    elif favloc_editinputnum == 5:
                        config['FAVORITE LOCATIONS']['favloc5'] = favloc_editinputLower
                        logger.debug("FAVORITE LOCATIONS/favloc5 is now: %s" % favloc_editinputLower)
                        config['FAVORITE LOCATIONS']['favloc5_data'] = "None"
                        logger.debug("FAVORITE LOCATIONS/favloc5_data is now 'None'")

                    try:
                        with open('storage//config.ini', 'w') as configfile:
                            config.write(configfile)
                        print(Fore.YELLOW + Style.BRIGHT + "Changes saved!")
                        continue
                    except:
                        print(Fore.RED + Style.BRIGHT + "An issue occurred when trying to write new options to your config file.",
                              Fore.RED + Style.BRIGHT + "Please note that no changes were made to your config file.", sep="\n")
                        continue

                if favloc_editinputLower.find("favoritelocation:") == 0 or favloc_editinputLower.find(
                        "favloc:") == 0:
                    logger.debug("Invalid query detected - favorite location")
                    print("", Fore.RED + Style.BRIGHT + "Whoops! You can't use a favorite location query as a favorite location.",
                          Fore.RED + Style.BRIGHT + "Makes sense, right? Returning to main menu.", sep="\n")
                    continue
                if favloc_editinputLower.find("currentlocation") == 0 or favloc_editinputLower.find(
                        "curloc") == 0:
                    logger.debug("Invalid query detected - current location")
                    print("", Fore.RED + Style.BRIGHT + "Whoops! You can't use a current location query as a favorite location.",
                          Fore.RED + Style.BRIGHT + "If you'd like to use your current location at boot, make sure that the",
                          Fore.RED + Style.BRIGHT + "current location feature is enabled (FIRSTINPUT/geoipservice_enabled should be True).",
                          Fore.RED + Style.BRIGHT + "Returning to main menu.", sep="\n")
                    continue

                # Commit to the config given that the location inputted is not special. A favorite location is committed to based on what
                # number a user entered.

                if favloc_editinputnum == 1:
                    config['FAVORITE LOCATIONS']['favloc1'] = favloc_editinputLower
                    logger.debug("FAVORITE LOCATIONS/favloc1 is now: %s" % favloc_editinputLower)
                    config['FAVORITE LOCATIONS']['favloc1_data'] = "None"
                    logger.debug("FAVORITE LOCATIONS/favloc1_data is now: 'None'")
                elif favloc_editinputnum == 2:
                    config['FAVORITE LOCATIONS']['favloc2'] = favloc_editinputLower
                    logger.debug("FAVORITE LOCATIONS/favloc2 is now: %s" % favloc_editinputLower)
                    config['FAVORITE LOCATIONS']['favloc2_data'] = "None"
                    logger.debug("FAVORITE LOCATIONS/favloc2_data is now: 'None'")
                elif favloc_editinputnum == 3:
                    config['FAVORITE LOCATIONS']['favloc3'] = favloc_editinputLower
                    logger.debug("FAVORITE LOCATIONS/favloc3 is now: %s" % favloc_editinputLower)
                    config['FAVORITE LOCATIONS']['favloc3_data'] = "None"
                    logger.debug("FAVORITE LOCATIONS/favloc3_data is now: 'None'")
                elif favloc_editinputnum == 4:
                    config['FAVORITE LOCATIONS']['favloc4'] = favloc_editinputLower
                    logger.debug("FAVORITE LOCATIONS/favloc4 is now: %s" % favloc_editinputLower)
                    config['FAVORITE LOCATIONS']['favloc4_data'] = "None"
                    logger.debug("FAVORITE LOCATIONS/favloc4_data is now: 'None'")
                elif favloc_editinputnum == 5:
                    config['FAVORITE LOCATIONS']['favloc5'] = favloc_editinputLower
                    logger.debug("FAVORITE LOCATIONS/favloc5 is now: %s" % favloc_editinputLower)
                    config['FAVORITE LOCATIONS']['favloc5_data'] = "None"
                    logger.debug("FAVORITE LOCATIONS/favloc5_data is now 'None'")

                try:
                    with open('storage//config.ini', 'w') as configfile:
                        config.write(configfile)
                    print(Fore.YELLOW + Style.BRIGHT + "Changes saved!")
                    continue
                except:
                    print(Fore.RED + Style.BRIGHT + "An issue occurred when trying to write new options to your config file.",
                          Fore.RED + Style.BRIGHT + "Please note that no changes were made to your config file.", sep="\n")
                    continue
            elif favconfig_menuinput == "4":
                print(Fore.YELLOW + Style.BRIGHT + "Which favorite location would you like to remove? Enter a number 1-5 representing",
                      Fore.YELLOW + Style.BRIGHT + "the favorite locations 1-5.", sep="\n")
                favloc_removeinputnum = input("Input here: ").lower()
                logger.debug("favloc_removeinputnum: %s" % favloc_removeinputnum)
                # Convert the input number to an integer, see if the user entered a number.
                # Floats get converted down to the first number.

                try:
                    favloc_removeinputnum = int(favloc_removeinputnum)
                except ValueError:
                    print("", Fore.RED + Style.BRIGHT + "Whoops! Your input didn't seem to be a number. Returning to the",
                          Fore.RED + Style.BRIGHT + "main menu.", sep="\n")
                    continue

                # Validate the input number is between 1 and 5. I understand this expression can be under 20 characters but
                # I trust this more.
                if favloc_removeinputnum < 1 or favloc_removeinputnum > 5:
                    print("", Fore.RED + Style.BRIGHT + "Whoops! You entered a favorite location to remove that was not between 1-5.",
                          Fore.RED + Style.BRIGHT + "Returning to the main menu.", sep="\n")
                    continue

                # Validate that the location that a user is trying to remove isn't "None".
                favloc_remove_isNone = False
                if favloc_removeinputnum == 1 and favoritelocation_1 == "None":
                    favloc_remove_isNone = True
                elif favloc_removeinputnum == 2 and favoritelocation_2 == "None":
                    favloc_remove_isNone = True
                elif favloc_removeinputnum == 3 and favoritelocation_3 == "None":
                    favloc_remove_isNone = True
                elif favloc_removeinputnum == 4 and favoritelocation_4 == "None":
                    favloc_remove_isNone = True
                elif favloc_removeinputnum == 5 and favoritelocation_5 == "None":
                    favloc_remove_isNone = True

                logger.debug("favloc_remove_isNone: %s" % favloc_remove_isNone)
                if favloc_remove_isNone is True:
                    print("", Fore.RED + Style.BRIGHT + "Whoops! The favorite location you're trying to remove isn't set to anything.",
                          Fore.RED + Style.BRIGHT + "Returning to the main menu.", sep="\n")
                    continue

                # Display variable for when we display what favorite location we're removing.
                if favloc_removeinputnum == 1:
                    favloc_removedisplay = favoritelocation_1d
                elif favloc_removeinputnum == 2:
                    favloc_removedisplay = favoritelocation_2d
                elif favloc_removeinputnum == 3:
                    favloc_removedisplay = favoritelocation_3d
                elif favloc_removeinputnum == 4:
                    favloc_removedisplay = favoritelocation_4d
                elif favloc_removeinputnum == 5:
                    favloc_removedisplay = favoritelocation_5d
                logger.debug("favloc_removedisplay: %s" % favloc_removedisplay)

                print(Fore.YELLOW + Style.BRIGHT + "Are you sure you want to delete favorite location " + Fore.CYAN + Style.BRIGHT + str(favloc_removeinputnum)
                      + Fore.YELLOW + Style.BRIGHT + "?",
                      Fore.YELLOW + Style.BRIGHT + "This favorite location is presently set to: " + Fore.CYAN + Style.BRIGHT + favloc_removedisplay,
                      Fore.YELLOW + Style.BRIGHT + "This action cannot be undone! Yes or No.", sep="\n")
                favloc_removeconfirm = input("Input here: ").lower()
                logger.debug("favloc_removeconfirm: %s" % favloc_removeconfirm)
                if favloc_removeconfirm == "yes":
                    logger.debug("removing favorite location...")
                elif favloc_removeconfirm == "no":
                    print("", Fore.YELLOW + Style.BRIGHT + "Not deleting favorite location " +
                          Fore.CYAN + Style.BRIGHT + str(favloc_removeinputnum) + Fore.YELLOW + Style.BRIGHT + ".",
                          Fore.CYAN + Style.BRIGHT + "Returning to the main menu.", sep="\n")
                    continue
                else:
                    print("", Fore.YELLOW + Style.BRIGHT + "Couldn't understand your input, and not deleting favorite location "
                          + Fore.CYAN + Style.BRIGHT + str(favloc_removeinputnum) + Fore.CYAN + Style.BRIGHT + ".",
                          Fore.YELLOW + Style.BRIGHT + "Returning to the main menu.", sep="\n")

                # Delete certain favorite locations based on what favorite location we're trying to delete.

                if favloc_removeinputnum <= 1:
                    config['FAVORITE LOCATIONS']['favloc1'] = favoritelocation_2
                    logger.debug("FAVORITE LOCATIONS/favloc1 is now: %s" % favoritelocation_2)
                    config['FAVORITE LOCATIONS']['favloc1_data'] = favoritelocation_2data
                    logger.debug("FAVORITE LOCATIONS/favloc1_data is now: %s" % favoritelocation_2data)
                if favloc_removeinputnum <= 2:
                    config['FAVORITE LOCATIONS']['favloc2'] = favoritelocation_3
                    logger.debug("FAVORITE LOCATIONS/favloc2 is now: %s" % favoritelocation_3)
                    config['FAVORITE LOCATIONS']['favloc2_data'] = favoritelocation_3data
                    logger.debug("FAVORITE LOCATIONS/favloc2_data is now: %s" % favoritelocation_3data)
                if favloc_removeinputnum <= 3:
                    config['FAVORITE LOCATIONS']['favloc3'] = favoritelocation_4
                    logger.debug("FAVORITE LOCATIONS/favloc3 is now: %s" % favoritelocation_4)
                    config['FAVORITE LOCATIONS']['favloc3_data'] = favoritelocation_4data
                    logger.debug("FAVORITE LOCATIONS/favloc3_data is now: %s" % favoritelocation_4data)
                if favloc_removeinputnum <= 4:
                    config['FAVORITE LOCATIONS']['favloc4'] = favoritelocation_5
                    logger.debug("FAVORITE LOCATIONS/favloc4 is now: %s" % favoritelocation_5)
                    config['FAVORITE LOCATIONS']['favloc4_data'] = favoritelocation_5data
                    logger.debug("FAVORITE LOCATIONS/favloc4_data is now: %s" % favoritelocation_5data)
                if favloc_removeinputnum <= 5:
                    config['FAVORITE LOCATIONS']['favloc5'] = "None"
                    logger.debug('FAVORITE LOCATIONS/favloc5 is now: "None"')
                    config['FAVORITE LOCATIONS']['favloc5_data'] = "None"
                    logger.debug("FAVORITE LOCATIONS/favloc5_data is now: 'None'")

                try:
                    with open('storage//config.ini', 'w') as configfile:
                        config.write(configfile)
                    print(Fore.YELLOW + Style.BRIGHT + "Changes saved!")
                    continue
                except:
                    print(Fore.RED + Style.BRIGHT + "An issue occurred when trying to write new options to your config file.",
                          Fore.RED + Style.BRIGHT + "Please note that no changes were made to your config file.", sep="\n")
                    continue

            elif favconfig_menuinput == "5":
                break
            else:
                print(Fore.YELLOW + Style.BRIGHT + "Your input could not be understood.")
                continue


# ModoUnreal working on previous location stuff here....

    elif moreoptions == "14":
        if previouslocation_enabled is False:
            print("", Fore.RED + Style.BRIGHT + "To manage previous locations, you'll need to enable the previous locations feature.",
                  Fore.RED + Style.BRIGHT + "Would you like me to enable previous locations for you?", sep="\n")
            enablepreviouslocations = input("Input here: ").lower()
            logger.debug("enablepreviouslocations: %s" % enablepreviouslocations)
            if enablepreviouslocations == "yes":
                config['PREVIOUS LOCATIONS']['enabled'] = 'True'
                logger.info("PREVIOUS LOCATIONS/enabled is now 'True'.")
                try:
                    with open('storage//config.ini', 'w') as configfile:
                        config.write(configfile)
                    print(Fore.YELLOW + Style.BRIGHT + "Previous locations is now enabled, and will be operational when you next boot up PyWeather.")
                    continue
                except:
                    print(Fore.RED + Style.BRIGHT + "An issue occured when trying to save new configuration options.",
                          Fore.RED + Style.BRIGHT + "Please enable previous locations in the config file. In the PREVIOUS LOCATIONS",
                          Fore.RED + Style.BRIGHT + "section, change enabled to True.")
                continue
            elif enablepreviouslocations == "no":
                print(Fore.YELLOW + Style.BRIGHT + "Not enabling previous locations. Returning to the main menu.",
                      "You can come back to this menu to reenable previous locations, or go into your config file and",
                      "enable PREVIOUS LOCATIONS/enabled (set it tp True).", sep="\n")
                continue
            else:
                print(Fore.YELLOW + Style.BRIGHT + "Your input wasn't understood, and as such previous locations will not be enabled.",
                      "You can come back to this menu to reenable previous locations, or go into your config file and",
                      "enable PREVIOUS LOCATIONS/enabled (set it to True).")

        while True:
            # Get up-to-date configuration information about previous locations.
            spinner.start(text="Loading your previous locations...")
            try:
                previouslocation_1 = config.get('PREVIOUS LOCATIONS', 'prevloc1')
                previouslocation_1d = previouslocation_1
                previouslocation_2 = config.get('PREVIOUS LOCATIONS', 'prevloc2')
                previouslocation_2d = previouslocation_2
                previouslocation_3 = config.get('PREVIOUS LOCATIONS', 'prevloc3')
                previouslocation_3d = previouslocation_3
                previouslocation_4 = config.get('PREVIOUS LOCATIONS', 'prevloc4')
                previouslocation_4d = previouslocation_4
                previouslocation_5 = config.get('PREVIOUS LOCATIONS', 'prevloc5')
                previouslocation_5d = previouslocation_5

                previouslocation_1data = config.get('PREVIOUS LOCATIONS', 'prevloc1_data')
                previouslocation_2data = config.get('PREVIOUS LOCATIONS', 'prevloc2_data')
                previouslocation_3data = config.get('PREVIOUS LOCATIONS', 'prevloc3_data')
                previouslocation_4data = config.get('PREVIOUS LOCATIONS', 'prevloc4_data')
                previouslocation_5data = config.get('PREVIOUS LOCATIONS', 'prevloc5_data')

            except:
                spinner.fail(text="Failed to load your previous locations!")
                print("")
                print(Fore.RED + Style.BRIGHT + "An error with your configuration file occured when",
                Fore.RED + Style.BRIGHT + "we tried to refresh current location information. For safety,",
                Fore.RED + Style.BRIGHT + "the previous location configurator will be exited out of.")
                printException()
                break
            logger.debug("previouslocation_1: %s ; previouslocation_1d: %s" %
                        (previouslocation_1, previouslocation_1d))
            logger.debug("previouslocation_2: %s ; previouslocation_2d: %s" %
                        (previouslocation_2, previouslocation_2d))
            logger.debug("previouslocation_3: %s ; previouslocation_3d: %s" %
                        (previouslocation_3, previouslocation_3d))
            logger.debug("previouslocation_4: %s ; previouslocation_4d: %s" %
                        (previouslocation_4, previouslocation_4d))
            logger.debug("previouslocation_5: %s ; previouslocation_5d: %s" %
                        (previouslocation_5, previouslocation_5d))


            logger.debug("previouslocation_1data: %s ; previouslocation_2data: %s" %
                        (previouslocation_1data, previouslocation_2data))

            logger.debug("previouslocation_3data: %s ; previouslocation_4data: %s" %
                        (previouslocation_3data, previouslocation_4data))
            logger.debug("previouslocation_5data: %s" % previouslocation_5data)

            if "pws:" in previouslocation_1d:
                # Delete pws from the display string
                previouslocation_1d = previouslocation_1d[4:]
                previouslocation_1d = "PWS " + previouslocation_1d.upper()
                logger.debug("previouslocation_1d: %s" % previouslocation_1d)


            if "pws:" in previouslocation_2d:
                # Delete pws from the display string
                previouslocation_2d = previouslocation_2d[4:]
                previouslocation_2d = "PWS " + previouslocation_2d.upper()
                logger.debug("previouslocation_2d: %s" % previouslocation_2d)

            if "pws:" in previouslocation_3d:
                # Delete pws from the display string
                previouslocation_3d = previouslocation_3d[4:]
                previouslocation_3d = "PWS " + previouslocation_3d.upper()
                logger.debug("previouslocation_3d: %s" % previouslocation_3d)

            if "pws:" in previouslocation_4d:
                # Delete pws from the display string
                previouslocation_4d = previouslocation_4d[4:]
                previouslocation_4d = "PWS " + previouslocation_4d.upper()
                logger.debug("previouslocation_4d: %s" % previouslocation_4d)

            if "pws:" in previouslocation_5d:
                # Delete pws from the display string
                previouslocation_5d = previouslocation_5d[4:]
                previouslocation_5d = "PWS " + previouslocation_5d.upper()
                logger.debug("previouslocation_5d: %s" % previouslocation_5d)

            spinner.stop()
            print("")
            print(Fore.YELLOW + Style.BRIGHT + "Your previously searched locations:")
            print(Fore.YELLOW + Style.BRIGHT + "Previous Location 1 - " + Fore.CYAN + Style.BRIGHT + previouslocation_1d)
            print(Fore.YELLOW + Style.BRIGHT + "Previous Location 2 - " + Fore.CYAN + Style.BRIGHT + previouslocation_2d)
            print(Fore.YELLOW + Style.BRIGHT + "Previous Location 3 - " + Fore.CYAN + Style.BRIGHT + previouslocation_3d)
            print(Fore.YELLOW + Style.BRIGHT + "Previous Location 4 - " + Fore.CYAN + Style.BRIGHT + previouslocation_4d)
            print(Fore.YELLOW + Style.BRIGHT + "Previous Location 5 - " + Fore.CYAN + Style.BRIGHT + previouslocation_5d)
            print("")
            print(Fore.YELLOW + Style.BRIGHT + "What would you like to do with your previous locations?")
            print(Fore.YELLOW + Style.BRIGHT + "- Remove a previous location - Enter " + Fore.CYAN + Style.BRIGHT + "1")
            print(Fore.YELLOW + Style.BRIGHT + "- Return to PyWeather - Enter " + Fore.CYAN + Style.BRIGHT + "2")
            prevconfig_menuinput = input("Input here: ").lower()

            logger.debug("prevconfig_menuinput: %s" % prevconfig_menuinput)
            if prevconfig_menuinput == "1":
                print(Fore.YELLOW + Style.BRIGHT + "Which location would you like to remove? Enter a number 1-5 representing",
                      Fore.YELLOW + Style.BRIGHT + "the previous locations 1-5.", sep="\n	          	")
                prevloc_removeinputnum = input("Input here: ").lower()
                logger.debug("prevloc_removeinputnum: %s" % prevloc_removeinputnum)
            
                try:
                    prevloc_removeinputnum = int(prevloc_removeinputnum)
                except ValueError:
                    print("", Fore.RED + Style.BRIGHT + "Whoops! Your input didn't seem to be a number. Returning to the",
                	  Fore.RED + Style.BRIGHT + "main menu.", sep="\n")
                    continue
                
                if prevloc_removeinputnum < 1 or prevloc_removeinputnum > 5:
                	print("", Fore.RED + Style.BRIGHT + "Whoops! You entered a previous location to remove that was not between 1-5.",
                              Fore.RED + Style.BRIGHT + "Returning to the main menu.", sep="\n")
                	continue
            
                prevloc_remove_isNone = False
                if prevloc_removeinputnum == 1 and previouslocation_1 == "None":
                	prevloc_remove_isNone = True
                if prevloc_removeinputnum == 2 and previouslocation_2 == "None":
                	prevloc_remove_isNone = True
                if prevloc_removeinputnum == 3 and previouslocation_3 == "None":
                	prevloc_remove_isNone = True
                if prevloc_removeinputnum == 4 and previouslocation_4 == "None":
                	prevloc_remove_isNone = True
                if prevloc_removeinputnum == 5 and previouslocation_5 == "None":
                	prevloc_remove_isNone = True
            
                logger.debug("prevloc_remove_isNone: %s" % prevloc_remove_isNone)
                if prevloc_remove_isNone is True:
                    print("", Fore.RED + Style.BRIGHT + "Whoops! The previous location you're trying to remove isn't set to anything.",
                          Fore.RED + Style.BRIGHT + "Returning to the main menu.", sep="\n")
                    continue
            
                if prevloc_removeinputnum == 1:
                    prevloc_removedisplay = previouslocation_1d
                elif prevloc_removeinputnum == 2:
                    prevloc_removedisplay = previouslocation_2d
                elif prevloc_removeinputnum == 3:
                    prevloc_removedisplay = previouslocation_3d
                elif prevloc_removeinputnum == 4:
                    prevloc_removedisplay = previouslocation_4d
                elif prevloc_removeinputnum == 5:
                    prevloc_removedisplay = previouslocation_5d
                logger.debug("prevloc_removedisplay: %s" % prevloc_removedisplay)
            
                print(Fore.YELLOW + Style.BRIGHT + "Are you sure you want to delete previous location " + Fore.CYAN + Style.BRIGHT + str(prevloc_removeinputnum)
                      + Fore.YELLOW + Style.BRIGHT + "?",
                      Fore.YELLOW + Style.BRIGHT + "This previous location is presently set to: " + Fore.CYAN + Style.BRIGHT + prevloc_removedisplay,
                      Fore.YELLOW + Style.BRIGHT + "This action cannot be undone! Yes or No.", sep="\n")
                prevloc_removeconfirm = input("Input here: ").lower()
                logger.debug("prevloc_removeconfirm: %s" % prevloc_removeconfirm)
                if prevloc_removeconfirm == "yes":
                    logger.debug("removing previous location...")
                elif prevloc_removeconfirm == "no":
                    print("", Fore.YELLOW + Style.BRIGHT + "Not deleting previous location " +
                          Fore.CYAN + Style.BRIGHT + str(prevloc_removeinputnum) + Fore.YELLOW + Style.BRIGHT + ".",
                	  Fore.CYAN + Style.BRIGHT + "Returning to the main menu.", sep="\n")
                    continue
                else:
                    print("", Fore.YELLOW + Style.BRIGHT + "Couldn't understand your input, and not deleting previous location "
                          + Fore.CYAN + Style.BRIGHT + str(prevloc_removeinputnum) + Fore.CYAN + Style.BRIGHT + ".",
                	  Fore.YELLOW + Style.BRIGHT + "Returning to the main menu.", sep="\n")
            
                if prevloc_removeinputnum <= 1:
                    config['PREVIOUS LOCATIONS']['prevloc1'] = previouslocation_2
                    logger.debug("PREVIOUS LOCATIONS/prevloc1 is now: %s" % previouslocation_2)
                    config['PREVIOUS LOCATIONS']['prevloc1_data'] = previouslocation_2data
                    logger.debug("PREVIOUS LOCATIONS/prevloc1_data is now: %s" % previouslocation_2data)
                if prevloc_removeinputnum <= 2:
                    config['PREVIOUS LOCATIONS']['prevloc2'] = previouslocation_3
                    logger.debug("PREVIOUS LOCATIONS/prevloc2 is now: %s" % previouslocation_3)
                    config['PREVIOUS LOCATIONS']['prevloc2_data'] = previouslocation_2data
                    logger.debug("PREVIOUS LOCATIONS/prevloc2_data is now: %s" % previouslocation_3data)
                if prevloc_removeinputnum <= 3:
                    config['PREVIOUS LOCATIONS']['prevloc3'] = previouslocation_4
                    logger.debug("PREVIOUS LOCATIONS/prevloc3 is now: %s" % previouslocation_4)
                    config['PREVIOUS LOCATIONS']['prevloc3_data'] = previouslocation_4data
                    logger.debug("PREVIOUS LOCATIONS/prevloc3_data is now: %s" % previouslocation_4data)
                if prevloc_removeinputnum <= 4:
                    config['PREVIOUS LOCATIONS']['prevloc4'] = previouslocation_5
                    logger.debug("PREVIOUS LOCATIONS/prevloc4 is now: %s" % previouslocation_5)
                    config['PREVIOUS LOCATIONS']['prevloc4_data'] = previouslocation_5data
                    logger.debug("PREVIOUS LOCATIONS/prevloc4_data is now: %s" % previouslocation_5data)
                if prevloc_removeinputnum <= 5:
                    config['PREVIOUS LOCATIONS']['prevloc5'] = "None"
                    logger.debug('PREVIOUS LOCATIONS/prevloc5 is now: "None"')
                    config['PREVIOUS LOCATIONS']['prevloc5_data'] = "None"
                    logger.debug('PREVIOUS LOCATIONS/prevloc2_data is now: "None"')
            
                try:
                    with open('storage//config.ini', 'w') as configfile:
                        config.write(configfile)
                    print(Fore.YELLOW + Style.BRIGHT + "Changes saved!")
                    continue
                except:
                    print(Fore.RED + Style.BRIGHT + "An issue occurred when trying to write new options to your config file.",
                          Fore.RED + Style.BRIGHT + "Please note that no changes were made to your config file.", sep="\n")
                    continue
            elif prevconfig_menuinput == "2":
                break
            else:
                print(Fore.YELLOW + Style.BRIGHT + "Your input could not be understood.")
                continue

# ModoUnreal work on stuff here...

#<--- Hurricane is above | About is below --->
    elif moreoptions == "16": # Changed
        print("", Fore.YELLOW + Style.BRIGHT + "-=-=- " + Fore.CYAN + Style.BRIGHT + "PyWeather" + Fore.YELLOW + Style.BRIGHT + " -=-=-",
              Fore.CYAN + Style.BRIGHT + "version " + about_version,
              Fore.YELLOW + Style.BRIGHT + "Build Number: " + Fore.CYAN + Style.BRIGHT + about_buildnumber,
              Fore.YELLOW + Style.BRIGHT + "Release Date: " + Fore.CYAN + Style.BRIGHT + about_releasedate,
              Fore.YELLOW + Style.BRIGHT + "Release Type: " + Fore.CYAN + Style.BRIGHT + about_releasetype,
              "",
              Fore.YELLOW + Style.BRIGHT + "Created, and mostly coded by: " + Style.BRIGHT + Fore.CYAN + about_maindevelopers,
              Fore.YELLOW + Style.BRIGHT + "Awesome contributors: " + Fore.CYAN + Style.BRIGHT + about_awesomecontributors,
              Fore.YELLOW + Style.BRIGHT + "Contributors: " + Fore.CYAN + Style.BRIGHT + about_contributors,
              "",
              Fore.YELLOW + Style.BRIGHT + "Powered by Weather Underground (wunderground.com)",
              "",
              Fore.YELLOW + Style.BRIGHT + "A special thanks to the developers of these libraries that are used in PyWeather:",
              Fore.CYAN + Style.BRIGHT + about_librariesinuse + Fore.RESET,
              "",
              Fore.YELLOW + Style.BRIGHT + "A special thanks to the developers & maintainers of these APIs that are used in PyWeather:",
              Fore.CYAN + Style.BRIGHT + about_apisinuse + Fore.RESET, sep="\n")
#<--- About is above, jokes are below --->
    elif moreoptions == "tell me a joke":
        logger.debug("moreoptions: %s" % moreoptions)
        # Jokes from searching "weather jokes" on DuckDuckGo (the first option)
        # They're jokes for kids.
        jokenum = randint(0,12)
        logger.debug("jokenum: %s" % jokenum)
        print("")
        if jokenum == 0:
            print(Fore.YELLOW + Style.BRIGHT + "How do hurricanes see?",
                  Fore.YELLOW + Style.BRIGHT + "With one eye!", sep="\n")
        elif jokenum == 1:
            print(Fore.YELLOW + Style.BRIGHT + "What does a cloud wear under his raincoat?",
                  Fore.YELLOW + Style.BRIGHT + "Thunderwear!", sep="\n")
        elif jokenum == 2:
            print(Fore.YELLOW + Style.BRIGHT + "What type of lightning likes to play sports?",
                  Fore.YELLOW + Style.BRIGHT + "Ball lightning!", sep="\n")
        elif jokenum == 3:
            print(Fore.YELLOW + Style.BRIGHT + "What type of cloud is so lazy, because it will never get up?",
                  Fore.YELLOW + Style.BRIGHT + "Fog!", sep="\n")
        elif jokenum == 4:
            print(Fore.YELLOW + Style.BRIGHT + "What did the lightning bolt say to the other lightning bolt?",
                  Fore.YELLOW + Style.BRIGHT + "You're shocking!", sep="\n")
        elif jokenum == 5:
            print(Fore.YELLOW + Style.BRIGHT + "Whatever happened to the cow that was lifted into the tornado?",
                  Fore.YELLOW + Style.BRIGHT + "Udder disaster!", sep="\n")
        elif jokenum == 6:
            print(Fore.YELLOW + Style.BRIGHT + "What did the one tornado say to the other?",
                  Fore.YELLOW + Style.BRIGHT + "Let's twist again like we did last summer.", sep="\n")
        elif jokenum == 7:
            print(Fore.YELLOW + Style.BRIGHT + "What did the thermometer say to the other thermometer?",
                  Fore.YELLOW + Style.BRIGHT + "You make my temperature rise.", sep="\n")
        elif jokenum == 8:
            print(Fore.YELLOW + Style.BRIGHT + "What's the difference between a horse and the weather?",
                  Fore.YELLOW + Style.BRIGHT + "One is reined up and the other rains down.", sep="\n")
        elif jokenum == 9:
            print(Fore.YELLOW + Style.BRIGHT + "What did the one raindrop say to the other raindrop?",
                  Fore.YELLOW + Style.BRIGHT + "My plop is bigger than your plop.", sep="\n")
        elif jokenum == 10:
            print(Fore.YELLOW + Style.BRIGHT + "Why did the woman go outdoors with her purse open?",
                  Fore.YELLOW + Style.BRIGHT + "Because she expected some change in the weather.", sep="\n")
        elif jokenum == 11:
            print(Fore.YELLOW + Style.BRIGHT + "What's the different between weather and climate?",
                  Fore.YELLOW + Style.BRIGHT + "You can't weather a tree, but you can climate.", sep="\n")
        elif jokenum == 12:
            print(Fore.YELLOW + Style.BRIGHT + "What did the hurricane say to the other hurricane?",
                  Fore.YELLOW + Style.BRIGHT + "I have my eye on you.", sep="\n")
# <--- Jokes are above | Programmer dad jokes is below --->
    elif moreoptions == "tell me a dad joke":
        logger.debug("moreoptions: %s" % moreoptions)
        dadjokenum = randint(0, 12)
        logger.debug("dadjokenum: %s" % dadjokenum)
        # Jokes from /r/programmerdadjokes top 12 posts
        # Top list fetched in late October 2017
        print("")
        if dadjokenum == 0:
            print(Fore.YELLOW + Style.BRIGHT + '["hip", "hip"]',
                  Fore.YELLOW + Style.BRIGHT + 'hip hip array!', sep="\n")
        elif dadjokenum == 1:
            print(Fore.YELLOW + Style.BRIGHT + "How did pirates collaborate before computers?",
                  Fore.YELLOW + Style.BRIGHT + "Pier to pier networking", sep="\n")
        elif dadjokenum == 2:
            print(Fore.YELLOW + Style.BRIGHT + "As a programmer, sometimes I feel a void",
                  Fore.YELLOW + Style.BRIGHT + "And I know I've reached the point of no return", sep="\n")
        elif dadjokenum == 3:
            print(Fore.YELLOW + Style.BRIGHT + "Why are 'i' and 'j' a good source of information?",
                  Fore.YELLOW + Style.BRIGHT + "They're always in the loop", sep="\n")
        elif dadjokenum == 4:
            print(Fore.YELLOW + Style.BRIGHT + "Two SQL developers walk into a bar & then walk straight out...",
                  Fore.YELLOW + Style.BRIGHT + "Because there were no tables they could join", sep="\n")
        elif dadjokenum == 5:
            print(Fore.YELLOW + Style.BRIGHT + "I'm starting a band called HTML Encoder",
                  Fore.YELLOW + Style.BRIGHT + "Looking to buy a guitar &amp;", sep="\n")
        elif dadjokenum == 6:
            print(Fore.YELLOW + Style.BRIGHT + "Why did the functions stop calling each other?",
                  Fore.YELLOW + Style.BRIGHT + "Because they had constant arguments.", sep="\n")
        elif dadjokenum == 7:
            print(Fore.YELLOW + Style.BRIGHT + "Why don't bachelors like Git?",
                  Fore.YELLOW + Style.BRIGHT + "Because they are afraid to commit.", sep="\n")
        elif dadjokenum == 8:
            print(Fore.YELLOW + Style.BRIGHT + "What do you call a skinny ghost?",
                  Fore.YELLOW + Style.BRIGHT + "BOOLEAN.", sep="\n")
        elif dadjokenum == 9:
            print(Fore.YELLOW + Style.BRIGHT + "You should be careful with functions that don't return a value.",
                  Fore.YELLOW + Style.BRIGHT + "In fact, I would just a void them.", sep="\n")
        elif dadjokenum == 10:
            print(Fore.YELLOW + Style.BRIGHT + "Kernel programming is like buying from IKEA.",
                  Fore.YELLOW + Style.BRIGHT + "Some assembly required.", sep="\n")
        elif dadjokenum == 11:
            print(Fore.YELLOW + Style.BRIGHT + "A man is sent to town by his wife to get bread",
                  Fore.YELLOW + Style.BRIGHT + "She says, 'oh and while you're there, get some eggs.'",
                  Fore.YELLOW + Style.BRIGHT + "He never came back.", sep="\n")
        elif dadjokenum == 12:
            print(Fore.YELLOW + Style.BRIGHT + "Why is gorillas' vision useful to programmers?",
                  Fore.YELLOW + Style.BRIGHT + "They have an apey eye.", sep="\n")
# <--- Programmer dad jokes is above | Yesterday's weather is below --->
    elif moreoptions == "9":
        yesterday_loops = 0
        yesterday_totalloops = 0
        logger.debug("yesterday_loops: %s ; yesterday_totalloops: %s"
                     % (yesterday_loops, yesterday_totalloops))
        logger.debug("yesterdayurl: %s" % yesterdayurl)
        if (yesterdaydata_prefetched is False or refresh_yesterdaydataflagged is True or time.time() - cachetime_yesterday >= cache_yesterdaytime):
            spinner.start(text="Refreshing yesterday's weather data...")
            try:
                yesterdayJSON = requests.get(yesterdayurl)
                yesterdaydata_prefetched = True
                cachetime_yesterday = time.time()
                refresh_yesterdaydataflagged = False
                logger.debug("yesterdaydata_prefetched: %s ; refresh_yesterdaydataflagged: %s" %
                             (yesterdaydata_prefetched, refresh_yesterdaydataflagged))
                spinner.stop()
            except:
                spinner.fail("Failed to refresh yesterday's weather data!")
                print("")
                print("When attempting to fetch yesterday's data, PyWeather ran into",
                      "an error. If you're on a network with a filter make sure that",
                      "'api.wunderground.com' is unblocked. Otherwise, make sure that",
                      "you have an internet connection, and that your Sega Megadrive works.",
                      sep="\n")
                printException()
                print("Press enter to continue.")
                input()
                continue

        spinner.start(text="Loading yesterday's weather information...")
        logger.debug("yesterdayJSON loaded with: %s" % yesterdayJSON)
        yesterday_json = json.loads(yesterdayJSON.text)
        if jsonVerbosity == True:
            logger.debug("yesterday_json: %s" % yesterday_json)
        else:
            logger.debug("Loaded 1 JSON.")
        yesterday_date = yesterday_json['history']['date']['pretty']
        logger.debug("yesterday_date: %s" % yesterday_date)
        spinner.stop()
        for data in yesterday_json['history']['dailysummary']:
            # Lay out display variables for yesterday's weather stuff.
            yesterday_showMinWind = True
            yesterday_showAvgWind = True
            logger.debug("yesterday_showMinWind: %s ; yesterday_showAvgWind: %s" %
                         (yesterday_showMinWind, yesterday_showAvgWind))
            yesterday_showMaxWind = True
            yesterday_showMinVis = True
            logger.debug("yesterday_showMaxWind: %s ; yesterday_showMinVis: %s" %
                         (yesterday_showMaxWind, yesterday_showMinVis))
            yesterday_showAvgVis = True
            yesterday_showMaxVis = True
            logger.debug("yesterday_showAvgVis: %s ; yesterday_showMaxVis: %s" %
                         (yesterday_showAvgVis, yesterday_showMaxVis))
            yesterday_showMinPress = True
            yesterday_showAvgPress = True
            logger.debug("yesterday_showMinPress: %s ; yesterday_showAvgPress: %s" %
                         (yesterday_showMinPress, yesterday_showAvgPress))
            yesterday_showMaxPress = True
            yesterday_showHumidity = True
            logger.debug("yesterday_showMaxPress: %s ; yesterday_showHumidity: %s" %
                         (yesterday_showMaxPress, yesterday_showHumidity))
            yesterday_showMinTemp = True
            yesterday_showAvgTemp = True
            logger.debug("yesterday_showMinTemp: %s ; yesterday_showAvgTemp: %s" %
                         (yesterday_showMinTemp, yesterday_showAvgTemp))
            yesterday_showMaxTemp = True
            yesterday_showMinDewpoint = True
            logger.debug("yesterday_showMaxTemp: %s ; yesterday_showMinDewpoint: %s" %
                         (yesterday_showMaxTemp, yesterday_showMinDewpoint))
            yesterday_showAvgDewpoint = True
            yesterday_showMaxDewpoint = True
            logger.debug("yesterday_showAvgDewpoint: %s ; yesterday_showMaxDewpoint: %s" %
                         (yesterday_showAvgDewpoint, yesterday_showMaxDewpoint))

            yesterday_avgTempF = str(data['meantempi'])
            yesterday_avgTempC = str(data['meantempm'])
            logger.debug("yesterday_avgTempF: %s ; yesterday_avgTempC: %s" %
                         (yesterday_avgTempF, yesterday_avgTempC))

            if yesterday_avgTempF == "" or yesterday_avgTempC == "":
                logger.info("yesterday_avgTempF is '' or yesterday_avgTempC is ''.")
                yesterday_showAvgTemp = False
                logger.debug("yesterday_showAvgTemp: %s" % yesterday_showAvgTemp)

            yesterday_avgDewpointF = str(data['meandewpti'])
            yesterday_avgDewpointC = str(data['meandewptm'])
            logger.debug("yesterday_avgDewpointF: %s ; yesterday_avgDewpointC: %s" %
                         (yesterday_avgDewpointF, yesterday_avgDewpointC))

            if yesterday_avgDewpointF == "" or yesterday_avgDewpointC == "":
                logger.info("yesterday_avgDewpointF is '' or yesterday_avgDewpointC is ''.")
                yesterday_showAvgDewpoint = False
                logger.debug("yesterday_showAvgDewpoint: %s" % yesterday_showAvgDewpoint)

            try:
                yesterday_avgPressureMB = str(data['meanpressurem'])
                logger.debug("yesterday_avgPressureMB: %s" % yesterday_avgPressureMB)
            except KeyError:
                yesterday_showAvgPress = False
                logger.debug("yesterday_showAvgPress: %s" % yesterday_showAvgPress)

            try:
                yesterday_avgPressureInHg = str(data['meanpressurei'])
                logger.debug("yesterday_avgPressureInHg: %s" % yesterday_avgPressureInHg)
            except KeyError:
                printException_loggerwarn()
                yesterday_showAvgPress = False
                logger.debug("yesterday_showAvgPress: %s" % yesterday_showAvgPress)

            try:
                yesterday_avgWindSpeedKPH = str(data['meanwindspdm'])
                logger.debug("yesterday_avgWindSpeedKPH: %s" % yesterday_avgWindSpeedKPH)
            except KeyError:
                printException_loggerwarn()
                yesterday_showAvgWind = False
                logger.debug("yesterday_showAvgWind: %s" % yesterday_showAvgWind)

            try:
                yesterday_avgWindSpeedMPH = str(data['meanwindspdi'])
                logger.debug("yesterday_avgWindSpeedMPH: %s" % yesterday_avgWindSpeedMPH)
            except KeyError:
                printException_loggerwarn()
                yesterday_showAvgWind = False
                logger.debug("yesterday_showAvgWind: %s" % yesterday_showAvgWind)

            try:
                yesterday_avgWindDegrees = str(data['meanwdird'])
                logger.debug("yesterday_avgWindDegrees: %s" % yesterday_avgWindDegrees)
            except KeyError:
                printException_loggerwarn()
                yesterday_showAvgWind = False
                logger.debug("yesterday_showAvgWind: %s" % yesterday_showAvgWind)

            try:
                yesterday_avgWindDirection = str(data['meanwdire'])
                logger.debug("yesterday_avgWindDirection: %s" % yesterday_avgWindDirection)
            except KeyError:
                printException_loggerwarn()
                yesterday_showAvgWind = False
                logger.debug("yesterday_showAvgWind: %s" % yesterday_showAvgWind)

            try:
                yesterday_avgVisibilityMI = str(data['meanvisi'])
                logger.debug("yesterday_AvgVisibilityMI: %s" % yesterday_avgVisibilityMI)
            except KeyError:
                printException_loggerwarn()
                yesterday_showAvgVis = False
                logger.debug("yesterday_showAvgVis: %s" % yesterday_showAvgVis)

            try:
                yesterday_avgVisibilityKM = str(data['meanvism'])
                logger.debug("yesterday_avgVisibilityKM: %s" % yesterday_avgVisibilityKM)
            except KeyError:
                printException_loggerwarn()
                yesterday_showAvgVis = False
                logger.debug("yesterday_showAvgVis: %s" % yesterday_showAvgVis)
            try:
                yesterday_maxHumidity = int(data['maxhumidity'])
                yesterday_minHumidity = int(data['minhumidity'])
                logger.debug("yesterday_maxHumidity: %s ; yesterday_minHumidity: %s" %
                             (yesterday_maxHumidity, yesterday_minHumidity))
            except ValueError:
                printException_loggerwarn()
                yesterday_showHumidity = False
                logger.debug("yesterday_showHumidity: %s" % yesterday_showHumidity)
            # This is a really nieve way of calculating the average humidity. Sue me.
            # In reality, WU spits out nothing for average humidity.

            # Run this code only if we have data.
            if yesterday_showHumidity is True:
                yesterday_avgHumidity = (yesterday_maxHumidity +
                                         yesterday_minHumidity)
                yesterday_avgHumidity = (yesterday_avgHumidity / 2)
                logger.debug("yesterday_avgHumidity: %s" % yesterday_avgHumidity)
                yesterday_maxHumidity = str(data['maxhumidity'])
                yesterday_minHumidity = str(data['minhumidity'])
                yesterday_avgHumidity = str(yesterday_avgHumidity)
                logger.info("Converted 3 vars to str.")

            yesterday_maxTempF = str(data['maxtempi'])
            yesterday_maxTempC = str(data['maxtempm'])
            logger.debug("yesterday_maxTempF: %s ; yesterday_maxTempC: %s" %
                         (yesterday_maxTempF, yesterday_maxTempC))

            if yesterday_maxTempF == "" or yesterday_maxTempC == "":
                logger.info("yesterday_maxTempF is '' or yesterday_maxTempC is ''.")
                yesterday_showMaxTemp = False
                logger.debug("yesterday_showMaxTemp: %s" % yesterday_showMaxTemp)

            yesterday_minTempF = str(data['mintempi'])
            yesterday_minTempC = str(data['mintempm'])
            logger.debug("yesterday_minTempF: %s ; yesterday_minTempC: %s" %
                         (yesterday_minTempF, yesterday_minTempC))

            if yesterday_minTempF == "" or yesterday_minTempC == "":
                logger.info("yesterday_minTempF is '' or yesterday_minTempC is ''.")
                yesterday_showMinTemp = False
                logger.debug("yesterday_showMinTemp: %s" % yesterday_showMinTemp)

            yesterday_maxDewpointF = str(data['maxdewpti'])
            yesterday_maxDewpointC = str(data['maxdewptm'])
            logger.debug("yesterday_maxDewpointF: %s ; yesterday_maxDewpointC: %s" %
                         (yesterday_maxDewpointF, yesterday_maxDewpointC))

            if yesterday_maxDewpointF == "" or yesterday_maxDewpointC == "":
                logger.info("yesterday_maxDewpointF is '' or yesterday_maxDewpointC is ''.")
                yesterday_showMaxDewpoint = False
                logger.debug("yesterday_showMaxDewpoint: %s" % yesterday_showMaxDewpoint)

            yesterday_minDewpointF = str(data['mindewpti'])
            yesterday_minDewpointC = str(data['mindewptm'])
            logger.debug("yesterday_minDewpointF: %s ; yesterday_minDewpointC: %s" %
                         (yesterday_minDewpointF, yesterday_minDewpointC))

            if yesterday_minDewpointF == "" or yesterday_minDewpointC == "":
                logger.info("yesterday_minDewpointF is '' or yesterday_minDewpointC is ''.")
                yesterday_showMinDewpoint = False
                logger.debug("yesterday_showMinDewpoint: %s" % yesterday_showMinDewpoint)

            try:
                yesterday_maxPressureInHg = str(data['maxpressurei'])
                logger.debug("yesterday_maxPressureInHg: %s" % yesterday_maxPressureInHg)
            except KeyError:
                printException_loggerwarn()
                yesterday_showMaxPress = False
                logger.debug("yesterday_showMaxPress: %s" % yesterday_showMaxPress)

            try:
                yesterday_maxPressureMB = str(data['maxpressurem'])
                logger.debug("yesterday_maxPressureMB: %s" % yesterday_maxPressureMB)
            except KeyError:
                printException_loggerwarn()
                yesterday_showMaxPress = False
                logger.debug("yesterday_showMaxPress: %s" % yesterday_showMaxPress)

            try:
                yesterday_minPressureInHg = str(data['minpressurei'])
                logger.debug("yesterday_minPressureInHg: %s" % yesterday_minPressureInHg)
            except KeyError:
                printException_loggerwarn()
                yesterday_showMinPress = False
                logger.debug("yesterday_showMinPress: %s" % yesterday_showMinPress)

            try:
                yesterday_minPressureMB = str(data['minpressurem'])
                logger.debug("yesterday_minPressureMB: %s" % yesterday_minPressureMB)
            except KeyError:
                printException_loggerwarn()
                yesterday_showMinPress = False
                logger.debug("yesterday_showMinPress: %s" % yesterday_showMinPress)

            try:
                yesterday_maxWindMPH = str(data['maxwspdi'])
                logger.debug("yesterday_maxWindMPH: %s" % yesterday_maxWindMPH)
            except KeyError:
                printException_loggerwarn()
                yesterday_showMaxWind = False
                logger.debug("yesterday_showMaxWind: %s" % yesterday_showMaxWind)

            try:
                yesterday_maxWindKPH = str(data['maxwspdm'])
                logger.debug("yesterday_maxWindKPH: %s" % yesterday_maxWindKPH)
            except KeyError:
                printException_loggerwarn()
                yesterday_showMaxWind = False
                logger.debug("yesterday_showMaxWind: %s" % yesterday_showMaxWind)

            try:
                yesterday_minWindMPH = str(data['minwspdi'])
                logger.debug("yesterday_minWindMPH: %s" % yesterday_minWindMPH)
            except KeyError:
                printException_loggerwarn()
                yesterday_showMinWind = False
                logger.debug("yesterday_showMinWind: %s" % yesterday_showMinWind)

            try:
                yesterday_minWindKPH = str(data['minwspdm'])
                logger.debug("yesterday_minWindKPH: %s" % yesterday_minWindKPH)
            except KeyError:
                printException_loggerwarn()
                yesterday_showMinWind = False
                logger.debug("yesterday_showMinWind: %s" % yesterday_showMinWind)

            try:
                yesterday_maxVisibilityMI = str(data['maxvisi'])
                logger.debug("yesterday_maxVisibilityMI: %s" % yesterday_maxVisibilityMI)
            except KeyError:
                printException_loggerwarn()
                yesterday_showMaxVis = False
                logger.debug("yesterday_showMaxVis: %s" % yesterday_showMaxVis)

            try:
                yesterday_maxVisibilityKM = str(data['maxvism'])
                logger.debug("yesterday_maxVisibilityKM: %s" % yesterday_maxVisibilityKM)
            except KeyError:
                printException_loggerwarn()
                yesterday_showMaxVis = False
                logger.debug("yesterday_showMaxVis: %s" % yesterday_showMaxVis)

            try:
                yesterday_minVisibilityMI = str(data['minvisi'])
                logger.debug("yesterday_minVisibilityMI: %s" % yesterday_minVisibilityMI)
            except KeyError:
                printException_loggerwarn()
                yesterday_showMinVis = False
                logger.debug("yesterday_showMinVis: %s" % yesterday_showMinVis)

            try:
                yesterday_minVisibilityKM = str(data['minvism'])
                logger.debug("yesterday_minVisibilityKM: %s" % yesterday_minVisibilityKM)
            except KeyError:
                printException_loggerwarn()
                yesterday_showMinVis = False
                logger.debug("yesterday_showMinVis: %s" % yesterday_showMinVis)

            yesterday_precipMM = str(data['precipm'])
            yesterday_precipIN = str(data['precipi'])
            logger.debug("yesterday_precipMM: %s ; yesterday_precipIN: %s" %
                         (yesterday_precipMM, yesterday_precipIN))


            # If the variable does exist (and a key error hasn't occurred), then validate the data.
            if yesterday_showMinWind is True:
                logger.info("yesterday_showMinWind is True.")
                if yesterday_minWindMPH == "":
                    logger.info("yesterday_mindWindMPH is ''.")
                    yesterday_showMinWind = False
                    logger.debug("yesterday_showMInWind: %s" % yesterday_showMinWind)
            if yesterday_showAvgWind is True:
                logger.info("yesterday_showAvgWind is True.")
                if yesterday_avgWindSpeedMPH == "":
                    logger.info("yesterday_avgWindSpeedMPH is ''.")
                    yesterday_showAvgWind = False
                    logger.debug("yesterday_showAvgWind: %s" % yesterday_showAvgWind)
            if yesterday_showMaxWind is True:
                logger.info("yesterday_showMaxWind is True.")
                if yesterday_maxWindMPH == "":
                    logger.info("yesterday_maxWindMPH is ''.")
                    yesterday_showMaxWind = False
                    logger.debug("yesterday_showMaxWind: %s" % yesterday_showMaxWind)
            if yesterday_showMinVis is True:
                logger.info("yesterday_showMinVis is True.")
                if yesterday_minVisibilityMI == "":
                    logger.info("yesterday_minVisibilityMI is ''.")
                    yesterday_showMinVis = False
                    logger.debug("yesterday_showMinVis: %s" % yesterday_showMinVis)

            if yesterday_showAvgVis is True:
                logger.info("yesterday_showAvgVis is True.")
                if yesterday_avgVisibilityMI == "":
                    logger.info("yesterday_avgVisibilityMI is ''.")
                    yesterday_showAvgVis = False
                    logger.debug("yesterday_showAvgVis: %s" % yesterday_showAvgVis)

            if yesterday_showMaxVis is True:
                logger.info("yesterday_showMaxVis is True.")
                if yesterday_maxVisibilityMI == "":
                    logger.info("yesterday_maxVisibilityMI is ''.")
                    yesterday_showMaxVis = False
                    logger.debug("yesterday_showMaxVis: %s" % yesterday_showMaxVis)

            if yesterday_showMinPress is True:
                logger.info("yesterday_showMinPress is True.")
                if yesterday_minPressureMB == "":
                    logger.info("yesterday_minPressureMB is ''.")
                    yesterday_showMinPress = False
                    logger.debug("yesterday_showMinPress: %s" % yesterday_showMinPress)

            if yesterday_showAvgPress is True:
                logger.info("yesterday_showAvgPress is True.")
                if yesterday_avgPressureMB == "":
                    logger.info("yesterday_avgPressureMB is ''.")
                    yesterday_showAvgPress = False
                    logger.debug("yesterday_showAvgPress: %s" % yesterday_showAvgPress)

            if yesterday_showMaxPress is True:
                logger.info("yesterday_showMaxPress is True.")
                if yesterday_maxPressureMB == "":
                    logger.info("yesterday_maxPressureMB is ''.")
                    yesterday_showMaxPress = False
                    logger.debug("yesterday_showMaxPress: %s" % yesterday_showMaxPress)

            if yesterday_precipMM == "T":
                logger.info("yesterday_precipMM is 'T'.")
                yesterday_precipdata = False
            else:
                yesterday_precipdata = True
            logger.debug("yesterday_precipdata: %s" % yesterday_precipdata)

        print(Fore.YELLOW + Style.BRIGHT + "Here's yesterday's weather for " + Fore.CYAN + Style.BRIGHT +
              str(location) + Fore.YELLOW + Style.BRIGHT + " on "
              + Fore.CYAN + Style.BRIGHT + yesterday_date)
        print("")
        print(Fore.YELLOW + Style.BRIGHT + "Here's the summary for the day.")
        if yesterday_showMinTemp is True:
            print(Fore.YELLOW + Style.BRIGHT + "Minimum Temperature: " + Fore.CYAN + Style.BRIGHT + yesterday_minTempF
                  + "°F (" + yesterday_minTempC + "°C)")
        if yesterday_showAvgTemp is True:
            print(Fore.YELLOW + Style.BRIGHT + "Average Temperature: " + Fore.CYAN + Style.BRIGHT + yesterday_avgTempF
                  + "°F (" + yesterday_avgTempC + "°C)")
        if yesterday_showMaxTemp is True:
            print(Fore.YELLOW + Style.BRIGHT + "Maxmimum Temperature: " + Fore.CYAN + Style.BRIGHT + yesterday_maxTempF
                  + "°F (" + yesterday_maxTempC + "°C)")
        if yesterday_showMinDewpoint is True:
            print(Fore.YELLOW + Style.BRIGHT + "Minimum Dew Point: " + Fore.CYAN + Style.BRIGHT + yesterday_minDewpointF
                  + "°F (" + yesterday_minDewpointC + "°C)")
        if yesterday_showAvgDewpoint is True:
            print(Fore.YELLOW + Style.BRIGHT + "Average Dew Point: " + Fore.CYAN + Style.BRIGHT + yesterday_avgDewpointF
                  + "°F (" + yesterday_avgDewpointC + "°C)")
        if yesterday_showMaxDewpoint is True:
            print(Fore.YELLOW + Style.BRIGHT + "Maximum Dew Point: " + Fore.CYAN + Style.BRIGHT + yesterday_maxDewpointF
                  + "°F (" + yesterday_maxDewpointC + "°C)")
        if yesterday_showHumidity is True:
            print(Fore.YELLOW + Style.BRIGHT + "Minimum Humidity: " + Fore.CYAN + Style.BRIGHT + yesterday_minHumidity
                  + "%")
            print(Fore.YELLOW + Style.BRIGHT + "Average Humidity: " + Fore.CYAN + Style.BRIGHT + yesterday_avgHumidity
                  + "%")
            print(Fore.YELLOW + Style.BRIGHT + "Maximum Humidity: " + Fore.CYAN + Style.BRIGHT + yesterday_maxHumidity
                  + "%")
        if yesterday_showMinWind is True:
            print(Fore.YELLOW + Style.BRIGHT + "Minimum Wind Speed: " + Fore.CYAN + Style.BRIGHT + yesterday_minWindMPH
                  + " mph (" + yesterday_minWindKPH + " kph)")

        if yesterday_showAvgWind is True:
            print(Fore.YELLOW + Style.BRIGHT + "Average Wind Speed: " + Fore.CYAN + Style.BRIGHT + yesterday_avgWindSpeedMPH
                  + " mph (" + yesterday_avgWindSpeedKPH + " kph)")

        if yesterday_showMaxWind is True:
            print(Fore.YELLOW + Style.BRIGHT + "Maximum Wind Speed: " + Fore.CYAN + Style.BRIGHT + yesterday_maxWindMPH
                  + " mph (" + yesterday_maxWindKPH + " kph)")

        if yesterday_showMinVis is True:
            print(Fore.YELLOW + Style.BRIGHT + "Minimum Visibility: " + Fore.CYAN + Style.BRIGHT + yesterday_minVisibilityMI
                  + " mi (" + yesterday_minVisibilityKM + " km)")

        if yesterday_showAvgVis is True:
            print(Fore.YELLOW + Style.BRIGHT + "Average Visibility: " + Fore.CYAN + Style.BRIGHT + yesterday_avgVisibilityMI
                  + " mi (" + yesterday_avgVisibilityKM + " km)")

        if yesterday_showMaxVis is True:
            print(Fore.YELLOW + Style.BRIGHT + "Maximum Visibility: " + Fore.CYAN + Style.BRIGHT + yesterday_maxVisibilityMI
                  + " mi (" + yesterday_maxVisibilityKM + " km)")

        if yesterday_showMinPress is True:
            print(Fore.YELLOW + Style.BRIGHT + "Minimum Pressure: " + Fore.CYAN + Style.BRIGHT + yesterday_minPressureInHg
                  + " inHg (" + yesterday_minPressureMB + " mb)")

        if yesterday_showAvgPress is True:
            print(Fore.YELLOW + Style.BRIGHT + "Average Pressure: " + Fore.CYAN + Style.BRIGHT + yesterday_avgPressureInHg
                  + " inHg (" + yesterday_avgPressureMB + " mb)")

        if yesterday_showMaxPress is True:
            print(Fore.YELLOW + Style.BRIGHT + "Maximum Pressure: " + Fore.CYAN + Style.BRIGHT + yesterday_maxPressureInHg
                  + " inHg (" + yesterday_maxPressureMB + " mb)")

        if yesterday_precipdata is True:
            print(Fore.YELLOW + Style.BRIGHT + "Total Precipitation: " + Fore.CYAN + Style.BRIGHT + yesterday_precipIN
                  + " in (" + yesterday_precipMM + " mm)")

        print("")
        print(Fore.RED + Style.BRIGHT + "To view hourly data for yesterday's weather, please press enter.")
        print(Fore.RED + Style.BRIGHT + "If you want to return to the main menu, press Control + C.")
        try:
            input()
        except KeyboardInterrupt:
            logger.debug("Continuing to the main menu...")
            continue

        # Start the pre-loop to see how many times we're looping.
        yesterdayhourlyLoops = 0
        for data in yesterday_json['history']['observations']:
            yesterday_tempF = str(data['tempi'])
            yesterdayhourlyLoops = yesterdayhourlyLoops + 1

        for data in yesterday_json['history']['observations']:
            logger.info("We're on iteration %s/%s. User iteration limit: %s."
                        % (yesterday_totalloops, yesterdayhourlyLoops, user_loopIterations))
            # Again, set up the display variables.
            yesterday_showWindSpeed = True
            yesterday_showWindGust = True
            logger.debug("yesterday_showWindSpeed: %s ; yesterday_showWindGust: %s" %
                         (yesterday_showWindSpeed, yesterday_showWindGust))
            yesterday_showVisibility = True
            yesterday_showWindChill = True
            logger.debug("yesterday_showVisibility: %s ; yesterday_showWindChill: %s" %
                         (yesterday_showVisibility, yesterday_showWindChill))
            yesterday_showHeatIndex = True
            yesterday_showPressure = True
            logger.debug("yesterday_showHeatIndex: %s ; yesterday_showPressure: %s" %
                         (yesterday_showHeatIndex, yesterday_showPressure))
            yesterday_showPrecip = True
            yesterday_showConditions = True
            logger.debug("yesterday_showPrecip: %s ; yesterday_showConditions: %s" %
                         (yesterday_showPrecip, yesterday_showConditions))
            yesterday_showTemp = True
            yesterday_showDewpoint = True
            logger.debug("yesterday_showTemp: %s ; yesterday_showDewpoint: %s" %
                         (yesterday_showTemp, yesterday_showDewpoint))
            yesterday_showWindDirection = True
            logger.debug("yesterday_showWindDirection: %s" % yesterday_showWindDirection)

            yesterday_time = data['date']['pretty']
            logger.debug("yesterday_time: %s" % yesterday_time)

            yesterday_tempF = str(data['tempi'])
            yesterday_tempC = str(data['tempm'])
            logger.debug("yesterday_tempF: %s ; yesterday_tempC: %s" %
                         (yesterday_tempF, yesterday_tempC))
            if yesterday_tempF == "-9999" or yesterday_tempF == "" or yesterday_tempC == "-9999" or yesterday_tempC == "":
                logger.info("yesterday_tempF is '-9999' or yesterday_tempF is '' or yesterday_tempC is '-9999' or yesterday_tempC is ''.")
                yesterday_showTemp = False
                logger.debug("yesterday_showTemp: %s" % yesterday_showTemp)

            yesterday_dewpointF = str(data['dewpti'])
            yesterday_dewpointC = str(data['dewptm'])
            logger.debug("yesterday_dewpointF: %s ; yesterday_dewpointC: %s" %
                         (yesterday_dewpointF, yesterday_dewpointC))

            if yesterday_dewpointF == "-9999" or yesterday_dewpointF == "" or yesterday_dewpointC == "-9999" or yesterday_dewpointC == "":
                logger.info("yesterday_dewpointF is '-9999' or yesterday_dewpointF is '' or yesterday_dewpointC is '-9999' or yesterday_dewpointC is ''.")
                yesterday_showDewpoint = False
                logger.debug("yesterday_showDewpoint: %s" % yesterday_showDewpoint)

            yesterday_windspeedKPH = str(data['wspdm'])
            yesterday_windspeedMPH = str(data['wspdi'])
            logger.debug("yesterday_windspeedKPH: %s ; yesterday_windspeedMPH: %s" %
                         (yesterday_windspeedKPH, yesterday_windspeedMPH))
            yesterday_windgustKPH = str(data['wgustm'])
            yesterday_windgustMPH = str(data['wgusti'])
            logger.debug("yesterday_windgustKPH: %s ; yesterday_windgustMPH: %s" %
                         (yesterday_windgustKPH, yesterday_windgustMPH))
            if yesterday_windspeedMPH == "-999.9" or yesterday_windspeedKPH == "-999.9" or yesterday_windspeedMPH == "" or yesterday_windspeedKPH == "":
                logger.info("yesterday_windspeedMPH is '-999.9' or yesterday_windspeedKPH is '' or yesterday_windspeedMPH is '' or yesterday_windspeedKPH is ''.")
                yesterday_showWindSpeed = False
                logger.debug("yesterday_showWindSpeed: %s" % yesterday_showWindSpeed)

            if yesterday_windgustMPH == "-999.0" or yesterday_windgustMPH == "-9999.0" or yesterday_windgustMPH == "" or yesterday_windgustKPH == "":
                logger.info("yesterday_windgustMPH is '-999.0' or yesterday_windgustMPH is '-9999.0' or yesterday_windgustMPH is '' or yesterday_windgustKPH is ''.")
                yesterday_showWindGust = False
                logger.debug("yesterday_showWindGust: %s" % yesterday_showWindGust)

            try:
                yesterday_windDegrees = str(data['wdird'])
            except KeyError:
                printException_loggerwarn()
                yesterday_showWindDirection = False
                logger.debug("yesterday_showWindDirection: %s" % yesterday_showWindDirection)

            try:
                yesterday_windDirection = data['wdire']
            except KeyError:
                printException_loggerwarn()
                yesterday_showWindDirection = False
                logger.debug("yesterday_showWindDirection: %s" % yesterday_showWindDirection)

            # If we haven't gotten a KeyError yet, check for bad wind direction data.
            if yesterday_showWindDirection is True:
                # Encase this inside of a true statement if we haven't hit a keyerror yet (yesterday_showWindDir is true).
                # This prevents variable errors to occur if there isn't any data.
                logger.info("yesterday_showWindDirection is True.")
                if yesterday_windDegrees == "" or yesterday_windDirection == "" or yesterday_windDegrees == "-9999":
                    logger.info("yesterday_windDegrees is '' or yesterday_windDirection is '' or yesterday_windDegrees is '-9999'.")
                    yesterday_showWindDirection = False
                    logger.debug("yesterday_showWindDirection: %s" % yesterday_showWindDirection)

            try:
                yesterday_visibilityKM = str(data['vism'])
            except KeyError:
                printException_loggerwarn()
                yesterday_showVisibility = False
                logger.debug("yesterday_showVisibility: %s" % yesterday_showVisibility)

            try:
                yesterday_visibilityMI = str(data['visi'])
            except KeyError:
                printException_loggerwarn()
                yesterday_showVisibility = False
                logger.debug("yesterday_showVisibility: %s" % yesterday_showVisibility)

            # Turn off showing yesterday's weather if visibility is -9999.0 mi or "" (no data)
            if yesterday_showVisibility is True:
                if yesterday_visibilityMI == "-9999.0" or yesterday_visibilityMI == "":
                    logger.info("yesterday_visibilityMI is '-9999.0' or yesterday_visibilityMI is ''.")
                    yesterday_showVisibility = False
                    logger.debug("yesterday_showVisibility: %s" % yesterday_showVisibility)

            try:
                yesterday_pressureMB = str(data['pressurem'])
            except KeyError:
                printException_loggerwarn()
                yesterday_showPressure = False
                logger.debug("yesterday_showPressure: %s" % yesterday_showPressure)

            try:
                yesterday_pressureInHg = str(data['pressurei'])
            except KeyError:
                printException_loggerwarn()
                yesterday_showPressure = False
                logger.debug("yesterday_showPressure: %s" % yesterday_showPressure)

            try:
                yesterday_windchillcheck = float(data['windchillm'])
            except KeyError:
                printException_loggerwarn()
                yesterday_showWindChill = False
                logger.debug("yesterday_showWindChill: %s" % yesterday_showWindChill)

            if yesterday_showWindChill is True:
                logger.info("yesterday_showWindChill is True.")
                if yesterday_windchillcheck == -999:
                    logger.info("yesterday_windchillcheck is '-999'.")
                    yesterday_showWindChill = False
                    logger.debug("yesterday_showWindChill: %s" % yesterday_showWindChill)
                else:
                    yesterday_showWindChill = False
                    yesterday_windchillC = str(data['windchillm'])
                    yesterday_windchillF = str(data['windchilli'])
                    logger.debug("yesterday_showWindChill: %s" % yesterday_showWindChill)
                    logger.debug("yesterday_windchillC: %s ; yesterday_windchillF: %s"
                                 % (yesterday_windchillC, yesterday_windchillF))

            try:
                yesterday_heatindexcheck = float(data['heatindexm'])
            except KeyError:
                printException_loggerwarn()
                yesterday_showHeatIndex = False
                logger.debug("yesterday_showHeatIndex: %s" % yesterday_showHeatIndex)

            if yesterday_showHeatIndex is True:
                logger.info("yesterday_showHeatIndex is True.")
                if yesterday_heatindexcheck == -9999:
                    logger.info("yesterday_heatindexcheck is '-9999'.")
                    yesterday_showHeatIndex = False
                    logger.debug("yesterday_showHeatIndex: %s" % yesterday_showHeatIndex)
                else:
                    yesterday_heatindexdata = True
                    yesterday_heatindexC = str(data['heatindexm'])
                    yesterday_heatindexF = str(data['heatindexi'])
                    logger.debug("yesterday_showHeatIndex: %s" % yesterday_showHeatIndex)
                    logger.debug("yesterday_heatindexC: %s ; yesterday_heatindexF: %s"
                                 % (yesterday_heatindexC, yesterday_heatindexF))
            try:
                yesterday_precipMM = float(data['precipm'])
                yesterday_precipIN = float(data['precipi'])
                yesterday_precipMM = str(yesterday_precipMM)
                yesterday_precipIN = str(yesterday_precipIN)
                logger.debug("yesterday_precipMM: %s ; yesterday_precipIN: %s" %
                             (yesterday_precipMM, yesterday_precipIN))
            except ValueError:
                printException_loggerwarn()
                yesterday_showPrecip = False
                logger.debug("yesterday_showPrecip: %s" % yesterday_showPrecip)
            except KeyError:
                printException_loggerwarn()
                yesterday_showPrecip = False
                logger.debug("yesterday_showPrecip: %s" % yesterday_showPrecip)

            if yesterday_showPrecip is True:
                logger.info("yesterday_showPrecip is True.")
                if yesterday_precipIN == "-9999.0":
                    logger.info("yesterday_precipIN is '-9999.0'.")
                    yesterday_showPrecip = False
                    logger.debug("yesterday_showPrecip: %s" % yesterday_showPrecip)


            try:
                yesterday_condition = str(data['conds'])
                logger.debug("yesterday_condition: %s" % yesterday_condition)
            except KeyError:
                printException_loggerwarn()
                yesterday_showConditions = False
                logger.debug("yesterday_showConditions: %s" % yesterday_showConditions)

            # Check for weather condition "" or "Unknown" - No data

            if yesterday_showConditions is True:
                logger.info("yesterday_showConditions is True.")
                if yesterday_condition == "" or yesterday_condition == "Unknown":
                    logger.info("yesterday_condition is '' or yesterday_condition is 'Unknown'.")
                    yesterday_showConditions = False
                    logger.debug("yesterday_showConditions: %s" % yesterday_showConditions)

            logger.info("Now printing weather data...")
            print("")
            print(Fore.YELLOW + Style.BRIGHT + yesterday_time + ":")
            if yesterday_showConditions is True:
                print(Fore.YELLOW + Style.BRIGHT + "Conditions: " + Fore.CYAN + Style.BRIGHT + yesterday_condition)
            if yesterday_showTemp is True:
                print(Fore.YELLOW + Style.BRIGHT + "Temperature: " + Fore.CYAN + Style.BRIGHT + yesterday_tempF
                      + "°F (" + yesterday_tempC + "°C)")
            if yesterday_showDewpoint is True:
                print(Fore.YELLOW + Style.BRIGHT + "Dew point: " + Fore.CYAN + Style.BRIGHT + yesterday_dewpointF
                      + "°F (" + yesterday_dewpointC + "°C)")
            if yesterday_showWindSpeed is True:
                print(Fore.YELLOW + Style.BRIGHT + "Wind speed: " + Fore.CYAN + Style.BRIGHT + yesterday_windspeedMPH
                      + " mph (" + yesterday_windspeedKPH + " kph)")

            if yesterday_showWindDirection is True:
                print(Fore.YELLOW + Style.BRIGHT + "Wind direction: " + Fore.CYAN + Style.BRIGHT + yesterday_windDirection
                      + " (" + yesterday_windDegrees + "°)")

            if yesterday_showWindGust is True:
                print(Fore.YELLOW + Style.BRIGHT + "Wind gusts: " + Fore.CYAN + Style.BRIGHT + yesterday_windgustMPH
                      + " mph (" + yesterday_windgustKPH + " kph)")

            if yesterday_showWindChill is True:
                print(Fore.YELLOW + Style.BRIGHT + "Wind chill: " + Fore.CYAN + Style.BRIGHT + yesterday_windchillF
                      + "°F (" + yesterday_windchillC + "°C)")

            if yesterday_showHeatIndex is True:
                print(Fore.YELLOW + Style.BRIGHT + "Heat index: " + Fore.CYAN + Style.BRIGHT + yesterday_heatindexF
                      + "°F (" + yesterday_heatindexC + "°C)")

            if yesterday_showPrecip is True:
                print(Fore.YELLOW + Style.BRIGHT + "Precipitation: " + Fore.CYAN + Style.BRIGHT + yesterday_precipIN
                      + " in (" + yesterday_precipMM + " mm)")

            if yesterday_showVisibility is True:
                print(Fore.YELLOW + Style.BRIGHT + "Visibility: " + Fore.CYAN + Style.BRIGHT + yesterday_visibilityMI
                      + " mi (" + yesterday_visibilityKM + " km)")

            yesterday_loops = yesterday_loops + 1
            yesterday_totalloops = yesterday_totalloops + 1
            logger.debug("yesterday_loops: %s ; yesterday_totalloops: %s"
                         % (yesterday_loops, yesterday_totalloops))

            if yesterday_totalloops == yesterdayhourlyLoops:
                logger.debug("Iterations now %s. Total iterations %s. Breaking..."
                             % (yesterday_totalloops, yesterdayhourlyLoops))

            if user_showCompletedIterations == True:
                print(Fore.YELLOW + Style.BRIGHT + "Completed iterations: " + Fore.CYAN + Style.BRIGHT + "%s/%s"
                      % (yesterday_totalloops, yesterdayhourlyLoops))

            if user_enterToContinue == True:
                if yesterday_totalloops == yesterdayhourlyLoops:
                    logger.debug("yesterday_totalloops = yesterdayhourlyLoops. breaking...")
                    break
                elif yesterday_loops == user_loopIterations:
                    logger.info("Asking user to continue.")
                    try:
                        print("")
                        print(Fore.RED + Style.BRIGHT + "Press enter to view the next " + str(user_loopIterations) +
                              " iterations of yesterday weather information.")
                        print(Fore.RED + Style.BRIGHT + "Otherwise, press Control + C to get back to the main menu.")
                        input()
                        yesterday_loops = 0
                        logger.info("Printing more weather data. yesterday_loops is now: %s"
                                    % yesterday_loops)
                    except KeyboardInterrupt:
                        logger.info("Breaking to main menu, user issued KeyboardInterrupt")
                        break

    elif moreoptions == "12":
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
        refresh_tidedataflagged = True
        logger.debug("refresh_sundataflagged: %s ; refresh_tidedataflagged: %s" %
                     (refresh_sundataflagged, refresh_tidedataflagged))
        refresh_hurricanedataflagged = True
        refresh_yesterdaydataflagged = True
        logger.debug("refresh_hurricanedataflagged: %s ; refresh_yesterdaydataflagged: %s" %
                     (refresh_hurricanedataflagged, refresh_yesterdaydataflagged))

    elif moreoptions == "extratools:1":
        if extratools_enabled is False:
            print(Fore.RED + Style.BRIGHT + "Whoops! Extra tools isn't enabled at this time.",
                  "If you'd like, I can enable the extra tools feature for you. Would you like the extratools feature at this time?",
                  "Yes or No.", sep="\n")
            extratools_enableinput = input("Input here: ").lower()
            logger.debug("extratools_enableinput: %s" % extratools_enableinput)
            if extratools_enableinput == "yes":
                config['UI']['extratools_enabled'] = 'True'
                logger.info("UI/extratools_enabled is now 'True'.")
                try:
                    with open('storage//config.ini', 'w') as configfile:
                        config.write(configfile)
                    print(Fore.YELLOW + Style.BRIGHT + "Extra tools is now enabled, and will be operational when you next boot up PyWeather.")
                    continue
                except:
                    print(Fore.RED + Style.BRIGHT + "An issue occurred when trying to save new configuration options.",
                          Fore.RED + Style.BRIGHT + "Please enable favorite locations in the config file. In the UI section, change",
                          Fore.RED + Style.BRIGHT + "extratools_enabled to 'True'.")
                    continue
            elif extratools_enableinput == "no":
                print(Fore.YELLOW + Style.BRIGHT + "Not enabling extra tools. Returning to the main menu.",
                      "You can come back to this menu to reenable extra tools, or go into your config file and",
                      "enable UI/extratools_enabled (set it to True).", sep="\n")
            else:
                print(Fore.YELLOW + Style.BRIGHT + "Your input wasn't understood, and as such favorite locations will not be enabled.",
                      "You can come back to this menu to reenable extra tools, or go into your config file and",
                      "enable UI/extratools_enabled (set it to True).")

        print(Fore.YELLOW + Style.BRIGHT + "Listing all cache times:")
        if cache_enabled is True:
            print(Fore.YELLOW + Style.BRIGHT + "PyWeather cache is ON (data will be automatically refreshed)")
        elif cache_enabled is False:
            print(Fore.YELLOW + Style.BRIGHT + "PyWeather cache is OFF (data will not be automatically refreshed)")
        print(Fore.YELLOW + Style.BRIGHT + "Current conditions: %s seconds (%s minutes) / limit %s seconds (%s minutes)" %
              (round(time.time() - cachetime_current, 2), round((time.time() - cachetime_current) / 60, 2), cache_currenttime, cache_currenttime / 60))
        # The variables in order: The raw cache time in seconds (rounded down to 2 decimal places, the raw cache time divided by 60, rounded to 2 (current cache time in mins)
        # After that, display the configured refresh cache limit, and divide the variable by 60 to get it in minutes.
        print(Fore.YELLOW + Style.BRIGHT + "Forecast data: %s seconds (%s minutes) / limit %s seconds (%s minutes)" %
              (round(time.time() - cachetime_forecast, 2), round((time.time() - cachetime_forecast) / 60, 2), cache_forecasttime, cache_forecasttime / 60))
        try:
            print(Fore.YELLOW + Style.BRIGHT + "Astronomy (sundata) data: %s seconds (%s minutes) / limit %s seconds (%s minutes)" %
                  (round(time.time() - cachetime_sundata, 2), round((time.time() - cachetime_sundata) / 60, 2), cache_sundatatime, cache_sundatatime / 60))
        except NameError:
            print(Fore.YELLOW + Style.BRIGHT + "Astronomy (sundata) data: Data not cached / limit %s seconds (%s minutes)" %
                  (cache_sundatatime, cache_sundatatime / 60))

        try:
            print(Fore.YELLOW + Style.BRIGHT + "10-day hourly data: %s seconds (%s minutes) / limit %s seconds (%s minutes)" %
                  (round(time.time() - cachetime_hourly10, 2), round((time.time() - cachetime_hourly10) / 60, 2), cache_tendayhourly, cache_tendayhourly / 60))
        except NameError:
            print(Fore.YELLOW + Style.BRIGHT + "10-day hourly data: Data not cached / limit %s seconds (%s minutes)" %
                  (cache_tendayhourly, cache_tendayhourly / 60))

        print(Fore.YELLOW + Style.BRIGHT + "1.5 day hourly data: %s seconds (%s minutes) / limit %s seconds (%s minutes)" %
              (round(time.time() - cachetime_hourly36, 2), round((time.time() - cachetime_hourly36) / 60, 2), cache_threedayhourly, cache_threedayhourly / 60))

        try:
            print(Fore.YELLOW + Style.BRIGHT + "Almanac data: %s seconds (%s minutes) / limit %s seconds (%s minutes)" %
                  (round(time.time() - cachetime_almanac, 2), round((time.time() - cachetime_almanac) / 60, 2), cache_almanactime, cache_almanactime / 60))
        except NameError:
            print(Fore.YELLOW + Style.BRIGHT + "Almanac data: Data not cached / limit %s seconds (%s minutes)" %
                  (cache_almanactime, cache_almanactime / 60))

        try:
            print(Fore.YELLOW + Style.BRIGHT + "Alerts data: %s seconds (%s minutes) / limit %s seconds (%s minutes)" %
                  (round(time.time() - cachetime_alerts, 2), round((time.time() - cachetime_alerts) / 60, 2), cache_alertstime, cache_alertstime / 60))
        except NameError:
            print(Fore.YELLOW + Style.BRIGHT + "Alerts data: Data not cached / limit %s seconds (%s minutes)" %
                  (cache_alertstime, cache_alertstime / 60))
        try:
            print(Fore.YELLOW + Style.BRIGHT + "Tide data: %s seconds (%s minutes) / limit %s seconds (%s minutes)" %
                  (round(time.time() - cachetime_tide, 2), round((time.time() - cachetime_tide) / 60, 2), cache_tidetime, cache_tidetime / 60))
        except NameError:
            print(Fore.YELLOW + Style.BRIGHT + "Tide data: Data not cached / limit %s secnods (%s minutes)" %
                  (cache_tidetime, cache_tidetime / 60))

        try:
            print(Fore.YELLOW + Style.BRIGHT + "Hurricane data: %s seconds (%s minutes) / limit %s seconds (%s minutes)" %
                  (round(time.time() - cachetime_hurricane, 2), round((time.time() - cachetime_hurricane) / 60, 2), cache_hurricanetime, cache_hurricanetime / 60))
        except NameError:
            print(Fore.YELLOW + Style.BRIGHT + "Hurricane data: Data not cached / limit %s seconds (%s minutes)" %
                  (cache_hurricanetime, cache_hurricanetime / 60))

        try:
            print(Fore.YELLOW + Style.BRIGHT + "Yesterday data: %s seconds (%s minutes), limit %s seconds (%s minutes)" %
                  (round(time.time() - cachetime_yesterday, 2), round((time.time() - cachetime_yesterday) / 60, 2), cache_yesterdaytime, cache_yesterdaytime / 60))
        except NameError:
            print(Fore.YELLOW + Style.BRIGHT + "Yesterday data: Data not cached / limit %s seconds (%s minutes)" %
                  (cache_yesterdaytime, cache_yesterdaytime / 60))


    else:
        logger.warn("Input could not be understood!")
        print(Fore.RED + Style.BRIGHT + "Not a valid option.")
        print("")
