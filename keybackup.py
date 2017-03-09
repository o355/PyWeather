# PyWeather API Key Backup - 0.4.2 beta
# (c) 2017, o355, GNU GPL 3.0

import configparser
import sys

config = configparser.ConfigParser()
config.read('storage//config.ini')

try:
    verbosity = config.getboolean('KEYBACKUP', 'keybackup_verbosity')
except:
    print("Could not load your config. Make sure your spelling is correct.")
    print("Setting variables to defaults...")
    print("")
    verbosity = False

if verbosity == True:
    import logging
    logger = logging.getLogger('pyweather_keybackup_0.4.2beta')
    logger.setLevel(logging.DEBUG)
    logformat = '%(asctime)s | %(levelname)s | %(message)s'
    logging.basicConfig(format=logformat)
    
print("Would you like to back up your API key?") 
confirmation = input("Input here: ").lower()
if verbosity == True:
    logger.debug("confirmation: %s" % confirmation)
if confirmation == "yes":
    print("Backing up your key...")
    apikey = open("storage//apikey.txt", 'r').close()
    open("backup//backkey.txt", 'w').close()
    open("backup//backkey.txt").write(apikey)
    open("backup//backkey.txt").close()
    print("Done!")