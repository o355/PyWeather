## Welcome to PyWeather (0.5 beta)!
Viewing the weather in a terminal has never been so much fun.

## BETA DISCLAIMER:
Even though PyWeather is in beta, it's still in active development. While releases are somewhat stable milestones of PyWeather, things may or may not work. If you update from GitHub, I may push updates that entirely break PyWeather, so please, take caution!

## Why?
Because I'd rather check my weather in a terminal. Unlike 99.98% of humans.

## Setup
I won't make you read the entire readme, so here's how to download PyWeather.

Simple. Download a release from the releases tab, unzip it, and run setup.py. The script will walk you through installing necessary libraries, instructions for retrieving an API key, and making sure things run smooth.

After that, double click termweather.py, input a location, and that's it! No, really. That's actually it. No completed config files, none of that. setup.py, termweather.py. Welcome to the world of simplicity! \ (•◡•) /


If you have Git, and you'd prefer to clone over PyWeather from Git, you've got your options.

Doing `git clone https://github.com/o355/pyweather.git` will clone PyWeather into your current folder. From testing, doing this should put PyWeather into a folder called "pyweather", but I'm not 100% sure. Use the option `--depth=1` as a precaution.

If you want to have the latest stable version (0.5), you can checkout to the release branch, by doing `git checkout v0.5-beta`.

If you want to live on the bleeding edge, nothing is required on your part, you'll have the latest updates as I code them (at the risk of things breaking). I don't do betas/RCs, as that's just a huge waste of time on my end. Doing `git pull` will let you get the latest updates, and I push updates Monday-Saturday, for the most part.

The only thing that will probably annoy you when doing `git pull` to check for new updates, you'll likely need to stash your config.ini file, if you made changes. This will get solved in 0.5.1 beta, when I pull config.ini from the master branch.

If PyWeather shows that a new update is available, starting with 0.5.1 beta, PyWeather will show you the branch tag in the updater, and you can just as well do `git pull`, and `git checkout`, and add the branch tag that was shown.

## What's PyWeather?
PyWeather is a script I made to accomplish a few things.

1. Make it easy for people to view the weather in Python.
2. Make a fast way for people to view the weather, instead of having to wait for apps on their phone launch.
3. Make a weather script that combines simplicity, and advanced features.
4. Have a mostly modular weather script, that'll easily let you turn on/off features.

I couldn't find any of this. None. Alas, PyWeather was born.

PyWeather is simple, it'll read you the forecast, and the current weather, but it's also easy to set up. Really easy. Yet, it contains lots of data for reading the almanac, previous weather, whatever. Plus, if you have a PWS from Wunderground, PyWeather (not presently) will let you view the weather for your PWS. Easy style.

PyWeather is pretty modular, and has some advanced configuration options. Using the config file, you can turn on/off options easily, and make PyWeather your own. It isn't completely modular, but maybe that'll come.

### What kind of data does PyWeather show?

Oh, and PyWeather is faster than opening up a web browser, going to the website, and letting it load. Seriously. I check my weather in PyWeather now.

Pro tip: If you're on mobile, and have a Linux box with SSH, get the Termius app (iPhone/Android). A) It's the best SSH/Telnet app for mobile, B) It's fast at launching/connecting, so you can check weather on your phone in more-or-less the same amount of time. A full guide to configuring SSH (for Ubuntu/Debian because I've only used those OSes) is in the Wiki.

## Contributing
I'm not a full time Python developer, and I can't skip school (I need to learn). Between school, my other life projects (e.g. administering web servers, and creating other servers), and gaming on the weekends, and sleeping (I wish I didn't have to sleep), I don't have tons of Python development time. While during the week, I try to squeeze in 30-60 minutes of coding time a day, it isn't enough. That's why you can go ahead, and contribute to PyWeather.

Read over contributing.md in the .github folder to get a general rundown of how things work. After that, do your thing! Bug test, translate, submit some pull requests, you get the idea. Every contribution, bug report, etc, will get thanked in a release changelog!
