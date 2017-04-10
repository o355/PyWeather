# PyWeather Setup - version 0.5.1 beta
# (c) 2017, o355, licensed under GNU GPL v3
# If any random imports show beneath here, blame Eclipse.

# Same deal as the main script.
# Verbosity turns on verbosity, jsonVerbosity outputs full JSONs.
# Because I'm cool, you can have verbosity off, but JSON verbosity on.


import configparser
import traceback
from pygame import display
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
        print("Here's the full traceback:")
        traceback.print_exc()
        
def printException_loggerwarn():
    if verbosity == True:
        logger.warn("Oh snap! We ran into a non-critical error. Here's the traceback.")
        logger.warn(traceback.print_exc())
        
    
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
    
logger.debug("Listing configuration options:")
logger.debug("verbosity: %s ; jsonVerbosity: %s" %
             (verbosity, jsonVerbosity))
logger.debug("tracebacksEnabled: %s" %
             (tracebacksEnabled))

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
      "I'm going to start by checking for necessary libraries (to run PyWeather).",
      "This can take a moment, so please hold tight while I check!", sep="\n")

try:
    import pip
except ImportError:
    logger.warn("pip is NOT installed! Asking user for automated install...")
    printException_loggerwarn()
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
        try:
            with urllib.request.urlopen('https://bootstrap.pypa.io/get-pip.py') as update_response, open('get-pip.py', 'wb') as update_out_file:
                logger.debug("update_response: %s ; update_out_file: %s"
                             % (update_response, update_out_file))
                shutil.copyfileobj(update_response, update_out_file)
        except:
            print("Can't download the PIP installer.",
                  "Make sure bootstrap.pypa.io is unblocked.", sep="\n")
            printException()
            print("Press enter to exit.")
            input()
            sys.exit()
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
    logger.warn("Colorama is not installed.")
    printException_loggerwarn()
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
    logger.warn("geopy is NOT installed.")
    printException_loggerwarn()
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
    logger.info("geocoder is NOT installed.")
    printException_loggerwarn()
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
            print("Hmm...Colorama didn't install properly.",
            "Try executing 'pip install colorama' in a command shell.",
            "As a precaution, I'm now exiting. (Error 52, setup.py)", sep="\n")
            printException()
            print("Press enter to exit.")
            input()
            sys.exit()
        try:
            import geopy
            logger.info("geopy installed successfully.")
        except ImportError:
            logger.warn("geopy was not installed successfully.")
            print("Hmm...geopy didn't install properly.",
                  "Try executing 'pip install geopy' in a command shell.",
                  "As a precaution, I'm now exiting. (Error 52, setup.py)", sep="\n")
            printException()
            print("Press enter to exit.")
            input()
            sys.exit()
        try:
            import geocoder
            logger.info("geocoder installed successfully.")
        except ImportError:
            logger.warn("geocoder was not installed successfully.")
            print("Hmm...geocoder didn't install properly.",
            "Try executing 'pip install geocoder' in a command shell.",
            "As a precaution, I'm now exiting. (Error 52, setup.py)", sep="\n")
            printException()
            print("Press enter to exit.")
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
    while True:
        logger.debug("User now re-entering key...")
        print("","Please input your API key below.", sep="\n")
        apikey_input = input("Input here: ")
        logger.debug("apikey_input: %s" % apikey_input)
        print("Just to confirm, the API key you gave me was: " + apikey_input
              + ".")
        apikey_confirm = input("Is the API key right? Yes or no: ").lower()
        if apikey_confirm == "yes":
            break
        elif apikey_confirm == "no":
            continue
        else:
            print("Couldn't understand your input.",
                  "I'll assume the API key is correct, moving on.", sep="\n")

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
    print("Where would you want me to backup the key to?")
    print("This is a directory. If I wanted my key at directory/backkey.txt,",
          "You would enter 'directory//'. The default directory is 'backup//'.", sep="\n")
    # Doing a .lower() here to prevent case insensitiveness.
    backup_APIkeydir = input("Input here: ").lower()
    try:
        folder_argument = backup_APIkeydir + "//backkey.txt"
        print("Creating a backup...")
        open(folder_argument, 'w+').close()
        open(folder_argument, 'a').write(apikey_input)
        open(folder_argument).close()
        config['KEYBACKUP']['savedirectory'] = backup_APIkeydir
        print("Backup successful!")
        logger.debug("Performed 3 ops. Overwrite "+ folder_argument + "backkey.txt, write to backkey.txt" + 
                     ", and close backkey.txt.")
    except:
        print("Could not find the location you wanted. Defaulting on the normal directory...")
        printException_loggerwarn()
        print("Creating backup...")
        open("backup//backkey.txt", 'w').close()
        open("backup//backkey.txt", 'a').write(apikey_input)
        open("backup//backkey.txt").close()
        config.read('storage//config.ini')
        config['KEYBACKUP']['savelocation'] = 'backup//'
        logger.debug("Performed 3 ops. Overwrite backup//backkey.txt, write to backkey.txt" + 
                     ", and close backkey.txt.")

print("Let's configure a few options for PyWeather.")
logger.debug("config: %s" % config)

print("","On the summary screen, would you like to show sunrise/sunset times?",
      "By default, this is disabled.",
      "Yes or No.", sep="\n")
sundata_Summary = input("Input here: ").lower()
logger.debug("sundata_Summary: %s" % sundata_Summary)
if sundata_Summary == "yes":
    config['SUMMARY']['sundata_summary'] = 'True'
    print("Changes saved.")
    logger.debug("Sundata on the summary is now ENABLED.")
elif sundata_Summary == "no":
    config['SUMMARY']['sundata_summary'] = 'False'
    print("Changes saved.")
    logger.debug("Sundata on the summary is now DISABLED.")
else:
    print("Could not understand what you inputted.")
    print("Defaulting to 'False'")
    config['SUMMARY']['sundata_summary'] = 'False'
    logger.debug("Could not recognize input. Defaulting to DISABLED.")
   
print("","On the summary screen, would you like to show almanac data?",
      "By default, this is disabled.",
      "Yes or no:", sep="\n")
almanacdata_Summary = input("Input here: ").lower()
logger.debug("almanacdata_Summary: %s" % almanacdata_Summary)
if almanacdata_Summary == "yes":
    config['SUMMARY']['almanac_summary'] = 'True'
    print("Changes saved.")
    logger.debug("Almanac on the summary is now ENABLED.")
elif almanacdata_Summary == "no":
    config['SUMMARY']['almanac_summary'] = 'False'
    print("Changes saved.")
    logger.debug("Almanac on the summary is now DISABLED.")
else:
    print("Could not understand what you inputted.")
    print("Defaulting to 'False'")
    config['SUMMARY']['almanac_summary'] = 'False'
    logger.debug("Could not recognize input. Defaulting to DISABLED.")

print("","On boot, would you like PyWeather to check for updates?",
      "By default, this is disabled, due to a load time increase of ~2-5 seconds.",
      "Yes or No.", sep="\n")
checkForUpdates = input("Input here: ").lower()
logger.debug("checkForUpdates: %s" % checkForUpdates)
if checkForUpdates == "yes":
    config['UPDATER']['autoCheckForUpdates'] = 'True'
    print("Changes saved.")
    logger.debug("Checking for updates on startup is ENABLED.")
elif checkForUpdates == "no":
    config['UPDATER']['autoCheckForUpdates'] = 'False'
    print("Changes saved.")
    logger.debug("Checking for updates on startup is DISABLED.")
else:
    print("Could not understand what you inputted.")
    print("Defaulting to 'False'")
    config['UPDATER']['autoCheckForUpdates'] = 'False'
    logger.debug("Could not recognize input. Defaulting to DISABLED.")
    
print("","When an error occurs, would you like PyWeather to show the full error?",
      "When enabled, you'll have easier access to the full error for reporting",
      "the bug on GitHub.",
      "By default, this is disabled, as errors look less pretty when enabled.",
      "Yes or no.", sep="\n")
displayTracebacks = input("Input here: ").lower()
logger.debug("displayTracebacks: %s" % displayTracebacks)
if displayTracebacks == "yes":
    config['TRACEBACK']['tracebacks'] = 'True'
    config['TRACEBACK']['setup_tracebacks'] = 'True'
    config['TRACEBACK']['updater_tracebacks'] = 'True'
    config['TRACEBACK']['keybackup_tracebacks'] = 'True'
    print("Changes saved.")
    logger.debug("Printing tracebacks is ENABLED.")
elif displayTracebacks == "no":
    config['TRACEBACK']['tracebacks'] = 'False'
    config['TRACEBACK']['setup_tracebacks'] = 'False'
    config['TRACEBACK']['updater_tracebacks'] = 'False'
    config['TRACEBACK']['keybackup_tracebacks'] = 'False'
    print("Changes saved.")
    logger.debug("Printing tracebacks is DISABLED.")
else:
    print("Couldn't understand what you inputted.",
          "Defaulting to 'False'", sep="\n")
    config['TRACEBACK']['tracebacks'] = 'False'
    config['TRACEBACK']['setup_tracebacks'] = 'False'
    config['TRACEBACK']['updater_tracebacks'] = 'False'
    config['TRACEBACK']['keybackup_tracebacks'] = 'False'
    logger.debug("Could not understand input. Defaulting to DISABLED.")

print("","When booting PyWeather up initially, would you like PyWeather to",
      "fetch the 10-day hourly forecast, instead of the 3-day forecast?",
      "This is disabled by default. When enabled, initial loading times are",
      "increased. However, when you view the 10-day hourly forecast, you won't",
      "have to wait for it to load, and use another API call.",
      "Yes or No.", sep="\n")
tenday_onboot = input("Input here: ").lower()
if tenday_onboot == "yes":
    config['HOURLY']['10dayfetch_atboot'] = 'True'
    print("Changes saved.")
    logger.debug("Fetching 10 day JSON at boot is ENABLED.")
elif tenday_onboot == "no":
    config['HOURLY']['10dayfetch_atboot'] = 'False'
    print("Changes saved.")
    logger.debug("Fetching 10 day JSON at boot is DISABLED.")
else:
    print("Couldn't understand what you inputted.",
          "Defaulting to the default value 'False'", sep="\n")
    config['HOURLY']['10dayfetch_atboot'] = 'False'
    logger.debug("Could not understand input. Defaulting to DISABLED.")
    
print("","When viewing detailed hourly, 10-day hourly, and historical hourly,",
      "detailed information, how many iterations should PyWeather go through",
      "before asking you to continue?",
      "By default, this is 6. An input above 10",
      "is not recommended.", sep="\n")
detailedloops = input("Input here: ")
try:
    detailedloops = int(detailedloops)
    detailedloops = str(detailedloops)
    config['UI']['detailedinfoloops'] = detailedloops
    print("Changes saved.")
    logger.debug("Detailed info loops now %s." % detailedloops)
except:
    print("Couldn't convert input into a number. Defaulting to '6'.")
    printException_loggerwarn()
    config['UI']['detailedinfoloops'] = '6'
    logger.debug("Detailed info loops now 6.")
    
print("","When viewing detailed 10-day forecast information, how many",
      "iterations should PyWeather go through, before asking you to",
      "continue?",
      "By default, this is 5. An input above 10 will not prompt",
      "the enter to continue prompt", sep="\n")
detailedForecastLoops = input("Input here: ")
try:
    detailedForecastLoops = int(detailedForecastLoops)
    detailedForecastLoops = str(detailedForecastLoops)
    config['UI']['forecast_detailedinfoloops'] = detailedForecastLoops
    print("Changes saved.")
    logger.debug("Detailed forecast info loops now %s" % detailedForecastLoops)
except:
    print("Couldn't convert input into a number. Defaulting to '5'.")
    printException_loggerwarn()
    config['UI']['forecast_detailedinfoloops'] = '5'
    logger.debug("Detailed forecast info loops now 5.")
    
print("","When PyWeather is going through detailed information, it can show",
      "how many iterations are completed.",
      "By default, this is disabled.",
      "Yes or No.", sep="\n")
showIterations = input("Input here: ").lower()
if showIterations == "yes":
    config['UI']['show_completediterations'] = 'True'
    print("Changes saved.")
    logger.debug("Showing completed iterations is ENABLED.")
elif showIterations == "no":
    config['UI']['show_completediterations'] = 'False'
    print("Changes saved.")
    logger.debug("Showing completed iterations is DISABLED.")
else:
    print("Couldn't understand what you inputted.",
          "Defaulting to 'FALSE'.", sep="\n")
    config['UI']['show_completediterations'] = 'False'
    logger.debug("Could not understand input. Defaulting to DISABLED.")
    
print("", "When PyWeather is going through detailed information, would",
      "you like the 'Enter to Continue' prompts not to pop up?",
      "By default, this is enabled.",
      "Yes or No.", sep="\n")
showEnterToContinue = input("Input here: ").lower()
if showEnterToContinue == "yes":
    config['UI']['show_entertocontinue'] = 'True'
    print("Changes saved.")
    logger.debug("Showing enter to continue prompts is ENABLED.")
elif showEnterToContinue == "no":
    config['UI']['show_entertocontinue'] = 'False'
    print("Changes saved.")
    logger.debug("Showing enter to continue prompts is DISABLED.")
else:
    print("Could not understand what you inputted.",
          "Defaulting to 'True'.", sep="\n")
    config['UI']['show_entertocontinue'] = 'True'
    logger.debug("Could not understand input. Defaulting to ENABLED.")
    
print("", "In the PyWeather Updater, the updater can show the release tag",
      "associated with the latest release. Helpful for those using Git to",
      "update PyWeather. By default, this is disabled.",
      "Yes or No.", sep="\n")
showReleaseTag = input("Input here: ").lower()
if showReleaseTag == "yes":
    config['UPDATER']['show_updaterreleasetag'] = 'True'
    print("Changes saved.")
    logger.debug("Showing release tag in updater is ENABLED.")
elif showReleaseTag == "no":
    config['UPDATER']['show_updaterreleasetag'] = 'False'
    print("Changes saved.")
    logger.debug("Showing release tag in updater is DISABLED.")
else:
    print("Could not understand what you inputted.",
          "Defaulting to 'False'.", sep="\n")
    config['UPDATER']['show_updaterreleasetag'] = 'False'
    logger.debug("Could not understand input. Defaulting to DISABLED.")
    
print("")
print("That's it! Now commiting config changes...")
with open('storage//config.ini', 'w') as configfile:
    logger.debug("configfile: %s" % configfile)
    config.write(configfile)
    print("Changes committed!")
    logger.info("Performed operation: config.write(configfile)")

print("We're wrapping up, and performing a few tests.")

print("Checking for parsing libraries...")
try:
    import json
    logger.debug("json is available.")
except:
    logger.warn("json isn't available...that's odd.")
    print("json is not available. This is odd, it's a default library.",
    "Try installing a usual Python install.", sep="\n")
    printException()
    print("Press enter to exit.")
    input()
    sys.exit()
try:
    import codecs
    logger.debug("codecs is available.")
except:
    logger.warn("codecs isn't available. Here's the traceback:")
    printException_loggerwarn()
    print("codecs is not available. This is odd, it's a default library.",
    "Try installing a usual Python install.", sep="\n")
    printException()
    print("Press enter to exit.")
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
    print("We ran into an error. Make sure Wunderground's API is unblocked, and",
          "you have an internet connection.", sep="\n")
    printException()
    print("Press enter to exit.")
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
    printException()
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
    printException()
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
    print("We ran into an error. Make sure Google's Geolocator is unblocked,",
          "and you have an internet connection.", sep="\n")
    printException()
    print("Press enter to exit.")
    input()
    sys.exit()

print("""\nEverything is set up and ready to rumble!
Enjoy using PyWeather! If you have any issues, please report them on GitHub!
Press enter to continue.""")
input()
sys.exit()
