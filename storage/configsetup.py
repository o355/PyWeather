# PyWeather Config Setup - 0.6 beta
# (c) 2017, o355. GNU GPL.

import sys
import configparser
import traceback

config = configparser.ConfigParser()
config.read("config.ini")

# Verbosity and all that fun stuff isn't available here.
# If the config isn't set up, and by default, verbosity is off
# why should I code it in?

print("Would you like me to set up PyWeather's config?",
      "Yes or No.", sep="\n")
cd_confirmation = input("Input here: ").lower()
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
    config.add_section('CHANGELOG')
    config.add_section('SUMMARY')
    config.add_section('VERBOSITY')
    config.add_section('TRACEBACK')
    config.add_section('UI')
    config.add_section('HOURLY')
    config.add_section('UPDATER')
    config.add_section('KEYBACKUP')
    config.add_section('VERSIONS')
    config.add_section('PYWEATHER BOOT')
    config.add_section('USER')
    config['SUMMARY']['sundata_summary'] = 'False'
    config['SUMMARY']['almanac_summary'] = 'False'
    config['SUMMARY']['showalertsonsummary'] = 'True'
    config['VERBOSITY']['verbosity'] = 'False'
    config['VERBOSITY']['json_verbosity'] = 'False'
    config['VERBOSITY']['setup_verbosity'] = 'False'
    config['VERBOSITY']['setup_jsonverbosity'] = 'False'
    config['VERBOSITY']['updater_verbosity'] = 'False'
    config['VERBOSITY']['updater_jsonverbosity'] = 'False'
    config['VERBOSITY']['keybackup_verbosity'] = 'False'
    config['VERBOSITY']['configdefault_verbosity'] = 'False'
    config['TRACEBACK']['tracebacks'] = 'False'
    config['TRACEBACK']['setup_tracebacks'] = 'False'
    config['TRACEBACK']['updater_tracebacks'] = 'False'
    config['TRACEBACK']['configdefault_tracebacks'] = 'False'
    config['UI']['show_entertocontinue'] = 'True'
    config['UI']['detailedinfoloops'] = '6'
    config['UI']['forecast_detailedinfoloops'] = '5'
    config['UI']['show_completediterations'] = 'False'
    config['HOURLY']['10dayfetch_atboot'] = 'False'
    config['UPDATER']['autocheckforupdates'] = 'False'
    config['UPDATER']['show_updaterreleasetag'] = 'False'
    config['KEYBACKUP']['savedirectory'] = 'backup//'
    config['UPDATER']['allowGitForUpdating'] = 'False'
    config['PYWEATHER BOOT']['validateapikey'] = 'True'
    config['UPDATER']['showReleaseNotes'] = 'True'
    config['UPDATER']['showReleaseNotes_uptodate'] = 'False'
    config['UPDATER']['showNewVersionReleaseDate'] = 'True'
    config['USER']['configprovisioned'] = 'True'
    print("Committing changes...")
    try:
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    except:
        print("Hmmf...an odd error occurred. A full traceback will be",
              "printed below. Please report this issue on GitHub",
              "(github.com/o355/pyweather), as that would be greatly appreciated",
              "for trying to fix the bug that you just encountered!", sep="\n")
        traceback.print_exc()
        print("Press enter to exit.")
        input()
        sys.exit()
    print("All done! Try relaunching the script that asked you to",
          "provision your config file.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()
elif cd_confirmation == "no":
    print("Not provisioning your config file.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()
else:
    print("Couldn't understand input. Not provisioning your config file.",
          "You can always relaunch this script if you'd like to provison your config file.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()