[Subscribe to the PyWeather Weekly Update, for all the latest in PyWeather news on a weekly basis!](https://owenthe.ninja/sign-pyweathers-weekly-newsletter/)

## Welcome to PyWeather (0.6.2 beta)!
Welcome to PyWeather, the fun way to check the weather in a terminal. Thanks for being here!

PyWeather is the culmination of thousands of hours of work poured into a silly little project that got more advanced over time.

I hope that you can enjoy PyWeather as much as I enjoy making PyWeather, so, let's get started!

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

Afterwards, run the setup script. However, the setup script might not be entirely reliable, especially once I've started working on a feature. I usually input setup file options last when making a feature.

Make sure you run `git pull` on a nightly basis :)

## Disclaimer
PyWeather **should not** be used during severe weather conditions, and should not be used to tell the public about weather conditions during a severe weather event.

Please listen to local authorities, and your country's weather service (NWS in the US, EC in Canada) during a severe storm.

However, during times of non-severe weather, PyWeather is a fun way to check the weather.

## Notices
Notices are important things you'll want to know about PyWeather.

### PyWeather 0.6.3 beta is now delayed
Right now, PyWeather 0.6.3 beta is officially delayed, and will most likely not be released on Friday.

FreeNAS 11 QA has just started. The only way 0.6.3 beta is getting released on December 1 (by 11:59pm EST) is if I find no bugs, and if I'm up to doing QA every day until Friday.

The estimated release time for PyWeather 0.6.3 beta is December 5, 2017.

### PyWeather's GitHub page will be discontinued whenever 0.6.3 beta is released
cool!

### Beta notice
If you haven't noticed, PyWeather is in beta. Basic features should work completely fine, but more advanced and newer features may not work 100% of the time.

## What's PyWeather?
PyWeather is a Python script that fetches the weather using Wunderground's API. I made PyWeather as a solution to a few things:
* The lack of script-based weather software that was coded in Python, and that relied on a decent enough API
* The long loading times (and loads of tracking/adverts) when visiting normal weather websites
* Having the ability to check my weather in a terminal.

As such, PyWeather was born. After 40,000 lines of code getting removed and added by 3 people, getting called a hacker a few times, and having a few teachers yell at me, this is what happened.

## Images and Demo
Just kidding, they're not here. I'll get around to capturing screencaps of 0.6.3 beta and running an asciinema demo soon.

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
	* Webcam images - Scrapped: Wunderground is removing this feature and the API on December 15, 2017.
	
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
Sadly, being a Python developer isn't my day job. I can't work on PyWeather for 8 hours a day, and about 45 hours a week. I have to go to school, do homework, sleep, eat, and other various things. I can't work on PyWeather for 5 hours afterschool, I'd be exhausted.

So, here's the deal. I can only work on PyWeather at max for 10 hours/week usually. At max, 6 hours during the workweek, and 4 hours on the weekend. This is usually lower, at around 3-5 hours/week. It's a lot, but it's not a lot.

I anticipate PyWeather 0.6.3 beta to consume about 50 hours to code in new features, but this might be even higher. QA will take another 10-15 hours. Given the usual 5 hours/week coding time, you can see why PyWeather releases take about 8-10 weeks to complete. Of course, these numbers are not set in stone, and will never be.

Here's the deal. I want faster releases as much as you do. I'd like releases to drop in 3-4 weeks while maintaining the code quality presented in 0.6.2 beta. If that could happen, I'd need more time for PyWeather. This is where you help.

If you don't know how to code Python, you can help report issues. I can't possibly catch every error with every setup. If you see a bug, report it! Every report improves PyWeather.

If you know some basic Python, try coding in some smaller features. As an example, adding prefetching yesterday's weather, caching yesterday's weather, and caching hurricane data are all features that are simple to add (you can easily copy/paste code and change a few variables around). Doing this helps tremendously, and lets me focus on more advanced features that take longer to code.

As another basic Python example, if you find a bug caused by a typo, a missing variable, etc, you're more than welcome to fix the bug.

If you know a solid chunk of Python, you might want to consider coding in more advanced features. However, if you're new to PyWeather, I'd suggest working on smaller features to get a feel for the program. If you're up to coding more advanced features, you'll want to contact me on Reddit, /u/therealo355. I'll give you a full explaination of what needs to get added.

To get a rundown of things, read the CONTRIBUTING.md file in the .github folder. Just know what by contributing code to PyWeather, you're helping to bring the delay between releases down, and reduces my time working a feature from multiple hours to >15 mins.

## Contributers
Thanks to these awesome people, they've helped out PyWeather by coding in bug fixes, new features, reporting bugs, and suggesting new stuff.

* ModoUnreal - Awesome contributor - Has made 10 pull requests, 5 of which were merged, and coded in 2 new features/1 data type
* creepersbane - Awesome contributor -  Has made 6 reports (3 of which required code changes), and 1 pull request.
* theletterandrew - Awesome contributor - Has made 2 reports, which required code changes, has made 1 pull requested which was merged, and coded in 1 new feature
* gsilvapt - Contributor - Has made 1 report, which required code changes
* DiSiqueira - Contributor - Has made 1 report.

## Sharing
I've, among others have poured in over 1,000 hours into making PyWeather what it is, and I plan to spend hundreds of more hours refining PyWeather.

If you'd like, please consider telling your friends, social media followers, whomever about PyWeather. Every star, fork, and user keeps me motivated to keep working on PyWeather.
