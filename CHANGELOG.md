# PyWeather changelog
**Note: The changelog being used for tracking PyWeather progress has been retiredish. Please check the projects tab of PyWeather for progress on the next versions of PyWeather.**

## version 0.6.4 beta - Should be released in late January 2018:
* Adds the ability to see the weather for airports
* Adds the ability to see and call the weather for previously looked up locations
* Adds the ability to see historical data for PWSes
* Adds the ability to see the weather on Mars!
* Adds further refinement to favorite locations (Instead of your location input being the shown favorite location, it'll be the official location given by Google's geocoder)
* Adds the ability to change your radar image size on the fly
* Adds the brand new Universal PyWeather Updater, making it a ton easier to update to new versions of PyWeather
* Improves the UI of the configuration updater. New configuration options are put on 2 lines of text.
* Lowers the default iterations for data down to 4 to prevent scrolling.
* Adds the ability for configsetup to run an automatic geocoder scheme
* Improves the disabling of having a custom geocoder API key, even though the scheme is set to HTTP (custom geocoder keys only work with HTTPS.
* Improves the UI in the setup file to not have overflowing lines of text.
* Adds an attribution to Meteoalarm for EU-based alerts
* Adds better exiting at multiple input prompts throughout PyWeather

## version 0.6.3 beta - Released on 12/3/2017:
**NEW FEATURES/REMOVALS:**
* Adds a nearby location feature to hurricane data (300km out)
* Will push the API key validation code up further thanks to new features.
* Adding a much nicer progress indicator.
* Adds the ability to prefetch yesterday's weather at boot, and a caching system. (thanks to @ModoUnreal for partially coding this in!)
* Adds the ability to view your current location through a GeoIP service
* Adds the ability to view data through a PWS at boot.
* Adds the ability to have up to 5 favorite locations.
* Adds the ability to manually define a Google Maps API key
* Much better error catching for the config file (thanks to @TheLetterAndrew for coding this in!)
* Adds the ability to view the chance of precipitation on the forecast page.
* Adding the ability to show cache timings.
* The ability to see pressure and visibility data has been added to historical hourly & yesterday hourly information. 
* Minor UI changes.

**BUG FIXES:**
* Fixed multiple major bugs regarding invalid historical summary data & historical hourly data
* Fixed multiple major bugs regarding invalid yesterday summary data & yesterday hourly data
* Fixed a bug where if you didn't have API key validation on, PyWeather validated your API key, and vice versa.
* Fixed potential bugs where PyWeather wouldn't properly display precip information for forecast data - The algorithm was reworked.
* Fixed a bug where if you manually flagged all data types to refresh, hurricane data wouldn't be refreshed.
* Fixed a minor bug where if the summary section couldn't be added in the setup file, the print statement indicated that the cache section wasn't added.
* Fixed a bug where PyWeather didn't catch bad visibility, UV index, and humidity data for current weather
* Fixed a bug where the visibility in km on the yesterday's summary screen read as "kph".
* Fixed a minor bug where on yesterday's weather hourly data, the degree symbol was placed too far right by 1 character.
* Fixed a potential bug where missing data on yesterday's weather would cause a crash.
* Fixed a potential bug where if almanac data is prefetched, it wouldn't display when viewing it in detail, and PyWeather would crash.
* Fixed a minor bug where on the historical weather summary, total precipitation data in mm had a "mb" label.
* Fixed a minor bug where historical hourly data wouldn't break when the current iterations equaled the total iterations.
* Fixed a minor bug where PyWeather wouldn't catch bad humidity data for current conditions.
* Fixed a bug where configsetup script set the default geocoder scheme to https, which caused issues on platforms that don't support the geocoder running in the HTTPS scheme.

**OTHER CHANGES:**
* The Git Updater has been completely removed, as it's been unreliable. A universal updater will be introduced later in time.
* The configupdate file will now properly catch a bad section error (not a plain except)

**KNOWN ISSUES:**
* Tide data may not be fully available for some cities. I'm working on a fix for 0.6.4 beta.
* Attempting to exit out of historical weather is bugged. I'm also working on a fix for 0.6.4 beta.
* Hurricanes in hurricane data will show up twice. I've already contacted Wunderground about the issue, but they haven't responded back. A fix is coming in 0.6.4 beta.
* A custom geocoder key won't work without an https-enabled scheme. There is a temporary fix in 0.6.3 beta, but a more comprehensive fix will be coming in 0.6.4 beta.
* The configsetup script will default to an http scheme regardless of if your OS is https compatible or not. A more comprehensive fix will be coming in 0.6.4 beta.

## version 0.6.2 beta - Released on 9/24/2017
**NEW FEATURES/REMOVALS**
* Adds the ability to view yesterday's weather. - Thanks to @ModoUnreal for coding this in!
* Adds the ability to view hurricane data in PyWeather.
* Adds the ability to view tide data in PyWeather.
* Adds the manual configuration of 3-day and 10-day hourly cache times. - Thanks to @ModoUnreal for coding this in!
* Fixes a major issue with a geocoder scheme issue. PyWeather can automatically select a geocoder scheme, depending on your OS.
* Adds the ability to input decimal numbers into cache times during setup.
* Adds the ability to manually define a version you're upgrading to in the configupdate script in the event your versioncheck file is gone.
* Removed the configdefault script. The configsetup script has taken it's place now.
* Added up-to-date and no matching version messages in the configupdate script.
* Minor UI changes.

**BUG FIXES**
* Fixed a critical bug where if geopy wasn't installed before setup, Pyweather Setup would install geocoder INSTEAD of geopy, and throw an error.
* Fixed a bug where I forgot to globalize variables relating to emptying the radar cache.
* Fixed a bug where if your configuration file failed to load, cache times were set insanely high (5 seconds for alert data, etc)
* Fixed a bug where if you entered nothing for the backup key directory, an error would occur. Thanks to @creepersbane for reporting the error!
* Fixed a bug where if your configuration file failed to load, enter to continue prompts were disabled by default.
* Fixed a bug where the last step in the setup process (bypassing radar confirmation) didn't have proper else catching, and if a "yes" or "no" was entered, PyWeather setup would crash.
* Fixed a bug where you weren't able to exit out of the summary screen when viewing historical data.
* Fixed a bug where wind chill data in celsius in historical hourly displayed "kph" instead of a degree C symbol.
* Fixed a bug where the 10 day forecast cache expire time was running off of the hourly cache time.
* Fixed a bug where PyWeather wouldn't properly catch no moonrise data, resulting in a crash.
* Fixed a bug where if alerts data wasn't getting prefetched at boot, when detailed alerts data was called up PyWeather would crash.
* Fixed a bug where if you had 10-day hourly prefetch enabled at boot, when you viewed detailed 10-day hourly information PyWeather would crash.
* Fixed a potential bug where the configupdate script might not at all work when you manually edit the version info file. It now searches the file instead of an exact match.
* Fixed a bug where yesterday precipitation data could say "T" on the summary screen. A data check has been added.
* Fixed a bug where if some almanac data wasn't available, PyWeather would crash - Thanks to @ModoUnreal for reporting the error!
* Fixed a "bug" where if you had no connection to the updater at boot with it enabled, PyWeather would exit instead of continue Thanks to @creepersbane for reporting the error!
* Fixed a potential bug where proper code to catch invalid sunrise/sunset data was not implemented.

**OTHER CHANGES**
* ModoUnreal is now an awesome contributor!
* The setup script will now forcefully write out a versioninfo file at the top of the script.

## version 0.6.1 beta - Released on 7/31/2017
**NEW FEATURES/REMOVALS**
* Adds caching and refreshing to PyWeather. After a user-defined amount of time, a cache will expire for certain components of PyWeather, prompting a re-fetch of data. A manual refresh option will also get added, in which a flag is enabled to refresh the cache.
* Removed the dependency on geocoder, and by extension, removed the unnecessary reverse geocoder, and 
* Added the dependency of appJar.
* Loading times have been increased by about 0.2 seconds, due to the removal of the unnecessary second geocoder.
* Added the last-resort option when installing Colorama in the setup file, and a warning to all last-resort options.
* Adds an experimental radar to PyWeather.
* Adds error checking for imports on all scripts (non-standard libraries)
* Adds a progress indicator during setup configuration.
* Adds requests as a necessary library to setup.
* PyWeather Setup now validates your API key after you input it (and after the backup)
* PyWeather Setup will now update PIP packages with user approval.
* Geopy's scheme was changed to HTTP due to issues on OS X.
* Adds wind direction data to historical hourly.
* Removed the keybackup script.
* Minor UI changes.

**BUG FIXES**
* Fixed a major bug where the PyWeather Git updater wouldn't, uh, fully update.
* Fixed a bug where configsetup's directory checking wasn't 100% compatible with Windows.
* Fixed a bug where if the sunrise/sunset/moonrise/moonset hour was 0, PyWeather wasn't correcting it to a 12.
* Fixed a bug where if you entered a weird name to check the weather for, an encoding error would occur.
* Fixed a major bug where alerts wouldn't iterate, due to a non-defined config variable.
* Fixed a super tiny bug where a logger.info statement would not print in the setup file, unless Geopy was not installed.
* Fixed a bug in the setup file, in which if sections were already added to a config file without the configprovisioned flag, PyWeather Setup would not run.
* Fixed a bug in which custom directories really didn't work for the backup API key in the setup script
* Fixed a bug in which PyWeather wasn't properly parsing wind data shown as "Variable". UI changes have been made to accommodate this data type
* Fixed many bugs in which PyWeather was unable to properly catch errors when parsing historical data, and wrong dates.

**OTHER CHANGES**
* Geocoder dependency was removed, as noted above.
* The PIP installer during setup now uses urllib, which is unreliable. An option was added for a user to manually download necessary files.

## version 0.6.0.1 beta - Released on 5/29/2017
* Fixes a critical bug where a user couldn't provision their config file when they first downloaded the program.
* Fixes a critical bug where if a user attempted to use the configuration defaults program, the program didn't properly reset their config file.

## version 0.6 beta (The "Alerts to change the PyWeather backbone" Update) - Released on 5/28/2017
The clever title comes from the addition of alerts, and the gigantic backbone update too.

**NEW FEATURES/REMOVALS**
* Adds an "About" page to PyWeather.
* Adds alerts information to PyWeather, including (of course) the ability to turn it on and off.
* Adds the option to show release notes through the updater.
* Adds the option to view when the next release should be dropping through the updater.
* The "What would you like to do now" menu will get switched to only a number-based input.
* Fixes for config stashing in regards to Git updating. There's a lot to do, so get a system where we can effectively update a user's config file for a lot of scenarios.
* Removed support for overriding version information. It won't work with the new updater when it comes to config updating.
* Adds error catching for a bad geolocator fetch in pyweather.py/setup.py.
* Minor UI changes.

**BUG FIXES**
* Fixed a bug where if your backup API key couldn't be found, key validation was entirely skipped. I guess this was intentional, but now your primary key is still validated, but if your backup key couldn't be loaded at first boot, it'll stop before trying to validate a non-existent backup key. 
* Fixed a bug where when running configdefault.py, "PYWEATHER BOOT/validateapikey" wasn't reset to it's default value.
* Fixed a bug where if you enabled update checking at boot, PyWeather would crash from an old JSON loading definition.
* Fixed a bug where in historical hourly information, if you had the iteration counter on, it'd print in red.


## version 0.5.2.1 beta - Released on 4/30/2017
* Fixes a bug in which if validating your API key wasn't enabled, a variable wasn't defined, crashing PyWeather at boot.

## version 0.5.2 beta - Released on 4/30/2017
**NEW FEATURES/REMOVALS**
* Adds the raw traceback output in keybackup.py
* Changes the error message when the config file fails to load (the potential for the file to not get loaded)
* Removes the error catching of a bad config file load, it's useless.
* Adds a fallback to doing a system "sudo pip3 install library" if a library is found not to be installed. (in setup)
* Added a warning to users using Python 3.0-3.4 in the setup script, it's known to cause errors.
* Switches the "here's the full traceback" thing from logger.error to a pure printout.
* Adds version checking in the setup script, while trying not to be Windows 10.
* Adds a warning to users on Python 3.5/3.6 and running Linux about Geocoder failing during install.
* Adds the ability to fetch all JSON files using a backup key, if the primary one fails. This is accomplished by using the first JSON fetch as a test, and seeing if a KeyError occurs. If a KeyError occurs, the backup key will be substituted.
* Adds the option to cancel a pending shell command in PyWeather setup (Ctrl+C), and increases the time until the command is executed to 5 seconds.
* Adds the ability to update with git through the command line.
* Adds back the iteration detections for historical hourly. This is accomplished by doing a for loop before user data is shown, and calculating the total amount of iterations that need to be done.
* Adds the ability to override the version number defined in PyWeather. This was done for debugging reasons.
* PyWeather is now using requests to get the API .json files, in favor of better reliability.
* Made error messages less vague. Hurray?
* Minor UI changes.

**BUG FIXES**
* Fixed a bug in which if tracebacks were enabled in the updater, the tracebacks wouldn't print properly, as such, producing a traceback. Huh.
* Fixed a bug in all scripts that involved issuing HTTP requests. This is now improved with user strings, and should prevent random 400 errors.

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
* Minor UI changes.

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
* Minor UI changes.

## version 0.4.1 beta - Released 3/8/2017
* Fixes a bug in which detailed sun/moon data wouldn't get shown
* API calls are more efficient
* Adds a "Press enter to continue" across PyWeather for users who view PW by double-clicking.
* Fully implements almanac on the summary screen
* Fully implements the config
* Fixes a variety of smaller bugs
* Minor UI changes

## version 0.4 beta (The Astronomy Update) - Released 3/4/2017
* Adds the almanac to PyWeather
* Adds sunrise/sunset data to PyWeather
* Mostly adds a config file to PyWeather
* Adds a separate updater to update PyWeather
* Minor UI changes
* Fixed bugs

## version 0.3.3 beta (The "Relapse of 0.2.3" Update) - Released 3/2/2017
* Updater fixed
* Minor UI changes

## version 0.3.2 beta (The More Verbosity Update) - Released 3/1/2017
* Adds verbosity to the updater
* Adds verbosity to setup
* Improves the updater some
* Minor UI changes

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
