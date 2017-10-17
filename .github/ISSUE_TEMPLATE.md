Hi! Thanks for your interest in contributing to PyWeather, by reporting an issue.

It's simply impossible for me to catch every bug in PyWeather, so you can help! Before you report an issue, run down this to-do list.
* Make sure PyWeather is up-to-date. I do manage to catch a fair amount of bugs in PyWeather releases.
* Make sure your issue isn't on the list of known issues. The page is available in the wiki, [here](https://github.com/o355/PyWeather/wiki/Known-Issues).
* Make sure you've properly set up PyWeather. Basically, this is running setup.py and going through all dialogs.
* If your issue can be replicated, turn on tracebacks in the config file for the script it occurs in. To do this, head into your config file, and enable tracebacks on all options (from False to True). A traceback is extremely helpful in troubleshooting a bug!
* You may report indev code, but you'll need to follow a few extra steps below:

**Reporting indev code:**
* Do not, and I repeat, **do not** report issues about a config issue at start. Config issues are **always** tested during QA, so there's no need to report. However, you may report an issue if PyWeather is 1-2 weeks off from the predicted release dates.
* Please avoid reporting issues about code that isn't done. Let's take this example: I'm 100% done with feature 1, but 50% done with feature 2. If you found a bug in feature 1, report it! If you found a bug in feature 2, please don't report it until it's finished.

In the end, if you're unsure about the requirements above, report the issue anyways.

Done with the list? Here's what you'll need for a report.
* The full traceback provided by Python, if applicable.
* System information (OS, Python version). You can get your Python version by typing in `python3` or `python`, and copying the first two lines outputted. For your OS, a description like `Windows 10`, or `Ubuntu 16.04` works.
* A description detailing the issue. Add as much detail as you can to your description, as the better the description, the faster I can figure out why the bug is occurring.

You can go the extra mile by adding this stuff to your report.
* Potential solutions. If you can do Python 3 coding, make a pull request, even if it's just one line of code!
* Testing where the issue occurs. Sometimes bugs only occur on a certain OS.
* A link to an XKCD comic (comics under 1800)

If you'd like to keep this template in your report, that's completely fine. Otherwise, report the issue!
