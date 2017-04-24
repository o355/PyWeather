## Welcome to PyWeather (0.5.1 beta)!
Viewing the weather in a terminal has never been so much fun.

## Yet another development notice (oh boy)
PyWeather 0.5.2 is on it's way, but if you have a quick glance at the changelog, everything changed.

I'm basically tired of adding bells and whistles, I want to push myself further, and the pending list of "rewrite prints" and all that fun stuff was making it so that I would play KSP (great game, by the way) or Cities:Skylines (make sure you have a supercomputer handy) instead of coding.

Code cleanup was meant to occur later down the road, and I'll add the bells and whistles in other releases. I want to really focus on getting real features in PyWeather.

Right now, PyWeather 0.5.2 beta is still slated to drop in Early May. 0.6 development will start afterwards.

## Why? Why should I check my weather in a terminal?
It's cooler. I think.

## Setup
I won't make you read the entire readme, so here's how to download PyWeather.

Download a release from the releases tab, unzip it, and run setup.py. The script will walk you through installing necessary libraries, instructions for retrieving an API key, letting you configure stuff, and making sure things work.

After that, double click pyweather.py, input a location, and that's it! No, really. That's actually it. No completed config files, none of that. setup.py, pyweather.py. Welcome to the world of simplicity! \ (•◡•) /

**Sometimes, the setup script will have a tendancy to fail in regards to installing geocoder. See the wiki page "Setup" for more information.**

If you have Git, and you'd prefer to clone over PyWeather from Git, please read the page on "Installing from Git" in the Wiki.

## What's PyWeather?
PyWeather was a script I made, because I couldn't find anything that I wanted (from a terminal-based weather machine)

1. Not have a library (because arguments suck)
2. Have a simple way to set up the script/library (instead of browsing through about no setup documentation)
3. Have something that actually works!

Alas, PyWeather was born. It's a Python script that let's you view weather data (lots of it), is easy to set up, and it actually works.

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

But that's just half the story. I've also baked in loads of other features, too!
* Color! Lots of color!
* The setup script!
* Verbosity for debugging!
* An updater (it's basic. Quite basic)
* Support for traceback printing!
* A super-configurable config file!
* No arguments!
* API key backups!
* A pretty simple to use UI!

Oh, I should mention that PyWeather is faster than going to Wunderground, is ad-free (duh), and gets loads more data (that's pretty easy to view), and does it all without confusing you.

Need mobile support? You could get Termux, but that doesn't work (tested it). The best option right now is to spin up a Linux box with SSH and PyWeather, and log into it using Termius (iPhone/Android).

## Contributing
I'm not a full time Python developer. I have school, I work on other projects, and have other hobbies, too (you can thank my love for KSP).

While I try to get in around 60 minutes of coding time a day, 80% of the time, I can't. Thanks school. Thanks. And, sometimes, I just need a break from coding Python, to focus on doing other projects, or spending time with family.

Contributing is the best way to help me out with the limited time I have to code PyWeather. Be it bug hunting, submitting feature ideas, coding parts of PyWeather, or telling me about something I can do better, I'm all for it.

Read over CONTRIBUTING.md in the .github folder to get a general rundown of how things work.

## Sharing
I've poured hundreds of hours into making PyWeather, and have thousands more to pour in. It would be awesome if you could help spread the word about PyWeather, and to let the courage ones know that they can check weather in their terminal.

It's simple. Share the GitHub link. Done.
