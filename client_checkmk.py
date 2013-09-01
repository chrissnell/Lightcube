#!/usr/bin/python

#
# statsfetcher.py
#
# Pulls system metrics from a check_mk "Livestatus" server over the Interwebs
# and stores them in circular buffers for use by the cube.
#

import socket
import time
from optparse import OptionParser
import collections
from collections import defaultdict


# Keep up to MAX_STATS_BUFFER_SIZE readings in our ring buffer
MAX_STATS_BUFFER_SIZE = 8


def main():

	# Set up a commandline argument parser
	parser = OptionParser(usage="usage: %prog <hostname> <port>")

	# Mandatory arguments
	parser.add_option("-s",dest="hostname",help="hostname of livestatus server")
	parser.add_option("-p",dest="port",help="port of livestatus server")

	# Store our options and arguments globally
	global options, args

	# Parse the options and arguments
	(options, args) = parser.parse_args()

	# If we weren't given two arguments, exit and throw up the help message
	if len(args) != 2:
		parser.error("Wrong number of arguments")

	


# Keep up to MAX_STATS_BUFFER_SIZE readings in our ring buffer
MAX_STATS_BUFFER_SIZE = 8

# Easy way to create deep dicts of dicts.  Heh.
def makehash():
	return collections.defaultdict(makehash)


# Set up a dictionary to hold stats ring buffers (keyed by hostname)
stats = makehash()

# This fetches CPU stats from the Livestatus server and parses them
def get_cpu_stats():

	# Set up a socket connection
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to our hostname:port
	s.connect((args[0], int(args[1])))

	# Send the Livestatus query
	# Documentation here:  http://mathias-kettner.de/checkmk_livestatus.html
	s.send("GET services\nFilter: description ~ CPU util\nColumns: host_name perf_data\n")

	# Close the socket
	s.shutdown(socket.SHUT_WR)

	# Receive our data with a big, fat buffer.
	answer = s.recv(100000000)

	statsdict = defaultdict(dict)

	# Iterate through the lines of our answer
	for line in answer.split('\n')[:-1]:	
		# Split on semicolons, but ignore blank fields (eg. ;;;;)
		params = filter(bool, line.split(';'))

		# Iterate through the metrics, looking for key=value pairs
		for item in params[1:]:
			if "=" in item:
				(key, value) = item.split('=')
				# If we find a key=value pair, store it in statsdict, cleaned of any leading/trailing whitespace
				statsdict[params[0]][key.strip()] = value
	return statsdict


# Main loop
def run():
	while True:
		# Fetch CPU stats
		statsreading = get_cpu_stats()

		# Iterate through each host in our results
		for host in statsreading:
			# If there's not a "wait" key in this host's dictionary, that means that it's a new host.
			if not stats[host]["cpu"]["wait"]:
				# Since it's a new host, we need to set up the ring buffers for each of the CPU metrics
				stats[host]["cpu"]["wait"] = collections.deque(maxlen=MAX_STATS_BUFFER_SIZE)
				stats[host]["cpu"]["user"] = collections.deque(maxlen=MAX_STATS_BUFFER_SIZE)
				stats[host]["cpu"]["system"] = collections.deque(maxlen=MAX_STATS_BUFFER_SIZE)

			# Insert the gathered metrics into the left side of the appropriate ring buffers
			stats[host]["cpu"]["wait"].appendleft(statsreading[host]["wait"])
			stats[host]["cpu"]["user"].appendleft(statsreading[host]["user"])
			stats[host]["cpu"]["system"].appendleft(statsreading[host]["system"])

		# Quick loop to print out what we have in our ring buffers
		for host in stats:
			print host + " -> " + str(list(stats[host]["cpu"]["user"]))
		print "----------------------------------"
		
		# Sleep for 60 seconds until the next check
		time.sleep(60)

if __name__ == "__main__":
	main()
	run()
