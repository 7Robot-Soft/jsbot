#!/usr/bin/env python3

from jsread import jsread
from settings import HOST, PORT, DEVICE, LIB
import argparse
import sys
sys.path.append("../atp")
from channel import Channel
import socket

class Processor:
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((HOST, PORT+5))
        self.asserv_file = self.sock.makefile(mode='rw')
        self.asserv = Channel(self.asserv_file.buffer,
                lambda name, args: name, proto = 'asserv')
        self.states = None

    def event(self, axes, buttons):
        if self.states:
            if self.states[0] == 0 and buttons[0] == 1:
                print("feu !")
            elif self.states[1] == 0 and buttons[1] == 1:
                pass
            elif self.states[2] == 0 and buttons[2] == 1:
                pass
            elif self.states[3] == 0 and buttons[3] == 1:
                pass
            elif self.states[4] == 0 and buttons[4] == 1:
                pass
            elif self.states[5] == 0 and buttons[5] == 1:
                pass
            elif self.states[6] == 0 and buttons[6] == 1:
                pass
            elif self.states[7] == 0 and buttons[7] == 1:
                pass
        self.states = buttons


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Control robot with joystick.', add_help = False)
    parser.add_argument('-d', '--device', dest='device', help='Joystick device to use.')
    parser.add_argument('-l', '--lib', dest='lib', help='Lib to use.')
    parser.add_argument('-h', '--host', dest='host', help='Connect to the specified host.')
    parser.add_argument('-p', '--port', dest='port', help='Base port to compute port to connect.')
    args = parser.parse_args()

    if args.device:
        device = args.device
    else:
        device = DEVICE
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

    processor = Processor(host, port)

    jsread(LIB, DEVICE, processor.event)
