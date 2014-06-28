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
			if (len(line) == 0 or '#' in line[0]):
				continue
			if (line[0:2] == '//'):
				line = line.split(' ', 1)[1]
			if (len(line.split(' ')) > 7):
				continue
			phrases.append(line)
			for word in line.split(' '):
				phrases.append(word)
	return sorted(list(set(phrases)))
