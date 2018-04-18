## Welcome to PyWeather (0.6.3 beta)!
Welcome to PyWeather, the fun way to check the weather in a terminal. Thanks for being here!

PyWeather is the culmination of thousands of hours of work poured into a silly little project that got more advanced over time.

I hope that you can enjoy PyWeather as much as I enjoy making PyWeather, so, let's get started!

## PyWeather Update - Mid April 2018:
Lots of changes from the last update. Here's what you need to know:
* I deleted the updater. It was getting way too ambitious and straying from the original goal.
* I'm fixing a lot of issues & enhancements that have been backlogged. Things should wrap up in June 2018.
* The updater will be rewritten last, and doing such should take around 4-8 weeks.
* PyWeather 1.0.0 will enter into QA in August 2018, and release in late September 2018.
* PyWeather will not go "multi-distro" (Windows edition, Mac edition, Snap edition) until PyWeather 1.0.2.
* PyWeather 1.0.1 will be released in early 2019, and will include code to deal with updating multiple types of PyWeather, the Termux fix, and other features.
* PyWeather 1.0.2 will be released in mid 2019, and will include code to configure the config file from a GUI, previous locations, radar location selecting on-the-fly, and other features. Creating a config the config file tool in purely a CLI is extremely hard, and would take a lot of time. It may come, one day.


## Requirements
To run PyWeather, you'll need:
* A computer (Windows, OS X, and most Linux distros)
* An internet connection
* Python 3 & PIP for Python 3 (download at https://python.org/downloads). For most Linux distros you can also download with the command line, given Python 3 isn't already included.
* ~5-10 MB of disk space

## Download/Setup
To download PyWeather, click the "Releases" button at the top of the page. Download the latest release, and unzip it.

If you'd rather, you can also download PyWeather with Git, using the following commands below.

```
git clone https://github.com/o355/pyweather.git ./pyweather
cd pyweather
git checkout 0.6.3-beta
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

Afterwards, run the setup script. However, the setup script might not be entirely reliable, especially once I've started working on a feature. I usually input setup file options last when making a feature.

Make sure you run `git pull` on a nightly basis :)

## Disclaimer
PyWeather **should not** be used during severe weather conditions, and should not be used to tell the public about weather conditions during a severe weather event.

Please listen to local authorities, and your country's weather service (NWS in the US, EC in Canada) during a severe storm.

However, during times of non-severe weather, PyWeather is a fun way to check the weather.

## Beta notice
If you haven't noticed, PyWeather is in beta. Basic features should work completely fine, but more advanced and newer features may not work 100% of the time.

If you do come across a bug, you should consider reporting the issue here. It'll help make PyWeather better when I know about the bug you're talking about.

## What's PyWeather?
PyWeather is a Python script that fetches the weather using Wunderground's API. I made PyWeather as a solution to a few things:
* The lack of script-based weather software that was coded in Python, and that relied on a decent enough API
* The long loading times (and loads of tracking/adverts) when visiting normal weather websites
* Having the ability to check my weather in a terminal.

As such, PyWeather was born. After 40,000 lines of code getting removed and added by 3 people, getting called a hacker a few times, and having a few teachers yell at me, this is what happened.

## Images and Demo
Asciinema demo: https://asciinema.org/a/XhvxO62rtXiruhs4Ra0LsBRT5

## What features does PyWeather have?
PyWeather has lots of them, and the list is ever expanding. Here's the present feature list:
* Easy setups. The one-run setup script will install necessary libraries (only two (three on some setups) extra libraries are required to run PyWeather), guide you through obtaining an API key easily, and letting you configure PyWeather to your liking.
* On the subject of API keys, PyWeather uses Wunderground's API, meaning you'll get accurate weather information. I find Wunderground to be the perfect API for this project, as it has accurate weather information, and has a free developer tier.
* PyWeather can be configured easily, and has lots of options to configure. You can fine tune nearly 40 variables of how PyWeather works, across different scripts. The config file being used is a .ini file, and a descriptive configuration readme is also provided.
* PyWeather is simple to use. I've tried to make PyWeather appeal to both people who don't know what Python is, to people who know how to use software. Either way, you can use PyWeather easily.
* Lots of data types. All these data types as a matter of a fact!
	* Current information
	* Alerts information (US/EU only due to Wunderground's API limits)
	* 36-hour and 10-day hourly forecasts
	* 10-day forecasts
	* Almanac information
	* Astronomy (sunrise/sunset/moonrise/moonset + moon) information
	* Historical weather information, including hourly weather for a historical date (PWSes are NOT supported at this time.)
	* Radar information (experimental, for now)
	* Yesterday's weather
	* Tide data
	* Hurricane data
	
* PyWeather is pretty modular. As I said earlier with the super-configurable config file, this also translates into modularity. PyWeather's features can be turned on and off at will.
* PyWeather has a built-in updater, provided you have git installed. I hope to eventually incorporate a universal "download the zip and unzip it" system down the road.
* PyWeather has a robust built-in debugger/logger. When turned on, it'll spam your console with verbosityness, or whatever that's called.
* PyWeather has a built-in geoIP service, which can detect your approximate location for even faster weather access. However, this may not be 100% accurate, especially on mobile networks.
* PyWeather supports the viewing of weather data for individual Wunderground Personal Weather Stations. You'll soon be able to also use PWSes as favorite locations!
* PyWeather can store 5 favorite locations of yours, and can easily call up those favorite locations when you boot up PyWeather.
* PyWeather can tell you which city a tropical storm is closest to, at a range of up to 300km.

In addition, these features will soon be coming to PyWeather:
* PyWeather will soon be able to show you the 5 previous locations you entered. - Coming in 0.6.4 beta
* PyWeather will soon have a universal updater that's not reliant on Git. This should increase the reliability of the updater, and will let Windows users be able to have an automatic updater. - Coming in 0.6.4 beta
* PyWeather will soon be able to show weather for airports worldwide. - Coming in 0.6.4 beta.

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
* PyWeather can be faster or slower than other weather apps. The favorite locations feature certainly improves initial loading speed, and can certainly be faster than AccuWeather or The Weather Channel, and even Wunderground's app.
* PyWeather can work in fringe coverage zones. PyWeather managed to load (albeit slowly) with just 1 bar of 1X service on Verizon.
* PyWeather uses monumentally less data than using native weather apps or visiting mobile websites, and has huge benefits on low-data mobile plans.

**Other advantages:**
* PyWeather is free open source software, uses completely open-source libraries, and PyWeather is licensed under GNU's GPL v3 license! Richard Stallman would approve.
* PyWeather can handly beat using websites and other services when on a slow internet connection. In PyWeather's default configuration, it only took 6 seconds for PyWeather to boot up on a simulated 28 kbps internet connection. In the real world, PyWeather was able to load in about 20-30 seconds on a fringe 1x connection.
* You'll look cool being that one person using a terminal to check your weather like it's the 80s. 
* PyWeather **doesn't track you!** I don't even know how many people are using PyWeather on a daily basis. I don't have code that "phones home", and I don't have code that relays back **any usage data**. However, do note that Wunderground does likely know your IP and basic system information about you from requesting their API, and the same goes for Google's geocoder that PyWeather uses. In the end, the amount of data you're giving to Wunderground and Google's geocoder by using PyWeather is much less than what you give to advertisers and trackers when visiting other weather sites.


## What's the current status of PyWeather?
PyWeather's main data types are done, so now it's on to rapid development of new features for PyWeather.

This stage of PyWeather will last a few versions, and span at last 6 months.    

## Contributing
Sadly, being a Python developer isn't my day job, and I can't manage to code for 8 hours a day. Thanks school...

In the end, I usually work on PyWeather for 1-2 hours daily, and that isn't a ton of time. Each new release usually takes at least 40 hours to code in new features, and at least another 10 hours to run QA.

It's a lot going solo and having limited time to find bugs, do QA, and code in new features. This all usually results in delayed releases, and having to wait 2-3 months for a new release of PyWeather.

However, you can help! Contributing to PyWeather is a great way to help with my limited time, shorten release waits, and help out with PyWeather. The best part? You don't need to know Python to get started!

Reporting bugs is always highly appreciated, as each bug report makes PyWeather more stable. Making a bug report is easy, click the Issues tab and follow the template provided.

If you know some Python, small pull requests are always highly appreciated, especially if they go along with a bug report. Even the smallest PRs are still highly appreciated.

If you'd like to take it up to the next level, you can code in entire features into PyWeather! It's best to contact me to arrange how the feature will be done, however.

You can get an incomplete rundown of contributing in the CONTRIBUTING.md file in the .github folder, including contact information.

If you have any questions about contributing, please don't hesitate to get in touch.

## Contributers
Thanks to these awesome people, they've helped out PyWeather by coding in bug fixes, new features, reporting bugs, and suggesting new stuff.

* ModoUnreal - Awesome contributor - Has made 10 pull requests, 5 of which were merged, and coded in 2 new features/1 data type
* creepersbane - Awesome contributor -  Has made 6 reports (3 of which required code changes), and 1 pull request.
* theletterandrew - Awesome contributor - Has made 2 reports, which required code changes, has made 1 pull requested which was merged, and coded in 1 new feature
* gsilvapt - Contributor - Has made 1 report, which required code changes
* DiSiqueira - Contributor - Has made 1 report.

## Sharing
I've, among others have poured in hundreds of hours into making PyWeather what it is, and I plan to spend hundreds of more hours refining PyWeather.

If you'd like, please consider telling your friends, social media followers, whomever about PyWeather. Every star, fork, and user keeps me motivated to keep working on PyWeather.
