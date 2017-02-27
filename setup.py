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
    coloramaInstalled = True
except ImportError:
    coloramaInstalled = False
    neededLibraries = neededLibraries + 1
    
try:
    import geopy
    geopyInstalled = True
except ImportError:
    geopyInstalled = False
    neededLibraries = neededLibraries + 1
    
try:
    import geocoder
    geocoderInstalled = True
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
print("Your email should be verified.")
print("Next, in your web browser, head back to https://www.wunderground.com/weather/api/.")
print("Then, click the 'Explore my Options' button, again.")
print("Press any key when you are done and ready.")
input()
print("Next, at the top of the page, make sure the button next to 'ANVIL PLAN' is selected.")
print("After that, confirm that the total underneath the 'Purchase Key' button says '$0 USD per month'")
print("If the total doesn't say that, in the pricing table, make sure the button next to 'Developer' is selected.")
print("Press any key when you are done and ready.")
input()
print("Next, click the 'Purchase Key' button, on top of your total (which should be $0 USD per month)")
print("Next, fill out the form, considering these tips:")
print("For the contact name/email, it's recommended you use your real name (first name last initial is fine).")
print("It's also recommended that you use your real email.")
print("For the project name, put in something generic, like 'to use a script that uses WU's API', or 'PyWeather user'")
print("For the project website, put in something generic, like 'google.com', or the homepage of PyWeather.")
print("Hint: The homepage of PyWeather is github.com/o355/py")
print("For the question 'Where will the API be used', answer Other.")
print("For the question 'Will the API be used for commercial use?', answer No.")
print("For the question 'Will the API be used for manufacturing mobile chip processing?', answer No.")
print("Answer yes if you somehow are manufacturing mobile chip processing. I doubt you are, however.")
print("For the country that you are based in, put your location.")
print("Before we move on, fill out these forms, and press any key when you are done and ready.")
input()
print("Next, for the brief description, put something like 'using an API key to use a script using Wunderground'.")
print("After that, check both boxes at the bottom of the page. Read the ToS if you feel like it.")
print("Finally, click 'Purchase Key'.")
print("You should land on a page that says 'Edit API Key'.")
print("Press any key when you are done and ready.")
input()
print("In the table to the left of the page, copy the text that's under Key ID. (Ctrl+C, right click)")
print("I'm now going to ask you to input the API key into the text entry below.")
print("The API key will be saved to storage/apikey.txt, so PyWeather can easily pull it up.")
print("Press any key when you are done and ready.")
input()
print("Please input your API key below.")
apikey_input = input("Input here: ")
print("Just to confirm, the API key you gave me was: " + apikey_input
      + ".")
print("Please double check your input, and confirm in the dialogue below.")
apikey_confirm = input("Is the API key right? Yes or no: ").lower()
if apikey_confirm == "no":
    print("Please input your API key below.")
    apikey_input = input("Input here: ")
    print("Just to confirm, the API key you gave me was: " + apikey_input
      + ".")
    print("If you got the API key wrong, please close out of setup, and try again. ")

print("Now saving your API key...")
with open("storage//apikey.txt", 'a') as out:
    out.write(apikey_input)
    out.close()
    
# once a config file is properly added, options for configuring the config will go here

print("We're wrapping up, and performing a few tests.")

print("Checking for parsing libraries...")
try:
    import json
except:
    print("json is not available. This is odd, it's a default library.")
    print("Try installing a usual Python install.")
    sys.exit()
try:
    import codecs
except:
    print("codecs is not available. This is odd, it's a default library.")
    print("Try installing a usual Python install.")
    sys.exit()

print("Testing the API connection, and seeing if the API key is valid...")
apitest_URL = 'http://api.wunderground.com/api/' + apikey_input + '/conditions/q/NY/New_York.json'
testreader = codecs.getreader("utf-8")

try:
    testJSON = urllib.request.urlopen(apitest_URL)
except:
    print("We ran into an error. Make sure Wunderground's API is unblocked, "
          + "and you have an internet connection.")
    sys.exit()
    
test_json = json.load(testreader(testJSON))

try:
    test_conditions = str(test_json['current_observation']['temp_f'])
except:
    print("We ran into an error. Make sure your API key is valid.")
    sys.exit()
    
print("Testing the Google geocoder connection...")

from geopy import GoogleV3
from geopy import Nominatim

geolocator = GoogleV3()
geolocator2 = Nominatim()

try:
    testlocation = geolocator.geocode("New York, NY", language="en")
    print("Yay! Google's geocoder works.")
except:
    print("We ran into an error. Make sure Google's geocoder is unblocked, " +
          "and you have an internet connection.")
    sys.exit()
    
print("Testing the Nominatim geocoder connection...")

try:
    testlocation2 = geolocator2.geocode("New York, NY")
    print("Yay! Nominatim's geocoder works.")
except:
    print("We ran into an error. Make sure Nominatim's geocoder is unblocked, " +
          "and you have an internet connection.")
    
print("Testing the reverse geocoder connection...")

try:
    testlocation3 = geocoder.google([testlocation.latitude, testlocation.longitude], method='reverse')
    print("Yay! The geolocator works.")
except:
    print("We ran into an error. Make sure Google's Geolocator is unblocked, " +
          "and you have an internet connection.")

print("")
print("Everything is set up and ready to rumble!")
print("Enjoy using PyWeather! If you have any issues, please report them on GitHub!")
sys.exit()


