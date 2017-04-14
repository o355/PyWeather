# PyWeather Configuration Defaults - 0.5.1 beta
# (c) 2017, o355

import sys
import configparser
import logging
import traceback

try:
    config = config = configparser.ConfigParser()
    config.read('storage//config.ini')
except:
    print("The config file couldn't be loaded. Make sure the file",
          "'storage//config.ini' can be loaded.",
          "Press enter to continue.", sep="\n")
    input()
    sys.exit()
    
