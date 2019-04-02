import json
import time
import readadc
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler


# see http://ww1.microchip.com/downloads/en/DeviceDoc/21295d.pdf for mcp 3008 data sheet
readadc.initialize()

#the main sensor reading and plotting loop
def read_tmp36(sensor_pin):
    sensor_data = readadc.readadc(sensor_pin,
                                  readadc.PINS.SPICLK,
                                  readadc.PINS.SPIMOSI,
                                  readadc.PINS.SPIMISO,
                                  readadc.PINS.SPICS)

    millivolts = sensor_data * (3300.0 / 1024.0)
    # 10 mv per degree
    temp_C = ((millivolts - 100.0) / 10.0) - 40.0
    # convert celsius to fahrenheit
    temp_F = (temp_C * 9.0 / 5.0) + 32
    # remove decimal point from millivolts
    millivolts = "%d" % millivolts
    # show only one decimal place for temprature and voltage readings
    temp_C = "%.1f" % temp_C
    temp_F = "%.1f" % temp_F

    # return the data
    return temp_C

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # ignore favicon
        if "favicon" in self.requestline:
            return
        try:
            sensor_pin = int(self.requestline.split()[1].split("/")[1])
            response = '{"value": %s}'%read_tmp36(sensor_pin)
        except ValueError: 
            response = "You must provide a sensor pin."
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode(response))

httpd = HTTPServer(('0.0.0.0', 80), SimpleHTTPRequestHandler)
httpd.serve_forever()

