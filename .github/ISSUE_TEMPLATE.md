Hi! Thanks for your interest in contributing to PyWeather, by reporting an issue.

It's simply impossible for me to catch every bug in PyWeather, so you can help! Before you report an issue, run down this to-do list.
* Make sure PyWeather is up-to-date. I do manage to catch a fair amount of bugs in PyWeather releases.
* Make sure your issue isn't on the list of known issues. The page is available in the wiki, [here](https://github.com/o355/PyWeather/wiki/Known-Issues).
* Make sure you've properly set up PyWeather, so no import errors (unless I made a typo), or config errors. If you're unsure, report the issue anyways.
* Speaking about configs, make sure your config file is provisioned.
* If your issue can be replicated, turn on tracebacks in the config file for the script it occurs in. If your issue occurs in the setup script, make setup_tracebacks true, and so on and so forth.
* You may report indev code, but you'll need to follow a few extra steps below:

**Reporting indev code:**
* Do not, and I repeat, **do not** report issues about a config issue at start. Config issues are **always** tested during QA, so there's no need to report. However, you may report an issue if PyWeather is 1-2 weeks off from the predicted release dates.
* Please avoid reporting issues about code that isn't done. Let's take this example: I'm 100% done with feature 1, but 50% done with feature 2. If you found a bug in feature 1, report it! If you found a bug in feature 2, please don't report it until it's finished.
* Please think before you report. Think if the bug is something I'll find out in a day or two, or if it's something that I'll completely miss.

In the end, if you're unsure about the requirements above, report the issue anyways.

Done with the list? Here's what you'll need for a report.
* The full traceback provided by the Python interpreter, if applicable.
* System information (OS version, Python version). You can get your Python version by typing in `python3` or `python`, and copying the first two lines outputted.
* A description detailing the issue. Add as much detail as you can to your description, as the better the description, the faster I can figure out why the bug is occurring.

You can go the extra mile by adding this stuff to your report.
* Potential solutions. If you can do Python 3 coding, make a pull request, even if it's just one line of code!
* Testing where the issue occurs. Sometimes bugs only occur on a certain OS.
* A link to an XKCD comic

If you'd like to keep this template in your report, that's completely fine. Otherwise, report the issue!
