# Contributing to PyWeather

When contributing to PyWeather, please follow the Code of Conduct, and how you can contribute in a meaningful way to PyWeather.

Please read through this document carefully. If you have any questions, please open an issue with your question.

## Reporting Issuesh
As a solo developer, I can't catch every single issue in PyWeather. To meaningfully report an issue, please follow these guidelines for your different types of reports.

### Bug Reports
To make a successful bug report, be sure to make sure that your bug doesn't contain the following:
* If you don't see a total Python error (usually a Traceback), don't report it. With these bugs, PyWeather has a safety net, and will tell you what you might be doing wrong. However, if you are 100% sure that you aren't doing anything wrong, you may report the issue. (you can also take out the safety net yourself, so you get a pure traceback)
* Make sure you can reproduce the bug 100% of the time, or when reproducing the bug, it happens on a steady interval. Basically, no "this bug happened once and never happened again in weeks" reports. Make sure the bug you're reporting can be reproduced 100% of the time, or happens on a steady interval.
* Turn on verbosity in the code (>0.3.3), or in the config file ( < 0.4), and see if anything looks odd.
* When reporting the issue, make sure to include every detail you can. The more details, the easier I can find the bug. When reporting a bug, you'll at least need to include an error output, and steps to reproduce the bug. Information about your OS, something like a video (I'm more visual), and any other details you want to include will help me fix the bug faster.
* Please, for the love of anything, if you have an error log/console output that's 20+ lines, please post it to a site like Pastebin.
* Don't share personal information in issues. If in a video, or detailed output, you input a location, try to not make it your own city, unless the issue happens ONLY in your city. (encoding error, etc.)

If you'd like to take a look at what an optimal report looks like: https://github.com/o355/pyweather/issues/2

A report should at least have the following information included.
* The error you got
* How the error occurred
* Your OS/Python version
* Some sort of output from the Python traceback

It's important to note that if you launch PyWeather through double-clicking, most of the time, the window will close on it's own. Try your best to open a terminal, and get the traceback/error information. If you can't, give me steps to reproduce the bug, and I'll try my best.

If you don't include the bare minimum of details in a report, or you report an issue that contains something that shouldn't be contained, I'll close the report. I'm not rude, I just need more information to help me understand your issue.

### Enhancement Reports
I can't come up with new ideas 24/7, so you can help me create new ideas for PyWeather. If you're a coder, or not a coder, you can help come up with new ideas on improving PyWeather.

Before you report your enhancement (that makes no sense), please make sure that your enhancement doesn't contain the following:
* An enhancement that I'm scheduled to release (check the Wiki -> Todo list).
* An enhancement I can't possibly code in. I'm limited to Wunderground's API, so don't expect me to accept your enhancement to solve quantum physics.
* Little detail. 

If your enhancement report doesn't contain this, I'll probably close/reject it. As I said above, I'm not a mean guy, I need details before I can pull the trigger on adding your idea in.

Instead, your report should really contain the following:
* A general TL;DR of your enhancement, and a descriptive description of your enhancement.
* Some sort of flow chart/mock up for your enhancement. I'm a visual guy, and I don't care if it's poorly drawn. If I can get what you're trying to portray, that's cool.
* If you feel so inclined, submit a pull request!

However, even with what I could code in, these are some things that will never happen.
* A .exe version of PyWeather
* A PyWeather library (I don't know how to make libraries)

I don't have any examples, but if I get you, it'll get tagged on the todo list. 

## Pull Requests
Why GitHub exists. Pull requests. I'm always happy to accept a pull request, but, before you do that, you'll need to make sure you follow these conditions.
* Don't do the versioning yourself. You handle the coding, I handle the versioning.
* Make sure your PR follows the style guide, available to view in the Wiki.
* Make sure your code updates all necessary parts of PyWeather. If you add a new function (Alerts), make sure you fully integrate it into the UI.
* When creating an addon for PyWeather (alerts, etc.), make sure it's integrated with PyWeather's structure (in that nice loop).

### Code Plagarism
I take plagarism seriously, and it annoys me when others mostly plagarize other code. I've done it, but I've had the courage to change variable names, at least.

PyWeather was born from an article, which was the basic framework of PW.

**and i realized...oh...it's 12:24am.**
