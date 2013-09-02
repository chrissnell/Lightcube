import struct
from ctypes import *


#
# Lightcube - a library for drawing graphics primitives on the Lightcube device.
#     This library assembles primitives (such as lines, pixels, boxes, etc) into
#     a frame which is sent across the network to a Lightcube.   The Lightcube
#     runs a simple network framebuffer, taking the frames and displaying them
#     on the cube.


#
#  The Lightcube coordinate system:
#
#     Y
#     ^
#  7  | O  O  O  O  O  O  O  O
#  6  | O  O  O  O  O  O  O  O
#  5  | O  O  O  O  O  O  O  O
#  4  | O  O  O  O  O  O  O  O
#  3  | O  O  O  O  O  O  O  O
#  2  | O  O  O  O  O  O  O  O
#  1  | O  O  O  O  O  O  O  O
#  0  | O  O  O  O  O  O  O  O
#     +-- -- -- -- -- -- -- --> X
#       0  1  2  3  4  5  6  7




class Frame(object):

	def __init__(self, retain_delay=0):
		self._retain_delay = retain_delay

		# Display Parameters
		# This is where we define the width and height (in LEDs) of our Lightcube
		self._DISP_WIDTH = 8
		self._DISP_HEIGHT = 8

		self._data = [[0 for x in xrange(self._DISP_WIDTH)] for x in xrange(self._DISP_HEIGHT)]

	def set_color_at(self, x, y, color):
		print x, y
		self._data[y][x] = color.rgb


class Coordinate(object):
	
	def __init__(self, x, y):
		self.x = x
		self.y = y



class Color(object):

	def __init__(self, rgb):
		self.rgb = rgb


# Define some generic colors
RED = Color(rgb="880000")
WHITE = Color(rgb="ffffff")
BLUE = Color(rgb="0000aa")
GREEN = Color(rgb="215E21")
YELLOW = Color(rgb="ffc400")
BLACK = Color(rgb="000000")
GREY = Color(rgb="222222")


class FramePacket(Structure):

	frame=Frame()

	# Define the data structure of our packet using the ctypes modules
	_fields_ = [ ('header', c_uint8), ('proto_version', c_uint8), \
	             ('display_width', c_uint8), ('display_height', c_uint8), \
	             ('retain_delay', c_uint8), ('RESERVED_SPACE', c_uint8 * 3), \
	             ('frame_data', c_uint8 * (frame._DISP_WIDTH * frame._DISP_HEIGHT)) ]


class AssembledFramePacket(object):
	def __init__(self,frame):
		self._frame = frame

	# c = (a << 4) + b
	# packed = struct.pack('!H',c)
	# unpacked = struct.unpack('!H',packed)
	# a1 = bin(unpacked[0] >> 4)
	# b1= bin(unpacked[0] & 0b00001111)

	def create_packet(self):

		# Frame ID
		FRAME_ID = 0x7

		# Frame Commands
		CMD_PING = 0x0
		CMD_STORE = 0x1
		CMD_PLAY = 0x2
		CMD_DEMO = 0x3
		CMD_CLEAR = 0xE
		CMD_WIPE = 0xF

		# Protocol Version (currently 1)
		PROTO_VER = 0x1

		# Frame Retain Delay, n * 1/10 second, n = (0x00..0xff) inclusive
		#      Max delay = 25.5 sec
		retain_delay = self._frame._retain_delay

		RESERVED_SPACE = 0x0, 0x0, 0x0

		# Shift the FRAME_ID four bits to the left and append CMD_STORE
		# This will produce a single 8-bit value that we'll use as our packet's header
		f_header = (FRAME_ID << 4) + CMD_STORE

		# Assemble the finished packet
		packet = FramePacket(f_header, PROTO_VER, self._frame._DISP_WIDTH, self._frame._DISP_HEIGHT, retain_delay, RESERVED_SPACE)

		# For debugging
		print "f_header: " + str(f_header)
		print "retain_delay: " + str(retain_delay)
		print "DISP_HEIGHT: " + str(packet.display_height)
		f = open("foo","wb")
		f.write(packet)
		f.close()




class FrameRenderer(object):

	def __init__(self,frame):
		self._frame = frame

	def inclusive_range(self, first,last):
		if first == last:
			return [first]
		if first < last:
			# return our range but be inclusive to 'last'
			# because Python's range is not inclusive of the last number
			return range(first, last + 1)
		if start > finish:
			# We'll need to count backwards (by -1)...and be inclusive (so we subtract 1 from finish)
			return range(first, last - 1, -1)



	def draw_line(self, start, end, color=WHITE):
		#
		# draw_line() - Draws a Bresenham-style line between two coordinates
		# 
		# params:	start - The starting point of the line (of class "Coordinate")
		#			end - The ending point of the line (of class "Coordinate")
		#			color - Color used to draw line (of class "Color") [optional]
		#
		#
		# This is an implementation of Bresenham's line algorithm (optimized version)
		# which can be found at:  http://en.wikipedia.org/wiki/Bresenham's_line_algorithm
		# This code is adapted from the implementation found here:  
		#  http://www.barricane.com/2009/08/28/bresenhams-line-algorithm-in-python.html

		if abs(end.y - start.y) > abs(end.x - start.x):
			steep = True
		else:
			steep = False

		if steep:
			start.x, start.y = start.y, start.x
			end.x, end.y = end.y, end.x
		
		if start.x > end.x:
			start.x, end.x = end.x, start.x
			start.y, end.y = end.y, start.y


		delta_x = end.x - start.x
		delta_y = abs(end.y - start.y)

		error = delta_x / 2

		y = start.y

		if start.y < end.y:
			y_step = 1
		else:
			y_step = -1

		for x in self.inclusive_range(start.x, end.x):
			if steep:
				self._frame.set_color_at(y,x, color)
			else:
				self._frame.set_color_at(x,y, color)

			error = error - delta_y

			if error < 0:
				y = y + y_step
				error = error + delta_x


	def draw_box(self, LL, width, height, color=WHITE):
		#
		# draw_box() - Draws a filled-in box
		# 
		# params:	LL - The lower left corner of the box (of class "Coordinate")
		#			width - The width of the box
		#			height - The height of the box
		#			color - Color used to draw line (of class "Color") [optional]
		#


		# LL -> Lower Left corner
		# LR -> Lower Right corner
		# UL -> Upper Left corner

		if (LL.x + width) > self._frame._DISP_WIDTH:
			# If this box is wider than 8 columns, truncate its width at x=(frame._DISP_WIDTH - 1)
			LR_x = (self._frame._DISP_WIDTH - 1)
		else:
			# Box is less than 8 columns wide, so calculate the lower-right corner (x-component)
			LR_x = LL.x + width - 1

		if (LL.y + height) > self._frame._DISP_HEIGHT:
			# If this box is taller than 8 rows, truncate its height at y=7
			UL_y = (self._frame._DISP_HEIGHT - 1)
		else:
			# Box is less than 8 rows high, so calculate the upper-left corner (y-component)
			UL_y = LL.y + height - 1


		# Iterate through each column of our box and draw vertical lines
		# from the baseline up to the top-most extent
		for x in self.inclusive_range(LL.x, LR_x):
			line_start = Coordinate(x, LL.y)
			line_end = Coordinate(x, UL_y)
			self.draw_line(line_start, line_end, color)
			x += 1

		# For debugging
		print "LL: (" + str(LL.x) + "," + str(LL.y) + ")"
		print "width: " + str(width) + "   height: " + str(height)
		print "UR: (" + str(LR_x) + "," + str(UL_y) + ")"


# Testing...

# Create a new Frame
myframe = Frame(retain_delay=0xA)
# and a FrameRenderer
myrenderer = FrameRenderer(frame=myframe)

# Define the start and end points of the line
line_start = Coordinate(x=0, y=3)
line_end = Coordinate(x=7, y=3)
# and draw a red line between them
myrenderer.draw_line(line_start, line_end, RED)

# Define the lower-left corner of a box
box_ll = Coordinate(x=0, y=0)
# and draw a 9x12 box starting there
myrenderer.draw_box(box_ll, 9, 12)

packet = AssembledFramePacket(frame=myframe)
packet.create_packet()
