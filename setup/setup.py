# PyWeather Setup 0.3 beta
# (c) 2017, o355, licensed under GNU GPL v3


print("Welcome to PyWeather setup.")
print("This is meant to run as a one-time program, when you first get PyWeather.")
print("Running preflight...")

import sys
if sys.version_info[0] < 3:
    print("Shucks! I can't proceed any further.")
    print("You'll need to install Python 3 to use PyWeather/PW Setup.")
    sys.exit()

print("Before we get started, I want to confirm some permissions from you.")
print("Is it okay if I use 1-5 MB of data (downloading libraries)" +
      ", save a small text file called apikey.txt (> 2 KB)," +
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