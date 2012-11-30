#!/usr/bin/python

import socket
import collections
from collections import defaultdict
import time

# Keep up to MAX_STATS_BUFFER_SIZE readings in our ring buffer
MAX_STATS_BUFFER_SIZE = 8

def makehash():
	return collections.defaultdict(makehash)


# Set up a dictionary to hold stats ring buffers (keyed by hostname)
stats = makehash()

def get_cpu_stats():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('mc.onethree.net', 6557))

	s.send("GET services\nFilter: description ~ CPU util\nColumns: host_name perf_data\n")

	s.shutdown(socket.SHUT_WR)

	answer = s.recv(100000000)

	statsdict = defaultdict(dict)

	for line in answer.split('\n')[:-1]:	
		params = filter(bool, line.split(';'))

		for item in params[1:]:
			if "=" in item:
				(key, value) = item.split('=')
				statsdict[params[0]][key.strip()] = value
	return statsdict


def run():
	while True:
		statsreading = get_cpu_stats()

		for host in statsreading:
			if not stats[host]["cpu"]["wait"]:
				stats[host]["cpu"]["wait"] = collections.deque(maxlen=MAX_STATS_BUFFER_SIZE)
				stats[host]["cpu"]["user"] = collections.deque(maxlen=MAX_STATS_BUFFER_SIZE)
				stats[host]["cpu"]["system"] = collections.deque(maxlen=MAX_STATS_BUFFER_SIZE)

			stats[host]["cpu"]["wait"].appendleft(statsreading[host]["wait"])
			stats[host]["cpu"]["user"].appendleft(statsreading[host]["user"])
			stats[host]["cpu"]["system"].appendleft(statsreading[host]["system"])

		for host in stats:
			print host + " -> " + str(list(stats[host]["cpu"]["user"]))
		print "----------------------------------"
		
		time.sleep(60)

if __name__ == "__main__":
	run()