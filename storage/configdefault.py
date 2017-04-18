# PyWeather Configuration Defaults - 0.5.1 beta
# (c) 2017, o355

import sys
import configparser
import logging
import traceback

try:
    config = configparser.ConfigParser()
    config.read('config.ini')
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
    
logger = logging.getLogger(name='pyweather_configdefault_0.5.1beta')
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
logger.debug("verbosity: %s ; tracebacksEnabled: %s"
             % (verbosity, tracebacksEnabled))

def printException():
    if tracebacksEnabled == True:
        print("Here's the full traceback (for error reporting):")
        traceback.print_exc()
    
print("Would you like me to set PyWeather configuration options to default?",
      "Yes or No.", sep="\n")
cd_confirmation = input("Input here: ").lower()
logger.debug("cd_confirmation: %s" % cd_confirmation)
if cd_confirmation == "yes":
    print("Resetting variables to their defaults.",
          "Setting variables...", sep="\n")
    config['SUMMARY']['sundata_summary'] = 'False'
    logger.debug("SUMMARY/sundata_summary is now 'False'.")
    config['SUMMARY']['almanac_summary'] = 'False'
    logger.debug("SUMMARY/almanac_summary is now 'False'.")
    config['VERBOSITY']['verbosity'] = 'False'
    logger.debug("VERBOSITY/verbosity is now 'False'.")
    config['VERBOSITY']['json_verbosity'] = 'False'
    logger.debug("VERBOSITY/json_verbosity is now 'False'.")
    config['VERBOSITY']['setup_verbosity'] = 'False'
    logger.debug("VERBOSITY/setup_verbosity is now 'False'.")
    config['VERBOSITY']['setup_jsonverbosity'] = 'False'
    logger.debug("VERBOSITY/setup_jsonverbosity is now 'False'.")
    config['VERBOSITY']['updater_verbosity'] = 'False'
    logger.debug("VERBOSITY/updater_verbosity is now 'False'.")
    config['VERBOSITY']['updater_jsonverbosity'] = 'False'
    logger.debug("VERBOSITY/updater_jsonverbosity is now 'False'.")
    config['VERBOSITY']['keybackup_verbosity'] = 'False'
    logger.debug("VERBOSITY/keybackup_verbosity is now 'False'.")
    config['VERBOSITY']['configdefault_verbosity'] = 'False'
    logger.debug("VERBOSITY/configdefault_verbosity is now 'False'.")
    config['TRACEBACK']['tracebacks'] = 'False'
    logger.debug("TRACEBACK/tracebacks is now 'False'.")
    config['TRACEBACK']['setup_tracebacks'] = 'False'
    logger.debug("TRACEBACK/setup_tracebacks is now 'False'.")
    config['TRACEBACK']['updater_tracebacks'] = 'False'
    logger.debug("TRACEBACK/updater_tracebacks is now 'False'.")
    config['TRACEBACK']['configdefault_tracebacks'] = 'False'
    logger.debug("TRACEBACK/configdefault_tracebacks is now 'False'.")
    config['UI']['show_entertocontinue'] = 'True'
    logger.debug("UI/show_entertocontinue is now 'True'")
    config['UI']['detailedinfoloops'] = '6'
    logger.debug("UI/detailedinfoloops is now '6'.")
    config['UI']['forecast_detailedinfoloops'] = '5'
    logger.debug("UI/forecast_detailedinfoloops is now '5'.")
    config['UI']['show_completediterations'] = 'False'
    logger.debug("UI/show_completediterations is now 'False'.")
    config['HOURLY']['10dayfetch_atboot'] = 'False'
    logger.debug("HOURLY/10dayfetch_atboot is now 'False'.")
    config['UPDATER']['autocheckforupdates'] = 'False'
    logger.debug("UPDATER/autocheckforupdates is now 'False'.")
    config['UPDATER']['show_updaterreleasetag'] = 'False'
    logger.debug("UPDATER/show_updaterreleasetag is now 'False'.")
    config['KEYBACKUP']['savedirectory'] = 'backup//'
    logger.debug("KEYBACKUP/savedirectory is now 'backup//'.")
    print("Committing changes...")
    try:
        with open('config.ini', 'w') as configfile:
            logger.debug("configfile: %s" % configfile)
            config.write(configfile)
            logger.info("Performed operation: config.write(configfile)")
    except:
        print("The config file couldn't be written to.",
              "Make sure the config file can be written to.", sep="\n")
        printException()
        print("Press enter to exit.")
        input()
        sys.exit()
    print("All done!",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()
elif cd_confirmation == "no":
    print("Not setting config options to default options.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()
else:
    print("Couldn't understand input. Not setting config options to",
          "default options.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()