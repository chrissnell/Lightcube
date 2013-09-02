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
   |Header |  CMD  |    Protocol   |    Display    |    Display    |
   |       |       |    Version    |     Width     |     Height    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |    Retain     |C|                                             |
   |Delay (10/sec) |L|          Reserved for future use            |
   |               |S|                                             |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Pixel(0,0) RED |Pixel(0,0) GRN |Pixel(0,0) BLU |Pixel(1,0) RED |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Pixel(1,0) GRN |Pixel(1,0) BLU |Pixel(2,0) RED |Pixel(2,0) GRN |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+   
         ...
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+   
   |Pixel(6,7) BLU |Pixel(7,7) RED |Pixel(7,7) GRN |Pixel(7,7) BLU |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

   Note that one tick mark represents one bit position.


   Header [4 bits]                   Will always be 0111

   CMD [4 bits]						 Command to perform
                                     0x0 - "ping"  - Instructs the Lightcube to send an acknoledgement that it is
                                                     up and responding to commands
                                     0x1 - "store" - Store this frame in a display queue
                                     0x2 - "play"  - Display all frames in queue (in order received)
                                     0x3 - "demo"  - Display a demo screen
                                     0xF - "wipe"  - Wipe all frames from queue and blank all pixels

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
                                     
   Pixel Data [24 bits/pixel]        Pixel data for the frame, starting at (0,0) in the lower-left corner and moving
                                     down the row.  When each row is complete, the data continues at the left-most cell
                                     of the row above, until the entire frame is complete.

                                     A total of 24 bits of color data is sent for each pixel, 8 bits per color for the 
                                     red (RED),green (GRN), and blue (BLU) components.  The 8-bit color value indicates
                                     the brightness for that component.  0xFF is maximum brightness, 0xFF is full dark.
                                     So, 0xFF 0xFF 0xFF would produce a bright white color in a pixel.

                                     The total packet size is determined by the Display Width and Display Height values.
                                     For an 8x8 Lightcube, this would be 200 bytes (8 bytes frame header, 
                                     196 bytes frame data).

```