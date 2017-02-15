# PyWeather Setup
# (c) 2017

# Exe version coming (eventually)
pyweathertype = "standalone"
neededlibraries = 0

print("Welcome to PyWeather setup.")
print("This is meant to run as a one-time program, when you first get PyWeather.")
print("Let's start.")
print("")
if pyweathertype == "standalone":
    try:
        import pip
    except:
        print("You'll need to install PIP before preceding.")
        # get the .py file, blah blah blah
    try:
        import colorama
    except:
        neededlibraries = neededlibraries + 1
        coloramaPresent = False
        # Dictionary for uninstalled libraries blah blah blah
    try:
        import geopy
    except:
        neededlibraries = neededlibraries + 1
        geopyPresent = False
        # Dictionary code
    try:
        import geocoder
    except:
        neededlibraries = neededlibraries + 1
        geocoderPresent = False
        # Dictionary code
if pyweathertype == "exe":
    print("Since you have the .exe version, all libraries are installed!")
print("Let's make sure you have a connection to necessary geocoders.")