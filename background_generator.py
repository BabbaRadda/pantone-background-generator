from screeninfo import *
from PIL import Image, ImageDraw, ImageFont
import re
import json
import random
import ctypes
import struct
import os
import time
 
class Monitor:

    def __init__(self,sizeStr,DPI):
        self.x = int(re.findall(r"(\d+)", sizeStr)[0])*DPI
        self.y = int(re.findall(r"(\d+)", sizeStr)[1])*DPI

class Colour:

    def __init__(self,code,name,r,g,b):
        self.code = code or null
        self.name = name or "Pantone Colour"
        self.r = r or 0
        self.g = g or 0
        self.b = b or 0

    def getRGB(self):
        return [self.r,self.g,self.b]

    def getHex(self):
        return '#%02x%02x%02x' % (self.r,self.g,self.b)

    def getName(self):
        return self.name
    
    def print(self):
        print('{}\n{}\nR:{} G:{} B:{}\nHex:{}'.format(self.code,self.name,self.r,self.g,self.b,self.getHex()))


def fetchCoated():
    with open('./assets/Coated.json') as f:
        return json.load(f)

def fetchUncoated():
    with open('./assets/Uncoated.json') as f:
        return json.load(f)

def storeColours():

    colours = []

    coated = fetchCoated()['colors']
    uncoated = fetchUncoated()['colors']

    for col in coated:
        colours.append(Colour(col['code'],col['name'],col['rgb']['r'],col['rgb']['g'],col['rgb']['b']))
    
    for col in uncoated:
        colours.append(Colour(col['code'],col['name'],col['rgb']['r'],col['rgb']['g'],col['rgb']['b']))

    return colours

def randomColour(colourArray):
    return colourArray[random.randint(0, len(colourArray)-1)]

def setAsBackground(path):
    
    SPI_SETDESKWALLPAPER = 20 

    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)    

    # if is_64bit_windows():
    # else:
    #     ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path, 0)
    
    
def is_64bit_windows():
    """Check if 64 bit Windows OS"""
    return struct.calcsize('P') * 8 == 64

def image(monitor,colour):
    imageName = '{}{}{}{}.jpg'.format(colour.code,colour.r,colour.g,colour.b).replace(' ','_')
    imagePath = os.getcwd()+'\\wallpapers\\'+imageName
    
    img = Image.new('RGB', (monitor.x, monitor.y), color = colour.getHex())
    
    drawFooter(img,monitor,colour)

    img.save(imagePath,quality=100)
    
    print("Setting New Pantone Background!\n")

    return imagePath

def drawFooter(image,monitor,colour):

    pos = [
        0,
        monitor.y*0.75,
        monitor.x,
        monitor.y
    ]

    draw = ImageDraw.Draw(image)
    draw.rectangle(pos, fill='white', outline=None)

    fontBold = ImageFont.truetype('./assets/helvetica-bold.ttf', 70)
    fontNormal = ImageFont.truetype('./assets/helvetica.ttf', 70)

    # draw text, half opacity
    draw.text(
        (pos[0]+(30*DPI),pos[1]+(30*DPI)), 
        "PANTONE", 
        font=fontBold, 
        fill=(0,0,0,255)
    )
    
    draw.text(
        (pos[0]+(30*DPI),pos[1]+(70*DPI)), 
        colour.code, 
        font=fontNormal, 
        fill=(0,0,0,255)
    )

    barTotal = (monitor.y*0.25)-200
    percR    = barTotal*((1.0/265.0) * float(colour.r+10))
    percG    = barTotal*((1.0/265.0) * float(colour.g+10))
    percB    = barTotal*((1.0/265.0) * float(colour.b+10))

    draw.rectangle(
        (
            pos[0]+250*DPI,
            pos[1]+30*DPI,
            pos[0]+270*DPI,
            (pos[1]+30*DPI)+(percR)
        ), 
        fill=(255,0,0,255), 
        outline=None
    )

    draw.rectangle(
        (
            pos[0]+270*DPI,
            pos[1]+30*DPI,
            pos[0]+290*DPI,
            (pos[1]+30*DPI)+(percG)
        ), 
        fill=(0,255,0,255), 
        outline=None
    )

    draw.rectangle(
        (
            pos[0]+290*DPI,
            pos[1]+30*DPI,
            pos[0]+310*DPI,
            (pos[1]+30*DPI)+(percB)
        ), 
        fill=(0,0,255,255), 
        outline=None
    )

DPI = 2  

# building monitor array
monitors = [Monitor(str(monitor),DPI)for monitor in get_monitors()]

colours = storeColours()

setAsBackground(
    image(
        monitors[0],
        randomColour(colours)
    )
)



