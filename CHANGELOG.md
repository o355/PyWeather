# PyWeather changelog

Quick note: While in beta, commits are not counted as versions. When I decide to push a release, I push a release. There will also be a running changelog for the in-development version, so I'm not remembering every single change I made in the version.

And for some reason, I like typing up 2-3 future versions in detail, because I found out that Eclipse supports markdown files.

## version 0.5 beta (The Back to the Future Update) - To be released between 3/15-3/21
* The naming comes from a combination of adding history (back), and 10-day future (future). Sorry.
* Adds historical weather information to PyWeather
* Adds 10-day hourly weather to PyWeather (you'll hit enter 40 times!...by default)
* Adds a separate config.py program, so you can configure every option in PyWeather (including verbosity!)
* Adds the ability to turn off the "enter to continue" things in the 10-day/hourly forecasts
* Adds the ability to set the interval in which the "enter to continue" will appear
* Reworks the config file some, sections are now where they need to be (aka verbosity has it's own section)
* Adds 0 easter eggs.

## version 0.4.2 beta - To be released 3/9/2017
* Adds an autoupdater to PyWeather
* Adds the ability to configure the config file in the setup script
* Adds verbosity (of course it did) to all scripts (yay)
* Adds the ability to "back up" your API key, and a script to do it (it's very simple...)
* The build number for this version of PyWeather is 42.
* Adds 0 easter eggs.

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
