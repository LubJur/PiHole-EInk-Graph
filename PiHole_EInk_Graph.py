from lib import epd2in13_V2
import time
from PIL import Image, ImageDraw, ImageFont
import pihole as ph
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", type=str, help="IP address of a system running PiHole", default="127.0.0.1")
piholeip = parser.parse_args()
"""
try:
    pihole = ph.PiHole(piholeip.a)
    pihole.refresh()
except OSError:
    print("This IP does not have a PiHole running")
    quit()
"""
epd = epd2in13_V2.EPD()
epd.init(epd.FULL_UPDATE)

image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
draw = ImageDraw.Draw(image)

def get_data():
    #pihole.refresh()
    #domains = pihole.getGraphData()["domains"]  # options: domains or ads
    domains = {'1534712100': 3, '1534712700': 87, '1534713300': 41, '1534713900': 45, '1534714500': 1, '1534715100': 28, '1534715700': 26, '1534716300': 0, '1534716900': 0, '1534717500': 0, '1534718100': 0, '1534718700': 0, '1534719300': 0, '1534719900': 0, '1534720500': 0, '1534721100': 0, '1534721700': 0, '1534722300': 0, '1534722900': 22, '1534723500': 5, '1534724100': 6, '1534724700': 2, '1534725300': 0, '1534725900': 3, '1534726500': 15, '1534727100': 1, '1534727700': 0, '1534728300': 0, '1534728900': 10, '1534729500': 8, '1534730100': 5, '1534730700': 0, '1534731300': 0, '1534731900': 0, '1534732500': 0, '1534733100': 0, '1534733700': 0, '1534734300': 0, '1534734900': 0, '1534735500': 0, '1534736100': 0, '1534736700': 0, '1534737300': 0, '1534737900': 0, '1534738500': 0, '1534739100': 0, '1534739700': 0, '1534740300': 0, '1534740900': 0, '1534741500': 0, '1534742100': 0, '1534742700': 0, '1534743300': 0, '1534743900': 0, '1534744500': 0, '1534745100': 0, '1534745700': 0, '1534746300': 0, '1534746900': 0, '1534747500': 0, '1534748100': 0, '1534748700': 0, '1534749300': 0, '1534749900': 0, '1534750500': 0, '1534751100': 0, '1534751700': 0, '1534752300': 0, '1534752900': 0, '1534753500': 0, '1534754100': 0, '1534754700': 0, '1534755300': 0, '1534755900': 0, '1534756500': 0, '1534757100': 0, '1534757700': 0, '1534758300': 0, '1534758900': 0, '1534759500': 0, '1534760100': 0, '1534760700': 0, '1534761300': 0, '1534761900': 0, '1534762500': 0, '1534763100': 0, '1534763700': 0, '1534764300': 0, '1534764900': 0, '1534765500': 0, '1534766100': 0, '1534766700': 0, '1534767300': 0, '1534767900': 0, '1534768500': 0, '1534769100': 0, '1534769700': 0, '1534770300': 0}
    values = [*domains.values()]
    del(domains)
    print(values)
    return values

def bar_graph(x1, y1, x2, y2, values):
    list_of_y = []
    list_of_x = []
    # another way to understand x1, y1,... is like this:
    # x1 = left offset
    # y1 = bottom offset
    # x2 = end of graph on x axis
    # y2 = end of graph on y axis
    # by combining them you can specify a rectangle of canvas with the graph
    space_orig = (x2-x1)/len(values)
    space = space_orig
    proportion = (y2-y1)/max(values) # direct proportion between the highest value and the height of display

    for i in values:
        y_value = i*proportion
        list_of_x.append(space+x1)
        list_of_y.append(abs(y_value - y2)) # this flips the value on y-axis
        space = space + space_orig

    for i in range(len(list_of_x)):
        # draws lines from bottom to the point
        draw.line([list_of_x[i],list_of_y[i] ,list_of_x[i], y2], width=1)

def line_graph(x1, y1, x2, y2, values):
    # beginning is the same as bar_graph
    space_orig = (x2-x1)/len(values)
    space = space_orig
    line_xy = []
    proportion =  (y2-y1)/max(values)

    for i in values:
        y_value = i*proportion
        line_xy.append(space + x1) 
        line_xy.append(abs(y_value - y2))  # this flips the value on y-axis
        space = space + space_orig

    draw.line(line_xy)

def y_axis(x1, y1, x2, y2, values):
    font = ImageFont.truetype("lib/JetBrainsMono-Regular.ttf", 9)
    draw.line([x1, y1, x2, y2], width=2)
    # anchors are there so the text is alignt to the left of the line
    # the font had to been a "truetype" for the anchor to work
    # for some reason they dont work on Pi zero so we flip text in show()
    draw.text([x1 + 1, y1], str(max(values)),font=font, anchor="rt")
    draw.text([x1 + 1, y2/2], str(int(max(values)/2)), font=font, anchor="rm")
    draw.text([x1 + 1, y2 - 9], str(min(values)), font=font, anchor="rb")

def show(image):
    #image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    image = image.transpose(method = Image.ROTATE_180)  # because anchor doesnt work
    epd.display(epd.getbuffer(image))
    print("som v show")

first_values = get_data()

try:
    values = get_data()
    bar_graph(0,5,225,120,values)
    y_axis(227, 5, 227, 120, values)
    show(image)
    while True:
        if first_values != values:
            print("Som tu 2")
            bar_graph(0,5,225,120,values)
            y_axis(227, 5, 227, 120, values)
            show(image)
            first_values = values
        del(values)
        time.sleep(300)  # 300s = 5 min
except KeyboardInterrupt:
    print("\nKeyboardInterrupt, clearing display")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd.sleep()
    epd.Dev_exit()
