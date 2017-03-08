# Config file readme
Because when commiting changes through ConfigParser, it hates comments.

But Eclipse supports nice formatting for markdown. Thanks Eclipse.

Please read through this carefully before you make changes, because you can seriously screw up PyWeather if you don't know what you're doing.

## SUMMARY section
This section controls options for the summary part of PyWeather.

### sundata_summary
This controls if sunrise/sunset data on the summary screen.

Turning this on will use 1 more API call every time you launch PyWeather, but will put sunrise/sunset data on the summary screen.

**Default setting: False**

### almanac_summary
This controls if almanac data on the summary screen.

Turning this on will use 1 more API call every time you launch PyWeather, but will put the record high/low, and the year that it was set in at the closest airport to you.

**Default setting: False**

## VERBOSITY section
This section controls options for verbosity in PyWeather (pyweather.py)

### verbosity
This controls if verbosity is enabled for PyWeather.

Verbosity will let you see if things are going wrong in PyWeather. It's useful for those who know what's going on behind the scenes.

**Default setting: False**

### json_verbosity
This controls if .json verbosity is enabled for PyWeather.

All this does is print out full .json files that PyWeather fetches. And it'll spam your console with 50+ lines of pure .json. Unless you're using tri-4K monitors, font size 3, and the window spread across all monitors.

**Default setting: False**

## UPDATER section
This section controls the integrated/separate updater for PyWeather.

### autocheckforupdates
This controls if PyWeather will automatically check for updates when it starts up.

If PyWeather is not up-to-date, and this option is enabled, something like this will pop up at the top of the console:

`PyWeather is not up to date! You have version x.xx, but the latest version is x.xx`

However, if you enable this, PyWeather can take upwards of 5 seconds to launch. So, take caution.

**Default setting: False**

### updater_verbosity
This controls if the external updater has verbosity. 

Useful for if things go wrong. For some reason.

**Default setting: False**

### updater_jsonverbosity
This controls is full .json files should be printed.

I mean, it's probably a line or two in the console.

**Default setting: False**