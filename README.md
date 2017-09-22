
## Welcome to PyWeather (0.6.1 beta)!
Viewing the weather in a terminal has never been so much fun.

## Notices
I had to start separating notices. Yay!

### 0.6.2 beta status update
PyWeather 0.6.2 beta is coming along nicely, however it has been delayed (again). ETA for release is 9/27.

### Python 3.7 compatibility notice
PyWeather 0.6.2 beta will not be quality assured using the newly released Python 3.7, but 0.6.3 beta will get tested with Python 3.7. I can't assure that you won't run into bugs using Python 3.7 on 0.6.2 beta.

I'm not about to delay PyWeather AGAIN due to Python 3.7 coming out. Sorry!

### Raspbian 9/Debian 9 compatibility notice
PyWeather 0.6.2 beta will not be quality assured using Raspbian 9 (and 8 for that matter), and I cannot certify that PyWeather works on Debian Stretch, or other distros based on Debian 9.

### Beta notice
If you haven't noticed, PyWeather is in beta. At this point, essential features mostly work.

However, newer or more complex features may not work as expected. It's also up to you to report bugs that you find, as it makes every new PyWeather release better.

## Download/Setup
The instructions for downloading PyWeather are somewhat awkward just for 0.6.1 beta. Basically, the geocoder that I use had an issue on Mac OS X, in which it could only run with the scheme set to http. This issue has been fixed in 0.6.2 beta, and I coded in automatic detection for what scheme your OS can run.

For PyWeather 0.6.1 beta, the default release has the geocoder set to run in http mode. There is another release, that changes the geocoder to run in https mode. For 95% of users, using the https release should work, but might not work for some users. If you run into geocoder issues in the setup process (given a working internet connection), you'll have to use the http release.

**Please note: In the http release, I didn't change the setup's geocoder to run in http mode. Getting a geocoder error during setup (given a working internet connection) 99% of the time just means that the geocoder couldn't run with https enabled.**

You can download the standard HTTP and HTTPS releases of PyWeather in the releases tab.

If you want to use Git to download the HTTP release of PyWeather (the https tag does NOT contain the code to run in https mode), use the commands below:

```
git clone https://github.com/o355/pyweather.git --depth=1
cd pyweather
git checkout 0.6.1-beta
```

Both the http and https version of PyWeather will be able to update to 0.6.2 beta when the time comes, and I've configured the config updater to automatically detect what mode the geocoder can operate on your OS.

If you want the latest and greatest bleeding edge code on a nightly basis, use this code:

```
git clone https://github.com/o355/pyweather.git --depth=`
cd pyweather
```

Make sure you run `git pull` on a nightly basis :)

**Please note: Only use the indev code if you really want the latest features. However, indev code is indev code, and I'll sometimes push broken code that will basically break PyWeather, or push out incomplete features.**


After that, run `setup.py`, and the setup file will guide you through setting up PyWeather. After that, run `pyweather.py`, and enjoy the magic of PyWeather! It's as easy as that.

## Disclaimer
PyWeather **should not** be used during severe weather conditions, and should not be used to tell the public about weather conditions during a severe weather event.

Please listen to local authorities, and your country's weather service (NWS in the US, EC in Canada) during a severe storm.

I cannot be held liable for injury or death caused in part or directly from using PyWeather. **There is no warranty associated with PyWeather. Use PyWeather at your own risk.**

TL;DR You can't sue me if you die from using PyWeather. It's in the license!

## What's PyWeather?
PyWeather is a Python script that fetches the weather using Wunderground's API. I made PyWeather as a solution to a few things:
* The lack of script-based weather software that was coded in Python, and that relied on a decent enough API
* The long loading times (and loads of tracking/adverts) when visiting normal weather websites
* Having the ability to check my weather in a terminal.

As such, PyWeather was born. After 30,000 lines of code removed and added by 3 people, all this hard work turned into this.

## Images and Demo
Just kidding, they're not here. I'll get around to capturing screencaps of 0.6.1 beta and running an asciinema demo soon.

## What features does PyWeather have?
PyWeather has lots of them, and the list is ever expanding. Here's the present feature list:
* Easy setups. The one-run setup script will install necessary libraries (only two (three on some setups) extra libraries are required to run PyWeather), guide you through obtaining an API key easily, and letting you configure PyWeather to your liking.
* On the subject of API keys, PyWeather uses Wunderground's API, meaning you'll get accurate weather information. I find Wunderground to be the perfect API for this project, as it has accurate weather information, and has a free developer tier.
* PyWeather can be configured easily, and has lots of options to configure. You can fine tune nearly 25 variables of how PyWeather works, across different scripts. The config file being used is a .ini file, and a descriptive configuration readme is also provided.
* PyWeather is simple to use. I've tried to make PyWeather appeal to both people who don't know what Python is, to people who know how to use software. Either way, you can use PyWeather easily.
* Lots of data types. As of PyWeather 0.6 beta, these data types can be viewed:
	* Current information
	* Alerts information (US/EU only due to Wunderground's API limits)
	* 36-hour and 10-day hourly forecasts
	* 10-day forecasts
	* Almanac information
	* Astronomy (sunrise/sunset/moonrise/moonset + moon) information
	* Historical weather information, including hourly weather for a historical date
	* Radar information (experimental, for now)
	
* In addition, you'll soon be able to view these data types soon:
	* Yesterday's weather - Coming in 0.6.2 beta (the code is done if you'd like to try!)
	* Tide data - Coming in 0.6.2 beta (the code is done if you'd like to try!)
	* Hurricane data - Coming in 0.6.2 beta
	
* PyWeather is pretty modular. As I said earlier with the super-configurable config file, this also translates into modularity. PyWeather's features can be turned on and off at will.
* PyWeather has a built-in updater, provided you have git installed. I hope to eventually incorporate a universal "download the zip and unzip it" system down the road.
* PyWeather has a robust built-in debugger/logger. When turned on, it'll spam your console with verbosityness, or whatever that's called.
* PyWeather has colors. I made the program colorful.

In addition, these features will soon be coming to PyWeather:
* PyWeather will soon be able to store 5 favorite locations of yours, and you can easily call your favorite locations when you boot up PyWeather. - Coming in 0.6.3 beta
* PyWeather will soon be able to tell the user the closest city that a tropical system is to (up to 300km) - Coming in 0.6.3 beta
* PyWeather will soon be able to show you the 5 previous locations you entered. - Coming in either 0.6.3 beta or 0.6.4 beta
* PyWeather will soon be able to automatically detect your location, so you can get the weather information for your location faster. Sadly, this may not be 100% accurate, as a GeoIP service would have to be used, since there isn't a known way to get a device's location using Python. - Coming in 0.6.4 beta
* PyWeather will soon be able to show weather data for individual Wunderground PWSes (Personal Weather Stations). This should be useful for those who run their own PWS. Along with this, you'll be able to add PWSes to your favorite locations. - Coming in 0.7 beta
* PyWeather will soon have a universal updater that's not reliant on Git. This should increase the reliability of the updater, and will let Windows users be able to have an automatic updater. - Coming in 0.7.1 beta
* PyWeather will soon have rounding enabled on all data type variables, to fix a major bug on some platforms where rounding issues occur on. - Coming sometime soon.

## Why actually use PyWeather over Wunderground, or other apps?
PyWeather has lots of advantages over using websites on your desktop, or even weather apps on mobile (PyWeather is compatible with Termux for Android, and other SSH apps of course)

**On a desktop:**
* If you have a desktop shortcut to the homepage of wunderground.com, or weather.com, PyWeather (given a shortcut on your desktop) can be faster than visiting Wunderground or weather.com, given you don't have the shortcut point to a specific location. However, when I code in favorite locations, PyWeather begins to compete with direct shortcuts on your desktop.
* PyWeather has no ads (or annoying articles), so you get distraction-free weather.
* PyWeather has the essential data types that other sites have, and has easy access to other hidden (or non-existant) features on other sites.
* PyWeather "gets to the point". It just shows you the weather, nothing else.

**On a phone:**
* PyWeather when paired with Termux, or an SSH client uses A LOT less battery (my GS7 reported Wunderground's app using 4% of battery power/hour!)
* PyWeather can easily save mobile data with default settings versus other weather apps, since ads aren't being loaded. If you more carefully tune PyWeather's settings, you can save even more data.
* PyWeather may be slower than opening apps, (Termux users, if you pay $1.99 for the widgets, it begins to compete with weather apps, and will get better with favorite locations coming soon) but PyWeather fetches data that most apps don't include (like the almanac, yesterday's weather, etc).

**Other advantages:**
* PyWeather is free open source software, uses completely open-source libraries, and PyWeather is licensed under GNU's GPL v3 license! Richard Stallman would approve.
* You'll look cool being that one person using a terminal to check your weather like it's the 80s. 
* PyWeather **doesn't track you!** I don't even know how many people are using PyWeather on a daily basis. I don't have code that "phones home", and I don't have code that relays back **any usage data**. However, do note that Wunderground does likely know your IP and basic system information about you from requesting their API, and the same goes for Google's geocoder that PyWeather uses. In the end, the amount of data you're giving to Wunderground and Google's geocoder by using PyWeather is much less than what you give to advertisers and trackers when visiting other weather sites.


## What's the current status of PyWeather?
PyWeather is presently in a rapid-development beta.

Until the end of 2017, I expect to continue adding new features to PyWeather at a rapid pace. Until this point, I'll be attempting to use every part of Wunderground's API, and implement it into PyWeather.

## Contributing
Since I don't have all the time in the world to work on PyWeather, contributing is a great way to help with PyWeather.

Bug reports, pull requests, feature suggestions, all that fun stuff can help me out with my limited time I have to code PyWeather. Read over CONTRIBUTING.md in the .github folder, to see how things work.

## Sharing
I've, among others have poured in hundreds of hours into making PyWeather what it is, and I plan to spend hundreds of more hours refining PyWeather.

If you'd like, please consider telling your friends, social media followers, whomever about PyWeather. Every star, fork, and user keeps me motivated to keep working on PyWeather.
