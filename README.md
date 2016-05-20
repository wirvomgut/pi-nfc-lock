# About

As a community we need to have a flexible key solution for our locks which are used by many. 
A normal key once lost needs to be replaced which might cost a lot and results in a lot of 
work. Using very cheap NFC Tags instead? Sounds good!

The Raspberry Pi in combination with a NFC Board actually provides a cost effective solution 
(< 100€). Also it is easy to setup and everybody in the community can learn a thing or two ;).

# What is needed?

## Hardware

- Raspberry Pi with enough GPIOs to support the NFC board
- EXPLORE-NFC-WW NFC board by element14
- card reader with support for micro or normal SD cards
- 5V micro usb charger (most android phones actually use those)
- relay which likes 5V
- door thingy which opens the lock when it gets the signal from the relay
- some patience to get the first working prototype going

## Software

- Raspbian OS (others might work too ofc)

# Setup 

## Hardware

Hopefully a guide is coming soon.

## Software

1. execute the following command: `sudo raspi-config`
2. go to Advanced Options > enable SPI and reboot
3. again in the terminal: 
```
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install nxppy
```
Please note that the last command might run for a long time as it  pulls down and builds 
NeardAL, WiringPi, and the NXP Reader Library from souce. Once finished you are ready to
use pi-nfc-lock!

# Usage

Download and extract or clone this repository. Execute pi-nfc-lock in the terminal: `sudo python pi-nfc-lock.py` 
Make sure that you are in the root directory of pi-nfc-lock. Once running it will show the uid of each NFC tag 
placed on the nfc board. Edit the list with known NFC tags in order to allow people to enter with their NFC tag.



