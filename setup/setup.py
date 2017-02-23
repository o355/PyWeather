# PyWeather Setup 0.3 beta
# (c) 2017, o355, licensed under GNU GPL v3


print("Welcome to PyWeather setup.")
print("This is meant to run as a one-time program, when you first get PyWeather.")
print("Running preflight...")

import sys
import urllib.request
import shutil
import time
neededLibraries = 0
if sys.version_info[0] < 3:
    print("Shucks! I can't proceed any further.")
    print("You'll need to install Python 3 to use PyWeather/PW Setup.")
    sys.exit()

print("Before we get started, I want to confirm some permissions from you.")
print("Is it okay if I use 1-5 MB of data (downloading libraries)" +
      ", save a small text file called apikey.txt (> 2 KB)" +
      ", and automatically install Python libraries?")
print("Please input yes or no below:")
confirmPermissions = input("Input here: ").lower()
if confirmPermissions == "no":
    print("Okay! Closing now.")
    sys.exit()
elif confirmPermissions != "yes":
    print("I couldn't understand what you said.")
    print("As a precaution, I won't proceed any further.")
    sys.exit()
    
print("Cool! Let's start.")
print("I'm going to start by checking for necessary libraries (to run PyWeather).")
print("This can take a moment, so please hold tight while I check!")

try:
    import pip
except ImportError:
    print("Shucks! I need PIP to check for/install libraries.")
    print("Can I install PIP for you? Yes or No.")
    pipConfirm = input("Input here: ").lower()
    if pipConfirm == "no":
        print("Okay! I'm closing setup, as I need PIP to continue.")
        sys.exit()
    elif pipConfirm == "yes":
        print("Okay!")
        print("I'll download PIP's installer, and run it.")
        print("Doing such uses about 2-4 MB of data, and will quit PW setup.")
        print("When the setup script finishes, you'll need to run the setup script again.")
        print("I'll start in a few seconds.")
        time.sleep(3)
        print("Downloading the installer...")
        with urllib.request.urlopen('https://bootstrap.pypa.io/get-pip.py') as update_response, open('get-pip.py', 'wb') as update_out_file:
            shutil.copyfileobj(update_response, update_out_file)
        print("Running the installer...")
        exec(open("get-pip.py").read())
    else:
        print("I didn't understand what you said.")
        print("As a precaution, I'm closing setup, as I need PIP to continue.")

try:
    import colorama
except ImportError:
    coloramaInstalled = False
    neededLibraries = neededLibraries + 1
    
try:
    import geopy
except ImportError:
    geopyInstalled = False
    neededLibraries = neededLibraries + 1
    
try:
    import geocoder
except ImportError:
    geocoderInstalled = False
    neededLibraries = neededLibraries + 1
    
print("All done!")
if neededLibraries == 0:
    print("You must be magic. All necessary libraries are installed! Let's move on.")
else:
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
    if neededLibrariesConfirm == "no":
        print("Okay. I needed to install necessary libraries to continue.")
        print("Now quitting...")
        sys.exit()
    elif neededLibrariesConfirm == "yes":
        print("Sweet! I'm now installing necessary libraries.")
        if coloramaInstalled == False:
            print("Installing Colorama...")
            pip.main(['install', 'colorama'])
        if geopyInstalled == False:
            print("Installing geopy...")
            pip.main(['install', 'geopy'])
        if geocoderInstalled == False:
            print("Installing geocoder...")
            pip.main(['install', 'geocoder'])
        print("Sweet! All libraries should be installed.")
        print("Just to confirm, I'm double checking if needed libraries are installed.")
        try:
            import colorama
        except ImportError:
            print("Hmm...Colorama didn't install properly.")
            print("Try executing 'pip install colorama' in a command shell.")
            print("As a precaution, I'm now exiting. (Error 52, setup.py)")
            sys.exit()
        try:
            import geopy
        except ImportError:
            print("Hmm...geopy didn't install properly.")
            print("Try executing 'pip install geopy' in a command shell.")
            print("As a precaution, I'm now exiting. (Error 52, setup.py)")
            sys.exit()
        try:
            import geocoder
        except ImportError:
            print("Hmm...geocoder didn't install properly.")
            print("Try executing 'pip install geocoder' in a command shell.")
            print("As a precaution, I'm now exiting. (Error 52, setup.py)")
            sys.exit()
        print("All libraries are good to go! Let's move on.")
    else:
        print("I'm not sure what you said.")
        print("As a precaution, I'm now closing.")
        sys.exit()

print("I'm now going to guide you through obtaining an API key.")
print("Please carefully read my detailed instructions, so you don't mess anything up.")

print("Let's begin.")
print("")
print("Start by opening a web browser, and going to https://www.wunderground.com/weather/api/.")
print("Press any key when you are done.")
input()
print("")
print("Next, click the 'Explore my options' button.")
print("Press any key when you are done.")
input()
print("")
print("Next, click the small button next to 'ANVIL PLAN'.")
print("After that, confirm that the total underneath the 'Purchase Key' button says '$0 USD per month'")
print("If the total underneath the 'Purchase Key' button doesn't say '$0 USD per month, " +
      "please ensure that the small button next to 'Developer' on the table in the middle of the screen " +
      "is selected, and the total says '$0 USD per month'")
print("Press any key when you are done.")
input()
print("Next, click the 'Purchase Key' button.")
print("Press any key when you are done.")
input()
print("Next, input your email, and a password to sign up for a Weather Underground account.")
print("Be sure to select the checkbox next to 'I agree to the Terms of Service'")
print("It's best if you leave the checkbox next to 'I would like to receive WU updates via email' unchecked.")
print("Press any key when you are done and ready.")
input()
print("Next, press the 'Sign up for free' button.")
print("When the welcome window pops up, be sure to click the X button at the top right of the popup.")
print("When clicking the X, you should be redirected to wunderground.com.")
print("Press any key when you are done and ready.")
input()
print("Next, click 'My Profile' at the top right corner of the homepage.")
print("In the dropdown, click 'My Email & Text Alerts'")
print("Press any key when you are done and ready.")
input()
print("Next, next to your email listed on the page, click the 'Edit / Verify' button.")
print("After you click the button, click the 'Verify Email' button.")
print("Press any key when you are done and ready.")
input()
print("Next, check your email in which you signed up with.")
print("If you got a letter from Weather Underground, titled 'Daily Forecast Email Verification'" +
      ", open that letter, and click the link.")
print("If you didn't get the letter, wait a few minutes, and be sure to check your spam folder.")
print("Hint: If you followed this guide exactly, WU will not be sending you daily forecasts to your email.")
print("Press any key when you are done and ready.")
input()