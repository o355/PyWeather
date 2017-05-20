# PyWeather Config Update - version 0.6

# This script is empty. With the improved 0.6 updater, there is no
# update from 0.6 to 0.6.

# From 0.6.1 and on, this file will actually fill up.

import sys
import configparser
import traceback

versioninfo = open("versioninfo.txt")
versioninfo = versioninfo.read()

if versioninfo == "0.6 beta":
    print("No changes to your config file is needed!",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()