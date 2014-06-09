"""
Basic glossary functional utilities.
"""

from file_utils import *


def get_phrases(gloss_list):
	"""
	Returns phrases from the glossary list.
	"""
	phrases = []
	for gloss in gloss_list:
		lines = read_to_lines(gloss, True)
		for line in lines:
			line = line.lower().strip()
			if (len(line) == 0 or line[0] == '#'):
				continue
			if (line[0:2] == '//'):
				line = line.split(' ', 1)[1]
			phrases.append(line)
	return sorted(list(set(phrases)))
