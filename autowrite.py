#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import argparse
from time import sleep
from termcolor import colored, cprint

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--image', type=str,
                    help='Path to image to use')
parser.add_argument('--no-sda', action='store_true', dest='rpi',
                    help='Ignore /dev/sda')
parser.add_argument('--validate', action='store_true',
                    help='Image the drive and compare it to the original image')
parser.add_argument('--rpi', action='store_true',
		    help='Enable ssh and wpa_supplicant on boot (wpa_supplicant.conf from ~/images)')
args = parser.parse_args()

global ignore
if args.rpi:
        ignore=' | grep -v sda '
else:
	ignore=' '

main_color="yellow"
sub_color="green"
cprint("  ___  _   _ _____ _____  _    _______ _____ _____ _____ ", main_color)
cprint(" / _ \| | | |_   _|  _  || |  | | ___ \_   _|_   _|  ___|", main_color)
cprint("/ /_\ \ | | | | | | | | || |  | | |_/ / | |   | | | |__  ", main_color)
cprint("|  _  | | | | | | | | | || |/\| |    /  | |   | | |  __| ", main_color)
cprint("| | | | |_| | | | \ \_/ /\  /\  / |\ \ _| |_  | | | |___ ", main_color)
cprint("\_| |_/\___/  \_/  \___/  \/  \/\_| \_|\___/  \_/ \____/ ", main_color)
cprint("---------------------------------------------------------", main_color)
cprint("      BusesCanFly                        76 32 2e 30     ", sub_color)
cprint("---------------------------------------------------------", main_color)

cprint("\n\nLocating storage devices to write to...", "green")
os.system("lsblk -i | grep disk | cut -d\  -f1 | grep -iE \"sd|mmcblk|hdd\""+ignore+" > ./devices.txt")

list = './devices.txt'
with open(list) as inf:
                devices = [line.strip() for line in inf]
os.system("rm ./devices.txt")

cprint("NOTE: use --no-sda to prevent overwriting /dev/sda if that is your host disk!", "red")

c=0
cprint("\nLocated devices:", "yellow")
while c < len(devices):
	print("/dev/"+devices[c])
	c+=1
print(raw_input(colored("\nPress any key to proceed to imaging ", "green")))

i=0
while i < len(devices):
	start_msg = colored("Starting write to ", "green")+colored("/dev/"+devices[i], "yellow")
        print(start_msg)
        os.system("sudo dd bs=4M if="+args.image+" of=/dev/"+devices[i]+" status=progress conv=fsync")
        cprint("Write complete", "green")
        sleep(1)

        if args.validate:
	        count=raw_input(colored("\nEnter the number before \"+0 records out\" to validate: ", "yellow"))
	        os.system("sudo dd bs=4M if=/dev/"+devices[i]+" of=./images/VALIDATE.img status=progress count="+count)
	        cprint("Comparing disk image to original... ", "green")
	        os.system("diff -s ./images/VALIDATE.img "+args.image)
	        sleep(1)
	        os.system("rm ./images/VALIDATE.img")

        if args.rpi:
                print(raw_input(colored("\nUnplug and replug the device, then hit any key ", "green")))
                cprint("Setting up ssh and wpa_supplicant.conf", "green")
                sleep(1)
		cprint("Mounting boot partition (1)", "green")
		os.system("sudo mount /dev/"+devices[i]+"p1 ./MOUNT/ 2>/dev/null")
		os.system("sudo mount /dev/"+devices[i]+"1 ./MOUNT/ 2>/dev/null")
		cprint("Creating 'ssh' file", "green")
                os.system('touch ./MOUNT/ssh')
		cprint("Copying ./images/wpa_suplicant.conf to boot partition", "green")
                os.system('cp ./images/wpa_supplicant.conf ./MOUNT/')
		os.system('sudo umount ./MOUNT/')
		i+=1

print colored("\n\nDone :)\n\n", "magenta")
