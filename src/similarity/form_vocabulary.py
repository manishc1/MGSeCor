#! /usr/bin/python

"""
Forms a vocabulary of words.
"""

import sys
import os

COMMON_DIR = os.path.abspath(__file__ + '/../../common/')

sys.path.insert(0, COMMON_DIR)
from constants import *

sys.path.insert(0, UTILS_DIR)
from file_utils import *
from glossary_utils import *


class Vocabulary_Creator(object):
	"""
	Class to create the vocabulary from given list of files.
	"""

	def __init__(self, directory, filename):
		"""
		Initializes the Vocabulary Creator class.
		"""
		self.directory = directory
		self.glossary = get_phrases(COMPUTER_SCIENCE_GLOSSARY_LIST + SECURITY_GLOSSARY_LIST)
		self.voc_filename = filename + '.voc'

	def create(self):
		"""
		Creates the vocabulary and writes to the file.
		"""
		print len(self.glossary)


def main(directory, filename):
	"""
	Main Function.
	"""
	vc = Vocabulary_Creator(directory, filename)
	vc.create()


if __name__ == "__main__":
	"""
	Entry point.
	"""
	nargs = len(sys.argv)
	args = sys.argv
	if nargs < 3:
		print "Usage: python form_vocabulary.py <positive-directory> <vocab-filename>"
	else:
		main(args[1], args[2])

