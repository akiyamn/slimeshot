import subprocess
import sys
import os
from playsound import playsound

"""
This module provides interactivity with the user other than basic printing and input() calls.
"""

def promptYesOrNo(prompt):
    """
    Prompts the user via the command line for a yes or a no input.
    Will only take the letters y (yes) and n (no) as input. (case-insensitive)
    No is the default option if an invalid input is given.
    :param prompt: the text prompt given to the user before a decision
    :return: True is the choice was a 'yes' and False in all other circumstances
    """
    choice = input(prompt + " [y/N]: ")[0].capitalize()
    return choice == "Y"


def notify(title, text="", icon="", quiet=False, error=False):
    """
    Sends a notification to the user using the notify-send found on GNU/Linux operating systems.
    Takes basic arguments of this command.
    :param title: The title string to be displayed on the notification
    :param text: The text string to be displayed on the notification's body
    :param icon: An image (as a path string) to be displayed on the notification
    :param quiet: (default=False) bool if to notify of anything at all
    :param error: (default=False) bool if the notification should be treated as an error
    """
    if not quiet:
        subprocess.Popen(["notify-send", "-i", os.path.abspath(icon), title, text])
        if not error:
            print("[NOTIFY]\t" + title + " - " + text)


# Sends an error notification to the user via 'notify-send'
def showError(message):
    """
    Displays a critical error to the user via notify() which uses the notify-send GNU/Linux command.
    Exits the program on execution which status of 1.
    :param message: the string body of the error message
    """
    notify("Slimeshot Error!", message, error=True)
    print("[ERROR]\t" + message)
    sys.exit(1)


def play(sound, silent=False):
    """
    Plays a sound to the system using the playsound library
    :param sound: the path to the sound's location
    :param silent: (default=False) does not play sound
    """
    if not silent:
        playsound(sound)
