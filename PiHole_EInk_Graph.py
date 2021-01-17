import epd2in13_V2
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import pihole as ph

#Write your PiHole IP between the quotation marks:
pihole = ph.PiHole("")

#Write your PiHole Password between the quotation marks:
pihole.authenticate("")

pihole.refresh()

epd = epd2in13_V2.EPD()
epd.init(epd.FULL_UPDATE)

def make_graph():
    domains = pihole.getGraphData()["domains"]  # options: domains or ads
    x_keys = domains.keys()
    x_keys = [*x_keys]
    y_values = domains.values()
    y_values = [*y_values]

    plt.figure(figsize=(1.911417, 0.9334646), dpi = 126, frameon = False)  # display size in inches (width, height) and DPI
    plt.tick_params(axis = "y", which = "both", right = False, width = 0.5, labelsize = 6)
    plt.tick_params(axis = "x", which = "both", top = False, bottom = False, labelbottom = False)
    plt.box(False)
    plt.title("Domains", size = "x-small")
    plt.plot(x_keys, y_values, color = "k", linewidth = 0.5)

    plt.savefig('line_plot.png', transparent = True, bbox_inches = "tight", pad_inches = 0)  

    img = Image.open("line_plot.png")
    img = img.convert('1')   
    img = img.resize((250, 122))  # display resolution (width, height), used when creating the .bmp
    img.save("line_plot.bmp") 

def show():
    image1 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    bmp = Image.open('line_plot.bmp')
    image1.paste(bmp, (0, 0))
    epd.display(epd.getbuffer(image1))

try:
    while True:
        print("Refreshed")
        make_graph()
        show()
        time.sleep(300)  # 900s = 15 min
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd.sleep()
    epd.Dev_exit()