#!/usr/bin/env python3

from jsread import jsread
from settings import *
import argparse
import sys
sys.path.append("../atp")
from channel import Channel
import socket
import pyinotify
import re
import time
from threading import Thread

class SpeedOrder(Thread):

    # TODO : utiliser un mutex sur x et y, et utiliser une condition dans le run

    def __init__(self, asserv, delay = DELAY):
        super().__init__()
        self.asserv = asserv
        self.delay = delay
        self.x = 0
        self.old_x = 0
        self.y = 0
        self.old_y = 0
        self.z = 0
        self.old_z = 0

    def update(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def run(self):
        while True:
            time.sleep(self.delay)
            if self.x != self.old_x or self.y != self.old_y or self.z != self.old_z:
                self.old_x = self.x
                self.old_y = self.y
                self.old_z = self.z
                self.send_command(self.x, self.y, self.z)

    def send_command(self, _x, _y, _z):
        print(_x, _y, _z)
        from math import floor, ceil
        x = (_x * Xmax) / 32767
        y = (_y * Ymax) / 32767
        z = (_z * Zmax) / 65536 + Zmax / 2

        left = - round((80 * (y + x)) / (80 + abs(x)))
        right = - round((80 * (y - x)) / (80 + abs(x)))
        z = round(z)

        #print(left, right, angle)
        print("[%+3d %+3d] (%4d)" %(right, left, z))
        #self.asserv.speed(self.x, self.y)

class Processor:
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((HOST, PORT+5))
        self.asserv_file = self.sock.makefile(mode='rw')
        self.asserv = Channel(self.asserv_file.buffer,
                lambda name, args: name, proto = 'asserv')
        self.states = None
        self.speed = SpeedOrder(self.asserv)
        self.speed.start()

    def event(self, axes, buttons):
        #print(axes, buttons)
        self.speed.update(axes[0], axes[1], axes[2])
        if self.states:
            if self.states[0] == 0 and buttons[0] == 1:
                print("Button 1 pressed!")
            elif self.states[1] == 0 and buttons[1] == 1:
                print("Button 2 pressed!")
            elif self.states[2] == 0 and buttons[2] == 1:
                print("Button 3 pressed!")
            elif self.states[3] == 0 and buttons[3] == 1:
                print("Button 4 pressed!")
            elif self.states[4] == 0 and buttons[4] == 1:
                print("Button 5 pressed!")
            elif self.states[5] == 0 and buttons[5] == 1:
                print("Button 6 pressed!")
            elif self.states[6] == 0 and buttons[6] == 1:
                print("Button 7 pressed!")
            elif self.states[7] == 0 and buttons[7] == 1:
                print("Button 8 pressed!")
        self.states = buttons


class MyHandler(pyinotify.ProcessEvent):

    def my_init(self):
        self.processor = Processor(host, port)
        self.re = re.compile(REGEXP)

    def open(self, name, pathname):
        if self.re.match(name):
            print("Opening %s…" %pathname)
            time.sleep(0.1)
            jsread(LIB, pathname, self.processor.event)

    def process_IN_CREATE(self, event):
        self.open(event.name, event.pathname)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Control robot with joystick.', add_help = False)
    parser.add_argument('-d', '--dir', dest='devices', help='Dir to watch for new joystick device.')
    parser.add_argument('-l', '--lib', dest='lib', help='Lib to use.')
    parser.add_argument('-h', '--host', dest='host', help='Connect to the specified host.')
    parser.add_argument('-p', '--port', dest='port', help='Base port to compute port to connect.')
    args = parser.parse_args()

    if args.devices:
        devices = args.devices
    else:
        devices = DEVICES
    if args.lib:
        lib = args.lib
    else:
        lib = LIB
    if args.host:
        host = args.host
    else:
        host = HOST
    if args.port:
        port = args.port
    else:
        port = PORT

    wm = pyinotify.WatchManager()
    handler = MyHandler()
    notifier = pyinotify.Notifier(wm, default_proc_fun=handler)
    wm.add_watch(devices, pyinotify.IN_CREATE)

    import glob
    import os.path
    for device in glob.glob(os.path.join(devices, '*')):
        handler.open(os.path.basename(device), device)

    notifier.loop()
