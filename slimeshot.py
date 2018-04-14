#!/usr/bin/python3

import subprocess
import requests
from playsound import playsound
import os
import sys

URL = 'http://slimecorp.biz/i/pics.php'


# Sends a GNU/Linux notification via 'notify-send'
def notify(title, text="", icon=""):
    subprocess.Popen(["notify-send", "-i", icon, title, text])


# Sends an error notification to the user via 'notify-send'
def showError(error):
    notify("Error", error)


# Sends 'data' to the clipboard
def clipboard(data):
    p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
    p.stdin.write(data.encode())
    p.stdin.close()


# Opens maim and allows the user to make a screenshot
## Returns whether the screenshot was successful
def clip():
    maim = subprocess.Popen(["maim", "-s", "temp.png"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = maim.communicate()
    err = err.decode()
    if err == "":
        return True
    else:
        showError("Error" , "Failed to clip the specified region.\n" + err)
        return False


# Sends a POST request to the screenshot server including the screenshot and the key
## Returns text sent back from the server
def post():
    with open("temp.png", "rb") as img:
        req = requests.post(URL, files={"photo": img}, data={"pass": key})
        img.close()
        return req.text


thisDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(thisDir)
if os.path.exists("key.txt"):   # Reads key from key.txt if no errors
    try:
        keyFile = open("key.txt", "rb")
        key = keyFile.read().decode().replace("\n","")
        keyFile.close()
    except IOError as e:
        showError("IOError: " + e)
else:   # Display error and create new file if key.txt doesn't exist
    showError("Please add a key to your key.txt file!")
    with open("key.txt", "w"): pass
    sys.exit(1)

message = ""
error = ""

if clip():
    message = post()

if message != "You fucked up." and message != "":   # Server returns successful status
    clipboard(message)
    notify("Screenshot successful!", message, thisDir + "/temp.png")
    playsound("success.wav")
else:   # Server denies screenshot, show error
    showError("Server failed to upload the screenshot.")
    sys.exit(1)
