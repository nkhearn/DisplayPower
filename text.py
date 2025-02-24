#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import requests
# import subprocess
from datetime import datetime
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

#def run_script(script_path):
#  subprocess.run(["python", script_path])

with open('/home/pi/emonpi', 'r') as file:
    emonip = file.read()


import re
import subprocess

def check_ip_address(variable):
  """Checks if the given variable is an IP address.

  Args:
    variable: The variable to check.

  Returns:
    True if the variable is an IP address, False otherwise.
  """

  ip_address_pattern = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
  return re.match(ip_address_pattern, str(variable)) is not None

variable_to_check = emonip[:-1]

if check_ip_address(variable_to_check):
  # Continue with your code here
  print("IP address found:", variable_to_check)
else:
  # Call the external script and exit
  subprocess.run(["python", "notfound.py"])
  exit()


t = datetime.now().strftime('%H:%M')
bal = "0"
volt = "0"

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd1in54
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    
    r = requests.get('http://' + emonip[:-1] + '/feed/fetch.json?ids=32,9')
    dict = r.json()
    
    if r.status_code != 200:
        #import notfound
        subprocess.run(["python", "notfound.py"])
        exit()
        
    if bal == 0:
        bal = str("  + ")
    else:
        bal = str(round(dict[0],1))
    volt = str(round(dict[1],1))
    
    print(bal)
    logging.info("epd1in54 Demo")
    
    epd = epd1in54.EPD()
    logging.info("init and Clear")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    
    # Drawing on the image
    logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    
    draw = ImageDraw.Draw(image)
    # Volts font
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 65)
    # Balance font
    fontm = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 50)
    # Face font
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 75)
    #Time font
    fontsmall = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 35)
    # Time
    draw.text((3,15), t, font = fontsmall, fill = 0)
    # Balance
    draw.text((6, 65), bal, font = fontm, fill = 0)
    # Volts
    draw.text((16, 120), volt, font = font, fill = 0)
    # Face
    if float(volt) < 23:
        draw.text((125,1), u"\u2639", font = font2, fill=0)
    else:
        draw.text((125,1), u"\u263a", font = font2, fill=0)
    epd.display(epd.getbuffer(image.rotate(0)))
    time.sleep(2)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd1in54.epdconfig.module_exit(cleanup=True)
    exit()
  
