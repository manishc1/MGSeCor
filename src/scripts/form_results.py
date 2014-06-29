#! /usr/bin/python

import sys
import os

COMMON_DIR = os.path.abspath(__file__ + '/../../common/')

sys.path.insert(0, COMMON_DIR)
from constants import *

sys.path.insert(0, UTILS_DIR)
from file_utils import *


def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False


def read_results(filename):
	result = []
	lines = read_to_lines(filename, False)
	for line in lines:
		line = line.strip()
		if (isfloat(line)):
			result.append(line)
	return result


def main(cybersec_result_file, generic_result_file, manual_result_file, result_file):
	cybersec_result = read_results(cybersec_result_file)
	generic_result = read_results(generic_result_file)
	manual_result = read_results(manual_result_file)
	result = []
	for i in range(len(cybersec_result)):
		result.append(cybersec_result[i] + ', ' + generic_result[i] + ', ' + manual_result[i])
	write_string(result_file, '\n'.join(result), False)


if __name__ == "__main__":
	"""
	Entry point.
	"""
	nargs = len(sys.argv)
	args = sys.argv
	if nargs < 5:
		print "Usage: python form_result.py <cybersec_result_file> <generic_result_file> <manual_result_file> <result_file>"
	else:
		main(args[1], args[2], args[3], args[4])
