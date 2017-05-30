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

config = configparser.ConfigParser()
config.read("storage//config.ini")

if versioninfo2 == "0.6 beta" or versioninfo2 == "0.6.0.1 beta":
    # A usual input() and sys.exit() isn't present here, as it's assumed this
    # is getting executed inside of the updater.
    print("Updating 6 configuration options...")
    try:
        config.add_section("CACHE")
    except:
        print("Failed to add the cache section. Does it exist?")
    
    try:
        config.add_section("RADAR GUI")
    except:
        print("Failed to add the cache section. Does it exist?")
        
    print("New configuration options are available. Would you like to configure",
          "them, or leave them to their defaults? Yes or No.", sep="\n")
    configurenewoptions_06beta = input("")
    with open("updater//versioninfo.txt", 'a') as out:
            out.write("0.6.1 beta")
            out.close()
    
    