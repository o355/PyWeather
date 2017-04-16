# PyWeather Configuration Defaults - 0.5.1 beta
# (c) 2017, o355

import sys
import configparser
import logging
import traceback

try:
    config = configparser.ConfigParser()
    config.read('storage//config.ini')
except:
    print("The config file couldn't be loaded. Make sure the file",
          "'storage//config.ini' can be loaded.",
          "Press enter to continue.", sep="\n")
    input()
    sys.exit()
    
try:
    verbosity = config.getboolean('VERBOSITY', 'configdefault_verbosity')
    tracebacksEnabled = config.getboolean('TRACEBACK', 'configdefault_tracebacks')
except:
    print("Couldn't load your config file. Make sure the config file has",
          "no typos. Setting config variables to their default.",
          "Here's the traceback if you need it:", sep="\n")
    traceback.print_exc()
    verbosity = False
    tracebacksEnabled = False
    
logger = logging.getLogger('pyweather_configdefault_0.5.1beta')
logformat = '%(asctime)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logformat)

# There are no critical messages in PyWeather, so this works by design.
if verbosity == True:
    logger.setLevel(logging.DEBUG)
elif tracebacksEnabled == True:
    logger.setLevel(logging.ERROR)
else:
    logger.setLevel(logging.CRITICAL)
    
logger.debug("Listing configuration options.")

    
print("Would you like me to set PyWeather configuration options to default?",
      "Yes or No:", sep="\n")
cd_confirmation = input("Input here: ").lower()
if cd_confirmation == "yes":
    print("Resetting variables to their defaults.")
    