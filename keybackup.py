# PyWeather API Key Backup - 0.5 beta
# (c) 2017, o355, GNU GPL 3.0

import configparser
import sys

config = configparser.ConfigParser()
config.read('storage//config.ini')

try:
    verbosity = config.getboolean('VERBOSITY', 'keybackup_verbosity')
    saveLocation = config.get('KEYBACKUP', 'savelocation')
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
    if verbosity == True:
        logger.info("Selected yes - Backup key")
    print("Backing up your key...")
    apikey = open('storage//apikey.txt')
    apikey2 = apikey.read()
    open(saveLocation, 'w').close()
    if verbosity == True:
        logger.debug("apikey: %s" % apikey)
    with open(saveLocation, 'a') as out:
        out.write(apikey2)
        out.close()
        if verbosity == True:
            logger.debug("Performed ops: out.write(apikey.read()), out.close()")
    print("Done!")
    print("Press enter to exit.")
    input()
    sys.exit()
elif confirmation == "no":
    if verbosity == True:
        logger.info("Selected no - do not back up API key.")
    print("No changes will be made. Now closing.")
    print("Press enter to exit.")
    input()
    sys.exit()
else:
    if verbosity == True:
        logger.info("Couldn't understand input.")
    print("Couldn't understand your input. Closing as a precaution...")
    print("Press enter to exit.")
    input()
    sys.exit()