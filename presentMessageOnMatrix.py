#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import os
import time
import argparse
from datetime import date
import json
import requests
#from currency_converter import CurrencyConverter

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

def startFeed():
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, width=32, height=8, rotate=0, block_orientation=-90)
    print("Created device")
    print("Showing rectangle")
    
    with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white")
    
    try:
        while(True):
            
            print("Parsing KONRAD-api")
            url = "http://94.255.156.221:1338"
            r = requests.get(url)
            json = r.json()["mailRecievedTable"]
            jsonLen = len(json)
            print(json)
            print(jsonLen)

            # Insert cool function

            printMessage = str(jsonLen)
            with canvas(device) as draw:
                #draw.rectangle(device.bounding_box, outline="white")
                text(draw, (0, 1), printMessage, fill="white", font=proportional(CP437_FONT))
                #text(draw, (0, 1), "73.93", fill="white", font=proportional(LCD_FONT))
            
            
            print("Sleep for 120 sec")
            time.sleep(120)
            print("Parse again!")
    except KeyboardInterrupt:
        print("Exiting program!")
        pass
    except:
        print("Failed to parse, trying again.")
        startFeed()
        pass

    
    #while(True):
        #d = datetime()
        #show_message(device, "193 mh/s", fill="white", font=proportional(LCD_FONT),scroll_delay=0.05)
        #show_message(device, "76.5 sek", fill="white", font=proportional(LCD_FONT),scroll_delay=0.05)
        #show_message(device, "1 Eth = 954 $", fill="white", font=proportional(LCD_FONT),scroll_delay=0.05)

if __name__ == "__main__":
    try:
        print("-> Starting program <-")
        startFeed()
    except:
        print("ERROR!")
        pass
