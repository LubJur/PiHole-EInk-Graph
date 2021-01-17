# PiHole-EInk-Graph
PiHole graph on a Waveshare 2.13" E-Ink display

## Technologies
* Python 3.8.7
* matplotlib
* PiHole 
* PiHole-api 2.6

## Dependencies
* Raspberry Pi (tested and developed on Raspberry Pi Zero WH, should work on others too)
* [Waveshare 2.13" E-Ink display V2](https://www.waveshare.com/2.13inch-e-paper-hat.htm)
    * For displays with other dimension you need to change sizes on lines 25 and 36
* [Waveshare e-Paper libraries](https://github.com/waveshare/e-Paper)
    * These libraries are already included in this repository
* matplotlib
* PiHole
* [PiHole-api](https://pypi.org/project/PiHole-api/)

## Setup
1. Install RaspberryPi OS (preferably the Lite version without desktop) on a RaspberryPi connected to the E-Ink display
2. Install [PiHole](https://pi-hole.net/) using command `curl -sSL https://install.pi-hole.net | bash`
3. Write down the **IP address** and **password** for the admin interface
4. Install matplotlib with `python -m pip install -U matplotlib`
5. Install PiHole-api with `pip install PiHole-api`
6. Open *PiHole_EInk_Graph.py* and rite your PiHole **IP address** between the quotation marks on line **8** and your **password** on line **11**
7. Run *PiHole_EInk_Graph.py* with `python3 PiHole_EInk_Graph.py`
8. If you want to exit the program you can press **Ctrl + C** which clears the E-Ink display and closes the application