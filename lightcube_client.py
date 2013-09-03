import Lightcube

# Define some generic colors
RED = Lightcube.Color(rgb="880000")
WHITE = Lightcube.Color(rgb="ffffff")
BLUE = Lightcube.Color(rgb="0000aa")
GREEN = Lightcube.Color(rgb="215E21")
YELLOW = Lightcube.Color(rgb="ffc400")
BLACK = Lightcube.Color(rgb="000000")
GREY = Lightcube.Color(rgb="222222")


# Create a new Frame
myframe = Lightcube.Frame(retain_delay=0xA)
# and a FrameRenderer
myrenderer = Lightcube.FrameRenderer(frame=myframe)

# Define the start and end points of the line
line_start = Lightcube.Coordinate(x=0, y=3)
line_end = Lightcube.Coordinate(x=7, y=3)
# and draw a red line between them
myrenderer.draw_line(line_start, line_end, RED)

# Define the lower-left corner of a box
box_ll = Lightcube.Coordinate(x=0, y=0)
# and draw a 9x12 box starting there
myrenderer.draw_box(box_ll, 9, 12)

packet = Lightcube.AssembledFramePacket(frame=myframe)
packet.create_packet()
packet.send_packet("127.0.0.1", 7070)
