# PyWeather API Key Backup - version 0.5.2.1 beta
# (c) 2017, o355, GNU GPL 3.0

import configparser
import sys
import logging
import traceback

# Try loading the versioninfo.txt file. If it isn't around, create the file with
# the present version info.

try:
    versioninfo = open('updater//versioninfo.txt')
except:
    open('updater//versioninfo.txt', 'w').close()
    with open("updater//versioninfo.txt", 'a') as out:
        out.write("0.6 beta")
        out.close()
        
# See if the config is "provisioned". If it isn't, a KeyError will occur,
# because it's not created. Creative.
try:
    configprovisioned = config.getboolean('USER', 'configprovisioned')
except KeyError:
    print("We ran into an error. Full traceback below.")
    traceback.print_exc()
    # In case of a code mistake when developing, confirmation is shown
    # to rewrite a user's config file.
    print("This isn't good. Your config file isn't provisioned.",
          "PyWeather can launch a script that will provision your config file.",
          "Would you like to provision your config file? Yes or No.", sep="\n")
    provisonconfig = input("Input here: ").lower()
    if provisonconfig == "yes":
        print("Now executing a script that will create your config file.")
        # using exec here, it should work on most platforms.
        exec(open("storage//configsetup.py").read())
    else:
        print("Either you selected no, or your input wasn't understood.",
              "PyWeather can still load, just with default configuration options.",
              "Would you like to continue loading PyWeather?"
              "Yes or No.", sep="\n")
        # Couldn't use the "continue" variable name. Eclipse got mad.
        contPWload = input("Input here: ").lower()
        if contPWload == "yes":
            print("You'll soon get an error that your config file couldn't be loaded.",
                  "This is normal, given the route you've taken.", sep="\n")
            continue
        elif contPWload == "no":
            print("Stopping PyWeather. If you want to provision your config, you",
                  "can laaunch configsetup.py in the storage folder.",
                  "Press enter to exit.", sep="\n")

config = configparser.ConfigParser()
config.read('storage//config.ini')

try:
    verbosity = config.getboolean('VERBOSITY', 'keybackup_verbosity')
    saveDirectory = config.get('KEYBACKUP', 'savedirectory')
    tracebacksEnabled = config.getboolean('TRACEBACK', 'keybackup_tracebacks')
except:
    print("Couldn't load your config file. Make sure there aren't any typos",
          "in the config, and that the config file is accessible.",
          "Setting config variables to their defaults.",
          "Here's the full traceback, in case you need it.", sep="\n")
    traceback.print_exc()
    verbosity = False
    saveDirectory = 'backup//backkey.txt'
    tracebacksEnabled = False

logger = logging.getLogger(name='pyweather_keybackup_0.5.2beta')
logformat = '%(asctime)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logformat)

if verbosity == True:
    logger.setLevel(logging.DEBUG)
elif tracebacksEnabled == True:
    logger.setLevel(logging.ERROR)
else:
    logger.setLevel(logging.CRITICAL)
    
def printException():
    if tracebacksEnabled == True:
        print("Here's the full traceback:")
        traceback.print_exc()
    
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
              "Please try again, and make sure your config file has the right spelling",
              "under the option for the backup directory. Furthermore, make sure that the",
              "backup directory specified in the config file has proper permissions.", sep="\n")
        printException()
        print("Press enter to exit.")
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
        print("We ran into an error when writing to the backup key text file.",
              "Please try again, and make sure your config file has the right spelling", 
              "under the option for the backup directory. Furthermore, make sure that the",
              "backup directory specified in the config has proper permissions.",sep="\n")
        printException()
        print("Press enter to exit.")
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
