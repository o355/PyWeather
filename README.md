## Welcome to PyWeather (0.6 beta)!
Viewing the weather in a terminal has never been so much fun.

## Development notice:
PyWeather progress is slow. Am I getting bored of developing Python? No. Am I busy? Yes.

PyWeather 0.6 beta is now scheduled for release on May 27, and is more of an under-the-hood release. Yes, some cool new features are here, but the backbone of PyWeather has been significantly changed.

## Download/Setup
You can download PyWeather by visiting the releases tab, and getting the latest zip.

You can also use git to download PyWeather, using the commands below.

```
git clone https://github.com/o355/pyweather.git
git checkout 0.5.2.1 beta (if you want indev code, don't perform this command)
```
After that, run setup.py, and the setup file will guide you through setting up PyWeather. After that, run pyweather.py, and enjoy the magic of PyWeather! It's as easy as that.

## What's PyWeather?
PyWeather was an idea born out of a need for a few things in a terminal weather script.
1. Accurate data (No OpenWeatherMap)
2. Lots, and lots of data.
3. Simplicity. No arguments, no libraries, no hard and confusing setups.

I couldn't find a script that like on GitHub, so I made my own. And look what it turned into...

## A brief history
For PyWeather 0.0.1 beta, I decided to use a premade library from Dark Sky to use to fetch weather. This was before PyWeather went public (or else I'd violate Dark Sky's ToS! woo!)

By PyWeather 0.0.3 beta? I guess, I had current data. Forecast data was next and woah! Raw data? No one likes that!

For PyWeather 0.1 beta? Yeah, okay, sure, I began using Wunderground's API to parse raw .jsons. I mean, look at PyWeather 0.2 beta! Look how far it's come!

## What kind of features are in PyWeather?
Want screenshots? https://imgur.com/a/n7L8B

*asciinema demo goes here*

(the almanac wasn't included, as I actually found a bug when taking the screenshots)

Even though PyWeather is in beta, it can presently do a lot. Here's what you can easily see in PyWeather.
* A nice "summary" screen for a location
* Detailed current information
* The 36-hour hourly forecast
* The 10 day hourly forecast
* The 10 day forecast
* The almanac
* Sunrise/sunset/moonrise/moonset/moon data
* Historical data

Through the magic of typing, these features will eventually work their way into PyWeather!
* Alerts data - Coming in 0.6 beta
* Radar/satellite data (experimental, for now) - Coming in 0.6.1 beta
* "Yesterday's weather" - I don't have a delorean - Coming in 0.6.2 beta
* Tide data - Coming in 0.7 beta
* Hurricane data - Coming in 0.7 beta
* PWS mode/data - Coming in 0.7.1 beta

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

Need mobile support? You could get Termux, but that doesn't work (tested it). The best option right now is to spin up a Linux box with SSH and PyWeather, and log into it using Termius (iPhone/Android).

PyWeather also has a few easter eggs.

## Contributing
I'm not a full time Python developer. I have school, I work on other projects, and have other hobbies, too (you can thank my love for KSP).

While I try to get in around 60 minutes of coding time a day, 80% of the time, I can't. Thanks school. Thanks. And, sometimes, I just need a break from coding Python, to focus on doing other projects, or spending time with family.

Contributing is the best way to help me out with the limited time I have to code PyWeather. Be it bug hunting, submitting feature ideas, coding parts of PyWeather, or telling me about something I can do better, I'm all for it.

Read over CONTRIBUTING.md in the .github folder to get a general rundown of how things work.

## Sharing
I've poured hundreds of hours into making PyWeather, and have thousands more to pour in. It would be awesome if you could help spread the word about PyWeather, and to let the courage ones know that they can check weather in their terminal.

It's simple. Share the GitHub link. Done.
