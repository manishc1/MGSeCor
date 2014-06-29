#! /usr/bin/python

import sys
import os

COMMON_DIR = os.path.abspath(__file__ + '/../../common/')

sys.path.insert(0, COMMON_DIR)
from constants import *

sys.path.insert(0, UTILS_DIR)
from file_utils import *

def traverse_dir(directory):
	"""
	Traverses the dir and cleans all the files in it.
	"""
	for rootdir, _, files in os.walk(directory):
		for f in files:
			if (f.endswith('.txt')):
				text = read_to_string(str(rootdir) + '/' + f, False)
				write_string(str(rootdir) + '/' + f, text, True)


def main(directory):
	"""
	Main function.
	"""
	if (os.path.isdir(directory)):
		traverse_dir(directory)
	else:
		print 'Invalid directory.'


if __name__ == "__main__":
	"""
	Entry point.
	"""
	nargs = len(sys.argv)
	args = sys.argv
	if nargs < 2:
		print "Usage: python clean_files.py <directory>"
	else:
		main(args[1])
