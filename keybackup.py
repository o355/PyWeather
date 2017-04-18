# PyWeather API Key Backup - version 0.5.1 beta
# (c) 2017, o355, GNU GPL 3.0

import configparser
import sys
import logging

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
    verbosity = config.getboolean('VERBOSITY', 'keybackup_verbosity')
    saveDirectory = config.get('KEYBACKUP', 'savedirectory')
    tracebacksEnabled = config.getboolean('TRACEBACK', 'keybackup_tracebacks')
except:
    print("Could not load your config. Make sure your spelling is correct.")
    print("Setting variables to defaults...")
    print("")
    verbosity = False
    saveDirectory = 'backup//backkey.txt'
    tracebacksEnabled = False

logger = logging.getLogger(name='pyweather_keybackup_0.5.1beta')
logformat = '%(asctime)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logformat)

if verbosity == True:
    logger.setLevel(logging.DEBUG)
elif tracebacksEnabled == True:
    logger.setLevel(logging.ERROR)
else:
    logger.setLevel(logging.CRITICAL)
    
logger.debug("Listing configuration options:")
logger.debug("verbosity: %s ; saveDirectory: %s" %
             (verbosity, saveDirectory))
logger.debug("tracebacksEnabled: %s" %
             (tracebacksEnabled))

print("Would you like to back up your API key?") 
confirmation = input("Input here: ").lower()
logger.debug("confirmation: %s" % confirmation)
if confirmation == "yes":
    logger.info("Selected yes - Backup key")
    print("Backing up your key.")
    apikey = open('storage//apikey.txt')
    apikey2 = apikey.read()
    saveLocation = saveDirectory + "backkey.txt"
    try:
        open(saveLocation, 'w').close()
    except:
        print("We ran into an error when overwriting a possibly existing file.",
              "Please try again, and make sure your config file has the right spelling.",
              "Press enter to continue.", sep="\n")
        input()
        sys.exit()
    logger.debug("apikey: %s" % apikey)
    logger.debug("Performed op: Delete %s" % saveLocation)
    try:
        with open(saveLocation, 'a') as out:
            logger.debug("out: %s" % out)
            out.write(apikey2)
            out.close()
            logger.debug("Performed ops: out.write(apikey2), out.close()")
    except:
        print("We ran into an error when writing to the backup file.",
              "Please try again, and make sure your config file has the right spelling.",
              "Press enter to continue.", sep="\n")
        input()
        sys.exit()
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
