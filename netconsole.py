#!/usr/bin/env python3
"""
netconsole client / server

--server:
    Prints the output from the netconsole on the cRIO.

    Messages from the cRIO are broadcast over the local network to all connected
    clients through UDP port 6666 by default.

    The server listens on this port for UDP datagrams and then echos them
    to stdout.

    Entering a space into stdin will pause the server

--client:
    Sends input from stdin to the robot cRIO.

    Messages are broadcast over port 6668 by default
"""

import sys
import socket
import asyncore
import atexit
import argparse
import re
import readline

DEFAULT_SERVER_PORT = 6666
DEFAULT_CLIENT_PORT = 6668
DEFAULT_TEAM = 4413

RE_EXIT = re.compile('^(quit|exit)$')

def team_number_to_ip(team):
    """team number (xxyy) -> 10.xx.yy.2"""
    xx = team / 100
    yy = team % 100
    return "10.%0d.%0d.2" % (xx, yy)

class NetconsoleUDPServer(asyncore.dispatcher):
    """UDP server. Prints incoming datagrams to stdout."""

    def __init__(self, port, pause_reader=None):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.pause_reader = pause_reader

    def handle_read(self):
        data = self.recv(8196)
        if not self.pause_reader.paused:
            sys.stdout.write(data.decode())

class PauseReader(asyncore.file_dispatcher):
    """Reads stdin and flips a 'pause' toggle when it hits a space."""

    paused = False

    def __init__(self):
        asyncore.file_dispatcher.__init__(self, sys.stdin)

    def handle_read(self):
        data = self.recv(1024).decode()
        # count number of spaces
        if data.rstrip('\n\r') == ' ':
            # toggle pause
            self.paused = not self.paused
            if self.paused:
                print(" > pause")
            else:
                print(" > unpause")

def start_server(port):
    pause_reader = PauseReader()
    server = NetconsoleUDPServer(port, pause_reader)

    def atexit_function():
        pause_reader.close()
        server.close()

    atexit.register(atexit_function)

    try:
        asyncore.loop(0.0)
    except KeyboardInterrupt:
        pass

def make_client_socket(port, addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    return sock

def start_client(port, team):
    #robot_addr = team_number_to_ip(team)
    robot_addr = '192.168.0.4'
    client = make_client_socket(port, robot_addr)

    atexit.register(client.close)

    # provide readline functionality if we're processing off a command line
    if sys.stdin.isatty():
        while True:
            line = input('--> ')
            if process_input(client, port, line):
                break
    else: # if we're not using a command line, process off of stdin
        for line in sys.stdin: # read from stdin
            if process_input(client, port, line):
                break

def process_input(client, port, line):
    if RE_EXIT.match(line):
        return True
    client.sendto(line.encode(), ('255.255.255.255', port))

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='FRC netconsole client/server')

    group = parse.add_mutually_exclusive_group(required=True)
    group.add_argument('--server', action='store_true', dest='server',
                       default=False, help='Run the netconsole server')
    group.add_argument('--client', action='store_true', dest='client',
                       default=False, help='Run the netconsole client')

    parse.add_argument('--team', action='store', dest='team',
                       default=DEFAULT_TEAM, type=int, help='Team number')
    parse.add_argument('--server-port', action='store', dest='server_port',
                       default=DEFAULT_SERVER_PORT, type=int,
                       help='The port to listen on')
    parse.add_argument('--client-port', action='store', dest='client_port',
                       default=DEFAULT_CLIENT_PORT, type=int,
                       help='The port to send commands over')

    args = parse.parse_args()

    if args.server:
        start_server(args.server_port)
    if args.client:
        start_client(args.client_port, args.team)
