# PyWeather Setup - version 0.6.1 beta
# (c) 2017, o355, licensed under GNU GPL v3

# Same deal as the main script.
# Verbosity turns on verbosity, jsonVerbosity outputs full JSONs.
# Because I'm cool, you can have verbosity off, but JSON verbosity on.

import sys
if sys.version_info < (3, 0, 0):
    print("You'll need Python 3 to run PyWeather.",
          "Press enter to exit.")
    input()
    sys.exit()
elif (sys.version_info > (3, 0, 0)
      and sys.version_info < (3, 5, 0)):
    print("You have a Python version between 3.0 and 3.4.",
          "While PyWeather will work, you may experience a few quirks.",
          "Try updating to Python 3.6, as it works more reliably.",
          "Please take note of this in PyWeather.","", sep="\n")

import configparser
import traceback
import subprocess
import logging
import os
import urllib

# Try loading the versioninfo.txt file. If it isn't around, create the file with
# the present version info.

try:
    versioninfo = open('updater//versioninfo.txt')
except:
    open('updater//versioninfo.txt', 'w').close()
    with open("updater//versioninfo.txt", 'a') as out:
        out.write("0.6.1 beta")
        out.close()

config = configparser.ConfigParser()
config.read('storage//config.ini')

def configprovision():
    try:
        config.add_section('SUMMARY')
    except configparser.DuplicateSectionError:
        print("Cache section could not be added.")

    try:
        config.add_section('VERBOSITY')
    except configparser.DuplicateSectionError:
        print("Verbosity section could not be added.")

    try:
        config.add_section('TRACEBACK')
    except configparser.DuplicateSectionError:
        print("Traceback section could not be added.")

    try:
        config.add_section('UI')
    except configparser.DuplicateSectionError:
        print("UI section could not be added.")

    try:
        config.add_section('HOURLY')
    except configparser.DuplicateSectionError:
        print("Hourly section could not be added.")

    try:
        config.add_section('UPDATER')
    except configparser.DuplicateSectionError:
        print("Updater section could not be added.")

    try:
        config.add_section('KEYBACKUP')
    except configparser.DuplicateSectionError:
        print("Key Backup section could not be added.")

    try:
        config.add_section('PYWEATHER BOOT')
    except configparser.DuplicateSectionError:
        print("PyWeather Boot section could not be added.")

    try:
        config.add_section('USER')
    except configparser.DuplicateSectionError:
        print("User section could not be added.")
    try:
        config.add_section('CACHE')
    except configparser.DuplicateSectionError:
        print("Cache section could not be added.")

    try:
        config.add_section('RADAR GUI')
    except configparser.DuplicateSectionError:
        print("Radar GUI section could not be added.")

    try:
        config.add_section('GEOCODER')
    except configparser.DuplicateSectionError:
        print("Geocoder section could not be added.")

    config['SUMMARY']['sundata_summary'] = 'False'
    config['SUMMARY']['almanac_summary'] = 'False'
    config['SUMMARY']['showalertsonsummary'] = 'True'
    config['SUMMARY']['showtideonsummary'] = 'False'
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
    config['UI']['alerts_usiterations'] = '1'
    config['UI']['alerts_euiterations'] = '2'
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
    config['CACHE']['enabled'] = 'True'
    config['CACHE']['alerts_cachedtime'] = '5'
    config['CACHE']['current_cachedtime'] = '10'
    config['CACHE']['hourly_cachedtime'] = '60'
    config['CACHE']['forecast_cachedtime'] = '60'
    config['CACHE']['almanac_cachedtime'] = '240'
    config['CACHE']['sundata_cachedtime'] = '480'
    config['CACHE']['tide_cachedtime'] = '480'
    config['RADAR GUI']['radar_imagesize'] = 'normal'
    config['RADAR GUI']['bypassconfirmation'] = 'False'
    config['GEOCODER']['scheme'] = 'https'
    try:
        with open('storage//config.ini', 'w') as configfile:
            config.write(configfile)
    except:
        print("Hmmf...an odd error occurred. A full traceback will be",
              "printed below. Please report this issue on GitHub",
              "(github.com/o355/pyweather), as that would be greatly appreciated",
              "for trying to fix the bug that you just encountered!", sep="\n")
        traceback.print_exc()
        # Giving users choice, unlike Microsoft.
        print("Would you like to continue using PyWeather with an unprovisioned config?",
              "It's highly recommended you don't continue, as you may encounter",
              "unexpected errors and issues with using PyWeather. Yes or No.", sep="\n")
        provisionfailed_continue = input("Input here: ").lower()
        if provisionfailed_continue == "yes":
            print("Continuing with PyWeather Setup. Please remember, you may encounter",
                  "unexpected errors and issues. You can always retry provisioning your config",
                  "by using the configsetup.py script in the storage folder.", sep="\n")
        elif provisionfailed_continue == "no":
            print("Stopping PyWeather Setup. You can retry to provision your config by using",
                  "the configsetup.py script in the storage folder.",
                  "Press enter to exit.", sep="\n")
            input()
            sys.exit()
        else:
            print("Couldn't understand your input. By default, PyWeather Setup is stopping.",
                  "You can retry to provision your config by using the configsetup.py script",
                  "in the storage folder. Press enter to exit.", sep="\n")
            input()
            sys.exit()

# See if the config is "provisioned". If it isn't, a KeyError will occur,
# because it's not created. Here, we set up the config to defaults if it's not
# provisioned.
try:
    configprovisioned = config.getboolean('USER', 'configprovisioned')
except:
    print("Your config likely isn't provisioned. Would you like to provision your config?",
          "It's highly recommended you provision your config. If you decide not to,",
          "you may run into issues using PyWeather.",
          "Yes or No.", sep="\n")
    provisionconfig = input("Input here: ").lower()
    if provisionconfig == "yes":
        print("Provisioning your config.")
        configprovision()
        print("Config file provisioned successfully! Moving on with PyWeather setup...")
    elif provisionconfig == "no":
        print("Not provisioning your config. You may encounter unexpected errors",
              "and issues when using PyWeather, however.", sep="\n")
    else:
        print("Couldn't understand your input. By default, I'm going to provision",
              "your config. Beginning now...", sep="\n")
        configprovision()
        print("Config file provisioned successfully! Moving on with PyWeather setup...")


try:
    verbosity = config.getboolean('VERBOSITY', 'setup_verbosity')
    jsonVerbosity = config.getboolean('VERBOSITY', 'setup_jsonverbosity')
    tracebacksEnabled = config.getboolean('TRACEBACK', 'setup_tracebacks')
except:
    print("Couldn't load your config file. Make sure there aren't any typos",
          "in the config, and that the config file is accessible.",
          "Setting config variables to their defaults.",
          "Here's the full traceback, in case you need it.", sep="\n")
    traceback.print_exc()
    verbosity = False
    jsonVerbosity = False
    tracebacksEnabled = False

def printException():
    if tracebacksEnabled == True:
        print("Here's the full traceback (for error reporting):")
        traceback.print_exc()

def printException_loggerwarn():
    if verbosity == True:
        logger.warning("Oh snap! We ran into a non-critical error. Here's the traceback.")
        traceback.print_exc()


logger = logging.getLogger(name='pyweather_setup_0.6.1beta')
logger.setLevel(logging.DEBUG)
logformat = '%(asctime)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logformat)

if verbosity == True:
    logger.setLevel(logging.DEBUG)
elif tracebacksEnabled == True:
    logger.setLevel(logging.ERROR)
else:
    logger.setLevel(logging.CRITICAL)

logger.debug("Listing configuration options:")
logger.debug("verbosity: %s ; jsonVerbosity: %s" %
             (verbosity, jsonVerbosity))
logger.debug("tracebacksEnabled: %s" %
             tracebacksEnabled)

print("Welcome to PyWeather setup.",
      "This is meant to run as a one-time program, when you first get PyWeather.","",
      "Running a few checks...", sep="\n")


import shutil
import time
import json
import codecs


buildnumber = 61
buildversion = "0.6.1 beta"

logger.debug("buildnumber: %s ; buildversion: %s" %
             (buildnumber, buildversion))

print("","Before we get started, I want to confirm some permissions from you.",
      "Is it okay if I use 1-5 MB of data (downloading libraries), save a small",
      "text file called apikey.txt (> 2 KB), and automatically install Python",
      "libraries?",
      "Please input yes or no below:", sep="\n")
confirmPermissions = input("Input here: ").lower()
logger.debug("confirmPermissions: %s" % confirmPermissions)
if confirmPermissions == "no":
    logger.debug("User denied permissions. Closing...")
    print("Okay! Closing now.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()
elif confirmPermissions != "yes":
    logger.debug("Couldn't understand. Closing...")
    print("I couldn't understand what you said.",
          "As a precaution, I won't proceed any further.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()

print("","Cool! Let's start.",
      "I'm going to start by checking for necessary libraries (to run PyWeather).",
      "This can take a moment, so please hold tight while I check!", sep="\n")

try:
    import pip
except ImportError:
    logger.warn("pip is NOT installed! Asking user for automated install...")
    printException_loggerwarn()
    print("","Shucks! PIP couldn't be imported, and I need PIP to install",
          "libraries for you. Would you like me to install PIP for you?",
          "Yes or No.", sep="\n")
    pipConfirm = input("Input here: ").lower()
    logger.debug("pipConfirm: %s" % pipConfirm)
    if pipConfirm == "no":
        logger.info("User denied PIP install, closing...")
        print("","Okay! I'm closing setup, as I need PIP to continue.",
        "Press enter to continue.", sep="\n")
        input()
        sys.exit()
    elif pipConfirm == "yes":
        logger.info("User allowed PIP install. Starting...")
        print("","Okay!",
        "I'll download PIP's installer, and run it.",
        "Doing such uses about 2-4 MB of data, and will quit PW setup.",
        "When the setup script finishes, you'll need to run the setup script again."
        "I'll start in a few seconds.", sep="\n")
        time.sleep(3)
        print("Downloading the installer...")
        # We use the built-in urllib library, as some Python installs don't include requests.
        try:
            with urllib.request.urlopen('https://bootstrap.pypa.io/get-pip.py') as update_response, open('get-pip.py',
                                                                                                         'wb') as update_out_file:
                logger.debug("update_response: %s ; update_out_file: %s"
                             % (update_response, update_out_file))
                shutil.copyfileobj(update_response, update_out_file)
        except:
            print("Couldn't download the PIP installer, either due to no internet connection, or the library that fetches",
                  "files has failed. As an alternative, you can download the installer yourself.",
                  "Please download this file: 'https://bootstrap.pypa.io/get-pip.py', and place it in PyWeather's base directory.",
                  "Afterwards, press enter to execute the installer. Press Control + C to exit.", sep="\n")
            printException()
            input()

        print("Running the installer...")
        logger.debug("Executing get-pip.py. If this script exits, please restart the setup script.")
        exec(open("get-pip.py").read())

    else:
        logger.warn("Couldn't understand the input. Closing...")
        print("","I didn't understand what you said.",
        "As a precaution, I'm closing setup, as I need PIP to continue.",
        "Press enter to exit.", sep="\n")
        input()
        sys.exit()
except PermissionError:
    traceback.print_exc()
    print("PIP has incorrect permissions on your machine. Please attempt to fix",
          "permissions on the folder that is listed in the traceback.",
          "Linux users: Use sudo chown -R <yourusername> <folder>, this should fix the issue.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()

print("Deleting the PIP installer file (if it exists)")
try:
    os.remove("get-pip.py")
except:
    printException_loggerwarn()
    print("The file get-pip.py didn't exist, or we had wrong permissions.")

neededLibraries = 0

try:
    import colorama
    coloramaInstalled = True
    logger.info("Colorama is installed.")
    logger.debug("coloramaInstalled: %s" % coloramaInstalled)
except ImportError:
    coloramaInstalled = False
    neededLibraries = neededLibraries + 1
    logger.warn("Colorama is not installed.")
    printException_loggerwarn()
    logger.debug("coloramaInstalled: %s ; neededLibraries: %s"
                % (coloramaInstalled, neededLibraries))


try:
    import geopy
    geopyInstalled = True
    logger.info("geopy is installed.")
    logger.debug("geopyInstalled: %s" % geopyInstalled)
except ImportError:
    geopyInstalled = False
    neededLibraries = neededLibraries + 1
    logger.info("geopy is NOT installed.")
    printException_loggerwarn()
    logger.debug("geopyInstalled: %s ; neededLibraries: %s"
                 % (geopyInstalled, neededLibraries))

try:
    from appJar import gui
    appjarInstalled = True
    logger.info("appjar is installed.")
    logger.debug("appjarInstalled: %s" % appjarInstalled)
except ImportError as e:
    if e == "No module named '_tkinter', please install the python3-tk package":
        print("appJar cannot run on this platform. Skipping installation...")
        appjarInstalled = True
        logger.debug("appjarInstalled: %s" % appjarInstalled)
    else:
        appjarInstalled = False
        neededLibraries = neededLibraries + 1
        logger.debug("appJar is NOT installed.")
        printException_loggerwarn()
        logger.debug("appjarInstalled: %s ; neededLibraries: %s" %
                     (appjarInstalled, neededLibraries))


try:
    import requests
    requestsInstalled = True
    logger.debug("requests is installed.")
    logger.debug("requestsInstalled: %s" % requestsInstalled)
except:
    requestsInstalled = False
    neededLibraries = neededLibraries + 1
    logger.debug("requests is NOT isntalled.")
    printException_loggerwarn()
    logger.debug("requestsInstalled: %s ; neededLibraries: %s" %
                 (requestsInstalled, neededLibraries))


print("All done!")
if neededLibraries == 0:
    logger.debug("All libraries are installed.")
    print("All necessary libraries have been installed!")
else:
    logger.debug("Libraries need to be installed.")
    print("Shucks. Not all necessary libraries are installed. Here's what needs to be installed:")
    if coloramaInstalled == False:
        print("- Colorama")
    if geopyInstalled == False:
        print("- Geopy")
    if appjarInstalled == False:
        print("- appJar")
    if requestsInstalled == False:
        print("- Requests")
    print("If you want me to, I can automatically install these libraries.",
    "Would you like me to do such? Yes or No.", sep="\n")
    neededLibrariesConfirm = input("Input here: ").lower()
    logger.debug("neededLibrariesConfirm: %s" % neededLibrariesConfirm)
    if neededLibrariesConfirm == "no":
        logger.warn("Not installing necessary libraries. Now exiting...")
        print("Okay. I needed to install necessary libraries to continue.",
        "Now quitting...",
        "Press enter to exit.", sep="\n")
        input()
        sys.exit()
    elif neededLibrariesConfirm == "yes":
        print("Now installing necessary libraries...")
        if coloramaInstalled == False:
            print("Installing Colorama...")
            pip.main(['install', 'colorama'])
        if geopyInstalled == False:
            print("Installing geopy...")
            pip.main(['install', 'geocoder'])
        if appjarInstalled == False:
            print("Installing appJar...")
            pip.main(['install', 'appJar'])
        if requestsInstalled == False:
            print("Installing requests...")
            pip.main(['install', 'requests'])

        logger.info("Running the double check on libraries...")
        print("Sweet! All libraries should be installed.",
              "Just to confirm, I'm double checking if needed libraries are installed.", sep="\n")
        try:
            import colorama
            logger.info("Colorama installed successfully.")
        except ImportError:
            logger.warn("colorama was not installed successfully.")
            print("Hmm...Colorama didn't install properly.")
            printException()
            print("As a last resort, we can use sudo -H to install packages.",
            "Do you want to use the shell option to install colorama?",
            "WARNING: Using the last-resort method may screw up PIP, and",
            "may require you to reinstall PIP on your machine."
            "Yes or No.", sep="\n")
            colorama_lastresort = input("Input here: ").lower()
            logger.debug("colorama_lastresort: %s" % colorama_lastresort)
            if colorama_lastresort == "yes":
                try:
                    print("Now executing `sudo -H pip3 install colorama`.",
                          "Please enter the password for sudo when the prompt",
                          "comes up. Press Control + C to cancel.",
                          "Starting in 5 seconds...", sep="\n")
                    time.sleep(5)
                    try:
                        subprocess.call(["sudo -H pip3 install colorama"], shell=True)
                        try:
                            print("Attempting to reimport colorama.")
                            import colorama
                            print("Colorama is FINALLY installed!")
                        except:
                            print("Colorama still wasn't successfully installed.",
                                  "Cannot continue without Colorama.",
                                  "Try doing a manual install of Colorama with PIP.", sep="\n")
                            printException()
                            print("Press enter to exit.")
                            input()
                            sys.exit()
                    except:
                        print("When running the command, an error occurred",
                              "Try doing a manual install of Colorama with PIP.", sep="\n")
                        printException()
                        print("Press enter to exit.")
                        input()
                        sys.exit()
                except KeyboardInterrupt:
                    print("Command execution aborted.",
                          "Cannot continue without Colorama.",
                          "Try and do a manual install of Colorama with PIP",
                          "in a command line.", sep="\n")
                    printException()
                    print("Press enter to exit.")
                    input()
                    sys.exit()
            elif colorama_lastresort == "no":
                print("Not installing Colorama with a shell command.",
                      "Cannot continue without Colorama.",
                      "Press enter to exit.", sep="\n")
                input()
                sys.exit()
            else:
                print("Did not understand your input. Defaulting to not installing",
                      "via the shell. Cannot continue without Colorama.",
                      "Try installing Colorama with PIP.",
                      "Press enter to exit.")
                input()
                sys.exit()

        try:
            import geopy
            logger.info("geopy installed successfully.")
        except ImportError:
            logger.warn("geopy was not installed successfully.")
            print("Hmm...geopy didn't install properly.")
            printException()
            print("As a last resort, we can use sudo -H to install packages.",
            "Do you want to use the shell option to install geopy?",
            "WARNING: Using the last-resort method may screw up PIP, and",
            "may require you to reinstall PIP on your machine."
            "Yes or No.", sep="\n")
            geopy_lastresort = input("Input here: ").lower()
            logger.debug("geopy_lastresort: %s" % geopy_lastresort)
            if geopy_lastresort == "yes":
                try:
                    print("Now executing `sudo -H pip3 install geopy`.",
                          "Please enter the password for sudo when the prompt",
                          "comes up. Press Control + C to cancel.",
                          "Starting in 5 seconds...", sep="\n")
                    time.sleep(5)
                    try:
                        subprocess.call(["sudo -H pip3 install geopy"], shell=True)
                        try:
                            print("Attempting to reimport geopy.")
                            import geopy
                            print("Geopy is FINALLY installed!")
                        except:
                            print("Geopy still wasn't successfully installed.",
                                  "Cannot continue without geopy.",
                                  "Try doing a manual install of geopy with PIP.", sep="\n")
                            printException()
                            print("Press enter to exit.")
                            input()
                            sys.exit()
                    except:
                        print("When running the command, an error occurred",
                              "Try doing a manual install of geopy with PIP.", sep="\n")
                        printException()
                        print("Press enter to exit.")
                        input()
                        sys.exit()
                except KeyboardInterrupt:
                    print("Command execution aborted.",
                          "Cannot continue without geopy.",
                          "Try and do a manual install of geopy with PIP",
                          "in a command line.", sep="\n")
                    printException()
                    print("Press enter to exit.")
                    input()
                    sys.exit()
            elif geopy_lastresort == "no":
                print("Not installing geopy with a shell command.",
                      "Cannot continue without geopy.",
                      "Press enter to exit.", sep="\n")
                input()
                sys.exit()
            else:
                print("Did not understand your input. Defaulting to not installing",
                      "via the shell. Cannot continue without geopy.",
                      "Try installing geopy with PIP.",
                      "Press enter to exit.")
                input()
                sys.exit()

        try:
            import requests
            logger.info("requests installed successfully.")
        except ImportError:
            logger.warning("Requests was not installed successfully.")
            print("Hmm...requests didn't install properly.")
            printException()
            print("As a last resort, we can use sudo -H to install packages.",
            "Do you want to use the shell option to install requests?",
            "WARNING: Using the last-resort method may screw up PIP, and",
            "may require you to reinstall PIP on your machine."
            "Yes or No.", sep="\n")
            requests_lastresort = input("Input here: ").lower()
            logger.debug("requests_lastresort: %s" % requests_lastresort)
            if requests_lastresort == "yes":
                try:
                    print("Now executing `sudo -H pip3 install requests`.",
                          "Please enter the password for sudo when the prompt",
                          "comes up. Press Control + C to cancel.",
                          "Starting in 5 seconds...", sep="\n")
                    time.sleep(5)
                    try:
                        subprocess.call(["sudo -H pip3 install requests"], shell=True)
                        try:
                            # Fun fact: This is inside THREE try/except things.
                            print("Attempting to reimport requests.")
                            import requests
                            print("requests is FINALLY installed!")
                        except:
                            print("requests still wasn't successfully installed.",
                                  "Cannot continue without requests.",
                                  "Try doing a manual install of requests with PIP.", sep="\n")
                            printException()
                            print("Press enter to exit.")
                            input()
                            sys.exit()
                    except:
                        print("When running the command, an error occurred",
                              "Try doing a manual install of requests with PIP.", sep="\n")
                        printException()
                        print("Press enter to exit.")
                        input()
                        sys.exit()
                except KeyboardInterrupt:
                    print("Command execution aborted.",
                          "Cannot continue without appJar.",
                          "Try and do a manual install of requests with PIP",
                          "in a command line.", sep="\n")
                    printException()
                    print("Press enter to exit.")
                    input()
                    sys.exit()
            elif requests_lastresort == "no":
                print("Not installing appJar with a shell command.",
                      "Cannot continue without requests.",
                      "Press enter to exit.", sep="\n")
                input()
                sys.exit()
            else:
                print("Did not understand your input. Defaulting to not installing",
                      "via the shell. Cannot continue without requests.",
                      "Try installing requests with PIP.",
                      "Press enter to exit.")
                input()
                sys.exit()

        print("","All libraries are installed!", sep="\n")
    else:
        logger.warn("Input was not understood. Closing...")
        print("I'm not sure what you said.",
        "As a precaution, I'm now closing.", sep="\n")
        sys.exit()

print("", "Would you like PyWeather to update all your PIP packages?",
      "If you had necessary libraries previously installed, it's best",
      "to update your PIP packages. Please note: This may not work",
      "on all platforms.", sep="\n")
confirm_updatepip = input("Input here: ").lower()
logger.debug("confirm_updatepip: %s" % confirm_updatepip)
if confirm_updatepip == "yes":
    print("Updating PIP packages.")
    totalpackages = 0
    updatecount = 1
    for pkgname in pip.get_installed_distributions():
        totalpackages = totalpackages + 1
        logger.debug("total package count now: %s" % totalpackages)

    for pkgname in pip.get_installed_distributions():
        print("Now updating package: %s (Update %s/%s)" %
              (pkgname, updatecount, totalpackages))
        pip.main(['install', '--upgrade', '%s' % pkgname.project_name])
        updatecount = updatecount + 1
elif confirm_updatepip == "no":
    print("Not updating PIP packages. You may run into issues with non-updated",
          "packages in future versions of PyWeather.")
else:
    print("Input not understood, not updating PIP packages. You may run into",
          "issues with non-updated packages in future versions of PyWeather.")

# Verbosity is not needed here.
print("I'm now going to guide you through obtaining an API key.",
"Please carefully read my detailed instructions, so you don't mess anything up.", sep="\n")

print("Let's begin.",
"Start by opening a web browser, and going to https://www.wunderground.com/weather/api/.",
"Press any key when you are done.", sep="\n")
input()
print("Next, click the 'Explore my options' button.",
"Press any key when you are done.", sep="\n")
input()
print("Next, click the small button next to 'ANVIL PLAN'.",
"After that, confirm that the total underneath the 'Purchase Key' button says",
"'$0 USD per month'.",
"If the total underneath the 'Purchase Key' button doesn't",
"say '$0 USD per month, please ensure that the small button next to 'Developer'",
"on the table in the middle of the screen is selected, and the total",
"says '$0 USD per month'",
"Press any key when you are done.", sep="\n")
input()
print("Next, click the 'Purchase Key' button.",
"Press any key when you are done.", sep="\n")
input()
print("Next, input your email, and a password to sign up for a Weather",
"Underground account.",
"Be sure to select the checkbox next to 'I agree to the Terms of Service'",
"It's best if you leave the checkbox next to 'I would like to receive WU",
"updates via email' unchecked.",
"Press any key when you are done and ready.", sep="\n")
input()
print("Next, press the 'Sign up for free' button.",
"When the welcome window pops up, be sure to click the X button at the top right of the popup.",
"When clicking the X, you should be redirected to wunderground.com.",
"Press any key when you are done and ready.", sep="\n")
input()
print("Next, click 'My Profile' at the top right corner of the homepage.",
"In the dropdown, click 'My Email & Text Alerts'",
"Press any key when you are done and ready.", sep="\n")
input()
print("Next, next to your email listed on the page, click the 'Edit / Verify' button.",
"After you click the button, click the 'Verify Email' button.",
"Press any key when you are done and ready.", sep="\n")
input()
print("Next, check your email in which you signed up with.",
"If you got a letter from Weather Underground, titled 'Daily Forecast",
"Email Verification', open that letter, and click the link.",
"If you didn't get the letter, wait a few minutes, and be sure to check your spam folder.",
"Hint: If you followed this guide exactly, WU will not be sending you daily forecasts to your email.",
"Press any key when you are done and ready.", sep="\n")
input()
print("Your email should be verified.",
"Next, in your web browser, head back to https://www.wunderground.com/weather/api/.",
"Then, click the 'Explore my Options' button, again.",
"Press any key when you are done and ready.", sep="\n")
input()
print("Next, at the top of the page, make sure the button next to 'ANVIL PLAN'",
"is selected.",
"After that, confirm that the total underneath the 'Purchase Key' button says",
"'$0 USD per month'",
"If the total doesn't say that, in the pricing table, make sure the button",
"next to 'Developer' is selected.",
"Press any key when you are done and ready.", sep="\n")
input()
print("Next, click the 'Purchase Key' button, on top of your total (which",
"should be $0 USD per month)",
"Next, fill out the form, considering these tips:",
"For the contact name/email, it's recommended you use your real name",
"(first name last initial is fine).",
"It's also recommended that you use your real email.",
"For the project name, put in something generic, like 'to use a script that",
"uses WU's API', or 'WU API test'. It's up to you.",
"For the project website, put in something generic, like 'google.com', or",
"some other site you feel like having as the project site.",
"For the question 'Where will the API be used', answer Other.",
"For the question 'Will the API be used for commercial use?', answer No.",
"For the question 'Will the API be used for manufacturing mobile chip",
"processing?', answer No.",
"Answer yes if you somehow are manufacturing mobile chip processing. I doubt",
"you are, however.",
"For the country that you are based in, put your location.",
"Before we move on, fill out these forms, and press any key when you are done "
"and ready.", sep="\n")
input()
print("Next, for the brief description, put something like 'using an API key",
"to use a script using Wunderground'.",
"After that, check both boxes at the bottom of the page. Read the ToS if you",
"feel like it.",
"Finally, click 'Purchase Key'.",
"You should land on a page that says 'Edit API Key'.",
"Press any key when you are done and ready.", sep="\n")
input()
print("In the table to the left of the page, copy the text that's under Key ID.",
"(Ctrl+C, right click)",
"I'm now going to ask you to input the API key into the text entry below.",
"The API key will be saved to storage/apikey.txt, so PyWeather can easily",
"pull it up.",
"Press any key when you are done and ready.", sep="\n")
input()
print("Please input your API key below.")
apikey_input = input("Input here: ")
logger.debug("apikey_input: %s" % apikey_input)
print("", "Just to confirm, the API key you gave me was: " + apikey_input
      + ".", sep="\n")
print("Please double check your input, and confirm in the dialogue below.")
apikey_confirm = input("Is the API key right? Yes or no: ").lower()
logger.debug("apikey_confirm: %s" % apikey_confirm)
if apikey_confirm == "no":
    while True:
        logger.debug("User now re-entering key...")
        print("","Please input your API key below.", sep="\n")
        apikey_input = input("Input here: ")
        logger.debug("apikey_input: %s" % apikey_input)
        print("Just to confirm, the API key you gave me was: " + apikey_input
              + ".")
        apikey_confirm = input("Is the API key right? Yes or no: ").lower()
        if apikey_confirm == "yes":
            break
        elif apikey_confirm == "no":
            continue
        else:
            print("Couldn't understand your input.",
                  "I'll assume the API key is correct, moving on.", sep="\n")

print("Now saving your API key...")
open('storage//apikey.txt', 'w').close()

with open("storage//apikey.txt", 'a') as out:
    logger.debug("out: %s" % out)
    out.write(apikey_input)
    out.close()
    logger.debug("Performed ops: overwrite apikey.txt, out.write(apikey_input), out.close()")

print("", "I can also back up your API key, in case you do something wrong.",
      sep="\n")
# A future release should bring customization as to the storage location.
print("Would you like me to save a backup? Yes or no.")
backup_APIkey = input("Input here: ").lower()
if backup_APIkey == "yes":
    print("","Where would you want me to backup the key to?",
        "This is a directory. If I wanted my key at directory/backkey.txt,",
          "You would enter 'directory'. The default directory is 'backup'.", sep="\n")
    # Doing a .lower() here to prevent case insensitiveness.
    backup_APIkeydirectory = input("Input here: ").lower()
    backup_APIkeydirectory2 = backup_APIkeydirectory + "//"
    folder_argument = backup_APIkeydirectory + "//backkey.txt"
    logger.debug("backup_APIkeydirectory: %s ; backup_APIkeydirectory2: %s" %
                 (backup_APIkeydirectory, backup_APIkeydirectory2))
    logger.debug("folder_argument: %s" % folder_argument)
    print("Creating a backup...")
    if backup_APIkeydirectory == "backup":
        logger.debug("Using the default directory.")
    elif backup_APIkeydirectory != "backup":
        try:
            os.mkdir(backup_APIkeydirectory2)
        except:
            printException_loggerwarn()
            print("Couldn't make the directory, does it exist?")
    # Overwrite the file, if it exists.
    open(folder_argument, 'w').close()
    open(folder_argument, 'a').write(apikey_input)
    open(folder_argument).close()
    config['KEYBACKUP']['savedirectory'] = backup_APIkeydirectory2
    print("The API key was backed up successfully!")
    logger.debug("Performed 3 ops. Overwrite "+ folder_argument + "backkey.txt, write to backkey.txt" +
                ", and close backkey.txt.")

print("Before we configure PyWeather, I'll now validate your API key.")

# Do an infinite loop of validation of the API key, so the user can reenter the API key
# if it was wrong.

while True:
    apitest_URL = 'http://api.wunderground.com/api/' + apikey_input + '/conditions/q/NY/New_York.json'
    testreader = codecs.getreader("utf-8")
    logger.debug("apitest_URL: %s ; testreader: %s" %
                (apitest_URL, testreader))

    try:
        testJSON = requests.get(apitest_URL)
        logger.debug("testJSON: %s" % testJSON)
    except:
        logger.warn("Couldn't connect to Wunderground's API! No internet?")
        print("When PyWeather Setup attempted to fetch the .json to validate your API key,",
            "it ran into an error. If you're on a network with a filter, make sure that",
            "'api.wunderground.com' is unblocked. Otherwise, make sure you have an internet",
            "connection.", sep="\n")
        printException()
        print("Press enter to exit.")
        input()
        sys.exit()

    test_json = json.loads(testJSON.text)
    if jsonVerbosity == True:
        logger.debug("test_json: %s" % test_json)

    try:
        test_conditions = str(test_json['current_observation']['temp_f'])
        logger.debug("test_conditions: %s" % test_conditions)
        print("Hurray! Your API key is valid and works.")
        break
    except:
        logger.warn("Error! Is the API key invalid?")
        print("When attempting to validate the API key that you entered/confirmed,",
              "PyWeather ran into an error. Would you like to reenter your API key to revalidate it?",
              "Please note, that this error might be caused by WU's API being down, or another cause.",
              "However, 90% of the time, this is due to a bad API key.",
              "Yes or No.", sep='\n')
        revalidateAPIkey = input("Input here: ").lower()
        if revalidateAPIkey == "yes":
            print("Enter in your API key below.")
            apikey_input = input("Input here: ")
            logger.debug("apikey_input: %s")
            print("Revalidating your API key...")
            continue
        elif revalidateAPIkey == "no":
            print("Not revalidating your API key. You'll need a valid API key to continue.",
                  "Press enter to exit.", sep="\n")
            input()
            sys.exit()
        printException()
        print("Press enter to exit.")
        input()
        sys.exit()

print("Let's configure PyWeather to your liking.")
logger.debug("config: %s" % config)

print("", "(1/27)","On the summary screen, would you like to show sunrise/sunset times?",
      "By default, this is disabled.",
      "Yes or No.", sep="\n")
sundata_Summary = input("Input here: ").lower()
logger.debug("sundata_Summary: %s" % sundata_Summary)
if sundata_Summary == "yes":
    config['SUMMARY']['sundata_summary'] = 'True'
    print("Changes saved.")
    logger.debug("Sundata on the summary is now ENABLED.")
elif sundata_Summary == "no":
    config['SUMMARY']['sundata_summary'] = 'False'
    print("Changes saved.")
    logger.debug("Sundata on the summary is now DISABLED.")
else:
    print("Could not understand what you inputted.",
          "Defaulting to 'False'", sep="\n")
    config['SUMMARY']['sundata_summary'] = 'False'
    print("Changes saved.")
    logger.debug("Could not recognize input. Defaulting to DISABLED.")

print("", "(2/27)","On the summary screen, would you like to show almanac data?",
      "By default, this is disabled.",
      "Yes or no:", sep="\n")
almanacdata_Summary = input("Input here: ").lower()
logger.debug("almanacdata_Summary: %s" % almanacdata_Summary)
if almanacdata_Summary == "yes":
    config['SUMMARY']['almanac_summary'] = 'True'
    print("Changes saved.")
    logger.debug("Almanac on the summary is now ENABLED.")
elif almanacdata_Summary == "no":
    config['SUMMARY']['almanac_summary'] = 'False'
    print("Changes saved.")
    logger.debug("Almanac on the summary is now DISABLED.")
else:
    print("Could not understand what you inputted.",
         "Defaulting to 'False'", sep="\n")
    config['SUMMARY']['almanac_summary'] = 'False'
    print("Changes saved.")
    logger.debug("Could not recognize input. Defaulting to DISABLED.")

print("", "(3/27)", "On the summary screen, would you like to show alerts data?",
      "By default, this is enabled. Please note, Wunderground",
      "only supports alert data in the US and EU at this time.",
      "Yes or No.", sep="\n")
alertsdata_Summary = input("Input here: ").lower()
logger.debug("alertsdata_Summary: %s" % alertsdata_Summary)
if alertsdata_Summary == "yes":
    config['SUMMARY']['showalertsonsummary'] = 'True'
    print("Changes saved.")
    logger.debug("Alerts on the summary is now ENABLED.")
elif alertsdata_Summary == "no":
    config['SUMMARY']['showalertsonsummary'] = 'False'
    print("Changes saved.")
    logger.debug("Alerts on the summary is now DISABLED.")
else:
    print("Could not understand what you inputted.",
          "Defaulting to 'True'", sep="\n")
    config['SUMMARY']['showAlertsOnSummary'] = 'True'

print("", "(4/27)","On boot, would you like PyWeather to check for updates?",
      "By default, this is disabled, due to a load time increase of ~2-5 seconds.",
      "Yes or No.", sep="\n")
checkForUpdates = input("Input here: ").lower()
logger.debug("checkForUpdates: %s" % checkForUpdates)
if checkForUpdates == "yes":
    config['UPDATER']['autoCheckForUpdates'] = 'True'
    print("Changes saved.")
    logger.debug("Checking for updates on startup is ENABLED.")
elif checkForUpdates == "no":
    config['UPDATER']['autoCheckForUpdates'] = 'False'
    print("Changes saved.")
    logger.debug("Checking for updates on startup is DISABLED.")
else:
    print("Could not understand what you inputted.",
        "Defaulting to 'False'", sep="\n")
    config['UPDATER']['autoCheckForUpdates'] = 'False'
    print("Changes saved.")
    logger.debug("Could not recognize input. Defaulting to DISABLED.")

print("", "(5/27)","When an error occurs, would you like PyWeather to show the full error?",
      "When enabled, you'll have easier access to the full error for reporting",
      "the bug on GitHub.",
      "By default, this is disabled, as errors look less pretty when enabled.",
      "Yes or no.", sep="\n")
displayTracebacks = input("Input here: ").lower()
logger.debug("displayTracebacks: %s" % displayTracebacks)
if displayTracebacks == "yes":
    config['TRACEBACK']['tracebacks'] = 'True'
    config['TRACEBACK']['setup_tracebacks'] = 'True'
    config['TRACEBACK']['updater_tracebacks'] = 'True'
    config['TRACEBACK']['keybackup_tracebacks'] = 'True'
    config['TRACEBACK']['configdefault_tracebacks'] = 'True'
    print("Changes saved.")
    logger.debug("Printing tracebacks is ENABLED.")
elif displayTracebacks == "no":
    config['TRACEBACK']['tracebacks'] = 'False'
    config['TRACEBACK']['setup_tracebacks'] = 'False'
    config['TRACEBACK']['updater_tracebacks'] = 'False'
    config['TRACEBACK']['keybackup_tracebacks'] = 'False'
    config['TRACEBACK']['configdefault_tracebacks'] = 'False'
    print("Changes saved.")
    logger.debug("Printing tracebacks is DISABLED.")
else:
    print("Couldn't understand what you inputted.",
          "Defaulting to 'False'", sep="\n")
    config['TRACEBACK']['tracebacks'] = 'False'
    config['TRACEBACK']['setup_tracebacks'] = 'False'
    config['TRACEBACK']['updater_tracebacks'] = 'False'
    config['TRACEBACK']['keybackup_tracebacks'] = 'False'
    print("Changes saved.")
    logger.debug("Could not understand input. Defaulting to DISABLED.")

print("", "(6/27)", "When booting PyWeather up initially, would you like PyWeather to",
      "fetch the 10-day hourly forecast, instead of the 3-day forecast?",
      "This is disabled by default. When enabled, initial loading times are",
      "increased. However, when you view the 10-day hourly forecast, you won't",
      "have to wait for it to load, and use another API call.",
      "Yes or No.", sep="\n")
tenday_onboot = input("Input here: ").lower()
if tenday_onboot == "yes":
    config['HOURLY']['10dayfetch_atboot'] = 'True'
    print("Changes saved.")
    logger.debug("Fetching 10 day JSON at boot is ENABLED.")
elif tenday_onboot == "no":
    config['HOURLY']['10dayfetch_atboot'] = 'False'
    print("Changes saved.")
    logger.debug("Fetching 10 day JSON at boot is DISABLED.")
else:
    print("Couldn't understand what you inputted.",
          "Defaulting to the default value 'False'", sep="\n")
    config['HOURLY']['10dayfetch_atboot'] = 'False'
    print("Changes saved.")
    logger.debug("Could not understand input. Defaulting to DISABLED.")

print("", "(7/27)", "When viewing detailed hourly, 10-day hourly, and historical hourly,",
      "detailed information, how many iterations should PyWeather go through",
      "before asking you to continue?",
      "By default, this is 6. An input above 10",
      "is not recommended.", sep="\n")
detailedloops = input("Input here: ")
try:
    detailedloops = int(detailedloops)
    detailedloops = str(detailedloops)
    config['UI']['detailedinfoloops'] = detailedloops
    print("Changes saved.")
    logger.debug("Detailed info iterations now %s." % detailedloops)
except:
    print("Couldn't convert input into a number. Defaulting to '6'.")
    printException_loggerwarn()
    config['UI']['detailedinfoloops'] = '6'
    print("Changes saved.")
    logger.debug("Detailed info loops now 6.")

print("", "(8/27)", "When viewing detailed 10-day forecast information, how many",
      "iterations should PyWeather go through, before asking you to",
      "continue?",
      "By default, this is 5. An input above 10 will not prompt",
      "the enter to continue prompt", sep="\n")
detailedForecastLoops = input("Input here: ")
try:
    detailedForecastLoops = int(detailedForecastLoops)
    detailedForecastLoops = str(detailedForecastLoops)
    config['UI']['forecast_detailedinfoloops'] = detailedForecastLoops
    print("Changes saved.")
    logger.debug("Detailed forecast info iterations now %s" % detailedForecastLoops)
except:
    print("Couldn't convert input into a number. Defaulting to '5'.")
    printException_loggerwarn()
    config['UI']['forecast_detailedinfoloops'] = '5'
    print("Changes saved.")
    logger.debug("Detailed forecast info loops now 5.")

print("", "(9/27)", "PyWeather has a caching system, in which if you're gone for some time",
      "data will automatically refresh. Would you like to turn this on?",
      "This is enabled by default. Yes or No.", sep="\n")
enablecache = input("Input here: ").lower()
if enablecache == "no":
    print("Cache will be disabled.")
    config['CACHE']['enabled'] = 'False'
    print("Changes saved.")
else:
    config['CACHE']['enabled'] = 'True'
    print("You entered yes, or your input wasn't understood (yes is the default.)",
          "In the next few inputs, enter the time in minutes that PyWeather should keep",
          "certain types of data, before a data refresh is automatically requested.",
          "If you want to leave cache values to their defaults, press enter at any prompt.", sep="\n")

    print("", "(10/27)", "Please enter the cache time for alerts data in minutes (default = 5)", sep="\n")
    alertscachetime = input("Input here: ").lower()
    try:
        alertscachetime = int(alertscachetime)
        alertscachetime = str(alertscachetime)
        config['CACHE']['alerts_cachedtime'] = alertscachetime
        print("Changes saved.")
        logger.debug("Alerts cache time now %s minutes." % alertscachetime)
    except:
        print("", "Your input couldn't be converted into a number. Setting alerts",
              "cache time to it's default value of '5'.", sep="\n")
        config['CACHE']['alerts_cachedtime'] = '5'
        logger.debug("Alerts cache time now 5 minutes.")

    print("", "(11/27)", "Please enter the cache time for current data in minutes (default = 10)", sep="\n")
    currentcachetime = input("Input here: ").lower()
    try:
        currentcachetime = float(currentcachetime)
        currentcachetime = str(currentcachetime)
        config['CACHE']['current_cachedtime'] = currentcachetime
        print("Changes saved.")
        logger.debug("Current cache time now %s minutes." % alertscachetime)
    except:
        print("", "Your input couldn't be converted into a number. Setting current",
              "cache time to it's default value of '10'.", sep="\n")
        config['CACHE']['current_cachedtime'] = '10'
        logger.debug("Current cache time now 10 minutes.")

    print("", "(12/27)", "Please enter the cache time for hourly data in minutes (default = 60)", sep="\n")
    hourlycachetime = input("Input here: ").lower()
    try:
        hourlycachetime = float(hourlycachetime)
        hourlycachetime = str(hourlycachetime)
        config['CACHE']['hourly_cachedtime'] = hourlycachetime
        print("Changes saved.")
        logger.debug("Hourly cache time now %s minutes." % hourlycachetime)
    except:
        print("", "Your input couldn't be converted into a number. Setting hourly",
              "cache time to it's default value of '60'.", sep="\n")
        config['CACHE']['hourly_cachedtime'] = '60'
        logger.debug("Hourly cache time now 60 minutes.")

    print("", "(13/27)", "Please enter the cache time for forecast data in minutes (default = 60)", sep="\n")
    forecastcachetime = input("Input here: ").lower()
    try:
        forecastcachetime = float(forecastcachetime)
        forecastcachetime = str(forecastcachetime)
        config['CACHE']['forecast_cachedtime'] = forecastcachetime
        print("Changes saved.")
        logger.debug("Forecast cache time now %s minutes." % forecastcachetime)
    except:
        print("", "Your input couldn't be converted into a number. Setting forecast",
              "cache time to it's default value of '60'.", sep="\n")
        config['CACHE']['forecast_cachedtime'] = '60'
        logger.debug("Forecast cache time now 60 minutes.")

    print("", "(14/27)", "Please enter the cache time for almanac data in minutes (default = 240)", sep="\n")
    almanaccachetime = input("Input here: ").lower()
    try:
        almanaccachetime = float(almanaccachetime)
        almanaccachetime = str(almanaccachetime)
        config['CACHE']['almanac_cachedtime'] = almanaccachetime
        print("Changes saved.")
        logger.debug("Almanac cache time now %s minutes." % almanaccachetime)
    except:
        print("", "Your input couldn't be converted into a number. Setting almanac",
              "cache time to it's default value of '240'.", sep="\n")
        config['CACHE']['almanac_cachedtime'] = '240'
        logger.debug("Almanac cache time now 240 minutes.")

    print("", "(15/27)", "Please enter the cache time for sun data in minutes (default = 480)", sep="\n")
    sundatacachetime = input("Input here: ").lower()
    try:
        sundatacachetime = float(sundatacachetime)
        sundatacachetime = str(sundatacachetime)
        config['CACHE']['sundata_cachedtime'] = forecastcachetime
        print("Changes saved.")
        logger.debug("Sun data cache time now %s minutes." % sundatacachetime)
    except:
        print("", "Your input couldn't be converted into a number. Setting sun data",
              "cache time to it's default value of '480'.", sep="\n")
        config['CACHE']['sundata_cachedtime'] = '480'
        logger.debug("Sun data cache time now 480 minutes.")
    print("", "(16/27)", "Please enter the cache time for tide data in minutes (default = 480)", sep="\n")
    tidecachetime = input("Input here: ").lower()
    try:
        tidecachetime = float(tidecachetime)
        tidecachetime = str(tidecachetime)
        config['CACHE']['tide_cachedtime'] = tidecachetime
        print("Changes saved.")
        logger.debug("Tide cache time now %s minutes." % tidecachetime)
    except:
        print("", "Your input couldn't be converted into a number. Setting tide data",
              "cache time to it's default value of '480'.", sep="\n")
        config['CACHE']['tide_cachedtime'] = '480'
        logger.debug("Tide data cache time now 480 minutes.")


print("", "(17/27)", "When viewing detailed EU alerts information, how many",
      "iterations should PyWeather go through, before asking you to",
      "continue?",
      "By default, this is 2.", sep="\n")
EUalertsloops = input("Input here: ")
try:
    EUalertsloops = int(EUalertsloops)
    EUalertsloops = str(EUalertsloops)
    config['UI']['alerts_EUiterations'] = EUalertsloops
    print("Changes saved.")
    logger.debug("Detailed EU alert iterations now %s" % EUalertsloops)
except:
    print("Couldn't convert input into a number. Defaulting to '2'.")
    printException_loggerwarn()
    config['UI']['alerts_EUiterations'] = '2'
    print("Changes saved.")
    logger.debug("Detailed EU alert iterations now 2.")

print("", "(18/27)", "When viewing detailed US alerts information, how many",
      "iterations should PyWeather go through, before asking you to",
      "continue?",
      "By default, this is 1.", sep="\n")
USalertsloops = input("Input here: ")
try:
    USalertsloops = int(USalertsloops)
    USalertsloops = str(USalertsloops)
    config['UI']['alerts_USiterations'] = USalertsloops
    print("Changes saved.")
    logger.debug("Detailed US alert iterations now %s" % USalertsloops)
except:
    print("Couldn't convert input to a number. Defaulting to '1'.")
    printException_loggerwarn()
    config['UI']['alerts_USiterations'] = '1'
    print("Changes saved.")
    logger.debug("Detailed US alert iterations now 1.")

print("", "(19/27)","When PyWeather is going through detailed information, it can show",
      "how many iterations are completed.",
      "By default, this is disabled.",
      "Yes or No.", sep="\n")
showIterations = input("Input here: ").lower()
if showIterations == "yes":
    config['UI']['show_completediterations'] = 'True'
    print("Changes saved.")
    logger.debug("Showing completed iterations is ENABLED.")
elif showIterations == "no":
    config['UI']['show_completediterations'] = 'False'
    print("Changes saved.")
    logger.debug("Showing completed iterations is DISABLED.")
else:
    print("Couldn't understand what you inputted.",
          "Defaulting to 'FALSE'.", sep="\n")
    config['UI']['show_completediterations'] = 'False'
    print("Changes saved.")
    logger.debug("Could not understand input. Defaulting to DISABLED.")

print("", "(20/27)", "When PyWeather is going through detailed information, would",
      "you like the 'Enter to Continue' prompts to pop up?",
      "By default, this is enabled.",
      "Yes or No.", sep="\n")
showEnterToContinue = input("Input here: ").lower()
if showEnterToContinue == "yes":
    config['UI']['show_entertocontinue'] = 'True'
    print("Changes saved.")
    logger.debug("Showing enter to continue prompts is ENABLED.")
elif showEnterToContinue == "no":
    config['UI']['show_entertocontinue'] = 'False'
    print("Changes saved.")
    logger.debug("Showing enter to continue prompts is DISABLED.")
else:
    print("Could not understand what you inputted.",
          "Defaulting to 'True'.", sep="\n")
    config['UI']['show_entertocontinue'] = 'True'
    print("Changes saved.")
    logger.debug("Could not understand input. Defaulting to ENABLED.")

print("", "(21/27)", "In the PyWeather Updater, the updater can show the release tag",
      "associated with the latest release. Helpful for those using Git to",
      "update PyWeather. By default, this is disabled.",
      "Yes or No.", sep="\n")
showReleaseTag = input("Input here: ").lower()
if showReleaseTag == "yes":
    config['UPDATER']['show_updaterreleasetag'] = 'True'
    print("Changes saved.")
    logger.debug("Showing release tag in updater is ENABLED.")
elif showReleaseTag == "no":
    config['UPDATER']['show_updaterreleasetag'] = 'False'
    print("Changes saved.")
    logger.debug("Showing release tag in updater is DISABLED.")
else:
    print("Could not understand what you inputted.",
          "Defaulting to 'False'.", sep="\n")
    config['UPDATER']['show_updaterreleasetag'] = 'False'
    print("Changes saved.")
    logger.debug("Could not understand input. Defaulting to DISABLED.")

print("", "(22/27)", "When you check for updates, and PyWeather notices",
      "a new version is out, PyWeather can use Git to update",
      "itself. Make sure you have Git installed if you enable this.",
      "By default, this is disabled. Keep this disabled if you're unsure",
      "you have Git installed.",
      "Yes or No.", sep="\n")
allowGitUpdating = input("Input here: ").lower()
if allowGitUpdating == "yes":
    config['UPDATER']['allowGitForUpdating'] = 'True'
    print("Changes saved.")
    logger.debug("Allowing updates with Git is ENABLED.")
elif allowGitUpdating == "no":
    config['UPDATER']['allowGitForUpdating'] = 'False'
    print("Changes saved.")
    logger.debug("Allowing updates with Git is DISABLED.")
else:
    print("Could not understand what you inputted.",
          "Defaulting to 'False'.", sep="\n")
    config['UPDATER']['allowGitForUpdating'] = 'False'
    print("Changes saved.")
    logger.debug("Could not understand input. Defaulting to DISABLED.")

print("", "(23/27)", "When PyWeather boots, it can validate your API key. If PyWeather",
      "finds your primary API key is invalid, it'll attempt to validate your",
      "backup key, and load that if it's validated successfully.",
      "By default, this is enabled, as it's well worth the 1 API call to make",
      "sure your key is valid. However, if you said 'Yes' to almanac/sun data",
      "on the summary screen, you might not want to enable this.",
      "Yes or No.", sep="\n")
validateKeyOnBoot = input("Input here: ").lower()
if validateKeyOnBoot == "yes":
    config['PYWEATHER BOOT']['validateAPIKey'] = 'True'
    print("Changes saved.")
    logger.debug("Validating API key on boot is ENABLED.")
elif validateKeyOnBoot == "no":
    config['PYWEATHER BOOT']['validateAPIKey'] = 'False'
    print("Changes saved.")
    logger.debug("Validating API key on boot is DISABLED.")
else:
    print("Could not understand what you inputted.",
          "Defaulting to 'True'.", sep="\n")
    config['PYWEATHER BOOT']['validateAPIKey'] = 'False'
    logger.debug("Could not understand input. Defaulting to ENABLED.")

print("", "(24/27)", "PyWeather now has a radar feature, which opens up a GUI on supported",
      "platforms. Depending on your screen resolution, you'll have to set how large",
      "the radar picture is when rendered. In the prompt below, enter one of five sizes.",
      "extrasmall - 320x240 window",
      "small - 480x320 window",
      "normal - 640x480 window",
      "large - 960x720 window",
      "extralarge - 1280x960 window",
      "By default, the resolution is normal. Adapt your choice to the screen resolution",
      "of the machine you're using.", sep="\n")
radar_resolutions = ["extrasmall", "small", "normal", "large", "extralarge"]
logger.debug("radar_resolutions: %s" % radar_resolutions)
radar_resolutioninput = input("Input here: ").lower()
for x in range(0, 4):
    if radar_resolutioninput == radar_resolutions[x]:
        logger.debug("Resolution input matched, end result: %s" % radar_resolutions[x])
        config['RADAR GUI']['radar_imagesize'] = radar_resolutions[x]
        print("Changes saved.")
        break
    # This works by design. If x = 4 (extralarge), the if would catch first.
    elif x == 4:
        print("Could not understand what you inputted. Defaulting to 'normal'.")
        config['RADAR GUI']['radar_imagesize'] = 'normal'
        print("Changes saved.")

print("", "(25/27)", "PyWeather's radar feature is unfortunately experimental as of PyWeather 0.6.1 beta.",
      "By default, a confirmation message will always appear when attempting to launch the radar.",
      "However, this can be turned off, if you plan to use the experimental radar on a regular basis.",
      "By default, bypassing the confirmation message is disabled. Yes or No.", sep="\n")
radar_bypassconfinput = input("Input here: ").lower()
logger.debug("radar_bypassconfinput: %s" % radar_bypassconfinput)
if radar_bypassconfinput == "yes":
    config['RADAR GUI']['bypassconfirmation'] = True
    logger.debug("RADAR GUI/bypassconfirmation is now TRUE")
    print("Changes saved.")
elif radar_bypassconfinput == "no":
    config['RADAR GUI']['bypassconfirmation'] = False
    logger.debug("RADAR GUI/bypassconfirmation is now FALSE")
    print("Changes saved.")
else:
    print("Could not understand what you inputted. Defaulting to 'False'.")
    config['RADAR GUI']['bypassconfirmation'] = False
    logger.debug("RADAR GUI/bypassconfirmation is now FALSE")
    print("Changes saved.")



print("", "(26/27)", "On the summary screen, would you like tide data to be shown?",
      "This uses an extra API call when enabled. Buy default, this is disabled.",
      "Yes or No.", sep="\n")
tideonsummary = input("Input here: ").lower()
logger.debug("tideonsummary: %s" % tideonsummary)
if tideonsummary == "yes":
    config['SUMMARY']['showtideonsummary'] = True
    logger.debug("SUMMARY/showtideonsummary is now TRUE")
    print("Changes saved.")
elif tideonsummary == "no":
    config['SUMMARY']['showtideonsummary'] = False
    logger.debug("SUMMARY/showtideonsummary is now FALSE")
    print("Changes saved.")
else:
    print("Could not understand what you inputted. Defaulting to 'False'.")
    config['SUMMARY']['showtideonsummary'] = False
    logger.debug("SUMMARY/showtideonsummary is now FALSE")
    print("Changes saved.")

print("", "(27/27)", "PyWeather's geocoder usually uses https, but issues have been discovered",
      "on some platforms, where the geocoder cannot operate in the https mode. If you press enter",
      "PyWeather will automatically detect which scheme to use. If you are an advanced user, and want",
      "to configure the scheme yourself, enter advancedconfig at the prompt below.", sep="\n")
configuregeopyscheme = input("Input here: ").lower()
logger.debug("configuregeopyscheme: %s" % configuregeopyscheme)
if configuregeopyscheme == "advancedconfig":
    print("Which geopy scheme would you like to use? 'https' works on most platforms",
          "but 'http' is needed on some platforms (OS X, as an example). Please input",
          "'https' or 'http' below.")
    geopyschemetype = input("Input here: ").lower()
    logger.debug("geopyschemetype: %s" % geopyschemetype)
    if geopyschemetype == "https":
        config['GEOCDER']['scheme'] = 'https'
        logger.debug("GEOCODER/scheme is now 'https'")
        print("Changes saved. Geocoder settings will not be validated.")
    


print("","That's it! Now commiting config changes...", sep="\n")
try:
    with open('storage//config.ini', 'w') as configfile:
        logger.debug("configfile: %s" % configfile)
        config.write(configfile)
        print("Changes committed!")
        logger.info("Performed operation: config.write(configfile)")
except:
    print("The config file couldn't be written to.",
          "Make sure the config file can be written to.", sep="\n")
    printException()
    print("Press enter to exit.")
    input()
    sys.exit()


print("We're wrapping up, and making sure everything works.",
      "Checking for default libraries...", sep="\n")
try:
    import json
    logger.debug("json is available.")
except:
    logger.warn("json isn't available...that's odd.")
    print("json is not available. This is odd, it's a default library.",
    "Try installing a usual Python install.", sep="\n")
    printException()
    print("Press enter to exit.")
    input()
    sys.exit()
try:
    import codecs
    logger.debug("codecs is available.")
except:
    logger.warn("codecs isn't available. Here's the traceback:")
    printException_loggerwarn()
    print("codecs is not available. This is odd, it's a default library.",
    "Try installing a usual Python install.", sep="\n")
    printException()
    print("Press enter to exit.")
    input()
    sys.exit()


print("Hurray! All default libraries are available.",
      "Testing the API key, and it's validity...", sep="\n")



print("Testing the connection to Google's geocoder...")

from geopy import GoogleV3

geolocator = GoogleV3()
logger.debug("geolocator: %s" % geolocator)

try:
    testlocation = geolocator.geocode("New York, NY", language="en")
    logger.debug("testlocation: %s" % testlocation)
    logger.debug("testlocation.latitude: %s ; testlocation.longitude: %s" %
                 (testlocation.latitude, testlocation.longitude))
    print("Hurray! The connection to Google's geocoder works.")
except:
    logger.warn("Couldn't connect to Google's geocoder. No internet?")
    print("When attempting to test the conection to Google's geocoder,",
          "PyWeather Setup ran into an error. If you're on a network with",
          "a filter, make sure that Google's geocoder is unblocked. Otherwise",
          "make sure that you have an internet connection.", sep="\n")
    printException()
    print("Press enter to exit.")
    input()
    sys.exit()


print("","Everything is set up and ready to rumble!",
      "Enjoy using PyWeather! If you have any issues, please report them on GitHub!",
      "Press enter to continue.", sep="\n")
input()
sys.exit()
