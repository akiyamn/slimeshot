#!/usr/bin/python3

__version__ = "0.4.0"

import subprocess
import requests
from playsound import playsound
import os
import sys
import argparse
import json

URL = 'https://slimecorp.biz/i/pics.php'

# Argument Parsing
parser = argparse.ArgumentParser(description="A simple Python-based screenshot program for slimecorp.biz/i.")
parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
parser.add_argument("-q", "--quiet", help="mutes all sound, text and notification output", action='store_true')
parser.add_argument("-r", "--reset", help="resets the key stored in key.txt to be empty", action='store_true')
parser.add_argument("--dryrun", help="takes a screenshot without uploading it", action='store_true')
parser.add_argument("--silent", help="disables audio output", action='store_true')
args = parser.parse_args()

if args.quiet:
    args.silent = True


# Prompts the user with a yes or no prompt (y/N) with 'no' being default
## Returns true if the input was 'yes' (y)
def promptYesOrNo(prompt):
    choice = input(prompt + " [y/N]: ")[0].capitalize()
    return choice == "Y"


# Sends a GNU/Linux notification via 'notify-send'
def notify(title, text="", icon="", error=False):
    if not args.quiet:
        subprocess.Popen(["notify-send", "-i", icon, title, text])
        if not error:
            print("[NOTIFY]\t" + title + " - " + text)


# Sends an error notification to the user via 'notify-send'
def showError(message):
    notify("Slimeshot Error!", message, error=True)
    print("[ERROR]\t" + message)
    sys.exit(1)


# Sends 'data' to the clipboard
def clipboard(data):
    p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
    p.stdin.write(data.encode())
    p.stdin.close()


# Opens maim and allows the user to make a screenshot
## Returns whether the screenshot was successful
def clip():
    maim = subprocess.Popen(["maim", "-s", "temp.png"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    maim.wait()
    out, err = maim.communicate()
    err = err.decode()
    if err == "":
        return True
    elif "right-click" in err:
        sys.exit(0)
    else:
        showError('Failed to clip the specified region.\n' + err)
    return False


# Sends a POST request to the screenshot server including the screenshot and the key
## Returns text sent back from the server
def post(key):
    with open("temp.png", "rb") as img:
        req = requests.post(URL, files={"photo": img}, data={"pass": key})
        img.close()
        return req


# Reading the key.txt file or prompting the user for one if none found
def getKey():
    thisDir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(thisDir)
    if os.path.exists("key.txt"):   # Reads key from key.txt if no errors
        try:
            keyFile = open("key.txt", "rb")
            key = keyFile.read().decode().replace("\n","")
            keyFile.close()
            return key
        except IOError as e:
            showError("IOError: " + e)
    else:   # Ask the user for a key and create new file if key.txt doesn't exist
        inputKey = input("A key.txt file was not found, so please enter your key: ")
        keyFile = open("key.txt", "w")
        try:
            keyFile.write(inputKey)
            print("Key successfully written to key.txt file!")
            keyFile.close()
            return inputKey
        except IOError as e:
            showError("IOError: " + e)

# Main body of the program
def init():
    message = ""
    httpstat = 0
    thisDir = os.path.dirname(os.path.realpath(__file__))

    # Key reset (-r)
    if args.reset and os.path.exists("key.txt"):
        if promptYesOrNo("Do you really want to reset your key?"):
            os.remove("key.txt")
        else:
            print("Key was not deleted.")

    # Get key and send the request off to servers
    key = getKey()
    if clip():
        if not args.dryrun:
            req = post(key)
            message = req.text
            httpstat = req.status_code
        else:
            message = "DRY RUN"

    # If a valid HTTP response is returned (200)
    if httpstat == 200:
        try:
            response = json.loads(message)
        except json.decoder.JSONDecodeError:
            showError("Invalid JSON response was received back:\n" + message)


        if response["status"] == 0:   # Server returns successful status
            clipboard(response["url"])
            notify("Screenshot successful!", response["url"], thisDir + "/temp.png")
            if not args.silent:
                playsound("success.wav")
        # Server denies screenshot, show error
        else:
            showError("Error Code: " + str(response["status"]) + "\n" + response["verbose"])
    # If an error HTTP is returned
    else:
        showError("Server Returned HTTP Error Code: " + str(httpstat))

init()
