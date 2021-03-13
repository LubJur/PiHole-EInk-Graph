import epd2in13_V2
import time
import matplotlib.pyplot as plt
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

x_keys = 0
y_values = 0

def get_data():
    global x_keys
    global y_values
    domains = pihole.getGraphData()["domains"]  # options: domains or ads
    x_keys = domains.keys()
    x_keys = [*x_keys]
    y_values = domains.values()
    y_values = [*y_values]
    del(domains)
    return x_keys, y_values

def make_graph(x_keys, y_values):
    plt.figure(figsize=(1.911417, 0.9334646), dpi = 126, frameon = False)  # display size in inches (width, height) and DPI
    plt.tick_params(axis = "y", which = "both", right = False, width = 0.5, labelsize = 6)
    plt.tick_params(axis = "x", which = "both", top = False, bottom = False, labelbottom = False)
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

def show():
    image1 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    bmp = Image.open('line_plot.bmp')
    image1.paste(bmp, (0, 0))
    epd.display(epd.getbuffer(image1))

get_data()
first_values = y_values

try:
    make_graph(x_keys, y_values)
    show()
    while True:
        get_data()
        if first_values != y_values:
            make_graph(x_keys, y_values)
            show()
            first_values = y_values
        del(y_values)
        del(x_keys)
        time.sleep(300)  # 300s = 5 min
except KeyboardInterrupt:
    print("\nKeyboardInterrupt, clearing display")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd.sleep()
    epd.Dev_exit()