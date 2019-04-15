from playsound import playsound
import os
import json

import src.slimeshot as ss
import src.io as io
from src.config import *


class SSDriver:

    def __init__(self):
        self.ss = ss.Slimeshot()

    def drive(self):
        if args.reset:
            self.resetKey()

        # Get key and send the request off to servers
        key = self.getKey()
        if self.ss.clip():
            if not args.dryrun:
                req = self.ss.post(key)
                self.handlePostReq(req)
            else:
                io.notify("Slimeshot", "Dry Run Complete", os.path.abspath(IMG_PATH))
                self.play(SOUND_PATH)

    def resetKey(self):
        # Key reset (-r)
        if os.path.exists(KEY_PATH):
            if io.promptYesOrNo("Do you really want to reset your key?"):
                os.remove(KEY_PATH)
            else:
                print("Key was not deleted.")
        else:
            print("Key not found, not deleted.")

    def getKey(self):
        thisDir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(thisDir)
        if os.path.exists(KEY_PATH):  # Reads key from key.txt if no errors
            try:
                keyFile = open(KEY_PATH, "rb")
                key = keyFile.read().decode().replace("\n", "")
                keyFile.close()
                return key
            except IOError as e:
                io.showError("IOError: " + e)
        else:  # Ask the user for a key and create new file if key.txt doesn't exist
            return self.askForKey()

    def handlePostReq(self, req):
        message = req.text
        httpstat = req.status_code
        response = {}
        # If a valid HTTP response is returned (200)
        if httpstat == 200:
            try:
                response = json.loads(message)
            except json.decoder.JSONDecodeError:
                io.showError("Invalid JSON response was received back:\n" + message)

            if response["status"] == 0:  # Server returns successful status
                self.ss.clipboard(response["url"])
                io.notify("Screenshot successful!", response["url"], os.path.abspath(IMG_PATH), args.quiet)
                self.play(SOUND_PATH)
            # Server denies screenshot, show error
            else:
                io.showError("Error Code: " + str(response["status"]) + "\n" + response["verbose"])
        # If an error HTTP is returned
        else:
            io.showError("Server Returned HTTP Error Code: " + str(httpstat))

    def askForKey(self):
        inputKey = input("A key.txt file was not found, so please enter your key: ")
        keyFile = open(KEY_PATH, "w")
        try:
            keyFile.write(inputKey)
            print("Key successfully written to key.txt file!")
            keyFile.close()
            return inputKey
        except IOError as e:
            io.showError("IOError: " + e)

    def play(self, sound):
        if not args.silent:
            playsound(sound)


if __name__ == "__main__":
    SSDriver().drive()
