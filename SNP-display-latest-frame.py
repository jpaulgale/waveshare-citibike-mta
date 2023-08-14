import sys
import os
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')
errordir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'error')

from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
import glob
import time

sys.path.append('lib')
from waveshare_epd import epd5in83_V2
epd = epd5in83_V2.EPD()

def get_latest_file(path, extension):
    # Get a list of all files that end with _snp-frame.png
    files = glob.glob(os.path.join(path, '*_snp-frame' + extension))

    # Define a function to convert a filename to a datetime object
    def filename_to_datetime(filename):
        base = os.path.basename(filename)
        date_str = base.split('_snp-frame')[0]
        return datetime.strptime(date_str, '%Y-%m-%d_%I%M%p')

    # Use max() function to find the latest (max) file
    latest_file = max(files, key=filename_to_datetime)

    return latest_file

# define funciton for writing image and sleeping for 5 min.
def write_to_screen(latest_file, sleep_seconds):
    print('Writing to screen.')
    # Write to screen
    h_image = Image.new('1', (epd.width, epd.height), 255)
    # Initialize the drawing context with template as background
    img = Image.open(latest_file)
    h_image.paste(img, (0, 0))
    img.close()
    epd.init()
    epd.display(epd.getbuffer(h_image))
    # Sleep
    time.sleep(2)
    epd.sleep()
    print('Sleeping for ' + str(sleep_seconds) +'.')
    time.sleep(sleep_seconds)

# define function for displaying error
def display_error(error_source):
    # Display an error
    print('Error in the', error_source, 'request.')
    # Initialize drawing
    error_image = Image.new('1', (epd.width, epd.height), 255)
    # Initialize the drawing
    draw = ImageDraw.Draw(error_image)
    draw.text((100, 150), error_source +' ERROR', font=font50, fill=black)
    draw.text((100, 300), 'Retrying in 30 seconds', font=font22, fill=black)
    current_time = datetime.now().strftime('%H:%M')
    draw.text((300, 365), 'Last Refresh: ' + str(current_time), font = font50, fill=black)
    # Save the error image
    error_image_file = 'error.png'
    error_image.save(os.path.join(errordir, error_image_file))
    # Close error image
    error_image.close()
    # Write error to screen 
    write_to_screen(error_image_file, 30)

# Set the fonts
font22 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 22)
font30 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 30)
font35 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 35)
font50 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 50)
font60 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 60)
font100 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 100)
font160 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 160)
# Set the colors
black = 'rgb(0,0,0)'
white = 'rgb(255,255,255)'
grey = 'rgb(235,235,235)'

# Initialize and clear screen
print('Starting initialization...')
epd.init()
print('Initialization done. Clearing screen...')
epd.Clear()
print('Screen cleared.')

path = '/home/pi/SNP_frame-image-generator/latest_images/'
extension = '.png'
latest_file = get_latest_file(path, extension)

# Change '300' to change sleep seconds 
write_to_screen(latest_file, 2)
