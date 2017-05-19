# (c) 2017, o355. GNU GPL.

import sys
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# Verbosity and all that fun stuff isn't available here.
# If the config isn't set up, and by default, verbosity is off
# why should I code it in?

print("Would you like me to set up PyWeather's config?",
      "Yes or No.", sep="\n")
cd_confirmation = input("Input here: ").lower()
logger.debug("cd_confirmation: %s" % cd_confirmation)
if cd_confirmation == "yes":
    try:
        provisioned = config['USER']['configprovisioned']
        print("Your config file is already provisioned! Would you still",
              "like to have your config provisioned?", 
              "Yes or No.", sep="\n")
        keepprovisioning = input("Input here: ").lower()
        if keepprovisioning == "yes":
            print("Re-provisioning your config...")
        elif keepprovisioning == "no":
            print("Not re-provisioning your config.",
                  "Press enter to exit.")
            input()
            sys.exit()
    except:
        print("Setting up your config...")
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
    config['VERSIONS']['overrideVersion'] = 'False'
    logger.debug("VERSIONS/overrideVersion is now 'False'.")
    config['VERSIONS']['overrideBuildNumber'] = '60'
    logger.debug("VERSIONS/overrideBuildNumber is now '60'.")
    config['VERSIONS']['overrideVersionText'] = '0.6 beta'
    logger.debug("VERSIONS/overrideVersionText is now '0.6 beta'.")
    config['SUMMARY']['showAlertsOnSummary'] = 'True'
    logger.debug("SUMMARY/showAlertsOnSummary is now 'True'.")
    config['UI']['alerts_EUiterations'] = '2'
    logger.debug("UI/alerts_EUiterations is now '2'.")
    config['UI']['alerts_USiterations'] = '1'
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