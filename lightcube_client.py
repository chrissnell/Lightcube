import Lightcube

# Define some generic colors
RED = Lightcube.Color(rgb=0x880000)
WHITE = Lightcube.Color(rgb=0xffffff)
BLUE = Lightcube.Color(rgb=0x0000aa)
GREEN = Lightcube.Color(rgb=0x215E21)
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
myrenderer.draw_box(box_ll, 9, 12, GREEN)

# Define the start and end points of the line
line_start = Lightcube.Coordinate(x=0, y=1)
line_end = Lightcube.Coordinate(x=0, y=7)
# and draw a red line between them
myrenderer.draw_line(line_start, line_end, RED)


# Create a new assembled frame packet
packet = Lightcube.AssembledFramePacket(frame=myframe)

# and populate it with data
packet.create_packet()

# and send it over the wire
packet.send_packet("127.0.0.1", 7070)
