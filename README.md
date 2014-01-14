FRC Netconsole Sender / Receiever
=================================


Description
-----------

netconsole_receiever listens on port 6666 for incoming UDP datagrams and prints
them to stdout.

netconsole_sender broadcasts commands over port 6668. If there is a tty 
attached to the client, it runs in interactive mode; else, it pipes stdin to
the UDP broadcast socket.


Installation
------------

Clone this repository

    $ git clone git@github.com:phlip9/netconsole.git

Install `socat`

    $ sudo apt-get install socat

(Optional) Add this folder to your path

    $ cd netconsole
    $ echo "export PATH=$PATH:$(pwd)" >> ~/.bashrc


Tutorial
--------

### Get the cRIO output ###

Listen for the cRIO output

    $ netconsole_receiver


### Send commands to the cRIO ###

    $ netconsole_sender
    --> help
    --> exit
    $

You should see the output of the commands in the `netconsole_receiver` if you have it open

The `netconsole_sender` also supports piping commands over stdin

    $ echo "help" | netconsole_sender
    $ netconsole_sender < some_script.sh

### VxWorks WindShell Documentation ###

[WindShell man page](http://www.vxdev.com/docs/vx55man/tornado/tools/windsh.html)

[VxWorks Tutorial](http://www-cdfonline.fnal.gov/daq/computing/vxworks/tutorial.html)

[vxWorks Command Cheat sheet](http://touro.ligo-la.caltech.edu/~cparames/CDS/vxWorks_commands.html)
