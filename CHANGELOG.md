# PyWeather changelog

Quick note: I generally use the changelog (thanks Eclipse for supporting MD files!) as a to-do list, and to see what I've done. I also type up what I'm probably going to do in future versions. So, that's why you'll see stuff like "- Done, and tested!", or "Should by finished by (date)".

## version 0.5.3 beta - Should be released on 5/18/2017
* Rewrites multiline prints in keybackup.py/updater.py (thanks to @gsilvapt for the PR/notifing me of the issue, and @Rhomboid on /r/learnpython for a good solution) - Should be finished by 5/8.
* Catches up config.py with the latest config options - Should be finished by 5/10.
* Adds the ability to update with git through the command line - Should be finished by 5/13. This is possible!
* Adds back the iteration detections for historical hourly. This is accomplished by doing a for loop before user data is shown, and calculating the total amount of iterations that need to be done. - Should be finished by 5/17
* Adds the option to cancel a pending shell command in PyWeather setup (Ctrl+C), and increases the time until the command is executed to 5 seconds. - Should be finished by 5/18

## version 0.5.2 beta - Should be released on 5/3/2017
**NEW FEATURES/REMOVALS**
* Adds the raw traceback output in keybackup.py - Done, and tested!
* Changes the error message when the config file fails to load (the potential for the file to not get loaded) - Done, and tested!
* Removes the error catching of a bad config file load, it's useless. - Done, and tested!
* Adds a fallback to doing a system "sudo pip3 install library" if a library is found not to be installed. (in setup) - Done, and tested!
* Added a warning to users using Python 3.0-3.4 in the setup script, it's known to cause errors. - Done, and tested!
* Switches the "here's the full traceback" thing from logger.error to a pure printout. - Done, and tested!
* Adds version checking in the setup script, while trying not to be Windows 10. - Done, and tested!
* Adds the library check script, which checks for libraries PyWeather needs. - Scrapped. I might reconsider adding it at a later time, but at the moment, this is useless.
* Adds the option during setup to chown -R /usr/local/bin/geocode to the home user. (Python 3.5-3.6 only) - 40% done, not tested.
* Adds a separate config.py script, to configure all available options. - Should be finished by 4/24.
* Adds the ability to fetch all JSON files using a backup key, if the primary one fails. This is accomplished by using the first JSON fetch as a test, and seeing if a KeyError occurs. If a KeyError occurs, the backup key will be substituted. - Should be finished by 4/26.
* Rewrites multiline prints in pyweather.py (thanks to @gsilvapt for the PR/notifing me of the issue, and @Rhomboid on /r/learnpython for a good solution) (some multiline prints with a lot of variables won't be condensed, for the sake of sanity.) - Should be finished by 5/2.
* Finally gets around to getting the "can't run you have Python 2" warning in all scripts. - Should be finished by 5/3.

**BUG FIXES**
* Fixed a bug in which if tracebacks were enabled in the updater, the tracebacks wouldn't print properly, as such, producing a traceback. Huh.

## version 0.5.1 beta - Released on 4/17/2017
**NEW FEATURES/REMOVALS:**
* Removes if verbosity == True in the separate updater, and keybackup scripts.
* Adds the ability to load your backup key if PyWeather can't access your primary key.
* Adds the raw traceback output in updater.py/setup.py.
* Adds the logger displaying configuration options at the start of every script.
* The backup key will now stay static to backkey.txt, with a configurable directory (thanks to @ModoUnreal for the PR).
* Changes the non-critical traceback print function from an info level to a warn level in all scripts.
* Catches up the setup file with the new configuration options added in 0.5 beta.
* PyWeather Updater will now show the release tag, even when PyWeather is up-to-date.
* In setup, the key-reconfirmation is now a while true infinite loop. - Done, and tested!
* Adds a check for "None" in of rain in the 10-day forecast, and -999 mph winds in the 10-day forecast on the current day.
* Rewrites multiline prints in setup.py (thanks to @gsilvapt for the PR/notifing me of the issue, and @Rhomboid on /r/learnpython for a good solution).
* Adds the configdefault.py script, to reset all configuration options to their default.
* Minor UI changes across most of the scripts.

**BUG FIXES:**
* Fixed a bug in which if the config file wouldn't load in the updater, the variable showReleaseTag wouldn't get defined, and it would presumably crash.
* Fixed a bug in which in the keybackup script, the logger name was not `pyweather_keybackup_0.5.1beta` (it was instead `pyweather_keybackup_0.4.2beta`.
* Fixed a bug in which if Wunderground gave >60 minute intervals for historical hourly information, PyWeather would only display 24 iterations. With this, the iteration break detection is gone, so a user may see "enter to continue", with no data following that.
* Fixes multiple bugs with UI issues in historical hourly, and 10-day hourly information.
* Fixes a "bug" in which if the config file couldn't be loaded, the error wasn't properly caught. This is actually useless in practice, so hurray for wasted time!
* Fixes a "bug" in which if the config file couldn't be properly written to in scripts, the error wasn't properly caught.
* Fixes a bug in which the logger name wasn't properly defined.

## version 0.5 beta (The Back to the Future Update) - Released on 3/31/2017
* The naming comes from a combination of adding history (back), and 10-day future (future). Sorry.
* This release is so big, I've had to separate new features from bug fixes.

**NEW FEATURES/REMOVALS:**
* Adds historical weather information to PyWeather.
* Adds output of the raw traceback in PyWeather errors (pyweather.py ONLY, on by default.)
* Adds 10-day hourly weather to PyWeather (you'll hit enter 40 times!...by default).
* Adds a method in which PyWeather will display rain data for the day/night if the temperature is above 32F. Otherwise, it'll just show snow data. Fixes the bug in which the detailed forecast showed both rain/snow data.
* Adds a config option I can't really describe here (fetching the 10 day JSON at boot, or the 3 day JSON at boot/10day when needed)
* Reworks the config file some, sections are now where they need to be (aka verbosity has it's own section)
* Adds the ability to turn off the "enter to continue" things in the 10-day/hourly forecasts
* Adds the ability to set the interval in which the "enter to continue" will appear
* Adds the ability to show how many iterations are left in the enter to continue thing (if it's on)
* Removes the if verbosity == True garbage in the setup file. 
* Adds the option to view the release tag in the updater.
* Adds verbosity for all new functions added. This will now be standard!
* Minor UI changes.

**BUG FIXES:**
* Fixes a bug in which if the config file wouldn't load, the program won't load (checkforupdates wasn't defined.)
* Fixes a bug in which if the autoupdater couldn't contact GitHub, it would try to parse the auto-updater information.
* Fixes a bug in which if exceptions occurred when fetching the almanac .json, the exception wouldn't get caught.
* Fixes a bug in which if astronomy data couldn't be fetched (in more details), PyWeather would completely exit.
* Fixes a bug in which the setup script wouldn't start, because copy and pasting is a thing.
* Fixes a bug in which if the config file wouldn't load, the sunrise/sunset data would show up on the summary screen

## version 0.4.2 beta - Released 3/14/2017
* Adds an autoupdater to PyWeather
* Adds the ability to configure the config file in the setup script
* Adds verbosity (of course it did) to almost all scripts (yay)
* Adds the ability to "back up" your API key, and a script to do it (it's very simple...)
* No more if verbosity == True in the main PyWeather script.
* Fixes a bug in which sunset/sunrise times would show 6:0, when it was really 6:00, etc.
* Fixes a bug in which if the sun/moon data or almanac data wasn't prefetched on summary, in the detailed view, every time a user viewed the data, a new API call was made.
* Cleans up some legacy code.

## version 0.4.1 beta - Released 3/8/2017
* Fixes a bug in which detailed sun/moon data wouldn't get shown
* API calls are more efficient
* Adds a "Press enter to continue" across PyWeather for users who view PW by double-clicking.
* Fully implements almanac on the summary screen
* Fully implements the config
* Fixes a variety of smaller bugs

## version 0.4 beta (The Astronomy Update) - Released 3/4/2017
* Adds the almanac to PyWeather
* Adds sunrise/sunset data to PyWeather
* Mostly adds a config file to PyWeather
* Adds a separate updater to update PyWeather
* UI changed some (wow)
* Fixed bugs

## version 0.3.3 beta (The "Relapse of 0.2.3" Update) - Released 3/2/2017
* Updater fixed
* Minor UI changes

## version 0.3.2 beta (The More Verbosity Update) - Released 3/1/2017
* Adds verbosity to the updater
* Adds verbosity to setup
* Improves the updater some
* Minor UI improvements

## version 0.3.1 beta (The Updater Update) - Released 2/27/2017
* Adds an updater to PyWeather to check for the latest updates, and download them
* Revamps the extra options selection screen
* The dew point is now shown on the summary screen
* PyWeather has a double redundancy geolocator situation, Google first, Nominatim second, then a fail if nothing returns.
* Setup script checks for a connection to Google/Nominatim, and for the shutil library

## version 0.3 beta (The Setup Update) - Released 2/26/2017
* Adds a setup script that guides new users through the setup process
* Switches the geolocator from Nominatim to Google's geolocator (experimental)

## version 0.2.3 beta (The Bug Snatching Update) - Released 2/24/2017
* Fixes a bug in which detailed hourly data wouldn't show without turning verbosity on
* Fixes a bug in which the temp in detailed hourly data wouldn't iterate properly
* Fixes a bug in which PyWeather didn't stop at 30 iterations of detailed hourly data
* Fixes a semi-bug in which PyWeather wouldn't properly handle a missing API key

## version 0.2.2 beta (The Pressure Update) - Released 2/22/2017
* Adds current/pressure data to the current screen
* Fixes a bug in which users in the UK would see their 1 hour precip as -9999 in/-- cm (now corrects to 0.0 in/cm)

## version 0.2.1 beta (The Verbosity Update) - Released 2/22/2017
* Adds verbosity to newer functions of PyWeather. PyWeather loves verbosity.
* Replaces double verbosity with jsonVerbosity, as to not confuse people.
* Adds a check for snow data. We made sure people living near the equator don't feel sad when "Snow data" is always 0.0 inches.
* The loading bars are now turned off when verbosity is enabled.
* PyWeather can now accept numbers as inputs for different functions, to make life a little easier.
* Fixes some other issues.

## version 0.2 beta (The Initial Update) - Released 2/22/2017
* Initial build


# Very future versions
The upcoming dates here do come with uncertain release dates. Features might be added on the fly.

## version 0.6 beta - Should be released on 6/9/2017
* Adds alerts information to PyWeather - Should be finished by 5/22.
* Adds radar/satellite loops to PyWeather - Should be finished by 5/28.
* Adds the option to show release notes through the updater - Should be finished by 6/8.

## version 0.6.1 beta - Should be released on 6/22/2017
* Catches up the setup file with the latest config options - Should be finished by 6/19.
* Catches up config.py with the latest config options - Should be finished by 6/21.

## version 0.7 beta - Should be released on 7/13/2017
* Adds the ability to view weather from a PWS - Should be finished by 6/30.
* Adds alerts information to PyWeather, with the ability to turn it on and off. - Should be finished by 7/12.

## version 0.7.1 beta - Should be released on 7/20/2017
* Catches up the setup file with the latest config options - Should be finished by 7/14.
* Catches up config.py with the latest config options - Should be finished by 7/19.

## version 0.8 beta - Should be released on 8/26/2017
* Adds PyWeather's Quick Weather, a nice way to get the weather in a pinch. - Should be finished by 8/18.
* Adds hurricane/tide data to PyWeather. - Should be finished by 8/25.

## version 0.8.1 beta - Should be released on 8/30/2017
* Catches up config.py with the latest config options - Should be finished by 8/29.
