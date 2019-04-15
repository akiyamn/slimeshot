#!/usr/bin/python3

__version__ = "0.4.0"

import subprocess
import requests
import sys
import argparse

URL = 'https://slimecorp.biz/i/pics.php'
KEY_PATH = "../key.txt"
SOUND_PATH = "../assets/success.wav"
IMG_PATH = "../assets/temp.png"

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


class Slimeshot:
    # Sends 'data' to the clipboard
    def clipboard(self, data):
        p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
        p.stdin.write(data.encode())
        p.stdin.close()

    # Opens maim and allows the user to make a screenshot
    ## Returns whether the screenshot was successful
    def clip(self):
        maim = subprocess.Popen(["maim", "-s", IMG_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        maim.wait()
        out, err = maim.communicate()
        err = err.decode()
        if err == "":
            return True
        elif "right-click" in err:
            sys.exit(0)
        else:
            self.showError('Failed to clip the specified region.\n' + err)
        return False

    # Sends a POST request to the screenshot server including the screenshot and the key
    ## Returns text sent back from the server
    def post(self, key):
        with open(IMG_PATH, "rb") as img:
            req = requests.post(URL, files={"photo": img}, data={"pass": key})
            img.close()
            return req