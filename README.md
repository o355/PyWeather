## Welcome to PyWeather (0.5 beta)!
Viewing the weather in a terminal has never been so much fun.

## BETA DISCLAIMER:
Even though PyWeather is in beta, it's still in active development. While releases are somewhat stable milestones of PyWeather, and while I do a quick QA pass (doing a full QA would take HOURS to complete) for each release, 99% of the time, something will break. So, there's your warning. Of course, if something breaks, you should report the issue. That's a good idea.

## Why? Why should I check my weather in a terminal?
It's cooler. I think.

## Setup
I won't make you read the entire readme, so here's how to download PyWeather.

Download a release from the releases tab, unzip it, and run setup.py. The script will walk you through installing necessary libraries, instructions for retrieving an API key, letting you configure stuff, and making sure things work.

After that, double click pyweather.py, input a location, and that's it! No, really. That's actually it. No completed config files, none of that. setup.py, pyweather.py. Welcome to the world of simplicity! \ (•◡•) /

If you have Git, and you'd prefer to clone over PyWeather from Git, please read the page on "Installing from Git" in the Wiki.

## What's PyWeather?
PyWeather was a script I made, because I couldn't find anything that I wanted (from a terminal-based weather machine)

1. Not have a library (because arguments suck)
2. Have a simple way to set up the script/library (instead of browsing through about no setup documentation)
3. Have something that actually works!

Alas, PyWeather was born. It's a Python script that let's you view weather data (lots of it), is easy to set up, and it actually works.

## What kind of features are in PyWeather?
Want screenshots? https://imgur.com/a/n7L8B

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
I'm not a full time Python developer, and I'm not about to skip school because I want to work on Python projects. Between school, and the other projects I work on (and gaming, too!), I try my best to get in Python coding time, but it's not enough. Coding all of 0.5 beta's new features took 3 weeks, because of the limited time I had. So, I'm open to contributions.

Read over contributing.md in the .github folder to get a general rundown of how things work. After that, do your thing! Bug test, translate, submit some pull requests, you get the idea. Every contribution, bug report, etc, will get thanked in a release changelog!

If you have something to give constructive criticism about, please tell me! I'm all for constructive criticism, and learning through criticism.
