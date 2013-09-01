Lightcube
=========

<img align=left padding=8 src="https://dl.dropboxusercontent.com/u/16837290/output.chrissnell.com/color_8x8_matrix.jpg" />
A colorful, programmable information visualizer for your desk.  The Lightcube is an 8x8 matrix
of RGB LEDs enclosed in a small wooden cube and connected to the network via WiFi/Ethernet.
Client applications can use a simple Python library to draw simple graphics primitives such as
dots, lines, boxes, bar graphs, etc., and send them over the network to the Lightcube.   The Lightcube
runs a simple framebuffer that displays whatever data is sent to it.   

Things that the Lightcube could display:

* A graph of the network utilization of your HAproxy load balancers
* The temperature outside your house
* The status of your code build after the most recent commit
* Up/down status of all of your servers, by server type

Architecture
============

![Lightcube architecture](https://raw.github.com/chrissnell/Lightcube/master/LightcubeArchitecture.png)
