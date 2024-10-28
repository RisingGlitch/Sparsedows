import os
import sys
import plistlib
import click
import traceback

from pymobiledevice3.cli.cli_common import Command
from pymobiledevice3.exceptions import NoDeviceConnectedError, PyMobileDevice3Exception
from pymobiledevice3.lockdown import LockdownClient

from sparserestore import backup, perform_restore

if os.path.isfile("com.apple.MobileGestalt.plist") != True:
    print("Gestalt not present! Please make sure the Gesalt is in the same folder.")
    input("Press enter to exit... ")
    sys.exit()

getsaltFile = open("com.apple.MobileGestalt.plist", "r")
gestaltRawData = getsaltFile.read()
gestaltData = plistlib.loads(gestaltRawData.encode())

def applyBecomeiPadOS():
    keysToApply = ['uKc7FPnEO++lVhHWHFlGbQ','mG0AnH/Vy1veoqoLRAIgTA','UCG5MkVahJxG1YULbbd5Bg','ZYqko/XM5zD3XBfN5RmaXA','nVh/gwNpy7Jv1NOk00CMrw','qeaj75wk3HF4DwQ8qbIi7g']
    for x in keysToApply:
        gestaltData["CacheExtra"][x] = 1
        print("Set key " + str(x) + " to " + str(gestaltData["CacheExtra"][x]))

    applyChanges()

def revertBecomeiPadOS():
    keysToRemove = ['uKc7FPnEO++lVhHWHFlGbQ','mG0AnH/Vy1veoqoLRAIgTA','UCG5MkVahJxG1YULbbd5Bg','ZYqko/XM5zD3XBfN5RmaXA','nVh/gwNpy7Jv1NOk00CMrw','qeaj75wk3HF4DwQ8qbIi7g']
    for x in keysToRemove:
        gestaltData["CacheExtra"].pop(x)

        if x in gestaltData["CacheExtra"]:
            print("Failed to remove the key " + x)
        else:
            print("Removed key " + str(x))

    applyChanges()

def main():
    print("Gestalt Present!")
    print("Tool by _Systemless, DM me on discord if any error occurs, I am not responsable for any damage caused by this program!")

    print("1 - Bypass 3 App Limit")
    if 'uKc7FPnEO++lVhHWHFlGbQ' in gestaltData["CacheExtra"]:
        print("2 - Revert Become iPadOS")
    else:
        print("2 - Become iPadOS")

    usrSel = input("Enter choice: ")

    if usrSel == "2":
        if 'uKc7FPnEO++lVhHWHFlGbQ' in gestaltData["CacheExtra"]:
            revertBecomeiPadOS()
        else:
            applyBecomeiPadOS()
    if usrSel == "1":
        print("no")


def applyChanges():

    print("Would you like to apply these changes to your device? (y/n)")

    usrChoice = input("Enter choice: ")
    if usrChoice == "n":
        return
    elif usrChoice == "y":
        print("Locating device...")
    else:
        print("Please answer (y/n)")
        applyChanges()
        return

    print("Backing up orginal gestalt...")

    backupGestalt()

    print("Saving changes to new gestalt...")

    newGetsaltFile = open("com.apple.MobileGestalt.plist", "w")
    newGetsaltFile.write(plistlib.dumps(gestaltData).decode())
    newGetsaltFile.close()

    try:
        cli(standalone_mode=False)
    except NoDeviceConnectedError: 
        print("You do not have a connected device!")
        print("Reverting gestalt changes... ")
        revertChanges()
    except:
        print("The following error occured: ")
        print(traceback.format_exc())
        print("Reverting gestalt changes... ")
        revertChanges()

def backupGestalt():
    if os.path.isfile("com.apple.MobileGestalt-backup.plist") == True:
        print("Backup already present, overwrite backup? (y/n)")
        usrChoice = input("(y/n): ")
        if usrChoice == "n":
            if doContinueWithoutOverwritingBackup() == False:
                print("Exiting...")
                sys.exit()
        if usrChoice == "y":
            backup = open("com.apple.MobileGestalt-backup.plist", "w")
            backup.write(gestaltRawData)
            backup.close()
    else:
        backup = open("com.apple.MobileGestalt-backup.plist", "w")
        backup.write(gestaltRawData)
        backup.close()

def doContinueWithoutOverwritingBackup():
    print("Would you like to proceed without a backup? (y/n)")
    usrChoice = input("(y/n): ")
    if usrChoice == "y":
        return True
    elif usrChoice == "n":
        return False
    else:
        print("Please enter either y/n")
        return doContinueWithoutOverwritingBackup()
    
def revertChanges():
    backupData = open("com.apple.MobileGestalt-backup.plist", "r")
    data = open("com.apple.MobileGestalt.plist", "w")
    data.write(backupData.read())
    backupData.close()
    data.close()
    print("Finished reverting changes")


@click.command(cls=Command)
@click.pass_context
def cli(ctx, service_provider: LockdownClient) -> None:
    print("hi!")

main()
