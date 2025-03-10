#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import requests
from datetime import datetime
import re
import subprocess
import logging
import time
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd1in54

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LIB_DIR = os.path.join(BASE_DIR, 'lib')
EMONPI_PATH = '/home/pi/emonpi'
NOTFOUND_SCRIPT_PATH = 'notfound.py'
DEJAVU_FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
EMONCMS_API_KEY = ""  # Define your emoncms API key here
EMONCMS_FEED_IDS = '32,9,18,19,44'  # Feed IDs as a string

# --- End Configuration ---

if os.path.exists(LIB_DIR):
    sys.path.append(LIB_DIR)

logging.basicConfig(level=logging.DEBUG)

try:
    with open(EMONPI_PATH, 'r') as file:
        emonip = file.read().strip()  # Read and remove trailing newline

    if not re.match(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", emonip):
        subprocess.run(["python", NOTFOUND_SCRIPT_PATH], check=True) # check=True will raise an error if the script fails.
        sys.exit()

    t = datetime.now().strftime('%H:%M')

    r = requests.get(f'http://{emonip}/feed/fetch.json?ids={EMONCMS_FEED_IDS}&apikey={EMONCMS_API_KEY}', timeout=10) # Added timeout
    r.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

    data = r.json()

    bal, volt, sol, ac, soli = round(data[0], 1), round(data[1], 1), bool(int(data[2])), bool(int(data[3])), bool(int(data[4]) > 1)

    print(bal)
    logging.info("epd1in54 Demo")

    epd = epd1in54.EPD()
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)

    image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)

    fonts = {
        65: ImageFont.truetype(DEJAVU_FONT_PATH, 65),
        50: ImageFont.truetype(DEJAVU_FONT_PATH, 50),
        75: ImageFont.truetype(DEJAVU_FONT_PATH, 75),
        35: ImageFont.truetype(DEJAVU_FONT_PATH, 35),
    }

    draw.text((3, 15), t, font=fonts[35], fill=0)
    draw.text((10, 65), str(bal), font=fonts[50], fill=0)
    draw.text((16, 120), str(volt), font=fonts[65], fill=0)

    face_char = u"\u2639" if volt < 23 else u"\u263a"
    draw.text((125, 1), face_char, font=fonts[75], fill=0)

    if sol:
        draw.text((133, 65), u"\u263c", font=fonts[65], fill=0)
    elif soli:
        draw.text((125, 65), u"\u263c", font=fonts[65], fill=0)
        draw.text((129, 65), u"\u2601", font=fonts[65], fill=0)
    else:
        draw.text((129, 55), u"\u2601", font=fonts[65], fill=0)

    if ac:
        draw.text((100, 65), u"\u26a1", font=fonts[65], fill=0)

    epd.display(epd.getbuffer(image.rotate(0)))
    time.sleep(2)

    logging.info("Goto Sleep...")
    epd.sleep()

except (IOError, requests.exceptions.RequestException, subprocess.CalledProcessError) as e: # Catch more specific Exceptions
    logging.error(f"An error occurred: {e}")

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd1in54.epdconfig.module_exit(cleanup=True)
    sys.exit()
    
