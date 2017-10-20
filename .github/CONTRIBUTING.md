# Contributing to PyWeather

**Warning: This document is undergoing renovation. Please excuse our apperance.**

Hey, thanks for your interest in contributing to PyWeather. If you don't taking 2 minutes of your day to read this, you'll get the run-down on how things work.

Oh, and quick side note, I'm (o355) am a GitHub novice. This is a learning experience for me, and this will adapt.

## A quick blurb about PyWeather & contributing
PyWeather has been the result of thousands of hours of worked poured in by people who want to help PyWeather be the best it can be. I apprecipate every single person who reports an issue, makes a pull request, and in general helps PyWeather in any shape or form.

Contrary to popular belief, you don't need to know how to code Python to contribute to PyWeather. Reporting bugs is tremendously helpful in contributing to PyWeather, or even making a pull request with one line of code helps out PyWeather. 

When contributing to PyWeather, start small. Reporting bugs and issues, OS compatibility reports, or even suggesting enhancements is a great way to get started in contributing to PyWeather. If you feel more comfortable reading code and making pull requests, you can without a doubt code in a small feature in PyWeather that's relevant, or you can quickly fix a bug you found. If you feel really comfortable, try coding in a larger feature. Please make sure to contact me first, however.

## Contacting me
If you need to ask me any questions about PyWeather without using GitHub, the best place to do so is on Reddit. I'll usually respond within 48 hours, since I get a notification on my phone whenever I get new Reddit mail.

My reddit username is `therealo355`. I have about 3100 karma if that helps to verify my account.

If you'd rather do email, you can email the PyWeather project email at `pyweather <at> owenthe <dot> ninja`. I usually don't respond as quickly to that email, so a response may take up to a few weeks. 

## Code of Conduct
When contributing to PyWeather, please make sure to follow the code of conduct, available here: https://github.com/o355/PyWeather/blob/master/CODE_OF_CONDUCT.md

## Bug reports
An easy, yet substantial way to contribute to PyWeather is in the form of bug reports. When you create an issue, you'll see an issue template, and this is the general format on how issues are created and formatted. This document will expand on what should ideally be in a report.

Just note, if at any time you are confused about if you should report an issue or not, just report the issue. I'd much rather have you report the issue and for me to fix a potential bug, versus not knowing about it.

### Doing the to-do list
It's really important to run down this list to save your time, and my time from unnecessary reports. This to-do list also includes steps to help your report be the best it can be.

### Reporting indev code
Reporting indev code is ok, under certain circumstances. As mentioned in the issue template, you'll not want to report config errors. At every PyWeather QA, this is automatically tested about 30x on 6 platforms. However, if PyWeather is close to release, and you find a config bug, you'll want to report a config error.

In addition, please don't make a bug report on a feature that's incomplete. However, feel free to report bugs on complete features.

### Necessary things for a report
When making a report, you'll want a full traceback (if applicable), System information, a detailed description, and some other extra information. Below I'll expand on what necessary things are needed for a report.

### A full traceback
A full traceback looks something like this:
```
Traceback (most recent call last):
  File "<stdin">, line 1, in <module>
ValueError: could not convert string to float: 'hello'
```
A traceback does not look like this:
```
Some horrible thing occurred that prevented PyWeather from loading!
I can't remember the actual error messages in PyWeather and I'm too lazy to reference one.
Press enter to exit.
```

You'll want a full traceback in your error report. In PyWeather, you'll deal with 2 types of tracebacks. Catched errors at a potential point of failure, or a random traceback that randomly exits PyWeather.

For catched errors, a traceback will be outputted, given you turn on tracebacks in the config file. Turning on tracebacks can be done in the setup script, or by making the `tracebacks` option in the `[TRACEBACKS]` section in the config file `True`.

It's important to know that you shouldn't report *some* catched errors. As an example...
* Reporting the geocoder rate limit error - Don't report this
* Reporting a config error when you've properly configured your config - Report this
* Reporting missing data for Wunderground at your location (and it's caught with a message like "no data") - Don't report this
* Reporting odd data without any message of bad data - Report this

If you also enable verbosity, please don't report non-critical errors. Most of them are due to bad conversions of data, and that actually helps to catch bad data.

However, for random tracebacks, report these! As soon as your PyWeather randomly quits, report the traceback. This is easy if you launch PyWeather in a terminal, but tricky if you double-click PyWeather. 

If you end up double-clicking to launch PyWeather, you'll want to immediately run PyWeather in a terminal (OS X - Launch `Terminal`, `cd pyweather` (or whereever PyWeather is, starts in home folder), `python3 pyweather.py`; Windows - File manager, go into PyWeather's folder, File, Open in Command Prompt (Windows 10 1703 and newer PowerShell), `python pyweather.py`; Linux - You know what to do), do exactly what you did, and get the traceback, and report the issue.

### System Information
In a report, you'll want what OS you're on, and the Python version you have.

To get the version you have, remember what version is installed on your box, or enter `python3` (sometimes `python` for python 3) into a terminal, and put down the Python version you have. Examples:

`Python 3` - Doesn't help. PyWeather runs on Python 3.
`Python 3.6` - Good, but having a specific version is better.
`Python 3.6.3` - Great! That's what I need.

Please note: If you're running Python 3.6, and just 3.6 (not 3.6.x), please report your Python version as `3.6.0`.

## Enhancements

## Enhancement suggestions

## Pull requests

## Wiki

## Translating

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
