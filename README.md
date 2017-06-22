
## Welcome to PyWeather (0.6.0.1 beta)!
Viewing the weather in a terminal has never been so much fun.

## Download/Setup
You can download PyWeather by visiting the releases tab, and getting the latest zip.

You can also use git to download PyWeather, using the commands below.

```
git clone https://github.com/o355/pyweather.git
git checkout 0.6.0.1-beta
```

If you'd prefer to live on the bleeding edge of PyWeather updates, run these commands.

```
git clone https://github.com/o355/pyweather.git
```

(please note: indev code is subject to work on some nights, and not on other nights. indev code is also indev code, so there will be bugs!)

After that, run `setup.py`, and the setup file will guide you through setting up PyWeather. After that, run `pyweather.py`, and enjoy the magic of PyWeather! It's as easy as that.

## What's PyWeather?
PyWeather is a Python script that fetches the weather using Wunderground's API. I made PyWeather as a solution to a few things:
* The lack of script-based weather software that was coded in Python, and that relied on a decent enough API
* The long loading times (and loads of tracking/adverts) when visiting normal weather websites
* Having the ability to check my weather in a terminal.

As such, PyWeather was born. After 30,000 lines of code removed and added by 3 people, all this hard work turned into this.

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
	
* In addition, you'll soon be able to view these data types soon:
	* Radar/satellite information (experimental for now. the developer of the GUI library I'm using is fixing it)
	* Yesterday's weather
	* Webcam images (a big maybe on animated videos)
	* Tide data
	* Hurricane data
	* Some form of a historical planner
* PyWeather is pretty modular. As I said earlier with the super-configurable config file, this also translates into modularity. PyWeather's features can be turned on and off at will.
* PyWeather has a built-in updater, provided you have git installed. I hope to eventually incorporate a universal "download the zip and unzip it" system down the road.
* PyWeather has a robust built-in debugger/logger. When turned on, it'll spam your console with verbosityness, or whatever that's called.
* PyWeather has colors. I made the program colorful.

## What's the current status of PyWeather?
PyWeather is presently in a rapid-development beta.

Until the end of September 2017, I expect to continue adding new features to PyWeather at a rapid pace. Until this point, I'll be attempting to use every part of Wunderground's API, and implement it into PyWeather.

## Contributing
Since I don't have all the time in the world to work on PyWeather, contributing is a great way to help with PyWeather.

Bug reports, pull requests, feature suggestions, all that fun stuff can help me out with my limited time I have to code PyWeather. Read over CONTRIBUTING.md in the .github folder, to see how things work.

## Staying up to date
From time-to-time, I'll release development news on how PyWeather is coming along on my website, here: https://owenthe.ninja/category/pyweather-news/

You'll find news on how new versions of PyWeather are coming along, among other things. It's the best way to stay updated on what's going on with PyWeather.

## Sharing
I've, among others have poured in hundreds of hours into making PyWeather what it is, and I plan to spend hundreds of more hours refining PyWeather.

If you'd like, please consider telling your friends, social media followers, whomever about PyWeather. It'll only motivate me more to keep working on PyWeather.
