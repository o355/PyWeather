# PyWeather API Key Backup - version 0.5.1 beta
# (c) 2017, o355, GNU GPL 3.0

import configparser
import sys

config = configparser.ConfigParser()
config.read('storage//config.ini')

try:
    verbosity = config.getboolean('VERBOSITY', 'keybackup_verbosity')
    saveLocation = config.get('KEYBACKUP', 'savelocation')
    tracebacksEnabled = config.getboolean('TRACEBACK', 'keybackup_tracebacks')
except:
    print("Could not load your config. Make sure your spelling is correct.")
    print("Setting variables to defaults...")
    print("")
    verbosity = False
    saveLocation = 'backup//backkey.txt'
    tracebacksEnabled = False

import logging
logger = logging.getLogger('pyweather_keybackup_0.5.1beta')
logformat = '%(asctime)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logformat)

if verbosity == True:
    logger.setLevel(logging.DEBUG)
elif tracebacksEnabled == True:
    logger.setLevel(logging.ERROR)
else:
    logger.setLevel(logging.CRITICAL)
    
print("Would you like to back up your API key?") 
confirmation = input("Input here: ").lower()
logger.debug("confirmation: %s" % confirmation)
if confirmation == "yes":
    logger.info("Selected yes - Backup key")
    print("Backing up your key...")
    apikey = open('storage//apikey.txt')
    apikey2 = apikey.read()
    open(saveLocation, 'w').close()
    logger.debug("apikey: %s" % apikey)
    logger.debug("Performed op: Delete %s" % saveLocation)
    with open(saveLocation, 'a') as out:
        logger.debug("out: %s" % out)
        out.write(apikey2)
        out.close()
        logger.debug("Performed ops: out.write(apikey2), out.close()")
    print("Done!")
    print("Press enter to exit.")
    input()
    sys.exit()
elif confirmation == "no":
    logger.info("Selected no - do not back up API key.")
    print("No changes will be made. Now closing.")
    print("Press enter to exit.")
    input()
    sys.exit()
else:
    logger.info("Couldn't understand input.")
    print("Couldn't understand your input. Closing as a precaution...")
    print("Press enter to exit.")
    input()
    sys.exit()