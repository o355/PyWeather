# PyWeather Configuration Defaults - 0.6 beta
# (c) 2017, o355

import sys
import configparser
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
        
config = configparser.ConfigParser()
config.read('config.ini')
    
try:
    verbosity = config.getboolean('VERBOSITY', 'configdefault_verbosity')
    tracebacksEnabled = config.getboolean('TRACEBACK', 'configdefault_tracebacks')
except:
    print("Couldn't load your config file. Make sure there aren't any typos",
          "in the config, and that the config file is accessible.",
          "Setting config variables to their defaults.",
          "Here's the full traceback, in case you need it.", sep="\n")
    traceback.print_exc()
    verbosity = False
    tracebacksEnabled = False
    
logger = logging.getLogger(name='pyweather_configdefault_0.5.2beta')
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
    config['UPDATER']['allowGitForUpdating'] = 'False'
    logger.debug("UPDATER/allowGitForUpdating is now 'False'.")
    logger.debug("UI/alerts_USiterations is now '1'.")
    config['PYWEATHER BOOT']['validateapikey'] = 'True'
    logger.debug("PYWEATHER BOOT/validateapikey is now 'True'.")
    config['UPDATER']['showReleaseNotes'] = 'True'
    logger.debug("UPDATER/showReleaseNotes is now 'True'.")
    config['UPDATER']['showReleaseNotes_uptodate'] = 'False'
    logger.debug("UPDATER/showReleaseNotes_uptodate is now 'False'")
    config['UPDATER']['showNewVersionReleaseDate'] = 'True'
    logger.debug("UPDATER/showNewVersionReleaseDate is now 'True'.")
    config['USER']['configprovisioned'] = 'True'
    logger.debug("USER/configprovisioned is now 'True'.")
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