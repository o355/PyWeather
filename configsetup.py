'''
_______
|      \  \           /         @@@;
|       \  \         /        `#....@
|        |  \       /       ,;@.....;,;
|        |   \     /       @..@........@`           PyWeather Config Setup
|        |    \   /        .............@           version 0.6.3 beta
|        /     \ /         .............@           (c) 2017-2018 - o355
|_______/       |          @...........#`
|               |           .+@@++++@#;
|               |             @ ;  ,
|               |             : ' .
|               |            @ # .`
|               |           @ # .`
'''

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
import configparser
import traceback
import time

config = configparser.ConfigParser()
config.read("storage//config.ini")

# Verbosity and all that fun stuff isn't available here.
# If the config isn't set up, and by default, verbosity is off
# why should I code it in?

print("Would you like to set up (or reset) PyWeather's config?",
      "Yes or No.", sep="\n")
cd_confirmation = input("Input here: ").lower()
if cd_confirmation == "yes":
    try:
        provisioned = config['USER']['configprovisioned']
        print("Your config file is already provisioned! Would you still",
              "like to have your config reprovisioned?",
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
        config.add_section("HURRICANE")
    except configparser.DuplicateSectionError:
        print("Hurricane section could not be added.")

    try:
        config.add_section("GEOCODER API")
    except configparser.DuplicateSectionError:
        print("Geocoder API section could not be added.")

    try:
        config.add_section("FAVORITE LOCATIONS")
    except configparser.DuplicateSectionError:
        print("Favorite locations section could not be added.")

    try:
        config.add_section("FIRSTINPUT")
    except configparser.DuplicateSectionError:
        print("Firstinput section could not be added.")
    
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
        config.add_section('PREFETCH')
    except configparser.DuplicateSectionError:
        print("Prefetch section could not be added.")

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
    config['SUMMARY']['showyesterdayonsummary'] = 'False'
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
    config['UI']['extratools_enabled'] = 'False'
    config['UPDATER']['autocheckforupdates'] = 'False'
    config['UPDATER']['show_updaterreleasetag'] = 'False'
    config['KEYBACKUP']['savedirectory'] = 'backup//'
    config['PYWEATHER BOOT']['validateapikey'] = 'True'
    config['UPDATER']['showReleaseNotes'] = 'True'
    config['UPDATER']['showReleaseNotes_uptodate'] = 'False'
    config['UPDATER']['showNewVersionReleaseDate'] = 'True'
    config['USER']['configprovisioned'] = 'True'
    config['CACHE']['enabled'] = 'True'
    config['CACHE']['alerts_cachedtime'] = '5'
    config['CACHE']['current_cachedtime'] = '10'
    config['CACHE']['threedayhourly_cachedtime'] = '60'
    config['CACHE']['tendayhourly_cachedtime'] = '60'
    config['CACHE']['forecast_cachedtime'] = '60'
    config['CACHE']['almanac_cachedtime'] = '240'
    config['CACHE']['sundata_cachedtime'] = '480'
    config['CACHE']['tide_cachedtime'] = '480'
    config['CACHE']['yesterday_cachedtime'] = '720'
    config['RADAR GUI']['radar_imagesize'] = 'normal'
    config['RADAR GUI']['bypassconfirmation'] = 'False'
    config['GEOCODER']['scheme'] = 'http'
    config['PREFETCH']['10dayfetch_atboot']= 'False'
    config['PREFETCH']['hurricanedata_atboot'] = 'False'
    config['PREFETCH']['yesterdaydata_atboot'] = 'False'
    config['CACHE']['hurricane_cachedtime'] = '180'
    config['FIRSTINPUT']['geoipservice_enabled'] = 'False'
    config['FIRSTINPUT']['allow_pwsqueries'] = 'True'
    config['HURRICANE']['enablenearestcity'] = 'False'
    config['HURRICANE']['enablenearestcity_forecast'] = 'False'
    config['HURRICANE']['api_username'] = 'pyweather_proj'
    config['HURRICANE']['nearestcitysize'] = 'medium'
    config['FAVORITE LOCATIONS']['enabled'] = 'True'
    config['FAVORITE LOCATIONS']['favloc1'] = 'None'
    config['FAVORITE LOCATIONS']['favloc2'] = 'None'
    config['FAVORITE LOCATIONS']['favloc3'] = 'None'
    config['FAVORITE LOCATIONS']['favloc4'] = 'None'
    config['FAVORITE LOCATIONS']['favloc5'] = 'None'
    config['GEOCODER API']['customkey_enabled'] = 'False'
    config['GEOCODER API']['customkey'] = 'None'

    # Begin to determine geocoder scheme
    print("Attempting to detect a geocoder scheme for your system, this should only take a few moments.")

    try:
        import geopy
        geopy_installed = True
    except ImportError:
        print("Failed to import geopy. It's recommended that you install geopy for PyWeather to work.",
              "Skipping geocoder scheme detection and defaulting to 'http' as the scheme.", sep="\n")
        geopy_installed = False

    if geopy_installed is True:
        # HTTPS validation
        from geopy import GoogleV3

        geocoder = GoogleV3(scheme='https')
        # I've found that one "warm up request", and then waiting ~15 seconds somehow helps determine if a platform is HTTP/HTTPS compatible.
        try:
            geocoder.geocode("123 5th Avenue, New York, NY")
        except:
            didthewarmupgeocodefail = "you bet"

        print("A warmup geocode has just been completed which helps with determining which scheme will work",
              "on your OS. Waiting 10 seconds before making another geocode requests (to prevent rate limiting).", sep="\n")
        time.sleep(10)

        try:
            geocoder.geocode("123 5th Avenue, New York, NY")
            print("The geocoder can operate with HTTPS enabled on your OS.")
            config['GEOCODER']['scheme'] = 'https'
            print("Changes saved.")
        except geopy.exc.GeocoderServiceError:
            print("Geopy probably can't run without HTTPS (or your internet went down). Trying HTTP as the scheme.")
            geocoder = GoogleV3(scheme='http')
            print("Waiting 10 seconds to avoid rate limiting after the previous geocode.")
            time.sleep(10)
            try:
                geocoder.geocode("123 5th Avenue, New York, NY")
                print("The geocoder can operate, but without HTTPS enabled on your OS. Saving these changes.")
                config['GEOCODER']['scheme'] = 'http'
                print("Changes saved.")
            except geopy.exc.GeocoderServiceError:
                print("You probably don't have an internet connection, as HTTPS and HTTP validation both failed.",
                      "Defaulting to HTTP as the geopy scheme.", sep="\n")
                config['GEOCODER']['scheme'] = 'http'
                print("Changes saved.")

    try:
        with open('storage//config.ini', 'w') as configfile:
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
    try:
        open('updater//versioninfo.txt', 'w').close()
        with open("updater//versioninfo.txt", 'a') as out:
            out.write("0.6.3 beta")
            out.close()
    except:
        print("Couldn't write the versioninfo file. This may cause issues with PyWeather down the road.")

    print("All done! Press enter to exit.")
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