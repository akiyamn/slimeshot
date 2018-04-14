# slimeshot.py

A simple screenshot script/program built for GNU/Linux which uploads to the [slimecorp.biz/i](http://slimecorp.biz/i) platform.
Written for the GNU/Linux platform, based on Python 3.6.

This program was inspired by the selective screenshot and upload feature of popular
Windows exclusive programs such as ShareX and puush.


## Basic Usage
Given execution permissions, simply:

`./slimeshot`

A file must be created in the main directory, called `key.txt`.
This file must include only one line, which is a valid keyFile
for the [slimecorp.biz/i](http://slimecorp.biz/i) platform to function correctly.

On the first launch, slimeshot will create a file named `key.txt` if it doesn't exist.


## Dependencies
### Packages
-   python3
-   maim
-   xclip
-   python3-pip (to install Python libs)

### Python Libs
-   request
-   playsound


## Installation

All packages shown above can be installed using the package manager relevent to your distro.
On Debain based systems this would be achieved by running:

`sudo apt-get install python3 maim xclip python3-pip`

Every "python lib" listed must be installed using pip. This can be done by running:

`pip3 install request playsound`

After downloading this git repository you may extract the file and run the program
as outlined above in the "Basic Usage" section.
