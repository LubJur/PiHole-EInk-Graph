import epd2in13_V2
import time
from PIL import Image, ImageDraw, ImageFont
import pihole as ph
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", type=str, help="IP address of a system running PiHole", default="127.0.0.1")
piholeip = parser.parse_args()

try:
    pihole = ph.PiHole(piholeip.a)
    pihole.refresh()
except OSError:
    print("This IP does not have a PiHole running")
    quit()

epd = epd2in13_V2.EPD()
epd.init(epd.FULL_UPDATE)

image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
draw = ImageDraw.Draw(image)

y_values = 0

def get_data():
    pihole.refresh()
    domains = pihole.getGraphData()["domains"]  # options: domains or ads
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

    epd.display(epd.getbuffer(image))

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

def show():
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    epd.display(epd.getbuffer(image))
    print("som v show")

y_values = get_data()
first_values = get_data()

try:
    bar_graph(25,5,245,120,get_data())
    print("Som tu 1")
    #show()
    while True:
        if first_values != get_data():
            print("Som tu 2")
            bar_graph(25,5,245,120,get_data())
            #show()
            first_values = y_values
        del(y_values)
        time.sleep(300)  # 300s = 5 min
except KeyboardInterrupt:
    print("\nKeyboardInterrupt, clearing display")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd.sleep()
    epd.Dev_exit()
