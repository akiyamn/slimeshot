import os
import json

from .screenshot import *
import src.ssio as io
from .config import *


class SSDriver:
    """

    A class which drives an instance of the Screenshot class in screenshot.py

    Extends on the basic functionality of the Screenshot class by implementing ways of utilising the screenshot
    e.g. uploading it to a server, sending to the clipboard etc...

    The responsibility of this class is to handle the output of a given screenshot (an image) while also evoking
    appropriate I/O with the user. E.g. in the form of notification popups, sounds being played etc...

    """

    def __init__(self):
        self.ss = Screenshot()

    def drive(self):
        """
        Converts between the given command line arguments (specified in config.py) and the actions required to do so.
        Intended to be run as soon as the class is created.
        """

        # Reset when '-r' argument is given
        if args.reset:
            self.resetKey()

        # Get key and send the request off to the server
        key = self.getKey()
        error = self.ss.clip()

        if error == "":

            if args.clipboard:  # Just save to clipboard (-c)
                self.ss.imageToClipboard(IMG_PATH)
                io.notify("Screenshot successful!", "Image copied to clipboard.", IMG_PATH)
                io.play(SOUND_PATH)
            elif args.local:
                saveError = self.ss.saveLocally()
                io.notify("Screenshot successful!", "Image saved locally.", IMG_PATH)
            elif not args.dryrun:  # Default behaviour, sends a normal screenshot off to the server (no args)
                req = self.ss.post(key)
                self.handlePostReq(req)
            else:  # Just save to temporary image location (--dryrun)
                io.notify("Slimeshot", "Dry Run Complete", IMG_PATH)
                io.play(SOUND_PATH)

        else:  # Display the error given by maim
            io.showError('Failed to clip the specified region.\n' + error)

    def resetKey(self):
        """
        Clears the key.txt file after confirming the request from the user via the command line
        """
        if os.path.exists(KEY_PATH):
            if io.promptYesOrNo("Do you really want to reset your key?"):
                os.remove(KEY_PATH)
            else:
                print("Key was not deleted.")
        else:
            print("Key not found, not deleted.")

    def getKey(self):
        """
        Reads in the key used to upload to the screenshot server, asking for a new one via the command line if none is given.
        :return: the key as a string read in from the file or the user
        """
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
        """
        Handles a post request sent to the screenshot server, by interpreting the JSON sent back by the server,
        reacting accordingly and providing the user with the information.

        On a successful screenshot, the URL is given to the clipboard.
        On a failure, the user is notified of the specific error.
        :param req: a request object returned by a Screenshot.post() call which represents the inital send request
        """
        message = req.text
        httpstat = req.status_code
        response = {}

        # If a valid HTTP response is returned (200)
        if httpstat == 200:

            # Make sure response from server is valid JSON
            try:
                response = json.loads(message)
            except json.decoder.JSONDecodeError:
                io.showError("Invalid JSON response was received back:\n" + message)

            # On server returns successful status
            if response["status"] == 0:
                self.ss.clipboard(response["url"])
                io.notify("Screenshot successful!", response["url"], IMG_PATH, args.quiet)
                io.play(SOUND_PATH, args.silent)

            # Server denies screenshot, show error
            else:
                io.showError("Error Code: " + str(response["status"]) + "\n" + response["verbose"])

        # If a HTTP error is given
        else:
            io.showError("Server Returned HTTP Error Code: " + str(httpstat))

    def askForKey(self):
        """
        Ask the user for a key via the command line and create new file if key.txt doesn't exist.
        :return: the key string provided by the user
        """
        inputKey = input("A key.txt file was not found, so please enter your key: ")
        keyFile = open(KEY_PATH, "w")
        try:
            keyFile.write(inputKey)
            print("Key successfully written to key.txt file!")
            keyFile.close()
            return inputKey
        except IOError as e:
            io.showError("IOError: " + e)
