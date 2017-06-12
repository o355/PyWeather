
## Welcome to PyWeather (0.6.0.1 beta)!
Viewing the weather in a terminal has never been so much fun.

## Development notice:
I'll be taking a ~3 week hiatus from PyWeather development, thanks to tests. I really wanted to squeak out 0.6 beta before I took a hiatus.

I'll be back at the end of mid-June for serious PyWeather development. Until then, expect sporadic development.

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

After that, run setup.py, and the setup file will guide you through setting up PyWeather. After that, run pyweather.py, and enjoy the magic of PyWeather! It's as easy as that.

## What's PyWeather?
PyWeather was an idea born out of a need for a few things in a terminal weather script.
1. No arguments. Most of the stuff I came across on GitHub were command-line utilities, but I wanted a script!
2. Accurate weather data. Some scripts use OpenWeatherMap, which in past experience, was inaccurate.
3. Simplicity! Most of the scripts I found were made with the open-mind that you knew how to acquire a Wunderground API key, and follow the tedious steps to get it (or something like that).

I couldn't find a script that like on GitHub, so I made my own. After typing and deleting around 28,000 lines of code, plus 343 lines from contributors, this is what happened. 

## What kind of features are in PyWeather?
Want screenshots? https://imgur.com/a/n7L8B - I'll update the screenshots for 0.6 beta soon!

An asciinema demo will come...eventually.

Even though PyWeather is in beta, it can presently do a lot. Here's what you can easily see in PyWeather.
* A nice "summary" screen for a location
* Detailed current information
* The 36-hour hourly forecast
* The 10 day hourly forecast
* The 10 day forecast
* The almanac
* Sunrise/sunset/moonrise/moonset/moon data
* Historical data
* Alerts data

Through the magic of typing, these features will eventually work their way into PyWeather.
* Radar/satellite data (experimental, for now) - Coming in 0.6.1 beta
* "Yesterday's weather" - I don't have a delorean - Coming in 0.6.2 beta
* Tide data - Coming in 0.7 beta
* Hurricane data - Coming in 0.7 beta
* PWS mode/data - Coming in 0.7.1 beta
* Raw tide data - Coming in 0.7.2 beta
* Webcams - Coming in 0.8 beta
* A historical "planner" - Coming in 0.8.1 beta - With these release, I would have effectively used every feature there is in the Wunderground API.

But that's just half the story. I've also baked in loads of other features, too!
* An easy setup! You can set PyWeather up (including getting an API key!) easily!
* Colors! Lots of em!
* A super configurable config file!
* Debugging tools!
* PyWeather is mostly modular! You can turn on/off features at will.
* An updater!
* No arguments! It's a script!
* A bunch of other cool features!

Oh, I should mention that PyWeather is faster than going to Wunderground, is ad-free (duh), and gets loads more data (that's pretty easy to view), and does it all without confusing you.

Need mobile support? Check out the non-existant but soon-to-be page in the Wiki!

PyWeather also has a few easter eggs.

## Contributing
I'm not a full time Python developer. I have school, I work on other projects, and have other hobbies, too (you can thank my love for KSP).

While I try to get in around 60 minutes of coding time a day, 80% of the time, I can't. Thanks school. Thanks. And, sometimes, I just need a break from coding Python, to focus on doing other projects, or spending time with family.

Contributing is the best way to help me out with the limited time I have to code PyWeather. Be it bug hunting, submitting feature ideas, coding parts of PyWeather, or telling me about something I can do better, I'm all for it.

Read over CONTRIBUTING.md in the .github folder to get a general rundown of how things work.

## Sharing
PyWeather is basically a solo project, done in my free time. I've been working on PyWeather for nearly 6 months (as of late May 2017), and I've poured in at least 200 hours, if not more into PyWeather.

If you like this project, it'd be great if you could share PyWeather! New stars and forks, along with issues and pull requests will continue to motivate me to improve PyWeather as time goes on.
