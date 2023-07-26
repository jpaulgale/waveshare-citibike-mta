import sys
import os
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')

from PIL import Image,ImageDraw,ImageFont,ImageOps
from datetime import datetime
import glob

sys.path.append('lib')
from waveshare_epd import epd5in83_V2
epd = epd5in83_V2.EPD()

epd.init()
epd.Clear()
