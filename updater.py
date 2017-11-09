# PyWeather Updater - version 0.6.3 beta
# Copyright (C) 2017 o355

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import json
try:
    import requests
except ImportError:
    print("When attempting to import the library requests, we ran into an import error.",
          "Please make sure that requests is installed.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()

import codecs
import shutil
import configparser
import traceback
import subprocess
from platform import release
reader = codecs.getreader("utf-8")
try:
    from colorama import Fore, Style, init
except ImportError:
    print("When attempting to import the library colorama, we ran into an import error.",
          "Please make sure that colorama is installed.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()

init()

config = configparser.ConfigParser()
config.read('storage//config.ini')

# Try loading the versioninfo.txt file. If it isn't around, create the file with
# the present version info.

try:
    versioninfo = open('updater//versioninfo.txt').close()
except:
    open('updater//versioninfo.txt', 'w').close()
    with open("updater//versioninfo.txt", 'a') as out:
        out.write("0.6.3 beta")
        out.close()
        
# See if the config is "provisioned". If it isn't, a KeyError will occur,
# because it's not created. Creative.
try:
    configprovisioned = config.getboolean('USER', 'configprovisioned')
except:
    print("We ran into an error. Full traceback below.")
    traceback.print_exc()
    # Not doing a separate script launch. Doing sys.exit in that script would just continue
    # PyWeather. We ask the user to run the script themselves.
    print("This isn't good. Your config file isn't provisioned.",
          "If you're new to PyWeather, you should run the setup script.",
          "Otherwise, try launching configsetup.py, which is available in the", 
          "storage folder. Press enter to exit.", sep="\n")
    input()
    sys.exit()

configerrorcount = 0
try:
    verbosity = config.getboolean('VERBOSITY', 'updater_verbosity')
except:
    print("When attempting to load your configuration file, an error occurred.",
          "VERBOSITY/updater_verbosity failed to load. Defaulting to 'False'.", sep="\n")
    configerrorcount += 1
    verbosity = False
try:
    jsonVerbosity = config.getboolean('VERBOSITY', 'updater_jsonverbosity')
except:
    print("When attempting to load your configuration file, an error occurred.",
          "VERBOSITY/updater_jsonverbosity failed to load. Defaulting to 'False'.", sep="\n")
    jsonVerbosity = False
    configerrorcount += 1
try:
    showReleaseTag = config.getboolean('UPDATER', 'show_updaterReleaseTag')
except:
    print("When attempting to load your configuration file, an error occurred.",
          "UPDATER/show_updaterReleaseTag failed to load. Defaulting to 'False'.", sep="\n")
    showReleaseTag = False
    configerrorcount += 1
try:
    tracebacksEnabled = config.getboolean('TRACEBACK', 'updater_tracebacks')
except:
    print("When attempting to load your configuration file, an error occurred.",
          "TRACEBACK/updater_tracebacks failed to load. Defaulting to 'False'.", sep="\n")
    tracebacksEnabled = False
    configerrorcount += 1

try:
    showReleaseNotes = config.getboolean('UPDATER', 'showReleaseNotes')
except:
    print("When attempting to load your configuration file, an error occurred.",
          "UPDATER/showReleaseNotes failed to load. Defaulting to 'True'.", sep="\n")
    showReleaseNotes = True
    configerrorcount += 1
try:
    showReleaseNotes_uptodate = config.getboolean('UPDATER', 'showReleaseNotes_uptodate')
except:
    print("When attempting to load your configuration file, an error occurred.",
          "UPDATER/showReleaseNotes_uptodate failed to load. Defaulting to 'False'.", sep="\n")
    showReleaseNotes_uptodate
    configerrorcount += 1

try:
    showNewVersionReleaseDate = config.getboolean('UPDATER', 'showNewVersionReleaseDate')
except:
    print("When attempting to load your configuration file, an error occurred.",
          "UPDATER/showNewVersionReleaseDate failed to load. Defaulting to 'True'.")
    showNewVersionReleaseDate
    configerrorcount += 1

if configerrorcount >= 1:
    print("", "When trying to load your configuration file, error(s) occurred.",
          "Try making sure that there are no typos in your config file, and try setting values",
          "in your config file to the default values as listed above. If all else fails, try using",
          "configsetup.py to set all config options to their defaults. If issues still occur,",
          "report the bug on GitHub.", sep="\n")
    
    
import logging
logger = logging.getLogger()
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
logger.debug("showReleaseNotes_uptodate: %s ; showNewVersionReleaseDate: %s" %
             (showReleaseNotes_uptodate, showNewVersionReleaseDate))
logger.debug("showReleaseNotes: %s" %
             (showReleaseNotes))

buildnumber = 63
buildversion = "0.6.3 beta"

logger.debug("buildnumber: %s ; buildversion: %s" %
             (buildnumber, buildversion))
print("Checking for updates. This shouldn't take that long.")
try:
    versioncheck = requests.get("https://raw.githubusercontent.com/o355/pyweather/master/updater/versioncheck.json")
    releasenotes = requests.get("https://raw.githubusercontent.com/o355/pyweather/master/updater/releasenotes.txt")
    logger.debug("versioncheck: %s ; releasenotes: %s" %
                 (versioncheck, releasenotes))
except:
    logger.warn("Couldn't check for updates! Is there an internet connection?")
    print(Style.BRIGHT + Fore.RED + "Couldn't check for updates.")
    print("Make sure GitHub user content is unblocked, and you have an internet connection.")
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
version_latestReleaseDate = versionJSON['updater']['releasedate']
version_nextVersionReleaseDate = versionJSON['updater']['nextversionreleasedate']
logger.debug("version_buildNumber: %s ; version_latestVersion: %s" %
             (version_buildNumber, version_latestVersion))
logger.debug("version_latestURL: %s ; version_latestFileName: %s" %
             (version_latestURL, version_latestFileName))
logger.debug("version_latestReleaseTag: %s ; version_latestReleaseDate: %s" %
             (version_latestReleaseTag, version_latestReleaseDate))
logger.debug("version_nextVersionReleaseDate: %s" % version_nextVersionReleaseDate)
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
    if showNewVersionReleaseDate == True:
        print(Fore.GREEN + "Psst, a new version of PyWeather should get released on: "
              + Fore.CYAN + version_nextVersionReleaseDate)
    if showReleaseNotes_uptodate == True:
        print(Fore.GREEN + "Here's the release notes for this release:",
              Fore.CYAN + releasenotes.text, sep="\n")
    print("", Fore.GREEN + "Press enter to exit.", sep="\n")
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
    if showReleaseNotes == True:
        print(Fore.RED + "Here's the release notes for the latest release:",
              Fore.CYAN + releasenotes.text, sep="\n")
    print("")
    print(Fore.RED + "Would you like to download the latest version?" + Fore.YELLOW)
    downloadLatest = input("Yes or No: ").lower()
    logger.debug("downloadLatest: %s" % downloadLatest)
    if downloadLatest == "yes":
        # Remove the git updater - It's no longer needed at this time.
        #if allowGitForUpdating == True:
        #    print("Would you like to use Git to update PyWeather?",
        #          "Yes or No.")
        #    confirmUpdateWithGit = input("Input here: ").lower()
        #    if confirmUpdateWithGit == "yes":
        #        print("Now updating with Git.")
        #        try:
        #            # Doesn't hurt to stash twice.
        #            subprocess.call(["git fetch"], shell=True)
        #            subprocess.call(["git stash"], shell=True)
        #            subprocess.call(["git checkout %s" % version_latestReleaseTag],
        #                            shell=True)
        #            print("Now updating your config file.")
        #            exec(open("configupdate.py").read())
        #            print("PyWeather has been successfully updated. To finish updating,",
        #                  "please press enter to exit PyWeather.", sep="\n")
        #            input()
        #            sys.exit()
        #        except:
        #            print("When attempting to update using git, either",
        #                  "when doing `git fetch`, `git checkout`, or to",
        #                  "execute the configupdate script, an error occurred."
        #                  "We can try updating using the .zip method.",
        #                  "Would you like to update PyWeather using the .zip method?",
        #                  "Yes or No.", sep="\n")
        #            printException()
        #            confirmZipDownload = input("Input here: ").lower()
        #            if confirmZipDownload == "yes":
        #                print("Downloading using the .zip method.")
        #            elif confirmZipDownload == "no":
        #                print("Not downloading latest updates using the",
        #                      ".zip method.",
        #                      "Press enter to exit.", sep="\n")
        #
        #            else:
        #                print("Couldn't understand your input. Defaulting",
        #                      "to downloading using a .zip.", sep="\n")
        #    elif confirmUpdateWithGit == "no":
        #        print("Not updating with Git. Would you like to update",
        #              "PyWeather using the .zip download option?",
        #              "Yes or No.", sep="\n")
        #        confirmZipDownload = input("Input here: ").lower()
        #        if confirmZipDownload == "yes":
        #            print("Downloading the latest update with a .zip.")
        #        elif confirmZipDownload == "no":
        #            print("Not downloading the latest PyWeather updates.",
        #                  "Press enter to exit.", sep="\n")
        #            input()
        #            sys.exit()
        #        else:
        #            print("Couldn't understand your input. Defaulting to",
        #                  "downloading the latest version with a .zip.", sep="\n")
        #    else:
        #        print("Couldn't understand your input. Defaulting to",
        #              "downloading the latest version with a .zip.", sep="\n")
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