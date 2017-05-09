# PyWeather Configurator - Version 0.6 beta
# (c) 2017, o355

import sys
import configparser
import traceback
import logging

config = configparser.ConfigParser()
config.read('config.ini')

try:
    verbosity = config.getboolean('VERBOSITY', 'config_verbosity')
    tracebacks = config.getboolean('TRACEBACK', 'config_tracebacks')
except:
    print("Could not load your config file! This could likely be an error",
          "from bad spelling, or another random error. Here's the traceback",
          "for error reporting, or a self-fix.", sep="\n")
    traceback.print_exc()
    verbosity = False
    tracebacks = False
    
logger = logging.getLogger(name='pyweather_configurator_0.6beta')
logformat = '%(asctime)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logformat)

if verbosity == True:
    logger.setLevel(logging.DEBUG)
elif tracebacksEnabled == True:
    logger.setLevel(logging.ERROR)
else:
    logger.setLevel(logging.CRITICAL)
    
logger.info("Starting up PyWeather Configurator 0.6 beta.")