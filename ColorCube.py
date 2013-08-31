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


def inclusive_range(first,last):
	if first == last:
		return [first]
	if first < last:
		# return our range but be incluside to 'last'
		# because Python's range is not inclusive of the last number
		return range(first, last + 1)
	if start > finish:
		# We'll need to count backwards (by -1)...and be inclusive (so we subtract 1 from finish)
		return range(first, last - 1, -1)



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



	def draw_line(self, start, end, color=WHITE):

		# This is an implementation of Bresenham's line algorithm (optimized version)
		# which can be found at:  http://en.wikipedia.org/wiki/Bresenham's_line_algorithm
		# This code is adapted from the implementation found here:  
		#  http://www.barricane.com/2009/08/28/bresenhams-line-algorithm-in-python.html

		# if this line rises (or falls) more than it runs...
		if abs(end.y - start.y) > abs(end.x - start.x):
			steep = True
		else:
			steep = False

		if steep:
			# swap x and y in the start and end points
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

		for x in inclusive_range(start.x, end.x):
			if steep:
				self._frame.set_color_at(y,x, color)
			else:
				self._frame.set_color_at(x,y, color)

			error = error - delta_y

			if error < 0:
				y = y + y_step
				error = error + delta_x




myframe = Frame()
myrenderer = FrameRenderer(frame=myframe)

line_start = Coordinate(x=0, y=0)
line_end = Coordinate(x=0, y=7)

myrenderer.draw_line(line_start, line_end)
