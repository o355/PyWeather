[![Twitter](https://img.shields.io/twitter/url/https/github.com/o355/pyweather.svg?style=social)](https://twitter.com/intent/tweet?text=Feel%20the%20urge%20to%20check%20your%20weather%20in%20a%20terminal?%20Check%20this%20out:%20%20&url=https%3A%2F%2Fgithub.com%2Fo355%2Fpyweather)

## Welcome to PyWeather (0.6.2 beta)!
Viewing the weather in a terminal has never been so much fun.

## Notices

### Indev code notice
Right now, there is an issue regarding the new spinner library conflicting with colorama's color styles that I use to color and brighten up text in PyWeather. It appears to only be occurring on Windows at the moment.

This doesn't affect PyWeather 0.6.2 beta, or any indev code from commit `bda1180` and earlier.

### Beta Notice
If you haven't noticed, PyWeather is in beta. This means that basic features should work fine, but more advanced and new features may not work.

If you do encounter bugs, make sure you report them on GitHub!

## Requirements
To run PyWeather, you'll need:
* A computer (Windows, OS X, most Linux distros)
* An internet connection (you have one if you're on here!)
* Python 3 (Python 3.5 and above is recommended) & PIP for Python 3
* ~5-10 MB of disk space

## Download/Setup
To download PyWeather, click the "Releases" button at the top of the page. Download the latest release, and unzip it.

If you'd rather, you can also download PyWeather with Git, using the following commands below.

```
git clone https://github.com/o355/pyweather.git ./pyweather
cd pyweather
git checkout 0.6.2-beta
```

After that, run `setup.py`, and the setup file will guide you through setting up PyWeather. After that, run `pyweather.py`, and enjoy the magic of PyWeather! It's as easy as that.

### Want the latest and greatest PyWeather nightly code?
You probably don't! Indev code is unstable, and could break from night to night. Indev code probably isn't for you, except if you really, really want the latest PyWeather features. Just note, updating your config is a pain whenever I add new config options, and I will sometimes leave broken code lying around.

If you want to, use the download button at the top of the page, and download into a .zip, and unzip the file. However, if you want indev code, it's strongly recommended you use Git.

Git users:
```
git clone https://github.com/o355/pyweather.git ./pyweather
cd pyweather
```

Afterwards, run the setup script, and things ~~might work~~ will work!

Make sure you run `git pull` on a nightly basis :)

## Disclaimer
PyWeather **should not** be used during severe weather conditions, and should not be used to tell the public about weather conditions during a severe weather event.

Please listen to local authorities, and your country's weather service (NWS in the US, EC in Canada) during a severe storm.

However, during times of non-severe weather, PyWeather is a fun way to check the weather.

## What's PyWeather?
PyWeather is a Python script that fetches the weather using Wunderground's API. I made PyWeather as a solution to a few things:
* The lack of script-based weather software that was coded in Python, and that relied on a decent enough API
* The long loading times (and loads of tracking/adverts) when visiting normal weather websites
* Having the ability to check my weather in a terminal.

As such, PyWeather was born. After 40,000 lines of code getting removed and added by 3 people, getting called a hacker a few times, and having a few teachers yell at me, this is what happened.

## Images and Demo
Just kidding, they're not here. I'll get around to capturing screencaps of 0.6.2 beta and running an asciinema demo soon.

## What features does PyWeather have?
PyWeather has lots of them, and the list is ever expanding. Here's the present feature list:
* Easy setups. The one-run setup script will install necessary libraries (only two (three on some setups) extra libraries are required to run PyWeather), guide you through obtaining an API key easily, and letting you configure PyWeather to your liking.
* On the subject of API keys, PyWeather uses Wunderground's API, meaning you'll get accurate weather information. I find Wunderground to be the perfect API for this project, as it has accurate weather information, and has a free developer tier.
* PyWeather can be configured easily, and has lots of options to configure. You can fine tune nearly 25 variables of how PyWeather works, across different scripts. The config file being used is a .ini file, and a descriptive configuration readme is also provided.
* PyWeather is simple to use. I've tried to make PyWeather appeal to both people who don't know what Python is, to people who know how to use software. Either way, you can use PyWeather easily.
* Lots of data types. All these data types as a matter of a fact!
	* Current information
	* Alerts information (US/EU only due to Wunderground's API limits)
	* 36-hour and 10-day hourly forecasts
	* 10-day forecasts
	* Almanac information
	* Astronomy (sunrise/sunset/moonrise/moonset + moon) information
	* Historical weather information, including hourly weather for a historical date
	* Radar information (experimental, for now)
	* Yesterday's weather
	* Tide data
	* Hurricane data
	* Webcam images - Coming in either 0.6.4 beta or 0.6.5 beta
	
* PyWeather is pretty modular. As I said earlier with the super-configurable config file, this also translates into modularity. PyWeather's features can be turned on and off at will.
* PyWeather has a built-in updater, provided you have git installed. I hope to eventually incorporate a universal "download the zip and unzip it" system down the road.
* PyWeather has a robust built-in debugger/logger. When turned on, it'll spam your console with verbosityness, or whatever that's called.
* PyWeather has a built-in geoIP service, which can detect your approximate location for even faster weather access. However, this may not be 100% accurate, especially on mobile networks. - Coming in 0.6.3 beta, the code is done!
* PyWeather supports the viewing of weather data for individual Wunderground Personal Weather Stations. You'll soon be able to also use PWSes as favorite locations! - Coming in 0.6.3 beta, the code is done!

In addition, these features will soon be coming to PyWeather:
* PyWeather will soon be able to store 5 favorite locations of yours, and you can easily call your favorite locations when you boot up PyWeather. - Coming in 0.6.3 beta
* PyWeather will soon be able to tell the user the closest city that a tropical system is to (up to 300km) - Coming in 0.6.3 beta
* PyWeather will soon be able to show you the 5 previous locations you entered. - Coming in 0.6.3 beta
* PyWeather will soon have a universal updater that's not reliant on Git. This should increase the reliability of the updater, and will let Windows users be able to have an automatic updater. - Coming in 0.6.4 beta

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
PyWeather's main data types are done, so now it's on to rapid development of new features for PyWeather.

This stage of PyWeather will last a few versions, and span at last 6 months.    

## Contributing


## Contributers
Thanks to these awesome people, they've helped out PyWeather by coding in bug fixes, new features, reporting bugs, and suggesting new stuff.

* ModoUnreal - Awesome contributor - Has made 8 pull requests, 5 of which were merged, and coded in 2 new features/1 data type
* creepersbane - Awesome contributor -  Has made 6 reports (3 of which required code changes), and 1 pull request.
* gsilvapt - Contributor - Has made 1 report, which required code changes
* DiSiqueira - Contributor - Has made 1 report.

## Sharing
I've, among others have poured in hundreds of hours into making PyWeather what it is, and I plan to spend hundreds of more hours refining PyWeather.

If you'd like, please consider telling your friends, social media followers, whomever about PyWeather. Every star, fork, and user keeps me motivated to keep working on PyWeather.
