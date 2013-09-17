import Lightcube

# Define some generic colors
RED = Lightcube.Color(rgb=0xFF0000)
WHITE = Lightcube.Color(rgb=0xffffff)
BLUE = Lightcube.Color(rgb=0x0000FF)
GREEN = Lightcube.Color(rgb=0x00FF00)
YELLOW = Lightcube.Color(rgb=0xffc400)
BLACK = Lightcube.Color(rgb=0x000000)
GREY = Lightcube.Color(rgb=0x222222)
MAGENTO = Lightcube.Color(rgb=0xff00ff)

# Create a new Frame
myframe = Lightcube.Frame(retain_delay=0xA)
# and a FrameRenderer
myrenderer = Lightcube.FrameRenderer(frame=myframe)

myrenderer.draw_line(Lightcube.Coordinate(x=0, y=0), Lightcube.Coordinate(x=0, y=0), RED)
myrenderer.draw_line(Lightcube.Coordinate(x=0, y=1), Lightcube.Coordinate(x=1, y=0), RED)
myrenderer.draw_line(Lightcube.Coordinate(x=0, y=2), Lightcube.Coordinate(x=2, y=0), YELLOW)
myrenderer.draw_line(Lightcube.Coordinate(x=0, y=3), Lightcube.Coordinate(x=3, y=0), YELLOW)
myrenderer.draw_line(Lightcube.Coordinate(x=0, y=4), Lightcube.Coordinate(x=4, y=0), MAGENTO)
myrenderer.draw_line(Lightcube.Coordinate(x=0, y=5), Lightcube.Coordinate(x=5, y=0), MAGENTO)
myrenderer.draw_line(Lightcube.Coordinate(x=0, y=6), Lightcube.Coordinate(x=6, y=0), BLUE)
myrenderer.draw_line(Lightcube.Coordinate(x=0, y=7), Lightcube.Coordinate(x=7, y=0), GREEN)
myrenderer.draw_line(Lightcube.Coordinate(x=1, y=7), Lightcube.Coordinate(x=7, y=1), WHITE)
myrenderer.draw_line(Lightcube.Coordinate(x=2, y=7), Lightcube.Coordinate(x=7, y=2), WHITE)
myrenderer.draw_line(Lightcube.Coordinate(x=3, y=7), Lightcube.Coordinate(x=7, y=3), GREEN)
myrenderer.draw_line(Lightcube.Coordinate(x=4, y=7), Lightcube.Coordinate(x=7, y=4), GREEN)
myrenderer.draw_line(Lightcube.Coordinate(x=5, y=7), Lightcube.Coordinate(x=7, y=5), BLUE)
myrenderer.draw_line(Lightcube.Coordinate(x=6, y=7), Lightcube.Coordinate(x=7, y=6), MAGENTO)
myrenderer.draw_line(Lightcube.Coordinate(x=7, y=7), Lightcube.Coordinate(x=7, y=7), YELLOW)

# Create a new assembled frame packet
packet = Lightcube.AssembledFramePacket(frame=myframe)

# and populate it with data
packet.create_packet()

# and send it over the wire
packet.send_packet("192.168.17.2", 7070)
