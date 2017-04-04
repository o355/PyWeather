# PyWeather Setup - version 0.5.1 beta
# (c) 2017, o355, licensed under GNU GPL v3
# If any random imports show beneath here, blame Eclipse.

# Same deal as the main script.
# Verbosity turns on verbosity, jsonVerbosity outputs full JSONs.
# Because I'm cool, you can have verbosity off, but JSON verbosity on.


import configparser
import traceback
config = configparser.ConfigParser()
config.read('storage//config.ini')
    
try:
    verbosity = config.getboolean('VERBOSITY', 'setup_verbosity')
    jsonVerbosity = config.getboolean('VERBOSITY', 'setup_jsonverbosity')
    tracebacksEnabled = config.getboolean('TRACEBACK', 'setup_tracebacks')
except:
    print("Couldn't load your config file. Make sure your spelling is correct.",
          "Setting variables to default...", sep="\n")
    
    verbosity = False
    jsonVerbosity = False
    tracebacksEnabled = False
    
def printException():
    if tracebacksEnabled == True:
        traceback.print_exc()
        
def printException_loggerinfo():
    if verbosity == True:
        logger.info(traceback.print_exc())
        
    
import logging
logger = logging.getLogger('pyweather_setup_0.5.1beta')
logger.setLevel(logging.DEBUG)
logformat = '%(asctime)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logformat)

if verbosity == True:
    logger.setLevel(logging.DEBUG)
elif tracebacksEnabled == True:
    logger.setLevel(logging.ERROR)
else:
    logger.setLevel(logging.CRITICAL)

print("Welcome to PyWeather setup.",
      "This is meant to run as a one-time program, when you first get PyWeather.",
      "Running preflight...", sep="\n")

if verbosity == True:
    logger.info("Starting, importing 4 default libraries...")
try:
    import sys
    import urllib.request
    import shutil
    import time
except:
    logger.warn("Odd, 4 default libraries are not available...")
    print("Hmm...I tried to import default libraries, but ran into an error.",
          "Make sure that sys, urllib.request, shutil, and are available with your",
          "installation of Python.", sep="\n")
    logger.error("Here's the full traceback:")
    printException()
neededLibraries = 0
if sys.version_info[0] < 3:
    logger.error("Python 3 is needed to run. You're using version: %s"
                % sys.version_info)
    print("Shucks! I can't proceed any further.",
          "You'll need to install Python 3 to use PyWeather/PW Setup.", sep="\n")
    logger.error("Here's the full traceback:")
    printException()
    print("Press enter to continue.")
    input()
    sys.exit()
# How to create a new line in 3 characters.
print("","Before we get started, I want to confirm some permissions from you.",
      "Is it okay if I use 1-5 MB of data (downloading libraries), save a small",
      "text file called apikey.txt (> 2 KB), and automatically install Python", 
      "libraries?","",
      "Please input yes or no below:", sep="\n")
confirmPermissions = input("Input here: ").lower()
logger.debug("confirmPermissions: %s" % confirmPermissions)
if confirmPermissions == "no":
    logger.debug("User denied permissions. Closing...")
    print("Okay! Closing now.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()
elif confirmPermissions != "yes":
    logger.debug("Couldn't understand. Closing...")
    print("I couldn't understand what you said.",
          "As a precaution, I won't proceed any further.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()
    
print("","Cool! Let's start.",
      "I'm going to start by checking for necessary libraries (to run PyWeather)."
      "This can take a moment, so please hold tight while I check!", sep="\n")

try:
    import pip
except ImportError:
    logger.warn("pip is NOT installed! Asking user for automated install...")
    logger.warn("Here's the traceback:")
    printException_loggerinfo()
    print("","Shucks! I need PIP to check for/install libraries.",
    "Can I install PIP for you? Yes or No.", sep="\n")
    pipConfirm = input("Input here: ").lower()
    logger.debug("pipConfirm: %s" % pipConfirm)
    if pipConfirm == "no":
        logger.info("User denied PIP install, closing...")
        print("","Okay! I'm closing setup, as I need PIP to continue.",
        "Press enter to continue.", sep="\n")
        input()
        sys.exit()
    elif pipConfirm == "yes":
        logger.info("User allowed PIP install. Starting...")
        print("","Okay!",
        "I'll download PIP's installer, and run it.",
        "Doing such uses about 2-4 MB of data, and will quit PW setup.",
        "When the setup script finishes, you'll need to run the setup script again."
        "I'll start in a few seconds.", sep="\n")
        time.sleep(3)
        print("Downloading the installer...")
        with urllib.request.urlopen('https://bootstrap.pypa.io/get-pip.py') as update_response, open('get-pip.py', 'wb') as update_out_file:
            logger.debug("update_response: %s ; update_out_file: %s"
                        % (update_response, update_out_file))
            shutil.copyfileobj(update_response, update_out_file)
        print("Running the installer...")
        logger.debug("Executing get-pip.py...")
        exec(open("get-pip.py").read())
    else:
        logger.warn("Couldn't understand the input. Closing...")
        print("","I didn't understand what you said.",
        "As a precaution, I'm closing setup, as I need PIP to continue.",
        "Press enter to exit.", sep="\n")
        input()
        sys.exit()

try:
    import colorama
    coloramaInstalled = True
    logger.info("Colorama is installed.")
    logger.debug("coloramaInstalled: %s" % coloramaInstalled)
except ImportError:
    coloramaInstalled = False
    neededLibraries = neededLibraries + 1
    logger.warn("Colorama is not installed. Here's the traceback:")
    printException_loggerinfo()
    logger.debug("coloramaInstalled: %s ; neededLibraries: %s"
                % (coloramaInstalled, neededLibraries))
    
try:
    import geopy
    geopyInstalled = True
    logger.info("geopy is installed.")
    logger.debug("geopyInstalled: %s" % geopyInstalled)
except ImportError:
    geopyInstalled = False
    neededLibraries = neededLibraries + 1
    logger.warn("geopy is NOT installed. Here's the traceback:")
    printException_loggerinfo()
    logger.debug("geopyInstalled: %s ; neededLibraries: %s"
                % (geopyInstalled, neededLibraries))
    
try:
    import geocoder
    geocoderInstalled = True
    logger.info("geocoder is installed.")
    logger.debug("geocoderInstalled: %s" % geocoderInstalled)
except ImportError:
    geocoderInstalled = False
    neededLibraries = neededLibraries + 1
    logger.info("geocoder is NOT installed. Here's the traceback:")
    printException_loggerinfo()
    logger.debug("geocoderInstalled: %s ; neededLibraries: %s"
                 % (geocoderInstalled, neededLibraries))
    
print("All done!")
if neededLibraries == 0:
    logger.debug("All libraries are installed.")
    print("You must be magic. All necessary libraries are installed! Let's move on.")
else:
    logger.debug("Libraries need to be installed.")
    print("Shucks. Not all libraries are installed. Here's what needs to be installed:")
    if coloramaInstalled == False:
        print("- Colorama")
    if geopyInstalled == False:
        print("- Geopy")
    if geocoderInstalled == False:
        print("- Geocoder")
    print("If you want me to, I can automatically install these libraries.")
    print("Would you like me to do such? Yes or No.")
    neededLibrariesConfirm = input("Input here: ").lower()
    logger.debug("neededLibrariesConfirm: %s" % neededLibrariesConfirm)
    if neededLibrariesConfirm == "no":
        logger.warn("Not installing necessary libraries. Now exiting...")
        print("Okay. I needed to install necessary libraries to continue.")
        print("Now quitting...")
        print("Press enter to exit.")
        input()
        sys.exit()
    elif neededLibrariesConfirm == "yes":
        logger.info("Installing necessary libraries...")
        print("Sweet! I'm now installing necessary libraries.")
        if coloramaInstalled == False:
            logger.debug("Installing colorama...")
            print("Installing Colorama...")
            pip.main(['install', 'colorama'])
        if geopyInstalled == False:
            logger.debug("Installing geopy...")
            print("Installing geopy...")
            pip.main(['install', 'geopy'])
        if geocoderInstalled == False:
            logger.debug("Installing geocoder...")
            print("Installing geocoder...")
            pip.main(['install', 'geocoder'])
            logger.info("Running the double check on libraries...")
        print("Sweet! All libraries should be installed.")
        print("Just to confirm, I'm double checking if needed libraries are installed.")
        try:
            import colorama
            logger.info("Colorama installed successfully.")
        except ImportError:
            logger.warn("Colorama was not installed successfully.")
            logger.error("Here's the traceback:")
            printException()
            print("""Hmm...Colorama didn't install properly.
            Try executing 'pip install colorama' in a command shell.
            As a precaution, I'm now exiting. (Error 52, setup.py)
            Press enter to exit.""")
            input()
            sys.exit()
        try:
            import geopy
            logger.info("geopy installed successfully.")
        except ImportError:
            logger.warn("geopy was not installed successfully.")
            logger.error("Here's the traceback:")
            printException()
            print("Hmm...geopy didn't install properly."
                  "Try executing 'pip install geopy' in a command shell."
                  "As a precaution, I'm now exiting. (Error 52, setup.py)"
                  "Press enter to exit..", sep="\n")
            input()
            sys.exit()
        try:
            import geocoder
            logger.info("geocoder installed successfully.")
        except ImportError:
            logger.warn("geocoder was not installed successfully.")
            logger.error("Here's the traceback:")
            printException()
            print("""Hmm...geocoder didn't install properly.
            Try executing 'pip install geocoder' in a command shell.
            As a precaution, I'm now exiting. (Error 52, setup.py)
            Press enter to exit.""")
            input()
            sys.exit()
        print("All libraries are good to go! Let's move on.")
    else:
        logger.warn("Input was not understood. Closing...")
        print("""I'm not sure what you said.
        As a precaution, I'm now closing.""")
        sys.exit()

# Verbosity is not needed here.
print("""I'm now going to guide you through obtaining an API key.
Please carefully read my detailed instructions, so you don't mess anything up.""")

print("""Let's begin.
Start by opening a web browser, and going to https://www.wunderground.com/weather/api/.
Press any key when you are done.""")
input()
print("""Next, click the 'Explore my options' button.
Press any key when you are done.""")
input()
print("""Next, click the small button next to 'ANVIL PLAN'.
After that, confirm that the total underneath the 'Purchase Key' button says 
'$0 USD per month'. 
If the total underneath the 'Purchase Key' button doesn't 
say '$0 USD per month, please ensure that the small button next to 'Developer' 
on the table in the middle of the screen is selected, and the total 
says '$0 USD per month'
Press any key when you are done.""")
input()
print("""Next, click the 'Purchase Key' button. 
Press any key when you are done.""")
input()
print("""Next, input your email, and a password to sign up for a Weather 
Underground account.
Be sure to select the checkbox next to 'I agree to the Terms of Service'
It's best if you leave the checkbox next to 'I would like to receive WU 
updates via email' unchecked.
Press any key when you are done and ready.""")
input()
print("""Next, press the 'Sign up for free' button.
When the welcome window pops up, be sure to click the X button at the top right of the popup.
When clicking the X, you should be redirected to wunderground.com.
Press any key when you are done and ready.""")
input()
print("""Next, click 'My Profile' at the top right corner of the homepage.
In the dropdown, click 'My Email & Text Alerts'
Press any key when you are done and ready.""")
input()
print("""Next, next to your email listed on the page, click the 'Edit / Verify' button.
After you click the button, click the 'Verify Email' button.
Press any key when you are done and ready.""")
input()
print("""Next, check your email in which you signed up with.
If you got a letter from Weather Underground, titled 'Daily Forecast 
Email Verification', open that letter, and click the link.
If you didn't get the letter, wait a few minutes, and be sure to check your spam folder.
Hint: If you followed this guide exactly, WU will not be sending you daily forecasts to your email.
Press any key when you are done and ready.""")
input()
print("""Your email should be verified.
Next, in your web browser, head back to https://www.wunderground.com/weather/api/.
Then, click the 'Explore my Options' button, again.
Press any key when you are done and ready.""")
input()
print("""Next, at the top of the page, make sure the button next to 'ANVIL PLAN' 
is selected.
After that, confirm that the total underneath the 'Purchase Key' button says 
'$0 USD per month'
If the total doesn't say that, in the pricing table, make sure the button 
next to 'Developer' is selected.
Press any key when you are done and ready.""")
input()
print("""Next, click the 'Purchase Key' button, on top of your total (which 
should be $0 USD per month)
Next, fill out the form, considering these tips:
For the contact name/email, it's recommended you use your real name 
(first name last initial is fine).
It's also recommended that you use your real email.
For the project name, put in something generic, like 'to use a script that 
uses WU's API', or 'PyWeather user'
For the project website, put in something generic, like 'google.com', or 
the homepage of PyWeather.
Hint: The homepage of PyWeather is github.com/o355/py
For the question 'Where will the API be used', answer Other.
For the question 'Will the API be used for commercial use?', answer No.
For the question 'Will the API be used for manufacturing mobile chip 
processing?', answer No.
Answer yes if you somehow are manufacturing mobile chip processing. I doubt 
you are, however.
For the country that you are based in, put your location.
Before we move on, fill out these forms, and press any key when you are done 
and ready.""")
input()
print("""Next, for the brief description, put something like 'using an API key 
to use a script using Wunderground'.
After that, check both boxes at the bottom of the page. Read the ToS if you 
feel like it.
Finally, click 'Purchase Key'.
You should land on a page that says 'Edit API Key'.
Press any key when you are done and ready.""")
input()
print("""In the table to the left of the page, copy the text that's under Key ID. 
(Ctrl+C, right click)
I'm now going to ask you to input the API key into the text entry below.
The API key will be saved to storage/apikey.txt, so PyWeather can easily 
pull it up.
Press any key when you are done and ready.""")
input()
print("Please input your API key below.")
apikey_input = input("Input here: ")
logger.debug("apikey_input: %s" % apikey_input)
print("Just to confirm, the API key you gave me was: " + apikey_input
      + ".")
print("Please double check your input, and confirm in the dialogue below.")
apikey_confirm = input("Is the API key right? Yes or no: ").lower()
logger.debug("apikey_confirm: %s" % apikey_confirm)
if apikey_confirm == "no":
    logger.debug("User now re-entering key...")
    print("Please input your API key below.")
    apikey_input = input("Input here: ")
    logger.debug("apikey_input: %s" % apikey_input)
    print("Just to confirm, the API key you gave me was: " + apikey_input
      + ".")
    print("If you got the API key wrong, please close out of setup, and try again. ")

print("Now saving your API key...")
open('storage//apikey.txt', 'w').close()

with open("storage//apikey.txt", 'a') as out:
    logger.debug("out: %s" % out)
    out.write(apikey_input)
    out.close()
    logger.debug("Performed ops: overwrite apikey.txt, out.write(apikey_input), out.close()")
   
print("I can also back up your API key, in case you do something wrong.")
# A future release should bring customization as to the storage location.
print("Would you like me to save a backup? Yes or no.")
backup_APIkey = input("Input here: ").lower()
if backup_APIkey == "yes":
    backup_APIkeydir = input("Where would you want me to add the backup key: ")
    try:
        folder_argument = backup_APIkeydir + "//backkey.txt"
        print("Creating a backup...")
        open(folder_argument, 'w+').close()
        open(folder_argument, 'a').write(apikey_input)
        open(folder_argument).close()
        config.read('storage//config.ini')
        config['KEYBACKUP']['savelocation'] = backup_APIkeydir
    
        logger.debug("Performed 3 ops. Overwrite "+ folder_argument + ", write to backkey.txt" + 
                     ", and close backkey.txt.")

    except:
        print("Could not find the location you input. Backup key is in default folder.")
        print("Creating  backup...")
        open("backup//backkey.txt", 'w').close()
        open("backup//backkey.txt", 'a').write(apikey_input)
        open("backup//backkey.txt").close()
        config.read('storage//config.ini')
        config['KEYBACKUP']['savelocation'] = 'backup//backkey.txt'
        logger.debug("Performed 3 ops. Overwrite backup//backkey.txt, write to backkey.txt" + 
                     ", and close backkey.txt.")
# once a config file is properly added, options for configuring the config will go here

print("Let's configure a few options for PyWeather.")
logger.debug("config: %s" % config)

print("""\nOn the summary screen, would you like to show sunrise/sunset times?
By default, this is disabled.
Yes or No.""")
sundata_Summary = input("Input here: ").lower()
logger.debug("sundata_Summary: %s" % sundata_Summary)
if sundata_Summary == "yes":
    config['SUMMARY']['sundata_summary'] = 'True'
    logger.debug("Sundata on the summary is now ENABLED.")
elif sundata_Summary == "no":
    config['SUMMARY']['sundata_summary'] = 'False'
    logger.debug("Sundata on the summary is now DISABLED.")
else:
    print("Could not understand what you said.")
    print("Defaulting to the default value 'False'")
    config['SUMMARY']['sundata_summary'] = 'False'
    logger.debug("Could not recognize input. Defaulting to DISABLED.")
   
print("""\nOn the summary screen, would you like to show almanac data?
By default, this is disabled.
Yes or No.""")
almanacdata_Summary = input("Input here: ").lower()
logger.debug("almanacdata_Summary: %s" % almanacdata_Summary)
if almanacdata_Summary == "yes":
    config['SUMMARY']['almanac_summary'] = 'True'
    logger.debug("Almanac on the summary is now ENABLED.")
elif almanacdata_Summary == "no":
    config['SUMMARY']['almanac_summary'] = 'False'
    logger.debug("Almanac on the summary is now DISABLED.")
else:
    print("Could not understand what you said.")
    print("Defaulting to the default value 'False'")
    config['SUMMARY']['almanac_summary'] = 'False'
    logger.debug("Could not recognize input. Defaulting to DISABLED.")

print("""\nOn boot, would you like PyWeather to check for updates?
By default, this is disabled, due to a load time increase of ~2-5 seconds.
Yes or No.""")
checkForUpdates = input("Input here: ").lower()
logger.debug("checkForUpdates: %s" % checkForUpdates)
if checkForUpdates == "yes":
    config['UPDATER']['autoCheckForUpdates'] = 'True'
    logger.debug("Checking for updates on startup is ENABLED.")
elif checkForUpdates == "no":
    config['UPDATER']['autoCheckForUpdates'] = 'False'
    logger.debug("Checking for updates on startup is DISABLED.")
else:
    print("Could not understand what you said.")
    print("Defaulting to the default value 'False'")
    config['UPDATER']['autoCheckForUpdates'] = 'False'
    logger.debug("Could not recognize input. Defaulting to DISABLED.")
    
print("That's it! Now commiting config changes...")
with open('storage//config.ini', 'w') as configfile:
    logger.debug("configfile: %s" % configfile)
    config.write(configfile)
    logger.info("Performed operation: config.write(configfile)")

print("We're wrapping up, and performing a few tests.")

print("Checking for parsing libraries...")
try:
    import json
    logger.debug("json is available.")
except:
    logger.warn("json isn't available...that's odd.")
    
    print("""json is not available. This is odd, it's a default library.
    Try installing a usual Python install.
    Press enter to exit.""")
    input()
    sys.exit()
try:
    import codecs
    logger.debug("codecs is available.")
except:
    logger.warn("codecs isn't available. Here's the traceback:")
    printException_loggerinfo()
    print("""codecs is not available. This is odd, it's a default library.
    Try installing a usual Python install.
    Press enter to exit.""")
    input()
    sys.exit()

print("Testing the API connection, and seeing if the API key is valid...")
apitest_URL = 'http://api.wunderground.com/api/' + apikey_input + '/conditions/q/NY/New_York.json'
testreader = codecs.getreader("utf-8")
logger.debug("apitest_URL: %s ; testreader: %s" %
             (apitest_URL, testreader))

try:
    testJSON = urllib.request.urlopen(apitest_URL)
    logger.debug("testJSON: %s" % testJSON)
except:
    logger.warn("Couldn't connect to Wunderground's API! No internet?")
    print("""We ran into an error. Make sure Wunderground's API is unblocked, and 
            you have an internet connection.
    Press enter to exit.""")
    input()
    sys.exit()
    
test_json = json.load(testreader(testJSON))
if jsonVerbosity == True:
    logger.debug("test_json: %s" % test_json)

try:
    test_conditions = str(test_json['current_observation']['temp_f'])
    logger.debug("test_conditions: %s" % test_conditions)
    print("Yay! Your API key is valid and works.")
except:
    logger.warn("Error! Is the API key invalid?")
    print("We ran into an error. Make sure your API key is valid.")
    print("Press enter to exit.")
    input()
    sys.exit()
    
print("Testing the Google geocoder connection...")

from geopy import GoogleV3

geolocator = GoogleV3()
logger.debug("geolocator: %s" % geolocator)

try:
    testlocation = geolocator.geocode("New York, NY", language="en")
    logger.debug("testlocation: %s" % testlocation)
    logger.debug("testlocation.latitude: %s ; testlocation.longitude: %s" %
                 (testlocation.latitude, testlocation.longitude))
    print("Yay! Google's geocoder works.")
except:
    logger.warn("Couldn't connect to Google's geocoder. No internet?")
    print("We ran into an error. Make sure Google's geocoder is unblocked, " +
          "and you have an internet connection.")
    print("Press enter to exit.")
    input()
    sys.exit()
    
    
print("Testing the reverse geocoder connection...")


try:
    testlocation3 = geocoder.google([testlocation.latitude, testlocation.longitude], method='reverse')
    logger.debug("testlocation3: %s" % testlocation3)
    logger.debug("testlocation3.city: %s ; testlocation3.state: %s" %
                 (testlocation3.city, testlocation3.state))
    print("Yay! The geolocator works.")
except:
    logger.warn("Couldn't connect to Google's geocoder. No internet?")
    print("We ran into an error. Make sure Google's Geolocator is unblocked, " +
          "and you have an internet connection.")
    print("Press enter to exit.")
    input()
    sys.exit()

print("""\nEverything is set up and ready to rumble!
Enjoy using PyWeather! If you have any issues, please report them on GitHub!
Press enter to continue.""")
input()
sys.exit()
