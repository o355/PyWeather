## PyWeather Configuration Readme - For PyWeather 0.5.2.1/0.6.0.1 beta
Since configparser hates comments, this will do for now.

Quick notice: This little readme will get an overhaul soon, but that overhaul requires me to look through old versions of PyWeather, to see what configuration options appeared when. That takes time.

## CHANGELOG
### forversion
**Available in PyWeather ? beta - 0.5.2.1 beta**

This is just to show you what version the config file is meant to be used for.

Changing this does nothing.

**Default option: The version of PyWeather you're running**

## SUMMARY section
### sundata_summary
This option will let you turn on/off PyWeather showing sunrise/sunset data on startup.

If this option is enabled, PyWeather may take a bit longer to start up, and will use 1 more API call at start.

**Default option: False**

### almanac_summary
This option will let you turn on/off PyWeather showing almanac data on startup.

If this option is enabled, PyWeather may take a bit longer to start up, and will use 1 more API call at start.

**Default option: False**

### showAlertsOnSummary
**Available in PyWeather 0.6 beta and above**

This option will let you turn on/off PyWeather showing you alerts on the summary screen.

This is on by default, but if you mainly search for non US/EU locations, you might want to turn this off, as you do use one API call at boot when this option is enabled.

**Default option: True**

## VERBOSITY section
PyWeather can give you extra information across all scripts, to help debug problems.

### verbosity
This option will let you turn on/off PyWeather showing logging information.

Useful for troubleshooting, and seeing if something is abnormal.

**Default option: False**

### json_verbosity
This option will let you turn on/off PyWeather printing out full .json files that it fetches.

Useful for troubleshooting, but it'll spam your console. Use wisely.

**Default option: False**

### setup_verbosity
This option will let you turn on/off PyWeather Setup showing logging information.

Useful for troubleshooting, and seeing if something is abnormal.

**Default option: False**

### setup_jsonverbosity
This option will let you turn on/off PyWeather Setup printing out .json files that it fetches.

Useful for troubleshooting, but it'll spam your console. Use wisely.

**Default option: False**

### updater_verbosity
This option will let you turn on/off PyWeather Updater showing logging information.

Useful for troubleshooting, and seeing if something is abnormal.

**Default option: False**

### updater_jsonverbosity
This option will let you turn on/off PyWeather Updater printing out .json files that it fetches.

Useful for troubleshooting, and it doesn't spam your console as much.

**Default option: False**

### keybackup_verbosity
This option will let you turn on/off PyWeather API Key Backup showing logging information.

Useful for troubleshooting, and seeing if something is abnormal.

**Default option: False**

### configdefault_verbosity
This option will let you turn on/off PyWeather Configuration Reset showing logging information.

Useful for troubleshooting, and seeing if something is abnormal.

**Default option: False**

## TRACEBACK section
PyWeather can optionally show you a full traceback when an error occurs in a safety net. Turning this on is especially useful when you need to report an error.

### tracebacks
This option allows you to turn on printing full tracebacks in PyWeather.

Useful for reporting issues, and seeing what went wrong.

**Default option: False**

### setup_tracebacks

This option allows you to turn on printing full tracebacks in PyWeather Setup.

Useful for reporting issues, and seeing what went wrong.

**Default option: False**

### updater_tracebacks

This option allows you to turn on printing full tracebacks in PyWeather Updater.

Useful for reporting issues, and seeing what went wrong.

**Default option: False**

### keybackup_tracebacks

This option allows you to turn on printing full tracebacks in PyWeather API Key Backup.

Useful for reporting issues, and seeing what went wrong.

**Default option: False**

### configdefault_tracebacks
This option allows you to turn on printing full tracebacks in PyWeather Configuration Reset.

Useful for reporting issues, and seeing what went wrong.

**Default option: False**

## UI section
This section controls parts of the UI in PyWeather.

### show_enterToContinue
This option allows you to show the "Enter to Continue" prompt when viewing detailed weather information.

This should probably be left on, unless you feel like scrolling through 240 iterations of 10 day hourly weather.

**Default option: True**

### detailedInfoLoops
This option allows you to control how many loops, or iterations PyWeather will go through before stopping for an "Enter to Continue" prompt, when viewing detailed hourly, 10 day hourly, and historical hourly information.

Increasing this option above 10 isn't recommended, as it gets pretty annoying to scroll up through a lot of iterations to get the information you need.

**Default option: 6**

### forecast_detailedInfoLoops
This option allows you to control how many loops, or iterations PyWeather will go through before stopping for an "Enter to Continue" prompt, when viewing detailed forecast information.

If you increase this option above 9, you basically get rid of the prompt.

**Default option: 5**

### show_completedIterations
This option allows you to see how many iterations you've gone through, when viewing detailed hourly, 10 day hourly, historical hourly, or the 10 day forecast.

It blends in with the rest of the data, so it can be a little hard to notice.

**Default option: False**

## HOURLY section

### 10dayfetch_atboot
This option controls if PyWeather should fetch the 10 day hourly forecast JSON at boot. Here's how it works.

By default, PyWeather fetches a 3 day hourly JSON at boot. When you go into the 10 day hourly menu, it'll fetch the 10 day hourly JSON. This method is less call-efficient, but doing this makes PyWeather load faster.

When enabled, PyWeather will only fetch the 10 day hourly JSON at boot. A downside to this is that loading will take longer, as it has more to download. However, you won't need to wait for PyWeather to fetch the 10 day JSON when you want to view 10 day hourly, and saves on calls.

This isn't a default in the code due to the pros/cons of using each method.

(and implementing this was a complete pain in the NECK.)

**Default option: False**

## PYWEATHER BOOT section
This section controls stuff that goes on when PyWeather boots.

### validateapikey
**Available in PyWeather 0.6 beta and above**
This option allows for PyWeather to validate your primary API key (stored at storage//apikey.txt), and make sure the key is valid.

PyWeather will try to open the file, fetch a test JSON, and validate the primary key. If the key is valid, everything continues. If the key isn't valid, PyWeather will attempt to load a backup key (with the directory specified in the config), and vertify that. If it's verified, variables are changed, and PW continues on. 

If the backup key can't be opened or verified, PyWeather stops.

This option is enabled, as it's well worth the extra API call to make sure your key is valid.

**Default option: True**

## UPDATER section
This section controls PyWeather's updating mechanism.

### autocheckforupdates
This option allows for PyWeather to automatically check for updates on boot.

It's very minimal, and all it'll say if PyWeather is out of date is something like "PyWeather is not up to date. You have version x, and the latest version is y".

If PyWeather is up to date, nothing will be outputted.

It's useful, but enabling this makes it so PyWeather starts a little slower at boot.

**Default option: False**

### show_updaterReleaseTag
This option allows you to show the release tag (branch) for the latest version of PyWeather.

This is especially useful for those using Git, who want to pull from the source, and check out to the latest stable version.

It's off by default as it's presumed you're not using Git to download and update PyWeather.

**Default option: False**

### allowGitForUpdating
This option allows you to control if PyWeather should prompt you to update with Git in PyWeather.

Only turn this on if you're sure that you have Git on your system, and that it's available in your default shell. When PyWeather updates with Git, it'll automatically check out to the master branch, stash any local changes, pull new changes, stash local changes again, and check out to the latest "branch".

When doing this, custom changes to your config file will be overwritten. PyWeather 0.6 beta will most likely be able to get around this, so it's just for now.

**Default option: False**

## RADAR GUI section
**Available in PyWeather 0.6 indev, and PyWeather 0.6.1 beta and above**
This section controls the GUI for displaying radar and other images.

### gifsize
This option allows you to control the size of the .gif image that is to be displayed.
This option will only accept 5 sizes, as defined below
(can't imagine how hard it'd be to code in every size ever. This is simpler, too)

* extrasmall = 320x240
* small = 480x320
* normal = 640x480
* large = 960x720
* extralarge = 1280x960

The default option is 640x480, it's a nice balance between size of the GUI and size of the radar image.

Of course, on newer laptops with FHD screens, you can increase the resolution of the image. Note, the higher the image size, the longer it takes to fetch the .gif.

**Default option: normal**

## KEYBACKUP section
This section allows you to control parts of the Key Backup script.

### savelocation
This option allows you to control where your backup API key is stored. It's a global setting, meaning (in future versions) that PyWeather will load your backup key (if your primary one is dead) from this location.

You can save it anywhere in PyWeather's folder. However, you'll want to take note of three things.

1. If you want to save your key to a folder that doesn't exist, make the folder first. If you don't do this, you might run into issues.

2. When you want your backup key in a folder, instead of doing "/" or "\" for the folder (e.g. test/test.txt, or test\test.txt), you'll want to use "//" instead. (e.g. test//test.txt)

3. The file extension is no more. PyWeather will automatically save the backup key document as backkey.txt, to prevent conflicts.

**Default option: backup//**

## VERSIONS section
**Available in PyWeather ? beta - PyWeather 0.5.2.1 beta**
This section controls version overriding, mainly for debugging reasons.

### overrideVersion
This option allows you to control if PyWeather should override set build numbers/version texts, for debugging or some other reason.

The two options below this are only valid if version overriding is enabled.

**Default option: False**

### overridebuildnumber
This option lets you control the build number PyWeather uses (mainly for update checking). This option MUST BE AN INTEGER.

Build numbers are basically the version number.

0.5 beta = 50
v1.0 = 100
v1.0.1 = 101
v1.1 = 110

And so on and so forth.

If a criticial hotfix needs to be applied (e.g. 0.5.2.1), the build number in such case would become 52.1.

**Default option: 52.1**

### overrideversiontext
This option lets you control the version text that is visible to the user (when showing "PyWeather is out of date, you have version <version>, etc). This option is a string, you can put whatever you want here, if you so desire.

**Default option: 0.5.2.1 beta**

## USER section
**Available in PyWeather 0.6 beta and above**

An explaination isn't needed.

### configprovisioned
This option controls if your config file is provisioned. This mainly does nothing, as this section/option is used to rat out an unprovisioned config.

Changing this should do nothing, but keep it True just to be safe.

**Default option: True**