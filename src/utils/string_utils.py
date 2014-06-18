"""
Basic string functional utilities.
"""

import re


def asciify(string):
	"""
	Removes non-ascii characters from the string.
	"""
	new_string = ''
	for c in string:
		if ((c == '\n') or (32 <= ord(c)) and (ord(c) <= 126)):
			new_string = new_string + c
		else:
			new_string = new_string + ' '
	return new_string


def detag(string):
	"""
	Remove words of type '&xxx;' from the string.
	"""
	lines = string.split('\n')
	new_lines = []
	for line in lines:
		words = line.split()
		new_words = []
		for word in words:
			word.strip()
			if ('&' in word and ';' in word):				
				word1 = word.split('&')[0]
				if (len(word1) > 0):
					new_words.append(word1)
				word2 = word.split(';')[1]
				if (len(word2) > 0):
					new_words.append(word2)
			else:
				new_words.append(word)
		if (len(new_words) > 0):
			new_lines.append(' '.join(new_words))
	return '\n'.join(new_lines)


def replace_abbrv(string):
    """
    Replace abbrv like & -> and in the string.
    """
    return string.replace('&', 'and').replace('/', '-').replace('.', '. ').replace(',', ', ').replace('!', '! ').replace('?', '? ')


def depunctuate(string):
	"""
	Extract alphanumeric words from the string.
	"""
	lines = string.split('\n')
	new_lines = []
	for line in lines:
		words = re.findall("[\w',.!?-]+", line)
		if (len(words) > 0):
			new_lines.append(' '.join(words))
	return '\n'.join(new_lines)


def dedigit(string):
	"""
	Remove digits from the string.
	"""
	lines = string.split('\n')
	new_lines = []
	for line in lines:
		words = line.split()
		new_words = []
		for word in words:
			if (word.isdigit() or (re.search('[a-zA-Z]+', word) is None)):
				continue
			if (len(word) > 0):
				new_words.append(word)
		new_lines.append(' '.join(new_words))
	return '\n'.join(new_lines)


def clean(string):
	"""
	Cleans the string to have ascii characters and somewhat valid words.
	"""
	if (string in ['', None]):
		return ''
	string = string.strip()
	string = asciify(string)
	string = detag(string)
	string = replace_abbrv(string)
	string = depunctuate(string)
	string = dedigit(string)
	return string


def paragraphify(string):
	"""
	Forms appropriate paragraphs.
	"""
	lines = string.split('\n')
	new_lines = []
	new_line = ''
	for line in lines:
		new_line = new_line + ' ' + line
		new_line = new_line.strip()
		if (new_line.endswith('.') or new_line.endswith('!') or new_line.endswith('?')):
			# If it is proper end of sentence.
			new_lines.append(new_line)
			new_line = ''
	return '\n'.join(new_lines)
