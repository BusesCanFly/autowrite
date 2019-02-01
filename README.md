# Autowrite
Automate dd'ing and verifying SD cards

This tool is useful for when you need to flash many SD cards/drives with a certain .iso/.img/etc. Autowrite automatically detects all plugged in disks and starts flashing them with the specified image.

# GUIDE:

## Installation
1. Install dependencies: `sudo pip install -U argparse termcolor`
2. Download autowrite: `git clone https://github.com/BusesCanFly/autowrite`
3. Navigate to autowrite: `cd ./autowrite`
4. Make autowrite.py executable `chmod +x autowrite.py`
* One line variant: `sudo pip install -U argparse termcolor && git clone https://github.com/BusesCanFly/autowrite && cd ./autowrite && chmod +x autowrite.py`

## Images
Place desired image into `autowrite/images/`
* Examples: 
    * [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
    * [Kali](https://www.kali.org/downloads/)
    * [Ubuntu](https://www.ubuntu.com/download)

## Usage
```
usage: autowrite.py [-h] [-f IMAGE] [-v] [--rpi] [--validate] [--safe]

optional arguments:
  -h, --help            show this help message and exit
  -f IMAGE, --image IMAGE
                        Path to image to use
  -v                    Enable dd's status=progress
  --rpi                 Ignore /dev/sda
  --validate            Image the drive and compare it to the original image
  --safe                Print, not dd
```
* Example: `./autowrite.py -v -f ./images/raspbian.img --validate`
* If running autowrite on a raspberry pi, use the `--rpi` flag to prevent overwriting /dev/sda, the pi's internal SD card

## Disclaimer
_Be careful not to overwrite your host's main drive_

I am not responsible for anything that happens
