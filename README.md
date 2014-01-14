FRC Netconsole Sender / Receiever
=================================

Description
-----------

netconsole_receiever listens on port 6666 for incoming UDP datagrams and prints
them to stdout.

netconsole_sender broadcasts commands over port 6668. If there is a tty 
attached to the client, it runs in interactive mode; else, it pipes stdin to
the UDP broadcast socket.

Requirements
------------

*socat* - sudo apt-get install socat
