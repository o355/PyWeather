# PyWeather Config Update - version 0.6.1

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
    try:
        config.add_section("CACHE")
    except:
        print("Failed to add the cache section. Does it exist?")
    
    try:
        config.add_section("RADAR GUI")
    except:
        print("Failed to add the cache section. Does it exist?")
        
    print("7 new configuration options have been added.",
          "Details:",
          "- CACHE/alerts_cachedtime - Sets the cache time on alert data - Defaults to 5",
          "- CACHE/current_cachedtime - Sets the cache time on current data - Defaults to 10",
          "- CACHE/hourly_cachedtime - Sets the cache time on hourly data - Defaults to 60",
          "- CACHE/forecast_cachedtime - Sets the cache time on forecast data - Defaults to 60",
          "- CACHE/almanac_cachedtime - Sets the cache time on almanac data - Defaults to 240",
          "- CACHE/sunrise_cachedtime - Sets the cache time on sunrise data - Defaults to 480",
          "- CACHE/enabled - Enables or disables the new cache system - Defaults to True",
          "- RADAR GUI/radar_imagesize - Sets the image size of radar animations - Defaults to normal", 
          "- RADAR GUI/bypassconfirmation - Sets if the experimental warning can be bypassed - Defaults to False", sep="\n")
    
    config['CACHE']['alerts_cachedtime'] = '5'
    config['CACHE']['current_cachedtime'] = '10'
    config['CACHE']['hourly_cachedtime'] = '60'
    config['CACHE']['forecast_cachedtime'] = '60'
    config['CACHE']['almanac_cachedtime'] = '240'
    config['CACHE']['sunrise_cachedtime'] = '480'
    config['RADAR GUI']['radar_imagesize'] = 'normal'
    config['RADAR GUI']['bypassconfirmation'] = 'False'
    config['CACHE']['enabled'] = 'True'
    
    try:
        with open('storage//config.ini', 'w') as configfile:
                config.write(configfile)
        print("Configuration options committed successfully!")
    except:
        print("Couldn't update your config file! A full error will be printed below.")
        traceback.print_exc()
        with open("updater//versioninfo.txt", 'a') as out:
            out.write("0.6.1 beta")
            out.close()
        print("Please report this bug to GitHub (github.com/o355/pyweather), along with",
              "the full error. Along with that, please manually add the configuration entries",
              "as listed above, with their default values in your configuration file.",
              "Press enter to exit.")
    with open("updater//versioninfo.txt", 'a') as out:
        out.write("0.6.1 beta")
        out.close()
    
    