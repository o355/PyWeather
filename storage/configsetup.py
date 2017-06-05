# PyWeather Config Setup - 0.6.0.1 beta
# (c) 2017, o355. GNU GPL.

import sys
import configparser
import traceback
import os

config = configparser.ConfigParser()
config.read("config.ini")

# Check our working directory. This script can't work in the base PyWeather folder.
        
if "/pyweather/storage" in os.getcwd():
    cool = True
elif "/pyweather/" in os.getcwd():
    # If we are in the base folder, it's a perfect time to write to versioninfo.txt!
    try:
        versioninfo = open('updater//versioninfo.txt').close()
    except:
        open('updater//versioninfo.txt', 'w').close()
        with open("updater//versioninfo.txt", 'a') as out:
            out.write("0.6.0.1 beta")
            out.close()
    print("Whoops! You're running this script from PyWeather's base folder, but",
          "the script can't work when running from the base folder of PyWeather.",
          "Move into the storage folder, and run the script there.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()
else:
    print("Whoops! You're running this script from PyWeather's base folder, but",
          "the script can't work when running from the base folder of PyWeather.",
          "Move into the storage folder, and run the script there.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()
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
        
    try:
        config.add_section('CHANGELOG')
    except:
        print("Couldn't add the changelog section.")
    
    try:
        config.add_section('SUMMARY')
    except:
        print("Couldn't add the summary section.")
    
    try:
        config.add_section('VERBOSITY')
    except:
        print("Couldn't add the verbosity section.")
        
    try:
        config.add_section('TRACEBACK')
    except:
        print("Couldn't add the traceback section.")
        
    try:
        config.add_section('UI')
    except:
        print("Couldn't add the UI section.")
        
    try:
        config.add_section('HOURLY')
    except:
        print("Couldn't add the hourly section.")
        
    try:
        config.add_section('UPDATER')
    except:
        print("Couldn't add the updater section.")
        
    try:
        config.add_section('KEYBACKUP')
    except:
        print("Couldn't add the keybackup section.")
    
    try:
        config.add_section('PYWEATHER BOOT')
    except:
        print("Couldn't add the pyweather boot section.")
        
    try:
        config.add_section('USER')
    except:
        print("Couldn't add the user section.")
        
    try:
        config.add_section('CACHE')
    except:
        print("Couldn't add the cache section.")
        
    try:
        config.add_section('RADAR GUI')
    except:
        print("Couldn't add the radar gui section.")
        
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
    config['CACHE']['alerts_cachedtime'] = '5'
    config['CACHE']['current_cachedtime'] = '10'
    config['CACHE']['hourly_cachedtime'] = '60'
    config['CACHE']['forecast_cachedtime'] = '60'
    config['CACHE']['almanac_cachedtime'] = '240'
    config['CACHE']['sundata_cachedtime'] = '480'
    config['RADAR GUI']['radar_imagesize'] = 'normal'
    config['RADAR GUI']['bypassconfirmation'] = 'False'
    config['CACHE']['enabled'] = 'True'
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