FRC Netconsole Client / Server
==============================

Description
-----------

An asyncronous, Python 3 netconsole implementation for the FIRST Robotics
Competition.

The server listens for UDP datagrams on port 6666 and prints them out to
stdout. It can be paused by typing a space into the terminal.
(" \n" -> stdin => pause).

The client broadcasts commands over port 6668. If there is a tty attached
to the client, it runs in interactive mode; else, it pipes stdin to the UDP
broadcast socket.

Usage
-----

    usage: netconsole.py [-h] (--server | --client) [--team TEAM]
                         [--server-port SERVER_PORT] [--client-port CLIENT_PORT]

    FRC netconsole client/server

    optional arguments:
      -h, --help            show this help message and exit
      --server              Run the netconsole server
      --client              Run the netconsole client
      --team TEAM           Team number
      --server-port SERVER_PORT
                            The port to listen on
      --client-port CLIENT_PORT
                            The port to send commands over
