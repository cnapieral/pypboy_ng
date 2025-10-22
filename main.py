import pygame
import optparse
import sys
import config
import os
import platform

parser = optparse.OptionParser(usage='python %prog -c True\nor:\npython %prog -c True', version="0.0.1", prog=sys.argv[0])
parser.add_option('-c','--cached-map',        action="store_true", help="Loads the cached map file stored in map.cache", dest="load_cached", default=False)
options, args = parser.parse_args()

# Init framebuffer/touchscreen environment variables

system = platform.system()
if system == 'Linux':
# Auf Desktop-Linux: X11 bevorzugen; auf Pi (ohne X): fbcon erlauben
    if os.environ.get('DISPLAY'):  # Wenn X-Server läuft (Desktop)
        print("X-Server gefunden, verwende x11 Treiber")
        os.putenv('SDL_VIDEODRIVER', 'x11')
    else:
        print("Verwende fbcon Treiber")
        os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Nur für echten Pi ohne X
# elif system == 'Windows':
#     os.putenvos.putenv('SDL_VIDEODRIVER', 'windib')
# elif system == 'Darwin':  # macOS
#     os.putenvos.putenv('SDL_VIDEODRIVER', 'cocoa')

os.putenv('SDL_FBDEV'      , '/dev/fb1')
os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    config.GPIO_AVAILABLE = True
except Exception as e:
    print("GPIO UNAVAILABLE (%s)" % e)
    config.GPIO_AVAILABLE = False

from pypboy.core import Pypboy

try:
    pygame.mixer.init(44100, -16, 2, 2048)
    config.SOUND_ENABLED = True
except:
    config.SOUND_ENABLED = False

if __name__ == "__main__":
    boy = Pypboy('Pip-Boy 3000', config.WIDTH, config.HEIGHT)
    print("RUN")
    boy.run()