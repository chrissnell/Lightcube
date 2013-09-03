import socket
import Lightcube


LIGHTCUBE_PORT=7070
LIGHTCUBE_LISTEN_IP="127.0.0.1"

# Open a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((LIGHTCUBE_LISTEN_IP, LIGHTCUBE_PORT))

while True:
	data, addr = sock.recvfrom(1024)
	print "PACKET RECEIVED"