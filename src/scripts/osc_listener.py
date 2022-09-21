"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import math

import click
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher


def print_volume_handler(unused_addr, args, volume):
    print("[{0}] ~ {1}".format(args[0], volume))


def print_compute_handler(unused_addr, args, volume):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](volume)))
    except ValueError:
        pass


@click.command()
@click.option("--ip", default="127.0.0.1", help="The ip to listen")
@click.option("--port", type=int, default=5005, help="The port to listen")
def main(ip, port):
    dispatcher = Dispatcher()
    dispatcher.map("/filter", print)
    dispatcher.map("/volume", print_volume_handler, "Volume")
    dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
