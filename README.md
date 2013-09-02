Lightcube
=========
<table border=0 cellpadding=8 style="border: 0px;">
 <td width=200 height=133 align=middle valign=middle>
  <img width=200 height=133 src="https://dl.dropboxusercontent.com/u/16837290/output.chrissnell.com/color_8x8_matrix.jpg" />
 </td>
 <td align=left valign=top>
A colorful, programmable information visualizer for your desk.  The Lightcube is an 8x8 matrix
of RGB LEDs enclosed in a small wooden cube and connected to the network via WiFi/Ethernet.
Client applications can use a simple Python library to draw simple graphics primitives such as
dots, lines, boxes, bar graphs, etc., and send them over the network to the Lightcube.   The Lightcube
runs a simple framebuffer that displays whatever data is sent to it.   
 </td>
</tr>
</table>

Things that the Lightcube could display:

* A graph of the network utilization of your HAproxy load balancers
* The temperature outside your house
* The status of your code build after the most recent commit
* Up/down status of all of your servers, by server type

Architecture
------------

![Lightcube architecture](https://raw.github.com/chrissnell/Lightcube/master/LightcubeArchitecture.png)


Lightcube Protocol
------------------
The Lightcube receives its graphical instructions in the form of data frames sent over a TCP/IP network.
The data is sent in a binary format, encoded in UDP datagrams.   The format is designed to be easily
parsed by low-end microcontrollers such as the Arduino and is intented to acommodate both the current
8x8 LED Lightcube, along with future Lightcubes with more LEDs.  

The Lightcube packets are constructed as follows:

```
    0                   1                   2                   3   
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |     Header    |    Protocol   |    Display    |    Display    |
   |               |    Version    |     Width     |     Height    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |    Retain     |C|                                             |
   |Delay (10/sec) |L|          Reserved for future use            |
   |               |S|                                             |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


   Header [8 bits]                   Will always be 01101011

   Protocol Version [8 bits]         Currently 00000001

   Display Width [8 bits]            The number of horizontal LEDs in the display.  Currently 00001000 
                                     (which is 8 in decimal)

   Display Height [8 bits]           The number of vertical LEDs in the display.   Currently 00001000 
                                     (which is 8 in decimal)

   Retain Delay (seconds) [8 bits]   The time (in 1/10 second increments) to display the current frame before advancing 
                                     to the next one.  If set to 00000000 (zero), the frame is displayed indefinitely.
                                     
   CLS [1 bit]                       Clear the display by turning all LEDs off.  All frame data is ignored, though the
                                     retain delay is still honored.   CLS + retain delay will blank the screen for the 
                                     time period specified by the retain delay.
                                     
```