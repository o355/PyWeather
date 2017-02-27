## Welcome to PyWeather (0.3 beta)!
A simple-to-use, but advanced way to view the weather with Python, in a terminal. And it's now in beta!

## BETA DISCLAIMER:
Even though PyWeather is in beta, it's still in active development. While releases are more stable milestones of PyWeather, there will certainly be unfinished/rough parts of PyWeather, even in releases. Make sure you check for the latest releases, since as the betas go on, PyWeather will be less unfinished/rough.

For those updating from GitHub directly, I may push a stable/unstable/broken build of PyWeather, so take heed.

## Why?
Because I'd rather check my weather in a terminal. Unlike 99.98% of humans.

## Setup
I won't make you read the entire readme, so here's how to download PyWeather.

Simple. Download a release from the releases tab, unzip it, and run setup.py. The script will walk you through installing necessary libraries, instructions for retrieving an API key, and making sure things run smooth.

After that, double click pyweather.py, input a location, and that's it! No, really. That's actually it. No completed config files, none of that. setup.py, pyweather.py. Welcome to the world of simplicity! \ (•◡•) /

***For users using a command-line only OS, make sure you're in the directory you want PyWeather to be stored in, and then run `git clone https://github.com/o355/pyweather.git`. Run the scripts using `python3 setup.py / python3 pyweather.py`. Simple. Effortless.***

## What's PyWeather?
PyWeather is a script that, as it says, shows the weather. In addition, PyWeather is pretty, includes a setup script for guidance on setting up PyWeather, and PyWeather provides detailed weather information, along with the short and simple version.

PyWeather can show you the conditions outside your window, how things may look outside your window in a few hours (and with detail!), and how things may look outside your window in a few days (with detail, of course!). PyWeather will soon be able to show alerts information, almanac data, and loads of other data from Wunderground, and all of this in a terminal. (~˘▾˘)~

## Why not use the dozens of other programs named PyWeather, etc?
Great question! What I generally found after scanning GitHub was three things.

One, most weather programs were a moduble, and not a script. Those programs had you issuing commands (e.g. pyweather -f NYC -d 3, etc), with arguments, and could get confusing fast.

Two, some weather programs used the infamously unreliable OpenWeatherMap. While a great service, when I used it, it provided somewhat inaccurate forecasts, for few locations in the US. 

Three, most, if not all these programs did not have simple instructions on installing necessary libraries (or the module itself), obtaining an API key, you get the point. As an example, you have a PyPI module, in which it gives you instructions to install through PIP. However, the module's documentation doesn't reference how you install PIP.

Lastly, I found some programs that were outdated, hardly worked, and weren't maintained.

(but I did find some other cool programs)

I set out to solve these issues by doing things a little differently. I'm using Wunderground, but it's a script, and PyWeather has a simple solution to getting itself set up. There isn't a pip install -r requirements.txt, or "go install xyz with pip". No. None of that. Those days are over.

I tried to design PyWeather (with my A+ not art skills) to focus on serving you what's important quickly, but still easily letting you dig into whatever data I could get from Wunderground, for more advanced users.

## Are there any TRUE advantages over PyWeather than going to Google/Wunderground?
Sure! PyWeather is about 3-4x faster than pulling up a web browser, and going to Wunderground. It's a little slower when it compares to going to Google (or your preferred search engine), but fetches more data. Best of all, PyWeather is ad-free, and doesn't track you. PyWeather just wants to serve you the weather.

## What's still coming?
Lots! While I'm grabbing the most important of data, there's still a lot of features coming, as seen on the To-Do list page.

## I'm having errors! Please help!
**It's important to note that errors are not fully implemented into PyWeather.**

Please refer to the Errors part of the Wiki.

## Contributing
Since I'm a solo developer, in which I'm forced to devote 33% of my life to school, 30% of my life to sleeping, and 10-15% of my life to doing other things (like homework, etc), that leaves about ~15-20% of my time to freely develop (akin to 2-3 hours). If you want to lend a helping hand to PyWeather, I encourage you to take on something from the todo list (preferrably, not the first thing on the list), and submit a pull request. ( ﾟヮﾟ)

If you don't know how to code Python, bug test the program! Test every aspect of the program, and report issues if you find something. Doing such will also get yourself eternally thanked for your contribution. 

I'll soon open the door to Wiki contributing/translations, but not yet. I still need to figure out the logistics of that.
