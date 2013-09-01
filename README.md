Lightcube
=========
<table border=0 cellpadding=8 style="border: none;">
 <td width=200 height=133 align=middle valign=top>
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
============

![Lightcube architecture](https://raw.github.com/chrissnell/Lightcube/master/LightcubeArchitecture.png)
