## PyWeather Configuration Readme
Since configparser hates comments, this will do for now.

## SUMMARY section
### sundata_summary
This option will let you turn on/off PyWeather showing sunrise/sunset data on startup.

If this option is enabled, PyWeather may take a bit longer to start up, and will use 1 more API call at start.

**Default option: False**

###almanac_summary
This option will let you turn on/off PyWeather showing almanac data on startup.

If this option is enabled, PyWeather may take a bit longer to start up, and will use 1 more API call at start.

**Default option: False**

## VERBOSITY section
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
This option will let you turn on/off 

## TRACEBACK section

## HOURLY section

### 10dayfetch_atboot
This option controls if PyWeather should fetch the 10 day hourly forecast JSON at boot. Here's how it works.

By default, PyWeather fetches a 3 day hourly JSON at boot. When you go into the 10 day hourly menu, it'll fetch the 10 day hourly JSON. This method is less call-efficient, but doing this makes PyWeather load faster.

When enabled, PyWeather will only fetch the 10 day hourly JSON at boot. A downside to this is that loading will take longer, as it has more to download. However, you won't need to wait for PyWeather to fetch the 10 day JSON when you want to view 10 day hourly, and saves on calls.

This isn't a default in the code due to the pros/cons of using each method.

(and implementing this was a complete pain in the NECK.)

**Default option: False**