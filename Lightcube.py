#
# Lightcube - a library for drawing graphics primitives on the Lightcube device.
#     This library assembles primitives (such as lines, pixels, boxes, etc) into
#     a frame which is sent across the network to a Lightcube.   The Lightcube
#     runs a simple network framebuffer, taking the frames and displaying them
#     on the cube.

class Frame(object):

	def __init__(self):
		self._data = [ [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0],[ 0, 0, 0, 0, 0, 0, 0, 0],[ 0, 0, 0, 0, 0, 0, 0, 0],[ 0, 0, 0, 0, 0, 0, 0, 0],[ 0, 0, 0, 0, 0, 0, 0, 0],[ 0, 0, 0, 0, 0, 0, 0, 0],[ 0, 0, 0, 0, 0, 0, 0, 0] ]

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



# Define some color constants
RED = Color(rgb="880000")
WHITE = Color(rgb="ffffff")
BLUE = Color(rgb="0000aa")
GREEN = Color(rgb="215E21")
YELLOW = Color(rgb="ffc400")
BLACK = Color(rgb="000000")
GREY = Color(rgb="222222")




class FrameRenderer(object):

	def __init__(self,frame):
		self._frame = frame

	def calc_slope(self, start, end):
		x1 = start.x
		x2 = end.x
		y1 = start.y
		y2 = end.y

		slope = ((x1 - x2) / (y1 - y2))

		return(slope)

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

		# This is an implementation of Bresenham's line algorithm (optimized version)
		# which can be found at:  http://en.wikipedia.org/wiki/Bresenham's_line_algorithm
		# This code is adapted from the implementation found here:  
		#  http://www.barricane.com/2009/08/28/bresenhams-line-algorithm-in-python.html

		# if this line rises more steeply than 45 deg
		if abs(end.y - start.y) > abs(end.x - start.x):
			steep = True
		else:
			steep = False

		if steep:
			# swap x and y in the start and end points
			# (reflecting it across the 45 deg line)
			start.x, start.y = start.y, start.x
			end.x, end.y = end.y, end.x
		
		# If it slopes down, flip start and endpoints		
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

		# LL -> Lower Left corner
		# LR -> Lower Right corner
		# UL -> Upper Left corner

		if (LL.x + width) > 8:
			# If this box is wider than 8 columns, truncate its width at x=7
			LR_x = 7
		else:
			# Box is less than 8 columns wide, so calculate the lower-right corner (x-component)
			LR_x = LL.x + width - 1

		if (LL.y + height) > 8:
			# If this box is taller than 8 rows, truncate its height at y=7
			UL_y = 7
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
myframe = Frame()
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
