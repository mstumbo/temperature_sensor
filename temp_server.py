import json
import time
import readadc
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse

parser = argparse.ArgumentParser(description='Simple tmp36 temperature sensor server.')
parser.add_argument("--port", "-p", dest="port", type=int, default=80, help='Port number to start the server on')  
args = parser.parse_args()

# temperature sensor middle pin connected channel 0 of mcp3008
sensor_pin = 0
readadc.initialize()

#the main sensor reading and plotting loop
def read_tmp36():
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
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode('{"value": %s}'%read_tmp36()))

httpd = HTTPServer(('0.0.0.0', args.port), SimpleHTTPRequestHandler)
httpd.serve_forever()

