# PyWeather Config Setup - Version 0.6 beta
# (c) 2017, o355

import sys
import configparser
import traceback
import logging

config = configparser.ConfigParser()
config.read('config.ini')

try:
    verbosity = config.getboolean('VERBOSITY', 'configsetup_verbosity')
    tracebacksEnabled = config.getboolean('TRACEBACK', 'configsetup_tracebacks')
except:
    print("Could not load your config file! This could likely be an error",
          "from bad spelling, or another random error. Here's the traceback",
          "for error reporting, or a self-fix.", sep="\n")
    traceback.print_exc()
    verbosity = False
    tracebacksEnabled = False
    
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
logger.info("Listing configuration options...")
logger.debug("verbosity: %s ; tracebacksEnabled: %s" %
             (verbosity, tracebacksEnabled))

def printException():
    if tracebacksEnabled == True:
        print("Here's the full traceback (for bug reporting):")
        traceback.print_exc()
        
def printException_loggerwarn():
    if verbosity == True:
        logger.warn("Snap! We hit a non-critical error. Here's the traceback.")
        logger.warn(traceback.print_exc())
        
print("Beginning the full PyWeather configurator.",
      "About 30 options will be asked for. At any time, press Control + C",
      "to exit, and no changes will be saved.", sep="\n")

print("On the summary screen, would you like PyWeather to show sunrise/",
      "sunset data? This uses 1 extra API call at boot when enabled.",
      "By default, this is disabled. Yes or No.", sep="\n")
sundatasummary_input = input("Input here: ").lower()
logger.debug("sundatasummary_input: %s" % sundatasummary_input)
if sundatasummary_input == "yes":
    config['SUMMARY']['sundata_summary'] = 'True'
    print("Changes saved.")
    logger.debug("SUMMARY/sundata_summary is 'True'.")
elif sundatasummary_input == "no":
    config['SUMMARY']['sundata_summary'] = 'False'
    print("Changes saved.")
    logger.debug("SUMMARY/sundata_summary is 'False'.")
else:
    print("Couldn't understand your input. Defaulting to 'False'.")
    config['SUMMARY']['sundata_summary'] = 'False'
    print("Changes saved.")
    logger.debug("SUMMARY/sundata_summary is 'False'.")
    
print("On the summary screen, would you like PyWeather to show almanac",
      "data? This uses 1 extra API call at boot when enabled.",
      "By default, this is disabled. Yes or No.", sep="\n")
almanacsummary_input = input("Input here: ").lower()
logger.debug("almanacsummary_input: %s" % almanacsummary_input)
if almanacsummary_input == "yes":
    config['SUMMARY']['almanac_summary'] = 'True'
    print("Changes saved.")
    logger.debug("SUMMARY/almanac_summary is 'True'.")
elif almanacsummary_input == "no":
    config['SUMMARY']['almanac_summary'] = 'False'
    print("Changes saved.")
    logger.debug("SUMMARY/almanac_summary is 'False'.")
else:
    print("Couldn't understand your input. Defaulting to 'False'.")
    config['SUMMARY']['almanac_summary'] = 'False'
    print("Changes saved.")
    logger.debug("SUMMARY/almanac_summary is 'False'.")
    
print("On the summary screen, would you like PyWeather to show alerts?",
      "This uses 1 extra API call at boot when enabled. Alerts only work",
      "for US and EU locations.",
      "By default, this is enabled. Yes or No.", sep="\n")
alertssummary_input = input("Input here: ").lower()
logger.debug("alertssummary_input: %s" % alertssummary_input)
if alertssummary_input == "yes":
    config['SUMMARY']['showAlertsOnSummary'] = 'True'
    print("Changes saved.")
    logger.debug("SUMMARY/showAlertsOnSummary is 'True'.")
elif alertssummary_input == "no":
    config['SUMMARY']['showAlertsOnSummary'] = 'False'
    print("Changes saved.")
    logger.debug("SUMMARY/showAlertsOnSummary is 'False'.")
else:
    print("Couldn't understand your input. Defaulting to 'False'.")
    config['SUMMARY']['showAlertsOnSummary'] = 'False'
    print("Changes saved.")
    logger.debug("SUMMARY/showAlertsOnSummary is 'False'.")
    
print("In PyWeather, you can turn on the option for PyWeather to output",
      "extra process information, known as verbosity. Enabling this helps",
      "to troubleshoot an issue (if you know what you're doing). However,",
      "enabling this will cause extra PyWeather output.",
      "By default, this is disabled. Yes or No.", sep="\n")
pyweatherverbosity_input = input("Input here: ").lower()
logger.debug("pyweatherverbosity_input: %s" % pyweatherverbosity_input)
if pyweatherverbosity_input == "yes":
    config['VERBOSITY']['verbosity'] = 'True'
    print("Changes saved.")
    logger.debug("VERBOSITY/verbosity is 'True'.")
elif pyweatherverbosity_input == "no":
    config['VERBOSITY']['verbosity'] = 'False'
    print("Changes saved.")
    logger.debug("VERBOSITY/verbosity is 'False'.")
else:
    print("Couldn't understand your input. Defaulting to 'False'.")
    config['VERBOSITY']['verbosity'] = 'False'
    print("Changes saved.")
    logger.debug("VERBOSITY/verbosity is 'False'.")
    
print("In PyWeather Setup, you can turn on the option for PyWeather Setup to output",
      "extra process information, known as verbosity. Enabling this helps",
      "to troubleshoot an issue (if you know what you're doing). However,",
      "enabling this will cause extra PyWeather output.",
      "By default, this is disabled. Yes or No.", sep="\n")
pyweathersetupverbosity_input = input("Input here: ").lower()
logger.debug("pyweathersetupverbosity_input: %s" % pyweathersetupverbosity_input)
if pyweatherversetupbosity_input == "yes":
    config['VERBOSITY']['setup_verbosity'] = 'True'
    print("Changes saved.")
    logger.debug("VERBOSITY/setup_verbosity is 'True'.")
elif pyweathersetupverbosity_input == "no":
    config['VERBOSITY']['setup_verbosity'] = 'False'
    print("Changes saved.")
    logger.debug("VERBOSITY/setup_verbosity is 'False'.")
else:
    print("Couldn't understand your input. Defaulting to 'False'.")
    config['VERBOSITY']['setup_verbosity'] = 'False'
    print("Changes saved.")
    logger.debug("VERBOSITY/setup_verbosity is 'False'.")
    
print("In PyWeather Updater, you can turn on the option for PyWeather Updater to output",
      "extra process information, known as verbosity. Enabling this helps",
      "to troubleshoot an issue (if you know what you're doing). However,",
      "enabling this will cause extra PyWeather output.",
      "By default, this is disabled. Yes or No.", sep="\n")
pyweatherupdaterverbosity_input = input("Input here: ").lower()
logger.debug("pyweatherupdaterverbosity_input: %s" % pyweatherupdaterverbosity_input)
if pyweatherupdaterverbosity_input == "yes":
    config['VERBOSITY']['updater_verbosity'] = 'True'
    print("Changes saved.")
    logger.debug("VERBOSITY/updater_verbosity is 'True'.")
elif pyweatherupdaterverbosity_input == "no":
    config['VERBOSITY']['updater_verbosity'] = 'False'
    print("Changes saved.")
    logger.debug("VERBOSITY/updater_verbosity is 'False'.")
else:
    print("Couldn't understand your input. Defaulting to 'False'.")
    config['VERBOSITY']['updater_verbosity'] = 'False'
    print("Changes saved.")
    logger.debug("VERBOSITY/updater_verbosity is 'False'.")
    
print("In PyWeather Key Backup, you can turn on the option for PyWeather Key Backup to output",
      "extra process information, known as verbosity. Enabling this helps",
      "to troubleshoot an issue (if you know what you're doing). However,",
      "enabling this will cause extra PyWeather output.",
      "By default, this is disabled. Yes or No.", sep="\n")
pyweatherkeybackupverbosity_input = input("Input here: ").lower()
logger.debug("pyweatherkeybackupverbosity_input: %s" % pyweatherkeybackupverbosity_input)
if pyweatherkeybackupverbosity_input == "yes":
    config['VERBOSITY']['keybackup_verbosity'] = 'True'
    print("Changes saved.")
    logger.debug("VERBOSITY/keybackup_verbosity is 'True'.")
elif pyweatherkeybackupverbosity_input == "no":
    config['VERBOSITY']['keybackup_verbosity'] = 'False'
    print("Changes saved.")
    logger.debug("VERBOSITY/keybackup_verbosity is 'False'.")
else:
    print("Couldn't understand your input. Defaulting to 'False'.")
    config['VERBOSITY']['keybackup_verbosity'] = 'False'
    print("Changes saved.")
    logger.debug("VERBOSITY/keybackup_verbosity is 'False'.")
    
print("In PyWeather Configuration Defaults, you can turn on the option for PyWeather Configuration Defaults to output",
      "extra process information, known as verbosity. Enabling this helps",
      "to troubleshoot an issue (if you know what you're doing). However,",
      "enabling this will cause extra PyWeather output.",
      "By default, this is disabled. Yes or No.", sep="\n")
pyweathercdverbosity_input = input("Input here: ").lower()
logger.debug("pyweathercdverbosity_input: %s" % pyweathercdverbosity_input)
if pyweathercdverbosity_input == "yes":
    config['VERBOSITY']['configdefault_verbosity'] = 'True'
    print("Changes saved.")
    logger.debug("VERBOSITY/configdefault_verbosity is 'True'.")
elif pyweathercdverbosity_input == "no":
    config['VERBOSITY']['configdefault_verbosity'] = 'False'
    print("Changes saved.")
    logger.debug("VERBOSITY/configdefault_verbosity is 'False'.")
else:
    print("Couldn't understand your input. Defaulting to 'False'.")
    config['VERBOSITY']['configdefault_verbosity'] = 'False'
    print("Changes saved.")
    logger.debug("VERBOSITY/configdefault_verbosity is 'False'.")
    
print("In PyWeather Config Setup, you can turn on the option for PyWeather Config Setup to output",
      "extra process information, known as verbosity. Enabling this helps",
      "to troubleshoot an issue (if you know what you're doing). However,",
      "enabling this will cause extra PyWeather output.",
      "By default, this is disabled. Yes or No.", sep="\n")
pyweathercsverbosity_input = input("Input here: ").lower()
logger.debug("pyweathercsverbosity_input: %s" % pyweathercsverbosity_input)
if pyweathercsverbosity_input == "yes":
    config['VERBOSITY']['configsetup_verbosity'] = 'True'
    print("Changes saved.")
    logger.debug("VERBOSITY/configsetup_verbosity is 'True'.")
elif pyweathercsverbosity_input == "no":
    config['VERBOSITY']['configsetup_verbosity'] = 'False'
    print("Changes saved.")
    logger.debug("VERBOSITY/configsetup_verbosity is 'False'.")
else:
    print("Couldn't understand your input. Defaulting to 'False'.")
    config['VERBOSITY']['configsetup_verbosity'] = 'False'
    print("Changes saved.")
    logger.debug("VERBOSITY/configsetup_verbosity is 'False'.")
    
