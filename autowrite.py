#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import argparse
from time import sleep
from termcolor import colored, cprint

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--image', type=str,
                    help='Path to image to use')
parser.add_argument('-v', dest='verbose', action='store_true',
                    help='Enable dd\'s status=progress')
parser.add_argument('--rpi', action='store_true',
                    help='Ignore /dev/sda')
parser.add_argument('--validate', action='store_true',
                    help='Image the drive and compare it to the original image')
parser.add_argument('--safe', action='store_true',
                    help='Print, not dd')
args = parser.parse_args()

global ignore
global verbose

if args.rpi:
        ignore=' | grep -v sda '
else:
	ignore=' '

if args.verbose:
        verbose=' status=progress '
else:
        verbose=' '

def find_and_flash():
	os.system("lsblk -i | grep disk | cut -d\  -f1 | grep -iE \"sd|mmcblk|hdd\""+ignore+" > ./devices.txt")

	list = './devices.txt'
	with open(list) as inf:
	                devices = [line.strip() for line in inf]

	os.system("rm ./devices.txt")
	i=0
	while i < len(devices):
		if not args.safe:
                        cprint("Starting write to /dev/"+devices[i], "yellow")
                        os.system("sudo dd bs=4M if="+args.image+" of=/dev/"+devices[i]+verbose+"conv=fsync")
                        cprint("Write complete", "yellow")
			sleep(1)
                        if args.validate:
                                count=raw_input("Enter the count from the initial dd to validate: ")
                                os.system("sudo dd bs=4M if=/dev/"+devices[i]+verbose+" of=./images/SDCARD.img count="+count)
                                cprint("Comparing disk image to original... ", "yellow")
                                os.system("diff -s ./images/SDCARD.img "+args.image)
				sleep(1)

	        else:
			cprint("Starting write to /dev/"+devices[i], "yellow")
			print("sudo dd bs=4M if="+args.image+" of=/dev/"+devices[i]+verbose+"conv=fsync")
			cprint("Write complete", "yellow")
			sleep(1)
			if args.validate:
				count=raw_input("Enter the count from the initial dd to validate: ")
				print("sudo dd bs=4M if=/dev/"+devices[i]+verbose+" of=./images/SDCARD.img count="+count)
				cprint("Comparing disk image to original... ", "yellow")
				print("diff -s ./images/SDCARD.img "+args.image)
				sleep(1)
		i+=1
find_and_flash()
