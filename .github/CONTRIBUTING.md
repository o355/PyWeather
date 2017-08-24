# Contributing to PyWeather

Hey, thanks for your interest in contributing to PyWeather. If you don't taking 2 minutes of your day to read this, you'll get the run-down on how things work.

Oh, and quick side note, I'm (o355) am a GitHub novice. This is a learning experience for me, and this will adapt.

## Code of Conduct
When contributing to PyWeather, please make sure to follow the code of conduct, available here: https://github.com/o355/PyWeather/blob/master/CODE_OF_CONDUCT.md

## Issues
When reporting an issue, make sure that you include lots of details. Details that contribute to a successful report are as follows:

### OS version
Make sure you detail your OS version. 

Pro-tip: Linux users: Use `uname -a` to get your kernel version.

`Windows 10 | Ubuntu 16.04 | Debian 8.7` - Is acceptable, but doesn't provide too much detail. Instead, try for:

`Windows 10 Pro version 1703 | Ubuntu Server 16.04.2 LTS | Debian 8.7 amd64` - Is good, but you can even try for more detail:

`Windows 10 Pro version 1703 build 15063.296 | Ubuntu Server 16.04.2 LTS, kernel 4.4.0-78-generic` - Is amazing!

### Python version
Make sure you detail what Python version you have.

Doing such is easy enough, open a Python 3 shell using the command `python` or `python3` in a command prompt. Detailed version info is in the first two lines of when you start up a Python 3 shell.

You'll want to paste something like this into your report:

```
Python 3.5.2 (default, Nov 17 2016, 17:05:23)
[GCC 5.4.0 20160609] on linux
```

### A full traceback
Providing a full traceback, if possible, will 90% of the time let me find the issue quickly. If the bug can be replicated, go into the `config.ini` file, located in the `storage` folder, and make your `[TRACEBACK]` section look like the following:

```
[TRACEBACK]
tracebacks = True
setup_tracebacks = True
updater_tracebacks = True
configdefault_tracebacks = True
```

### If it's needed, the location that causes the issue
Sometimes, bugs are location-based. If you need to share your location for a bug report, please do so in a way that respects your privacy.

`123 5th Avenue, New York, NY` is not acceptable, as that is violating your privacy.

`5th Avenue, New York, NY` is not acceptable, as that is still technically violating your privacy.

`New York, NY` is acceptable, that's a general location.

If you make a report with a location, once I notice the issue, I'll immediately censor the location provided. If you insist on making a bug report, please contact me, at pyweather at owenthe dot ninja. 

Along with that, a full description is always nice to have, along with potential solutions.

I'll usually get back to reports within 24-48 hours, sometimes less. I have an IFTTT trigger set up on my phone to alert me whenever a new issue is created.

## Enhancement suggestions
If you'd like to suggest an enhancement, you'll generally want these things:

### A full description of the enhancement
Just saying "add 1 year ago weather" doesn't help. Instead, try for something along the lines of this:

"I'd like to suggest adding 1 year ago weather in the similar fashion of yesterday's weather. A user would be able to see the weather 1 year ago, look at the daily summary, and then dive into detailed hourly information. The 1 year ago weather would be determined based on year."

### Add suggestions for parts of the implementation
This isn't required, but you can help bring your idea to fruition by suggesting how I should code your suggestion in.

Something like this is what you should shoot for:

"For finding the one year ago date, try and grab the current year, date, and month off of the user's box. The date and month should have leading 0s for the API. Make the year a int, then subtract by 1. Combine the year, date, month into a string like this:

YEARMONTHDATE, and then make an API request.

When making the enhancement, for now, add the prefix [ENHANCEMENT] to the report's name. I'll most likely get back to enhancement reports in 24-48 hours, and I'll see if I can code it in.

## OS compatibility reports
If you saw the wiki page, and would like to report that an OS works with PyWeather, you'll want to do some testing, and add some things into your report, to make the OS you're reporting officially work with PyWeather.

### When testing, test most basic functions.
Run the setup script, set it up as a real user. Launch PyWeather, go into all the options, and then launch the other scripts and see if they work, too.

### When making the report, detail the OS that PyWeather is compatible with.
As the title says.

### Add (a) screenshot(s) (or better, a video/asciinema) of PyWeather working.
Make sure you launch into a generic location when recording or taking (a) screenshot(s) when you do so. If you record the set up process, in which you input your API key, you should really change it afterwards.

### Add the [OS REPORT] prefix to your alert name.
Shabang.

As stated above, I'll get back to you within 24-48 hours, and add it to the wiki, if you have all your detail. If you miss out on some detail, I'll notify you.

## Pull Requests
I'm not the best at pull requests, and I sometimes mess up PyWeather (thanks ModoUnreal for bearing with my git stupidity). However, try to follow these general "recommendations" for working on new PyWeather features.

* Submit your PR when you're done with your code. I update Git like a ninja (get it, my domain name is owenthe dot ninja), so try your best to not submit your PR until you're done.
* I have a to-do list of things to do. If you have enough free time on your hands, you can code in those features. Make sure it isn't a feature that I'll be working on soon (e.x. don't code in a feature that i'll code for 0.6.2 beta when I'm working on 0.6.2 beta).
* You can easily base your code from other PyWeather functions. A solid amount of code in PyWeather is copy and paste, just with changes. If you go this method, you can forgo adding logger functionality.

However, please keep in mind these requirements when coding in something for PyWeather:
* Make sure that your code addition has a logger, if necessary. Changing a variable? Log it. Loggers begin with `logger`.
* If you are adding a new option to PyWeather, set the menu number as something <15. I'll do another commit which brings the menu item to the proper number.
* I'll handle logistics, you code.
* If worse comes to worse, and we both mess up, you do agree that I can copy & paste in your code from a PR, and "accept" your PR. I'll still give you credit and all that fun stuff.

In return, you'll get credit for your work, in the changelog.

## Wiki

## Rules
Please have a look at the CODE_OF_CONDUCT.md file located in the master branch for details on the code of conduct.

## Translating PyWeather
Translating PyWeather is not available yet.

## Contributing Rewards/Acknowledgements
In return for contributing to PyWeather, I'll acknowledge how much of a cool person you are through acknowledgements and contributing levels. The levels are as follows:

* Contributor: You've reported at least 1 issue that required code changes, and/or made 1 pull request.
* Awesome Contributor: You've reported 3 issues that required code changes, and/or made 3 pull requests.
* Ultra Contributor: You've reported 10 issues that required code changes, and/or made 6 pull requests.
* Is PyWeather your side job? You've reported 20 issues that required code changes, and/or made 12 pull requests.
* Bug Snatcher: You've reported 40 issues that required code changes.
* Senior Reporter: You've reported 60 issues that required code changes.
* PR master: You've made 16 pull requests.
* PR legend: You've made 24 pull requests.
* Secondary developer: ~15% of PyWeather's codebase is code that you've provided.
* Main developer: ~25% of PyWeather's codebase is code that you've provided.
* Feature developer: You've coded in at least 3 features into PyWeather.
* Data type developer: You've coded in at least 3 data types into PyWeather.

Contributors are acknowledged in the about page of PyWeather (updated each new release), and are updated on an as-needed basis in the readme file.

Anything that a contributor has done (report an issue, code in a new feature) will be given full acknowldegement in the changelog for each new release.
