# This is the old, PyWeather Updater v2.
# I deleted this code as it was getting too complex and ambitious.

# This file is here for reference, and will be removed before 1.0.0 is released.

# Define the variable for if we had a corrupted updater package
# for auto-deletion
updater_corruptpackage = False
logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)

while True:
# If in a previous iteration we had a corrupted file, attempt to delete it here. The variables for the file name are already defined.

if updater_corruptpackage is True:
print("")
print(Fore.YELLOW + Style.BRIGHT + "The PyWeather Updater had to exit due to a corrupt updater package or a hash mismatch.",
      Fore.YELLOW + Style.BRIGHT + "If you'd like, I can try to delete the updater package, so when you update again more issues",
      Fore.YELLOW + Style.BRIGHT + "don't occur. Input yes or no to allow or deny the attempted deletion of the updater package.", sep="\n")
updater_deleteCorruptPackage = input("Input here: ").lower()
logger.debug("updater_deleteCorruptPackage: %s" % updater_deleteCorruptPackage)
if updater_deleteCorruptPackage == "yes":
    print("Attempting to delete the updater package.")
    # Define the filename variable depending on the updater method
    if updater_updatemethod == "new":
        updater_corruptfilename = updater_latestDirlessFileName
    elif updater_updatemethod == "old":
        updater_corruptfilename = updater_latestFileName

    logger.debug("updater_corruptfilename: %s" % updater_corruptfilename)

    try:
        os.remove(updater_corruptfilename)
    except os.error():
        print(Fore.YELLOW + Style.BRIGHT + "When attempting to delete the updater package, an error occurred. This could be due to bad permissions,",
              Fore.YELLOW + Style.BRIGHT + "a very corrupt file, or that the file has already been deleted or renamed.",
              Fore.YELLOW + Style.BRIGHT + "Press enter to return to the PyWeather Updater.", sep="\n")
        printException()
        input()
    except NameError:
        print(Fore.YELLOW + Style.BRIGHT + "When attempting to delete the updater package, an error occurred regarding missing variable data for the updater",
              Fore.YELLOW + Style.BRIGHT + "package name. Please attempt to delete the updater package yourself.",
              Fore.YELLOW + Style.BRIGHT + "Press enter to return to the PyWeather Updater.", sep="\n")
        printException()
        input()
    except:
        print(Fore.YELLOW + Style.BRIGHT + "An unknown error occurred when attempting to delete the updater package. Please try deleting the updater",
              Fore.YELLOW + Style.BRIGHT + "package yourself. Press enter to return to the PyWeather Updater.", sep="\n")
        printException()
        input()
elif updater_deleteCorruptPackage == "no":
    print(Fore.YELLOW + Style.BRIGHT + "Not deleting the updater package at this time. However, this may cause issues with updating PyWeather.")
else:
    print(Fore.YELLOW + Style.BRIGHT + "Your input could not be understood. Not deleting the updater package at this time. It's recommended you delete the",
          Fore.YELLOW + Style.BRIGHT + "file manually, as not doing such may cause issues with updating PyWeather.")

# At the start of every loop we need to fetch the updater branch to allow on-the-fly changes
spinner.start(text="Loading the PyWeather Updater...")
try:
updater_branch = config.get('UPDATER', 'branch')
spinner.stop()
except:
spinner.fail(text="Failed to load the updater! (a configuration error occurred)")
print("")
print(Fore.RED + Style.BRIGHT + "An error with your configuration file occurred when attempting to",
      Fore.RED + Style.BRIGHT + "load updater branch settings. Please make sure that your config file",
      Fore.RED + Style.BRIGHT + "is accessible, and that UPDATER/branch exists. Closing the updater.",
      sep="\n")
break

print("")
print(Fore.YELLOW + Style.BRIGHT + "Welcome to the PyWeather Updater. What would you like to do?",
  Fore.YELLOW + Style.BRIGHT + "- Check for updates & update PyWeather - Enter " + Fore.CYAN + Style.BRIGHT + "1",
  Fore.YELLOW + Style.BRIGHT + "- Change your update branch - Enter " + Fore.CYAN + Style.BRIGHT + "2",
  Fore.YELLOW + Style.BRIGHT + "- Info on the new updater - Enter " + Fore.CYAN + Style.BRIGHT + "3",
  Fore.YELLOW + Style.BRIGHT + "- Return to PyWeather - Enter " + Fore.CYAN + Style.BRIGHT + "4",
  sep="\n")
updater_mainmenu_input = input("Input here: ").lower()
logger.debug("updater_mainmenu_input: %s" % updater_mainmenu_input)
if updater_mainmenu_input == "1":
print(Fore.YELLOW + Style.BRIGHT + "Now checking for PyWeather updates.")

# Start the updater check process here - Also avoiding an indentation nightmare is a good thing to do
spinner.start(text="Checking for updates...")
try:
    updaterJSON = requests.get(
        "https://raw.githubusercontent.com/o355/pyweather/master/updater/versioncheck_V2.json")
    logger.debug("updaterJSON fetched with end result: %s" % updaterJSON)
except:
    spinner.fail(text="Failed to check for updates! (error occurred while fetching updater JSON)")
    print("")
    logger.warning("Couldn't check for updates! Is there an internet connection?")
    print(Fore.YELLOW + Style.BRIGHT + "When attempting to fetch the update data file, PyWeather",
          Fore.YELLOW + Style.BRIGHT + "ran into an error. If you're on a network with a filter,",
          Fore.YELLOW + Style.BRIGHT + "make sure that 'raw.githubusercontent.com' is unblocked. Otherwise,",
          Fore.YELLOW + Style.BRIGHT + "make sure that you have an internet connecction.", sep="\n")
    printException()
    continue

# Parse the updater JSON and get the release notes file - Dependent on branch!
updaterJSON = json.loads(updaterJSON.text)
if jsonVerbosity is True:
    logger.debug("updaterJSON: %s" % updaterJSON)
else:
    logger.debug("updaterJSON loaded.")

updater_releasenotesURL = updaterJSON['branch'][updater_branch]['releasenotesurl']
logger.debug("updater_releasenotesURL: %s" % updater_releasenotesURL)

# Fetch the updater notes URL, dependent on the URL as defined above
try:
    updater_releasenotes = requests.get(updater_releasenotesURL)
    logger.debug("updater_releasenotes fetched with end result: %s" % updater_releasenotes)
except:
    spinner.fail(text="Failed to check for updates! (error occurred while fetching release notes)")
    print("")
    logger.warning("Couldn't check for updates! Is there an internet connection?")
    print(Fore.YELLOW + Style.BRIGHT + "When attempting to fetch the release notes file, PyWeather",
          Fore.YELLOW + Style.BRIGHT + "ran into an error. If you're on a network with a filter,",
          Fore.YELLOW + Style.BRIGHT + "make sure that 'raw.githubusercontent.com' is unblocked. Otherwise,",
          Fore.YELLOW + Style.BRIGHT + "make sure that you have an internet connecction.", sep="\n")
    printException()
    continue

# Before parsing updater information, check to see if the user's branch is depreciated. If so, exit the updater
# and ask the user to change their branch.

updater_depreciated = updaterJSON['branch'][updater_branch]['depreciated']
# Make sure that the stable branch can never be depreciated.
if updater_depreciated == "True" and updater_branch != "stable":
    print(Fore.RED + Style.BRIGHT + "The updater branch you're on is unfortunately depreciated. As such, we cannot continue",
          Fore.RED + Style.BRIGHT + "to check for updates. Please change your branch by selecting option 2 at the updater main menu.",
          Fore.RED + Style.BRIGHT + "Press enter to return to the PyWeather Updater main menu.", sep="\n")
    input()
    continue

# Start parsing updater information - Also dependent on the branch

updater_buildNumber = float(updaterJSON['branch'][updater_branch]['latestbuild'])
updater_latestVersion = updaterJSON['branch'][updater_branch]['latestversion']
updater_latestTag = updaterJSON['branch'][updater_branch]['latestversiontag']
updater_latestFileName = updaterJSON['branch'][updater_branch]['latestfilename']
updater_latestDirlessFileName = updaterJSON['branch'][updater_branch]['latestdirlessfilename']
updater_latestReleaseTag = updaterJSON['branch'][updater_branch]['latestversiontag']
updater_latestReleaseDate = updaterJSON['branch'][updater_branch]['releasedate']
# Dirless is the default URL for the updater
updater_latestdirlessURL = updaterJSON['branch'][updater_branch]['latestdirlessurl']
# This is the URL for the .zip edition with a directory inside
updater_latestURL = updaterJSON['branch'][updater_branch]['latesturl']
updater_latestExtractDirectory = updaterJSON['branch'][updater_branch]['extractdirectory']
updater_latestMD5sum = updaterJSON['branch'][updater_branch]['md5sum']
updater_latestMD5dirlessSum = updaterJSON['branch'][updater_branch]['md5sum-dirless']
updater_latestSHA1sum = updaterJSON['branch'][updater_branch]['sha1sum']
updater_latestSHA1dirlessSum = updaterJSON['branch'][updater_branch]['sha1sum-dirless']
updater_latestSHA256sum = updaterJSON['branch'][updater_branch]['sha256sum']
updater_latestSHA256dirlessSum = updaterJSON['branch'][updater_branch]['sha256sum-dirless']
updater_nextversionReleaseDate = updaterJSON['branch'][updater_branch]['nextversionreleasedate']
updater_latestFileSize = updaterJSON['branch'][updater_branch]['size']
updater_latestDirlessFileSize = updaterJSON['branch'][updater_branch]['dirlesssize']
logger.debug("updater_buildNumber: %s ; updater_latestVersion: %s" %
             (updater_buildNumber, updater_latestVersion))
logger.debug("updater_latestTag: %s ; updater_latestFileName: %s" %
             (updater_latestTag, updater_latestFileName))
logger.debug("updater_latestReleaseTag: %s ; updater_latestReleaseDate: %s" %
             (updater_latestReleaseTag, updater_latestReleaseDate))
logger.debug("updater_latestdirlessURL: %s ; updater_latestURL: %s" %
             (updater_latestdirlessURL, updater_latestURL))
logger.debug("updater_latestExtractDirectory: %s ; updater_latestMD5sum: %s" %
             (updater_latestExtractDirectory, updater_latestMD5sum))
logger.debug("updater_latestMD5dirlessSum: %s ; updater_latestSHA1sum: %s" %
             (updater_latestMD5dirlessSum, updater_latestSHA1sum))
logger.debug("updater_latestSHA1dirlessSum: %s ; updater_latestSHA256sum: %s" %
             (updater_latestSHA1dirlessSum, updater_latestSHA256sum))
logger.debug("updater_latestSHA256dirlessSum: %s ; updater_nextversionReleaseDate: %s" %
             (updater_latestSHA256dirlessSum, updater_nextversionReleaseDate))
logger.debug("updater_latestFileSize: %s ; updater_latestDirlessFileSize: %s" %
             (updater_latestFileSize, updater_latestDirlessFileSize))
logger.debug("updater_latestdirlessFileName: %s" % updater_latestDirlessFileName)


if updater_branch == "rc":
    # Grab additional data about release state for RC branch users
    updater_RCreleaseflag = str(updaterJSON['branch'][updater_branch]['rcrelease'])
    updater_stablereleaseflag = str(updaterJSON['branch'][updater_branch]['stablerelease'])
    logger.debug("updater_RCreleaseflag: %s ; updater_stablereleaseflag: %s" %
                 (updater_RCreleaseflag, updater_stablereleaseflag))

spinner.stop()
if buildnumber >= updater_buildNumber:
    # If we're up to date, enter this dialogue.
    logger.info("PyWeather is up to date. Local build (%s) >= latest build (%s)." %
                (buildnumber, updater_buildNumber))
    print("")
    print(Fore.GREEN + Style.BRIGHT + "Your copy of PyWeather is up to date! :)")
    print(Fore.GREEN + Style.BRIGHT + "You have PyWeather version: " + Fore.CYAN + Style.BRIGHT + buildversion)
    print(Fore.GREEN + Style.BRIGHT + "The latest PyWeather version is: " + Fore.CYAN + Style.BRIGHT + updater_latestVersion)
    # User-defined options to show data.
    if user_showUpdaterReleaseTag is True:
        print(Fore.GREEN + Style.BRIGHT + "The latest release tag is: " + Fore.CYAN + Style.BRIGHT + updater_latestReleaseTag)
    if showNewVersionReleaseDate is True:
        print(Fore.GREEN + Style.BRIGHT + "A new version of PyWeather should come out in: " + Fore.CYAN + Style.BRIGHT + updater_nextversionReleaseDate)
    if showUpdaterReleaseNotes_uptodate is True:
        # Release notes get long, so ask to print the release notes if up to date.
        print("")
        print(Fore.GREEN + Style.BRIGHT + "Would you like to see the release notes for this release?",
              Fore.GREEN + Style.BRIGHT + "If so, enter 'yes' at the input below. Otherwise, press enter to continue.", sep="\n")
        updater_showReleaseNotesInput = input("Input here: ").lower()
        logger.debug("updater_showReleaseNotesInput: %s" % updater_showReleaseNotesInput)
        if updater_showReleaseNotesInput == "yes":
            print(Fore.GREEN + Style.BRIGHT + "Here's the release notes for this release:")
            # To make reading the release notes easier on the eyes, display it without color.
            print(releasenotes.text)

    print("")
    print(Fore.GREEN + Style.BRIGHT + "Press enter to return to the PyWeather Updater main menu.")
    input()
    continue

elif buildnumber < updater_buildNumber:
    logger.info("PyWeather is not up to date. Local build (%s) < latest build (%s)" %
                (buildnumber, updater_buildNumber))
    print("")
    print(Fore.RED + Style.BRIGHT + "Your copy of PyWeather isn't up to date! :(")
    print(Fore.RED + Style.BRIGHT + "You have PyWeather version: " + Fore.CYAN + Style.BRIGHT + buildversion)
    print(Fore.RED + Style.BRIGHT + "The latest PyWeather version is: " + Fore.CYAN + Style.BRIGHT + updater_latestVersion)
    if updater_branch == "rc":
        # If the updater branch is set to RC, display if this is a stable or RC release
        if updater_RCreleaseflag == "True":
            print(Fore.RED + Style.BRIGHT + "The latest version of PyWeather is a"
                  + Fore.CYAN + Style.BRIGHT + " RC"
                    + Fore.RED + Style.BRIGHT + " release.")
        elif updater_RCreleaseflag == "True":
            print(Fore.RED + Style.BRIGHT + "The latest version of PyWeather is a"
                  + Fore.CYAN + Style.BRIGHT + " Stable" + Fore.RED + Style.BRIGHT + " release.")
    # More user-defined things to show
    print(Fore.RED + Style.BRIGHT + "And it was released on: " + Fore.CYAN + Style.BRIGHT + updater_latestReleaseDate)
    if user_showUpdaterReleaseTag is True:
        print(Fore.RED + Style.BRIGHT + "The latest release tag is: " + Fore.CYAN + Style.BRIGHT + updater_latestReleaseTag)
    print(Fore.RED + Style.BRIGHT + "Update size: " + Fore.CYAN + Style.BRIGHT)
    if showUpdaterReleaseNotes is True:
        # Having a prompt to view the release notes is better given how long they can get.
        print("")
        print(Fore.RED + Style.BRIGHT + "Would you like to see the release notes for this release?",
              Fore.RED + Style.BRIGHT + "If so, enter 'yes' at the input below. Otherwise, press enter to continue.",
              sep="\n")
        updater_showReleaseNotesInput = input("Input here: ").lower()
        logger.debug("updater_showReleaseNotesInput: %s" % updater_showReleaseNotesInput)
        if updater_showReleaseNotesInput == "yes":
            print(Fore.RED + Style.BRIGHT + "Here's the release notes for this release:")
            # To make reading the release notes easier on the eyes, display it without color.
            print(releasenotes.text)

    print(Fore.YELLOW + Style.BRIGHT + "Would you like to update PyWeather automatically to the latest version?",
          Fore.YELLOW + Style.BRIGHT + "If you prefer to use the old .zip download method, enter 'oldyes' at the input.",
          Fore.YELLOW + Style.BRIGHT + "Yes, Oldyes or No.", sep="\n")
    updater_confirmupdate_input = input("Input here: ").lower()
    logger.debug("updater_confirmupdate_input: %s" % updater_confirmupdate_input)
    # Define what updater method we're going to use as we still allow .zip downloads. Convert the inputs to a method.
    updater_updatemethod = "new"
    if updater_confirmupdate_input == "yes":
        print(Fore.YELLOW + Style.BRIGHT + "Now automatically updating PyWeather.")
        updater_updatemethod = "new"
        logger.debug("updater_updatemethod: %s" % updater_updatemethod)
    elif updater_confirmupdate_input == "oldyes":
        print(Fore.YELLOW + Style.BRIGHT + "Now updating PyWeather using the old .zip download method.")
        updater_updatemethod = "old"
        logger.debug("updater_updatemethod: %s" % updater_updatemethod)
    elif updater_confirmupdate_input == "no":
        print(Fore.YELLOW + Style.BRIGHT + "Not updating PyWeather, and returning to the updater main menu.")
        continue
    else:
        print(Fore.YELLOW + Style.BRIGHT + "Couldn't understand your input. As a result,",
              Fore.YELLOW + Style.BRIGHT + "not updating PyWeather, and returning to the updater main menu.", sep="\n")
        continue

#
#   ||
#   ||      PyWeather Universal Updater
#   \/      version 0.0.0 indev - for PyWeather 0.6.4 beta
#           (c) 2018, o355 under the GNU GPL v3.0 license
#  -----
#

if updater_updatemethod == "new":
    # Set a timeout of 20 seconds for when we download.
    print(Fore.YELLOW + Style.BRIGHT + "Now updating PyWeather, this should only take a moment.")
    try:
        updatepackage = requests.get(updater_latestdirlessURL, stream=True, timeout=20)
    except requests.exceptions.ConnectionError:
        print("")
        print(Fore.RED + Style.BRIGHT + "When attempting to start the download of the update, an error",
              Fore.RED + Style.BRIGHT + "occurred. Make sure that you have an internet connection, and that",
              Fore.RED + Style.BRIGHT + "github.com is unblocked on your network. Press enter to return to the updater",
              Fore.RED + Style.BRIGHT + "main menu.", sep="\n")
        printException()
        input()
        continue

    # Get the total length of the file for the progress bar
    updater_package_totalLength = int(file.headers.get('content-length'))
    updater_package_totalLength = int(updater_package_totalLength / 1024)
    logger.debug("updater_package_totalLength: %s" % updater_package_totalLength)

    # Here's the actual updater loop
    with click.progressbar(length=updater_package_totalLength, label='Downloading') as bar:
        with open(updater_latestFileName, 'wb'):
            try:
                for chunk in updatepackage.iter_content(chunk_size=1024):
                    bar.update(1)
                    if chunk:
                        # I am truly sorry for how indented this is.
                        f.write(chunk)
                        f.flush()
            except requests.exceptions.ConnectionError:
                print("")
                print(Fore.RED + Style.BRIGHT + "When downloading update data, an error occurred.",
                      Fore.RED + Style.BRIGHT + "Please make sure you have an internet connection, and that",
                      Fore.RED + Style.BRIGHT + "github.com is unblocked on your network. Press enter to return",
                      Fore.RED + Style.BRIGHT + "to the updater main menu.", sep="\n")
                printException()
                input()
                continue

    # Now we verify. No progress bar here, unfortunately.

    # Define 3 hash types, md5, sha1, and sha256.
    hash_md5 = hashlib.md5()
    hash_sha1 = hashlib.sha1()
    hash_sha256 = hashlib.sha256()

    print("Verifying update data...")

    # Do the MD5 hash
    try:
        with open(updater_latestDirlessFileName, "rb") as f:
            # I did not Ctrl+C & Ctrl+V this off of Stack Overflow, trust me
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
            # Get the MD5 hash
            updater_package_md5hash = hash_md5.hexdigest()
            logger.debug("updater_package_md5hash: %s" % updater_package_md5hash)
    except:
        print("")
        # If there is a failed file load, exit to the main menu.
        print(Fore.RED + Style.BRIGHT + "Failed to load file to do a checksum verification.",
              Fore.RED + Style.BRIGHT + "Cannot continue as the file may be corrupt/non-existant.",
              Fore.RED + Style.BRIGHT + "Press enter to return to the updater main menu.", sep="\n")
        printException()
        input()
        updater_corruptpackage = True
        logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)
        continue

    # Verify the MD5 hash/sum/whatever you call it
    if updater_latestMD5dirlessSum != updater_package_md5hash:
        logger.warning("MD5 VERIFICATION FAILED! Checksum mismatch.")
        logger.debug("Expected sum (%s) was not sum of the download data (%s)" %
                     (updater_latestMD5dirlesssum, updater_package_md5hash))
        # While I would provide an option to continue even after a hash mismatch, I've devided not to.
        # Hash mismatches can corrupt PyWeather, so I've modeled apt and how it won't update repos or install
        # if a hash mismatch occurs.
        print("")
        print(Fore.RED + Style.BRIGHT + "Failed to verify the download data, a hash mismatch occurred.",
              Fore.RED + Style.BRIGHT + "Please try again at another time, or use a different connection.",
              Fore.RED + Style.BRIGHT + "Press enter to return to the updater main menu.", sep="\n")
        input()
        updater_corruptpackage = True
        logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)
        continue
    else:
        logger.debug("MD5 sum verified.")
        logger.debug("Expected sum (%s) was the sum of the download data (%s)" %
                     (updater_latestMD5dirlesssum, updater_package_md5hash))


    # Do the SHA1 hash
    try:
        with open(updater_latestDirlessFileName, "rb") as f:
            # I did not Ctrl+C & Ctrl+V this off of Stack Overflow, trust me
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha1.update(chunk)
            # Get the SHA1 hash
            updater_package_sha1hash = hash_sha1.hexdigest()
            logger.debug("updater_package_sha1hash: %s" % updater_package_sha1hash)
    except:
        print("")
        print(Fore.RED + Style.BRIGHT + "Failed to load file to do a checksum verification.",
              Fore.RED + Style.BRIGHT + "Cannot continue as the file may be corrupt/non-existant.",
              Fore.RED + Style.BRIGHT + "Press enter to return to the updater main menu.", sep="\n")
        printException()
        input()
        updater_corruptpackage = True
        logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)
        continue

    # Verify the SHA1 hash/sum/whatever you call it
    if updater_latestSHA1dirlessSum != updater_package_sha1hash:
        logger.warning("SHA1 VERIFICATION FAILED! Checksum mismatch.")
        logger.debug("Expected sum (%s) was not sum of the download data (%s)" %
                     (updater_latestSHA1dirlesssum, updater_package_sha1hash))
        print("")
        print(
            Fore.RED + Style.BRIGHT + "Failed to verify the download data, a hash mismatch occurred.",
            Fore.RED + Style.BRIGHT + "Please try again at another time, or use a different connection.",
            Fore.RED + Style.BRIGHT + "Press enter to return to the updater main menu.", sep="\n")
        input()
        updater_corruptpackage = True
        logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)
        continue
    else:
        logger.debug("SHA1 sum verified.")
        logger.debug("Expected sum (%s) was the sum of the download data (%s)" %
                     (updater_latestSHA1dirlesssum, updater_package_sha1hash))

    # Do the SHA256 hash
    try:
        with open(updater_latestDirlessFileName, "rb") as f:
            # I did not Ctrl+C & Ctrl+V this off of Stack Overflow, trust me
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
            # Get the SHA256 hash
            updater_package_sha256hash = hash_sha256.hexdigest()
            logger.debug("updater_sha256hash: %s" % updater_package_sha256hash)
    except:
        print("")
        print(Fore.RED + Style.BRIGHT + "Failed to load file to do a checksum verification.",
              Fore.RED + Style.BRIGHT + "Cannot continue as the file may be corrupt/non-existant.",
              Fore.RED + Style.BRIGHT + "Press enter to return to the updater main menu.", sep="\n")
        printException()
        input()
        updater_corruptpackage = True
        logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)
        continue

    # Verify the SHA256 hash/sum/whatever you call it
    if updater_latestSHA256dirlessSum != updater_package_sha256hash:
        logger.warning("SHA256 VERIFICATION FAILED! Checksum mismatch.")
        logger.debug("Expected sum (%s) was not sum of the download data (%s)" %
                     (updater_latestSHA256dirlesssum, updater_package_sha256hash))
        print("")
        print(Fore.RED + Style.BRIGHT + "Failed to verify the download data, a hash mismatch occurred.",
            Fore.RED + Style.BRIGHT + "Please try again at another time, or use a different connection.",
            Fore.RED + Style.BRIGHT + "Press enter to return to the updater main menu.", sep="\n")
        input()
        updater_corruptpackage = True
        logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)
        continue
    else:
        logger.debug("SHA256 sum verified.")
        logger.debug("Expected sum (%s) was the sum of the download data (%s)" %
                     (updater_latestSHA256dirlesssum, updater_package_sha256hash))

    print("Update data verified. Extracting...")
    try:
        zf = zipfile.ZipFile(updater_latestDirlessFileName)
    except zipfile.BadZipFile:
        print("")
        print(Fore.RED + Style.BRIGHT + "Failed to load the updater .zip file, a bad zip file error occurred.",
              Fore.RED + Style.BRIGHT + "The updater package could be corrupt or has bad permissions.",
              Fore.RED + Style.BRIGHT + "Press enter to return to the updater main menu.", sep="\n")
        printException()
        input()
        updater_corruptpackage = True
        logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)
        continue
    except:
        print("")
        print(Fore.RED + Style.BRIGHT + "An error occurred when loading the .zip file. The updater",
              Fore.RED + Style.BRIGHT + "could be corrupt, have bad permissions, or could have been deleted.",
              Fore.RED + Style.BRIGHT + "Press enter to return to the updater main menu.", sep="\n")
        printException()
        input()
        updater_corruptpackage = True
        logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)
        continue

    try:
        for file in zf.namelist():
            zf.extract(file, "")
    except:
        print("")
        print(Fore.RED + Style.BRIGHT + "An error ocurred when extracting the contents of the updater .zip",
              Fore.RED + Style.BRIGHT + "file. The updater could be corrupt, have bad permissions, or could",
              Fore.RED + Style.BRIGHT + "have been deleted. Press enter to return to the updater main menu.", sep="\n")
        printException()
        input()
        updater_corruptpackage = True
        logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)
        continue

    print("Update extracted. Launching configuration updater...")
    try:
        exec(open("configupdate.py").read())
    except:
        print(Fore.RED + Style.BRIGHT + "An error occurred when attempting to launch the configupdate.py",
              Fore.RED + Style.BRIGHT + "script to update your configuration file. The script may not exist,",
              Fore.RED + Style.BRIGHT + "or it might be corrupt. Press enter to return to the updater main menu.", sep="\n")
        printException()
        input()
        # No corrupt updater package, here we only deal with the config updating script.
        continue

    # Delete the updater .zip file
    print(Fore.YELLOW + Style.BRIGHT + "If you would like to, the now unnecessary updater file can be automatically deleted for you.",
          Fore.YELLOW + Style.BRIGHT + "Would you like to have the updater file %s deleted for you? Yes or No." % updater_latestDirlessFileName, sep="\n")
    updater_deleteupdaterfile = input("Input here: ").lower()
    logger.debug("updater_deleteupdaterfile: %s" % updater_deleteupdaterfile)
    if updater_deleteupdaterfile == "yes":
        print(Fore.YELLOW + Style.BRIGHT + "Now deleting the updater file.")
        try:
            os.remove(updater_latestDirlessFileName)
        except:
            print(Fore.YELLOW + Style.BRIGHT + "Failed to delete the updater file. The file could no longer exist, have bad permissions,",
                  Fore.YELLOW + Style.BRIGHT + "or be corrupt.", sep="\n")
    elif updater_deleteupdaterfile == "no":
        print(Fore.YELLOW + Style.BRIGHT + "Not deleting the updater file.")
    else:
        print(Fore.YELLOW + Style.BRIGHT + "Your input could not be understood. The updater file will not be deleted automatically.")

    # We're now done, exit PyWeather
    print(Fore.YELLOW + Style.BRIGHT + "PyWeather is now up-to-date. To complete the updater process, PyWeather needs to be shut down.",
          Fore.YELLOW + Style.BRIGHT + "Please press enter to shut down PyWeather.", sep="\n")
    input()
    sys.exit()

elif updater_updatemethod == "old":
    # The old updater, but improved with hash matching and the new progress bar.
    print(Fore.YELLOW + Style.BRIGHT + "Downloading the latest version of PyWeather. This should only take a moment.")
    try:
        updatepackage = requests.get(updater_latestURL, stream=True, timeout=20)
    except requests.exceptions.ConnectionError:
        print("")
        print(Fore.RED + Style.BRIGHT + "When attempting to start the download of the update, an error",
              Fore.RED + Style.BRIGHT + "occurred. Make sure that you have an internet connection, and that",
              Fore.RED + Style.BRIGHT + "github.com is unblocked on your network. Press enter to return to the updater",
              Fore.RED + Style.BRIGHT + "main menu.", sep="\n")
        printException()
        input()
        continue

    # Get the total length of the file for the progress bar
    updater_package_totalLength = int(file.headers.get('content-length'))
    updater_package_totalLength = int(updater_package_totalLength / 1024)
    logger.debug("updater_package_totalLength: %s" % updater_package_totalLength)

    with click.progressbar(length=updater_package_totalLength, label='Downloading') as bar:
        with open(updater_latestFileName, 'wb'):
            try:
                for chunk in updatepackage.iter_content(chunk_size=1024):
                    bar.update(1)
                    if chunk:
                        # I am truly sorry for how indented this is.
                        f.write(chunk)
                        f.flush()
            except requests.exceptions.ConnectionError:
                print("")
                print(Fore.RED + Style.BRIGHT + "When downloading update data, an error occurred.",
                      Fore.RED + Style.BRIGHT + "Please make sure you have an internet connection, and that",
                      Fore.RED + Style.BRIGHT + "github.com is unblocked on your network. Press enter to return",
                      Fore.RED + Style.BRIGHT + "to the updater main menu.", sep="\n")
                printException()
                input()
                continue

    # Now we verify with md5, sha1, and sha256. For the old download method if a hash mismatch occurs
    # the user can skip (and optionally view the checksums), as it's their responsibility if a corruption
    # occurs.

    # Define the 3 hash types
    hash_md5 = hashlib.md5()
    hash_sha1 = hashlib.sha1()
    hash_sha256 = hashlib.sha256()

    print("Verifying update data...")

    # MD5 hash verification

    try:
        with open(updater_latestFileName, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
            # Get the MD5 hash
            updater_package_md5hash = hash_md5.hexdigest()
            logger.debug("updater_package_md5hash: %s" % updater_package_md5hash)
    except:
        print("")
        # If there is a failed file load, exit to the main menu regardless.
        print(Fore.RED + Style.BRIGHT + "Failed to load .zip to do a checksum verification.",
              Fore.RED + Style.BRIGHT + "Cannot continue as the .zip may be corrupt/non-existant.",
              Fore.RED + Style.BRIGHT + "Press enter to return to the updater main menu.", sep="\n")
        printException()
        input()
        updater_corruptpackage = True
        logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)
        continue

        # I completely understand how absurdly long this input dialogue is. Oh well.
    if updater_latestMD5sum != updater_package_md5hash:
        logger.warning("MD5 VERIFICATION FAILED! Checksum mismatch.")
        logger.debug("Expected sum (%s) was not sum of the download data (%s)" %
                     (updater_latestMD5sum, updater_package_md5hash))
        # Ask the user if they'd like to continue updating. To view the checksums the user has
        # to include "view sums" in their input. Instead of exact input checking we do a find.
        print("")
        print(Fore.RED + Style.BRIGHT + "When attempting to verify the updater package, a hash mismatch occurred.",
              Fore.RED + Style.BRIGHT + "Despite this, would you like to continue to download the latest .zip file?",
              Fore.RED + Style.BRIGHT + "Yes or No. To view checksums, put 'view sums' to your input.")
        updater_zipMD5verify_input = input("Input here: ").lower()
        logger.debug("updater_zipMD5verify_input: %s" % updater_zipMD5verify_input)
        # See if we have a user selection before we enter into 'view sums'.
        if updater_zipMD5verify_input.find("yes") == 0 or updater_zipMD5verify_input.find("no") == 0:
            updater_zipMD5verify_selection = True
        else:
            updater_zipMD5verify_selection = False

        logger.debug("updater_zipMD5verify_selection: %s" % updater_zipMD5verify_selection)

        if updater_zipMD5verify_input.find("view sums") == 0:
            print("")
            print(Fore.YELLOW + Style.BRIGHT + "Here's the checksums for MD5 verification.")
            print(Fore.YELLOW + Style.BRIGHT + "Original checksum: " + updater_latestMD5sum)
            print(Fore.YELLOW + Style.BRIGHT + "Local checksum: " + updater_package_md5hash)
            print("")

            if updater_zipMD5verify_selection is False:
                # If the user didn't have a selection and only entered view sums
                print(Fore.YELLOW + Style.BRIGHT + "Would you like to continue downloading the latest .zip file?",
                      Fore.YELLOW + Style.BRIGHT + "Yes or No.", sep="\n")
                updater_zipMD5verify_input("Input here: ").lower()
                logger.debug("updater_zipMD5verify_input: %s" % updater_zipMD5verify_input)

        # In a separate if block, run the input checking.

        if updater_zipMD5verify_input.find("yes") == 0:
            print(Fore.YELLOW + Style.BRIGHT + "Continuing with the .zip download.")
        elif updater_zipMD5verify_input.find("yes") == 0:
            print(Fore.YELLOW + Style.BRIGHT + "Stopping the .zip download, and returning to the PyWeather Updater main menu.",
                  Fore.YELLOW + Style.BRIGHT + "Please consider deleting the corrupt .zip file, as not doing so may cause",
                  Fore.YELLOW + Style.BRIGHT + "additional issues to occur.", sep="\n")
            continue
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Could not understand your input. Stopping the .zip download, and returning to the",
                  Fore.YELLOW + Style.BRIGHT + "PyWeather Updater main menu. Please consider deleting the corrupt .zip file, as not doing",
                  Fore.YELLOW + Style.BRIGHT + "so may cause additional issues to occur.", sep="\n")
            continue


    else:
        logger.debug("MD5 sum verified.")
        logger.debug("Expected sum (%s) was the sum of the download data (%s)" %
                     (updater_latestMD5sum, updater_package_md5hash))

    # Get SHA1 sum

    try:
        with open(updater_latestFileName, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha1.update(chunk)
            # Get the SHA1 hash
            updater_package_sha1hash = hash_sha1.hexdigest()
            logger.debug("updater_package_sha1hash: %s" % updater_package_sha1hash)
    except:
        print("")
        # If there is a failed file load, exit to the main menu regardless.
        print(Fore.RED + Style.BRIGHT + "Failed to load .zip to do a checksum verification.",
              Fore.RED + Style.BRIGHT + "Cannot continue as the .zip may be corrupt/non-existant.",
              Fore.RED + Style.BRIGHT + "Press enter to return to the updater main menu.", sep="\n")
        printException()
        input()
        updater_corruptpackage = True
        logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)
        continue

    # Verify SHA1 sum

    if updater_latestSHA1sum != updater_package_SHA1hash:
        logger.warning("SHA1 VERIFICATION FAILED! Checksum mismatch.")
        logger.debug("Expected sum (%s) was not sum of the download data (%s)" %
                     (updater_latestSHA1sum, updater_package_sha1hash))
        # Ask the user if they'd like to continue updating. To view the checksums the user has
        # to include "view sums" in their input. Instead of exact input checking we do a find.
        print("")
        print(Fore.RED + Style.BRIGHT + "When attempting to verify the updater package, a hash mismatch occurred.",
              Fore.RED + Style.BRIGHT + "Despite this, would you like to continue to download the latest .zip file?",
              Fore.RED + Style.BRIGHT + "Yes or No. To view checksums, put 'view sums' to your input.")
        updater_zipSHA1verify_input = input("Input here: ").lower()
        logger.debug("updater_zipSHA1verify_input: %s" % updater_zipSHA1verify_input)
        # See if we have a user selection before we enter into 'view sums'.
        if updater_zipSHA1verify_input.find("yes") == 0 or updater_zipSHA1verify_input.find("no") == 0:
            updater_zipSHA1verify_selection = True
        else:
            updater_zipSHA1verify_selection = False

        logger.debug("updater_zipSHA1verify_selection: %s" % updater_zipSHA1verify_selection)

        if updater_zipSHA1verify_input.find("view sums") == 0:
            print("")
            print(Fore.YELLOW + Style.BRIGHT + "Here's the checksums for SHA1 verification.")
            print(Fore.YELLOW + Style.BRIGHT + "Original checksum: " + updater_latestSHA1sum)
            print(Fore.YELLOW + Style.BRIGHT + "Local checksum: " + updater_package_sha1hash)
            print("")

            if updater_zipSHA1verify_selection is False:
                # If the user didn't have a selection and only entered view sums
                print(Fore.YELLOW + Style.BRIGHT + "Would you like to continue downloading the latest .zip file?",
                      Fore.YELLOW + Style.BRIGHT + "Yes or No.", sep="\n")
                updater_zipSHA1verify_input("Input here: ").lower()
                logger.debug("updater_zipSHA1verify_input: %s" % updater_zipSHA1verify_input)

        # In a separate if block, run the input checking.

        if updater_zipSHA1verify_input.find("yes") == 0:
            print(Fore.YELLOW + Style.BRIGHT + "Continuing with the .zip download.")
        elif updater_zipSHA1verify_input.find("yes") == 0:
            print(Fore.YELLOW + Style.BRIGHT + "Stopping the .zip download, and returning to the PyWeather Updater main menu.",
                  Fore.YELLOW + Style.BRIGHT + "Please consider deleting the corrupt .zip file, as not doing so may cause",
                  Fore.YELLOW + Style.BRIGHT + "additional issues to occur.", sep="\n")
            continue
        else:
            print(Fore.YELLOW + Style.BRIGHT + "Could not understand your input. Stopping the .zip download, and returning to the",
                  Fore.YELLOW + Style.BRIGHT + "PyWeather Updater main menu. Please consider deleting the corrupt .zip file, as not doing",
                  Fore.YELLOW + Style.BRIGHT + "so may cause additional issues to occur.", sep="\n")
            continue
    else:
        logger.debug("SHA1 sum verified.")
        logger.debug("Expected sum (%s) was the sum of the download data (%s)" %
                     (updater_latestSHA1sum, updater_package_sha1hash))

    # Get SHA256 sum

    try:
        with open(updater_latestFileName, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
            # Get the SHA256 hash
            updater_package_sha256hash = hash_sha256.hexdigest()
            logger.debug("updater_package_sha256hash: %s" % updater_package_sha256hash)
    except:
        print("")
        # If there is a failed file load, exit to the main menu regardless.
        print(Fore.RED + Style.BRIGHT + "Failed to load .zip to do a checksum verification.",
              Fore.RED + Style.BRIGHT + "Cannot continue as the .zip may be corrupt/non-existant.",
              Fore.RED + Style.BRIGHT + "Press enter to return to the updater main menu.", sep="\n")
        printException()
        input()
        updater_corruptpackage = True
        logger.debug("updater_corruptpackage: %s" % updater_corruptpackage)
        continue

    # Verify SHA256 sum

    if updater_latestSHA256sum != updater_package_SHA256hash:
        logger.warning("SHA256 VERIFICATION FAILED! Checksum mismatch.")
        logger.debug("Expected sum (%s) was not sum of the download data (%s)" %
                     (updater_latestSHA256sum, updater_package_sha256hash))
        # Ask the user if they'd like to continue updating. To view the checksums the user has
        # to include "view sums" in their input. Instead of exact input checking we do a find.
        print("")
        print(
            Fore.RED + Style.BRIGHT + "When attempting to verify the updater package, a hash mismatch occurred.",
            Fore.RED + Style.BRIGHT + "Despite this, would you like to continue to download the latest .zip file?",
            Fore.RED + Style.BRIGHT + "Yes or No. To view checksums, put 'view sums' to your input.")
        updater_zipSHA256verify_input = input("Input here: ").lower()
        logger.debug("updater_zipSHA1verify_input: %s" % updater_zipSHA256verify_input)
        # See if we have a user selection before we enter into 'view sums'.
        if updater_zipSHA256verify_input.find("yes") == 0 or updater_zipSHA256verify_input.find("no") == 0:
            updater_zipSHA256verify_selection = True
        else:
            updater_zipSHA256verify_selection = False

        logger.debug("updater_zipSHA256verify_selection: %s" % updater_zipSHA256verify_selection)

        if updater_zipSHA256verify_input.find("view sums") == 0:
            print("")
            print(Fore.YELLOW + Style.BRIGHT + "Here's the checksums for SHA256 verification.")
            print(Fore.YELLOW + Style.BRIGHT + "Original checksum: " + updater_latestSHA256sum)
            print(Fore.YELLOW + Style.BRIGHT + "Local checksum: " + updater_package_sha256hash)
            print("")

            if updater_zipSHA256verify_selection is False:
                # If the user didn't have a selection and only entered view sums
                print(Fore.YELLOW + Style.BRIGHT + "Would you like to continue downloading the latest .zip file?",
                      Fore.YELLOW + Style.BRIGHT + "Yes or No.", sep="\n")
                updater_zipSHA256verify_input("Input here: ").lower()
                logger.debug("updater_zipSHA256verify_input: %s" % updater_zipSHA256verify_input)

        # In a separate if block, run the input checking.

        if updater_zipSHA256verify_input.find("yes") == 0:
            print(Fore.YELLOW + Style.BRIGHT + "Continuing with the .zip download.")
        elif updater_zipSHA256verify_input.find("yes") == 0:
            print(
                Fore.YELLOW + Style.BRIGHT + "Stopping the .zip download, and returning to the PyWeather Updater main menu.",
                Fore.YELLOW + Style.BRIGHT + "Please consider deleting the corrupt .zip file, as not doing so may cause",
                Fore.YELLOW + Style.BRIGHT + "additional issues to occur.", sep="\n")
            continue
        else:
            print(
                Fore.YELLOW + Style.BRIGHT + "Could not understand your input. Stopping the .zip download, and returning to the",
                Fore.YELLOW + Style.BRIGHT + "PyWeather Updater main menu. Please consider deleting the corrupt .zip file, as not doing",
                Fore.YELLOW + Style.BRIGHT + "so may cause additional issues to occur.", sep="\n")
            continue
    else:
        logger.debug("SHA256 sum verified.")
        logger.debug("Expected sum (%s) was the sum of the download data (%s)" %
                     (updater_latestSHA256sum, updater_package_sha256hash))

    print(Fore.YELLOW + Style.BRIGHT + "The latest version of PyWeather has been downloaded to the base directory of PyWeather,",
          Fore.YELLOW + Style.BRIGHT + "and has been saved as: " + Fore.CYAN + Style.BRIGHT + updater_latestFileName +
          Fore.YELLOW + Style.BRIGHT + ".", Fore.YELLOW + Style.BRIGHT + "Returning to the updater main menu.", sep="\n")
    continue


else:
    print(Fore.RED + Style.BRIGHT + "A critical error has occured, an updater method has not been defined internally.",
          Fore.RED + Style.BRIGHT + "Please try to update PyWeather again. If the issue persists please report this issue",
          Fore.RED + Style.BRIGHT + "on GitHub (github.com/o355/pyweather). Returning to the updater main menu.")

# Updater branch updating is here.
elif updater_mainmenu_input == "2":
# Hit the updater API and see if the user's branch is out of date.
spinner.start(text="Checking branch information...")
try:
    updater_branchJSON = requests.get("https://raw.githubusercontent.com/o355/pyweather/master/updater/versioncheck_V2.json")
    logger.debug("updater_branchJSON fetched with end result: %s" % updater_branchJSON)
    spinner.stop()
except:
    spinner.fail(text="Failed to check for branch information! (error occurred while fetching updater JSON)")
    print("")
    logger.warning("Couldn't check for branch info! Is there an internet connection?")
    print(Fore.YELLOW + Style.BRIGHT + "When attempting to query the updater API, PyWeather ran",
          Fore.YELLOW + Style.BRIGHT + "into an error. If you're on a network with a filter, make sure",
          Fore.YELLOW + Style.BRIGHT + "that 'raw.githubusercontent.com' is unblocked. Otherwise, make sure that",
          Fore.YELLOW + Style.BRIGHT + "you have an internet connection.", sep="\n")
    printException()
    continue

# Load the JSON
updater_branchJSON = json.loads(updater_branchJSON.text)
if jsonVerbosity is True:
    logger.debug("updater_branchJSON: %s" % updater_branchJSON)
else:
    logger.debug("updater_branchJSON loaded successfully.")

updater_availbranches = updater_branchJSON['info']['availbranches']

# Define vars & arrays beforehand
supportedBranches = []
depreciatedBranches = []
userBranch_depreciated = False
logger.debug("supportedBranches: %s ; depreciatedBranches: %s" %
             (supportedBranches, depreciatedBranches))
logger.debug("userBranch_depreciated: %s" % userBranch_depreciated)

# Loop through the available branches, make arrays as to supported branches and depreciated branches.
# Also check if the user's branch is depreciated

for branch in updater_availbranches:
    branchDepreciatedFlag = ['branch'][branch]['depreciated']
    logger.debug("branchDepreciatedFlag: %s" % branchDepreciatedFlag)

    if branchDepreciatedFlag == "True":
        depreciatedBranches.append(branch)
    elif branchDepreciatedFlag == "False":
        supportedBranches.append(branch)


    if updater_branch == branch and branchDepreciatedFlag is True:
        userBranch_depreciated = True
        logger.debug("userBranch_depreciated: %s" % userBranch_depreciated)

print(Fore.YELLOW + Style.BRIGHT + "The branch that you're currently on is: " + Fore.CYAN + Style.BRIGHT + updater_branch)
if userBranch_depreciated is True:
    print(Fore.RED + Style.BRIGHT + "** Warning ** : The branch you're currently on is depreciated. Please select a new branch",
          Fore.RED + Style.BRIGHT + "to get the latest Pyweather updates.", sep="\n")

print("")
print(Fore.YELLOW + Style.BRIGHT + "Would you like to pick a new branch for the updater? Yes or No.")
updater_confirmBranchChange = input("Input here: ").lower()
logger.debug("updater_confirmBranchChange: %s" % updater_confirmBranchChange)
if updater_confirmBranchChange == "yes":
    logger.debug("beginning branch update process.")
elif updater_confirmBranchChange == "no":
    print(Fore.YELLOW + Style.BRIGHT + "Cancelling the branch updating process, and returning to the main menu.")
    continue
else:
    print(Fore.YELLOW + Style.BRIGHT + "Could not understand your input. Cancelling the branch updating process,",
          Fore.YELLOW + Style.BRIGHT + "and returning to the main menu.", sep="\n")
    continue

# List out not depreciated branches
print(Fore.YELLOW + Style.BRIGHT + "From the list below, please input a branch you'd like to use.",
      Fore.YELLOW + Style.BRIGHT + "You can also define a branch to use that isn't on the list.", sep="\n")
# Just show the supported branches in raw variable style
print(Fore.YELLOW + supportedBranches)
print("")
print(Fore.YELLOW + Style.BRIGHT + "Please enter the branch you'd like to switch to below.")
updater_userBranchInput = input("Input here: ").lower()
logger.debug("updater_userBranchInput: %s" % updater_userBranchInput)

# Define a config write function
def updater_configwrite():
    try:
        with open('storage//config.ini', 'w') as configfile:
            config.write(configfile)
        print(Fore.YELLOW + Style.BRIGHT + "Changes saved. Returning to the updater main menu.")
        return
    except:
        print(Fore.RED + Style.BRIGHT + "Failed to write to the config file. This could be caused by bad",
              Fore.RED + Style.BRIGHT + "permissions, or the file missing. Returning to the updater main menu.",
              Fore.RED + Style.BRIGHT + "If this continues, try running configupdate.py.")
        return

# If the user is on a supported branch
for branch in supportedBranches:
    if updater_userBranchInput == branch:
        print(Fore.YELLOW + Style.BRIGHT + "Successfully switched to the %s branch.", branch)
        config['UPDATER']['branch'] = branch
        updater_configwrite()
        continue

# Warn the user if they're on a depreciated branch
for branch in depreciatedBranches:
    if updater_userBranchInput == branch:
        print(Fore.RED + Style.BRIGHT + "The branch you selected to use is depreciated. Would you still",
              Fore.RED + Style.BRIGHT + "like to use this branch anyways? Yes or No.", sep="\n")
        updater_yourbranchisdepreciatedInput = input("Input here: ").lower()
