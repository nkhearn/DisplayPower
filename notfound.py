#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd1in54
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import subprocess

def notfound():
  """
  This function executes the bash script 'emonip.sh'
  """
  try:
    subprocess.run(["bash", "emonip.sh"])
  except subprocess.CalledProcessError as error:
    print(f"Error: {error}")



logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd1in54 Demo")
    
    epd = epd1in54.EPD()
    logging.info("init and Clear")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    
    # read bmp file 
    logging.info("2.read bmp file...")
    image = Image.open(os.path.join(picdir, 'notfound.bmp'))
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    notfound()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd1in54.epdconfig.module_exit(cleanup=True)
    exit()
  
