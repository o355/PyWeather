# PyWeather Updater - version 0.5.2 beta
# (c) 2017, o355, GNU GPL 3.0


import sys
import json
import requests
import codecs
import shutil
import configparser
import traceback
import subprocess
reader = codecs.getreader("utf-8")
from colorama import Fore, Style, init
init()

config = configparser.ConfigParser()
config.read('storage//config.ini')


try:
    verbosity = config.getboolean('VERBOSITY', 'updater_verbosity')
    jsonVerbosity = config.getboolean('VERBOSITY', 'updater_jsonverbosity')
    showReleaseTag = config.getboolean('UPDATER', 'show_updaterReleaseTag')
    tracebacksEnabled = config.getboolean('TRACEBACK', 'updater_tracebacks')
    allowGitForUpdating = config.getboolean('UPDATER', 'allowGitForUpdating')
    overrideVersion = config.getboolean('VERSION', 'overrideVersion')
    overrideBuildNumber = config.getint('VERSION', 'overrideBuildNumber')
    overrideVersionText = config.get('VERSION', 'overrideVersionText')
except:
    print("Couldn't load your config file. Make sure there aren't any typos",
          "in the config, and that the config file is accessible.",
          "Setting config variables to their defaults.",
          "Here's the full traceback, in case you need it.", sep="\n")
    traceback.print_exc()
    verbosity = False
    jsonVerbosity = False
    showReleaseTag = False
    tracebacksEnabled = False
    allowGitForUpdating = False
    overrideVersion = False
    overrideBuildNumber = 52
    overrideVersionText = "0.5.2 beta"
    
    
import logging
logger = logging.getLogger(name='pyweather_updater_0.5.2beta')
logformat = '%(asctime)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logformat)

def printException():
    if tracebacksEnabled == True:
        print("Here's the full traceback:")
        traceback.print_exc()
        
def printException_loggerwarn():
    if verbosity == True:
        logger.warn("Oh snap! We ran into a non-critical error. Here's the traceback.")
        logger.warn(traceback.print_exc())

if verbosity == True:
    logger.setLevel(logging.DEBUG)
elif tracebacksEnabled == True:
    logger.setLevel(logging.ERROR)
else:
    logger.setLevel(logging.CRITICAL)
    
logger.debug("Listing configuration options:")
logger.debug("verbosity: %s ; jsonVerbosity: %s" %
             (verbosity, jsonVerbosity))
logger.debug("showReleaseTag: %s ; tracebacksEnabled: %s" %
             (showReleaseTag, tracebacksEnabled))
logger.debug("overrideVersion: %s ; overrideBuildNumber: %s" %
             (overrideVersion, overrideBuildNumber))
logger.debug("overrideVersionText: %s" %
             (overrideVersionText))

if overrideVersion == True:
    logger.info("Overriding version info.")
    buildnumber = overrideBuildNumber
    buildversion = overrideVersionText
else:    
    buildnumber = 52
    buildversion = "0.5.2 beta"

logger.debug("buildnumber: %s ; buildversion: %s" %
             (buildnumber, buildversion))
print("Checking for updates. This shouldn't take that long.")
try:
    versioncheck = requests.get("https://raw.githubusercontent.com/o355/pyweather/master/updater/versioncheck.json")
    logger.debug("versioncheck: %s" % versioncheck)
except:
    logger.warn("Couldn't check for updates! Is there an internet connection?")
    print(Style.BRIGHT + Fore.RED + "Couldn't check for updates.")
    print("Make sure GitHub user content is unblocked, and you have an internet connection.")
    print("Error 54, updater.py")
    printException()
    print("Press enter to exit.")
    input()
    sys.exit()
    
versionJSON = json.loads(versioncheck.text)
if jsonVerbosity == True:
    logger.debug("versionJSON: %s" % versionJSON)
logger.debug("Loaded versionJSON with reader %s" % reader)
version_buildNumber = float(versionJSON['updater']['latestbuild'])
version_latestVersion = versionJSON['updater']['latestversion']
version_latestURL = versionJSON['updater']['latesturl']
version_latestFileName = versionJSON['updater']['latestfilename']
version_latestReleaseTag = versionJSON['updater']['latestversiontag']
logger.debug("version_buildNumber: %s ; version_latestVersion: %s"
             % (version_buildNumber, version_latestVersion))
logger.debug("version_latestURL: %s ; verion_latestFileName: %s"
             % (version_latestURL, version_latestFileName))
logger.debug("version_latestReleaseTag: %s" % version_latestReleaseTag)
version_latestReleaseDate = versionJSON['updater']['releasedate']
logger.debug("version_latestReleaseDate: %s" % version_latestReleaseDate)
if buildnumber >= version_buildNumber:
    logger.info("PyWeather is up to date.")
    logger.info("local build (%s) >= latest build (%s)"
                % (buildnumber, version_buildNumber))
    print("")
    print(Style.BRIGHT + Fore.GREEN + "PyWeather is up to date!")
    print("You have version: " + Fore.CYAN + buildversion)
    print(Fore.GREEN + "The latest version is: " + Fore.CYAN + version_latestVersion)
    if showReleaseTag == True:
        print(Fore.GREEN + "The latest release tag is: " + Fore.CYAN +
              version_latestReleaseTag)
    print(Fore.GREEN + "Press enter to exit.")
    input()
    sys.exit()

elif buildnumber < version_buildNumber:
    print("")
    logger.warn("PyWeather is NOT up to date.")
    logger.warn("local build (%s) < latest build (%s)"
                % (buildnumber, version_buildNumber))
    print(Fore.RED + Style.BRIGHT + "PyWeather is not up to date! :(")
    print(Fore.RED + "You have version: " + Fore.CYAN + buildversion)
    print(Fore.RED + "The latest version is: " + Fore.CYAN + version_latestVersion)
    print(Fore.RED + "And it was released on: " + Fore.CYAN + version_latestReleaseDate)
    if showReleaseTag == True:
        print(Fore.RED + "The latest release tag is: " + Fore.CYAN +
              version_latestReleaseTag)
    print("")
    print(Fore.RED + "Would you like to download the latest version?" + Fore.YELLOW)
    downloadLatest = input("Yes or No: ").lower()
    logger.debug("downloadLatest: %s" % downloadLatest)
    if downloadLatest == "yes":
        if allowGitForUpdating == True:
            print("Would you like to use Git to update PyWeather?",
                  "Yes or No.")
            confirmUpdateWithGit = input("Input here: ").lower()
            if confirmUpdateWithGit == "yes":
                print("Now updating with Git.")
                try:
                    subprocess.call(["git stash"], shell=True)
                    subprocess.call(["git pull"], shell=True)
                    subprocess.call(["git stash"], shell=True)
                    subprocess.call(["git checkout %s" % version_latestReleaseTag],
                                    shell=True)
                    print("Successfully updated with Git!",
                          "Press enter to exit.", sep="\n")
                    input()
                    sys.exit()
                except:
                    print("When attempting to execute `git stash`,",
                          "`git pull`, and/or `git checkout`,",
                          "an error occurred. Make sure you have git",
                          "installed in your shell, and that it can be used",
                          "from a shell. Anyways, would you like to try and update",
                          "PyWeather by using a .zip download?",
                          "Yes or No.", sep="\n")
                    printException()
                    confirmZipDownload = input("Input here: ").lower()
                    if confirmZipDownload == "yes":
                        print("Downloading using the .zip method.")
                    elif confirmZipDownload == "no":
                        print("Not downloading latest updates using the",
                              ".zip method.", 
                              "Press enter to exit.", sep="\n")
                        
                    else:
                        print("Couldn't understand your input. Defaulting",
                              "to downloading using a .zip.", sep="\n")
            elif confirmUpdateWithGit == "no":
                print("Not updating with Git. Would you like to update",
                      "PyWeather using the .zip download option?",
                      "Yes or No.", sep="\n")
                confirmZipDownload = input("Input here: ").lower()
                if confirmZipDownload == "yes":
                    print("Downloading the latest update with a .zip.")
                elif confirmZipDownload == "no":
                    print("Not downloading the latest PyWeather updates.",
                          "Press enter to exit.", sep="\n")
                    input()
                    sys.exit()
                else:
                    print("Couldn't understand your input. Defaulting to",
                          "downloading the latest version with a .zip.", sep="\n")
            else:
                print("Couldn't understand your input. Defaulting to",
                      "downloading the latest version with a .zip.", sep="\n")        
        print("")
        logger.debug("Downloading latest version...")
        print(Fore.YELLOW + "Downloading the latest version of PyWeather...")
        try:
            updatezip = requests.get(version_latestURL)
            with open(version_latestFileName, 'wb') as fw:
                for chunk in updatezip.iter_content(chunk_size=128):
                    fw.write(chunk)
                fw.close()
        except:
            logger.warn("Couldn't download the latest version!")
            logger.warn("Is the internet online?")
            print("When attempting to download the latest .zip file",
                  "for PyWeather, an error occurred. If you're on a",
                  "network with a filter, make sure that",
                  "'raw.githubusercontent.com' is unblocked.",
                  "Otherwise, make sure you have an internet connection.",
                  sep="\n")
            logger.error("Here's the full traceback (for bug reports):")
            printException()
            print("Press enter to exit.")
            input()
            sys.exit()
        logger.debug("Latest version was saved, filename: %s"
                    % version_latestFileName)
        print(Fore.YELLOW + "The latest version of PyWeather was downloaded " +
              "to the base directory of PyWeather, and saved as " +
             Fore.CYAN + version_latestFileName + Fore.YELLOW + ".")
        print("Press enter to exit.")
        input()
        sys.exit()
    elif downloadLatest == "no":
        logger.debug("Not downloading the latest version.")
        print(Fore.YELLOW + "Not downloading the latest version of PyWeather.")
        print("For reference, you can download the latest version of PyWeather at:")
        print(Fore.CYAN + version_latestURL)
        print("Press enter to exit.")
        input()
        sys.exit()
    else:
        logger.warn("Input could not be understood!")
        print(Fore.GREEN + "Your input couldn't be understood.")
        print("Press enter to exit.")
        input()
        sys.exit()
else:
    logger.warn("PW updater failed. Variables corrupt, maybe?")
    print("When attempting to compare version variables, PyWeather ran",
          "into an error. This error is extremely rare. Make sure you're",
          "not trying to travel through a wormhole with Cooper, and report",
          "the error on GitHub, while it's around."
          "Press enter to exit.", sep='\n')
    input()
    sys.exit()    