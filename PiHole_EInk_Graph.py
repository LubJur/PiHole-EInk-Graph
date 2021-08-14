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

image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
draw = ImageDraw.Draw(image)

epd = epd2in13_V2.EPD()
epd.init(epd.FULL_UPDATE)


def get_data():
    domains = pihole.getGraphData()["domains"]  # options: domains or ads
    values = [*domains.values()]
    del(domains)
    return values

def make_graph(x_keys, y_values):
    plt.figure(figsize=(1.911417, 0.9334646), dpi = 126, frameon = False)  # display size in inches (width, height) and DPI
    plt.tick_params(axis = "y", which = "both", right = False, width = 0.5, labelsize = 6)
    plt.tick_params(axis = "x", which = "both", top = False, bottom = False, labelbottom = False)
    plt.yticks(fontsize = 5.5)
    plt.box(False)
    plt.title("Domains", size = "x-small")
    plt.plot(x_keys, y_values, color = "k", linewidth = 0.005)
    plt.savefig('line_plot.png', transparent = True, bbox_inches = "tight", pad_inches = 0)  
    plt.close("all")
    plt.clf()
    img = Image.open("line_plot.png")
    img = img.convert('1')   
    img = img.resize((250, 122))  # display resolution (width, height), used when creating the .bmp
    img.save("line_plot.bmp") 

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

def show():
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    epd.display(epd.getbuffer(image))

get_data()

try:
    bar_graph(25,5,245,120,values)
    show()
    while True:
        get_data()
        if first_values != y_values:
            bar_graph(25,5,245,120,values)
            show()
            first_values = y_values
        del(y_values)
        time.sleep(300)  # 300s = 5 min
except KeyboardInterrupt:
    print("\nKeyboardInterrupt, clearing display")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd.sleep()
    epd.Dev_exit()