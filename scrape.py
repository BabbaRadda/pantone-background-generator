import json
import requests
from lxml import html
import re

class Colour:

    def __init__(self,name,r,g,b):
        self.name = name
        self.r = r or 0
        self.g = g or 0
        self.b = b or 0

    def getRGB(self):
        return [self.r,self.g,self.b]

    def getHex(self):
        return '#{}{}{}'.format(hex(self.r)[-2:],hex(self.g)[-2:],hex(self.b)[-2:])

    def getName(self):
        return self.name

def scrape():

    colours = []

    # request header properties like (user agent) text
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

    # iterating over all fetched cells
    for cell in html.fromstring(requests.get("https://www.pantone-colours.com/",headers=headers).content).xpath('//tr/td'):
        if 'style' in cell.attrib:
            rgb = re.findall(r"(\d+)", cell.attrib['style'])[-3:]
            if len(rgb) > 2 and (rgb[0] != rgb[1] and rgb[1] != rgb[2] and rgb[0] != rgb[2]) :                
                text = re.sub(r"\n|\xa0",'',str(cell.find('div/small').text))[:-2]
                colours.append(Colour(text,int(rgb[0]),int(rgb[1]),int(rgb[2])))

    return colours


def createStore(colours):

    data = {}
    data['colours'] = []

    for colour in colours:
        data['colours'].append(
            {
                "name" : colour.name,
                "hex"  : colour.getHex(),
                "r"    : colour.r,
                "g"    : colour.g,
                "b"    : colour.b
            })
    
    with open('colours.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=False)
    
createStore(scrape())