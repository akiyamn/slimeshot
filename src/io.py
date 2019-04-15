import subprocess
import sys


def promptYesOrNo(prompt):
    choice = input(prompt + " [y/N]: ")[0].capitalize()
    return choice == "Y"


# Sends a GNU/Linux notification via 'notify-send'
def notify(title, text="", icon="", quiet=False, error=False):
    if not quiet:
        subprocess.Popen(["notify-send", "-i", icon, title, text])
        if not error:
            print("[NOTIFY]\t" + title + " - " + text)


# Sends an error notification to the user via 'notify-send'
def showError(message):
    notify("Slimeshot Error!", message, error=True)
    print("[ERROR]\t" + message)
    sys.exit(1)