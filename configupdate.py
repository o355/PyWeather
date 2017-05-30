# PyWeather Config Update - version 0.6.0.1

# This script is empty. With the improved 0.6 updater, there is no
# update from 0.6 to 0.6.

# From 0.6.1 and on, this file will actually fill up.

import sys
import configparser
import traceback

versioninfo = open("updater//versioninfo.txt")
versioninfo2 = versioninfo.read()
versioninfo.close()

if versioninfo2 == "0.6 beta":
    # A usual input() and sys.exit() isn't present here, as it's assumed this
    # is getting executed inside of the updater.
    print("No changes to your config file is needed!")
elif versioninfo2 == "0.6.0.1 beta":
    print("No changes to your config file is needed!")
    with open("updater//versioninfo.txt", 'a') as out:
            out.write("0.6.0.1 beta")
            out.close()
    