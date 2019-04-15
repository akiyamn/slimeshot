from slimeshot import *


def main():
    ss = Slimeshot()

    message = ""
    httpstat = 0
    thisDir = os.path.dirname(os.path.realpath(__file__))

    # Key reset (-r)
    if args.reset and os.path.exists("key.txt"):
        if ss.promptYesOrNo("Do you really want to reset your key?"):
            os.remove("key.txt")
        else:
            print("Key was not deleted.")

    # Get key and send the request off to servers
    key = ss.getKey()
    if ss.clip():
        if not args.dryrun:
            req = ss.post(key)
            message = req.text
            httpstat = req.status_code
        else:
            message = "DRY RUN"

    # If a valid HTTP response is returned (200)
    if httpstat == 200:
        try:
            response = json.loads(message)
        except json.decoder.JSONDecodeError:
            ss.showError("Invalid JSON response was received back:\n" + message)

        if response["status"] == 0:  # Server returns successful status
            ss.clipboard(response["url"])
            ss.notify("Screenshot successful!", response["url"], thisDir + "/temp.png")
            if not args.silent:
                playsound("success.wav")
        # Server denies screenshot, show error
        else:
            ss.showError("Error Code: " + str(response["status"]) + "\n" + response["verbose"])
    # If an error HTTP is returned
    else:
        ss.showError("Server Returned HTTP Error Code: " + str(httpstat))


if __name__ == "__main__":
    main()
