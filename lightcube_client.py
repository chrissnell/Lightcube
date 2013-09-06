import Lightcube

# Define some generic colors
RED = Lightcube.Color(rgb=0xFF0000)
WHITE = Lightcube.Color(rgb=0xffffff)
BLUE = Lightcube.Color(rgb=0x0000FF)
GREEN = Lightcube.Color(rgb=0x00FF00)
YELLOW = Lightcube.Color(rgb=0xffc400)
BLACK = Lightcube.Color(rgb=0x000000)
GREY = Lightcube.Color(rgb=0x222222)


# Create a new Frame
myframe = Lightcube.Frame(retain_delay=0xA)
# and a FrameRenderer
myrenderer = Lightcube.FrameRenderer(frame=myframe)


# Define the lower-left corner of a box
box_ll = Lightcube.Coordinate(x=0, y=0)
# and draw a 9x12 box starting there
myrenderer.draw_box(box_ll, 4, 4, RED)

# Define the start and end points of the line
line_start = Lightcube.Coordinate(x=0, y=0)
line_end = Lightcube.Coordinate(x=0, y=7)
# and draw a red line between them
myrenderer.draw_line(line_start, line_end, GREEN)


myrenderer.draw_line(Lightcube.Coordinate(x=4, y=0), Lightcube.Coordinate(x=4, y=2), BLUE)

myrenderer.draw_line(Lightcube.Coordinate(x=5, y=0), Lightcube.Coordinate(x=5, y=1), BLUE)

myrenderer.draw_line(Lightcube.Coordinate(x=7, y=0), Lightcube.Coordinate(x=2, y=7), YELLOW)

myrenderer.draw_point(Lightcube.Coordinate(x=5, y=5), WHITE)
myrenderer.draw_point(Lightcube.Coordinate(x=5, y=6), WHITE)
myrenderer.draw_point(Lightcube.Coordinate(x=5, y=7), WHITE)
myrenderer.draw_point(Lightcube.Coordinate(x=6, y=7), WHITE)
myrenderer.draw_point(Lightcube.Coordinate(x=7, y=7), WHITE)
myrenderer.draw_point(Lightcube.Coordinate(x=7, y=6), WHITE)
myrenderer.draw_point(Lightcube.Coordinate(x=7, y=5), WHITE)
myrenderer.draw_point(Lightcube.Coordinate(x=6, y=5), WHITE)








# Create a new assembled frame packet
packet = Lightcube.AssembledFramePacket(frame=myframe)

# and populate it with data
packet.create_packet()

# and send it over the wire
packet.send_packet("192.168.17.2", 7070)
