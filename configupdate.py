# PyWeather Config Update - version 0.6.2 beta
# (c) 2017, licensed under the GNU GPL v3

# This script is empty. With the improved 0.6 updater, there is no
# update from 0.6 to 0.6.

# From 0.6.1 and on, this file will actually fill up.

import sys
import configparser
import traceback
import os

versioninfo = open("updater//versioninfo.txt")
versioninfo2 = versioninfo.read()
versioninfo.close()

config = configparser.ConfigParser()
config.read("storage//config.ini")

def geopycheck():
    print("In version 0.6.2 beta and above, your geocoder scheme needs to get set, based on your OS.",
          "PyWeather can automatically do this now, or you can manually define your scheme.",
          "Type in 'automaticsetup' for the automatic setup, and 'manualsetup' for manual setup",
          "in the prompt below.", sep="\n")
    setupmethod = input("Input here: ").lower()
    if setupmethod == "manualsetup":
        print("Geopy's Google geocoder can work in HTTPS-enabled mode on 95% of platforms,",
              "but has a tendancy to fail on OS X, or other platforms. In the prompt below,",
              "enter 'https' for geopy to work in https mode, or 'http' for http mode.",
              "Please note: Your settings will not be validated!", sep="\n")
        geopymode = input("Input here: ").lower()
        if geopymode == "https":
            config['GEOCODER']['scheme'] = 'https'
            print("Changes saved.")
        else:
            config['GEOCODER']['scheme'] = 'https'
            if geopymode == "http":
                print("Changes saved.")
            else:
                print("Couldn't understand your input. Defaulting to 'http'.")
    else:
        if setupmethod == "automaticsetup":
            print("Starting automatic setup.")
        else:
            print("Couldn't understand your input. Defaulting to automatic setup.")

        import geopy
        from geopy import GoogleV3
        geocoder = GoogleV3(scheme='https')
        try:
            location = geocoder.geocode("123 5th Avenue, New York, NY")
            print("The geocoder can operate with HTTPS enabled on your OS. Saving these changes...")
            config['GEOCODER']['scheme'] = 'https'
            print("Changes saved.")
        except geopy.exc.GeocoderServiceError:
            print("Geopy probably can't run without HTTPS (or your internet went down). Trying HTTP as the scheme...")
            geocoder = GoogleV3(scheme='http')
            try:
                location = geocoder.geocode("123 5th Avenue, New York, NY")
                print("The geocoder can operate, but without HTTPS enabled on your OS. Saving these changes...")
                config['GEOCODER']['scheme'] = 'http'
                print("Changes saved.")
            except geopy.exc.GeocoderServiceError:
                print("You probably don't have an internet connection, as HTTPS and HTTP validation both failed.",
                      "Defaulting to HTTP as the geopy scheme...", sep="\n")
                config['GEOCODER']['scheme'] = 'http'
                print("Changes saved.")


if "0.6 beta" or "0.6.0.1 beta" in versioninfo2:
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

    try:
        config.add_section("GEOCODER")
    except:
        print("Failed to add the geocoder section. Does it exist?")

    try:
        config.add_section("PREFETCH")
    except:
        print("Failed to add the prefetch section. Does it exist?")
        
    print("New configuration options have been added.",
          "Details:",
          "- CACHE/alerts_cachedtime - Sets the cache time on alert data - Defaults to 5",
          "- CACHE/current_cachedtime - Sets the cache time on current data - Defaults to 10",
          "- CACHE/threedayhourly_cachedtime - Sets the cache time on 1.5 day hourly data - Defaults to 60",
          "- CACHE/tendayhourly_cachedtime - Sets the cache time on 10 day hourly data - Defaults to 60",
          "- CACHE/forecast_cachedtime - Sets the cache time on forecast data - Defaults to 60",
          "- CACHE/almanac_cachedtime - Sets the cache time on almanac data - Defaults to 240",
          "- CACHE/sundata_cachedtime - Sets the cache time on sunrise data - Defaults to 480",
          "- CACHE/enabled - Enables or disables the new cache system - Defaults to True",
          "- RADAR GUI/radar_imagesize - Sets the image size of radar animations - Defaults to normal", 
          "- RADAR GUI/bypassconfirmation - Sets if the experimental warning can be bypassed - Defaults to False",
          "- CACHE/tide_cachedtime - Sets the cache time on tide data - Defaults to 480",
          "- CACHE/hurricane_cachedtime - Sets the cache time on hurricane data - Defaults to 180",
          "- SUMMARY/showtideonsummary - Sets if tide data should be shown on the summary screen - Defaults to False",
          "- GEOCODER/scheme - Sets the geocoder scheme (https on 95% of platforms, http on others) - Defaults to https",
          "- PREFETCH/10dayfetch_atboot - Sets if PyWeather should fetch 10-day hourly at boot - Defaults to False",
          "- PREFETCH/hurricanedata_atboot - Sets if PyWeather should fetch hurricane data at boot - Defaults to False", sep="\n")

    print("")
    print("2 old configuration options, and 2 sections are now unused. Please delete these options from your config file.",
          "Details:",
          "- CACHE/hourly_cachedtime - Used to set the global hourly cache time - Now removed",
          "- HOURLY/10dayhourly_atboot - Used to set if PyWeather should fetch 10-day hourly at boot - Now removed",
          "- HOURLY section - No longer in use for any configuration options.",
          "- CHANGELOG section - No longer in use for any configuration options.", sep="\n")
    
    config['CACHE']['alerts_cachedtime'] = '5'
    config['CACHE']['current_cachedtime'] = '10'
    config['CACHE']['threedayhourly_cachedtime'] = '60'
    config['CACHE']['tendayhourly_cachedtime'] = '60'
    config['CACHE']['forecast_cachedtime'] = '60'
    config['CACHE']['almanac_cachedtime'] = '240'
    config['CACHE']['sundata_cachedtime'] = '480'
    config['RADAR GUI']['radar_imagesize'] = 'normal'
    config['RADAR GUI']['bypassconfirmation'] = 'False'
    config['CACHE']['enabled'] = 'True'
    config['CACHE']['tide_cachedtime'] = '480'
    config['SUMMARY']['showtideonsumary'] = 'False'
    config['PREFETCH']['10dayfetch_atboot'] = 'False'
    config['PREFETCH']['hurricanedata_atboot'] = 'False'
    config['CACHE']['hurricane_cachedtime'] = '180'
    geopycheck()

elif "0.6.1 beta" in versioninfo2:
    try:
        config.add_section("GEOCODER")
    except:
        print("Failed to add the geocoder section. Does it exist?")

    print("New configuration options have been added.",
          "Details:",
          "- CACHE/tide_cachedtime - Sets the cache time on tide data - Defaults to 480",
          "- SUMMARY/showtideonsummary - Sets if tide data should be shown on the summary screen - Defaults to False",
          "- CACHE/threedayhourly_cachedtime - Sets the cache time on 1.5 day hourly data - Defaults to 60",
          "- CACHE/tendayhourly_cachedtime - Sets the cache time on the 10 day hourly data - Defaults to 60",
          "- CACHE/hurricane_cachedtime - Sets the cache time on hurricane data - Defaults to 180",
          "- GEOCODER/scheme - Sets the geocoder scheme (https on 95% of platforms, http on others) - Defaults to https",
          "- PREFETCH/10dayfetch_atboot - Sets if PyWeather should fetch 10-day hourly at boot - Defaults to False",
          "- PREFETCH/hurricanedata_atboot - Sets if PyWeather should fetch hurricane data at boot - Defaults to False", sep="\n")

    print("")
    print("2 old configuration options, and 2 sections have been deleted.",
          "Details:",
          "- CACHE/hourly_cachedtime - Used to set the global hourly cache time - Now removed",
          "- HOURLY/10dayhourly_atboot - Used to set if PyWeather should fetch 10-day hourly at boot - Now removed",
          "- HOURLY section - No longer in use for any configuration options.",
          "- CHANGELOG section - No longer in use for any configuration options.", sep="\n")

    config['CACHE']['tide_cachedtime'] = '480'
    config['SUMMARY']['showtideonsumary'] = 'False'
    config['CACHE']['threedayhourly_cachedtime'] = '60'
    config['CACHE']['tendayhourly_cachedtime'] = '60'
    config['PREFETCH']['10dayfetch_atboot'] = 'False'
    config['PREFETCH']['hurricanedata_atboot'] = 'False'
    config['CACHE']['hurricane_cachedtime'] = '180'
    geopycheck()

elif "0.6.2 beta" in versioninfo2:
    print("PyWeather is up-to-date. As such, we don't need to make any configuration changes.")
    sys.exit()

try:
    with open('storage//config.ini', 'w') as configfile:
            config.write(configfile)
    print("Configuration options committed successfully!")
except:
    print("Couldn't update your config file! A full error will be printed below.")
    traceback.print_exc()
    print("Please report this bug to GitHub (github.com/o355/pyweather), along with",
          "the full error. Along with that, please manually add the configuration entries",
          "as listed above, with their default values in your configuration file.",
          "Press enter to exit.")
    input()
    try:
        open("updater//versioninfo.txt", 'w').close()
        with open("updater//versioninfo.txt", 'a') as out:
            out.write("0.6.2 beta")
            out.close()
    except:
        print("Could not write out an updated versioninfo text file. Please",
              "modify 'updater/versioninfo.txt' to display '0.6.2 beta'.", sep="\n")
    sys.exit()
try:
    open("updater//versioninfo.txt", 'w').close()
    with open("updater//versioninfo.txt", 'a') as out:
        out.write("0.6.2 beta")
        out.close()
except:
    print("Could not write out an updated versioninfo text file. Please",
          "modify 'updater/versioninfo.txt' to display '0.6.2 beta'.", sep="\n")
    
    