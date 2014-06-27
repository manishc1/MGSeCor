#! /usr/bin/python

"""
Forms a bag of words.
"""

import sys
import os

COMMON_DIR = os.path.abspath(__file__ + '/../../common/')

sys.path.insert(0, COMMON_DIR)
from constants import *

sys.path.insert(0, UTILS_DIR)
from file_utils import *


class Frequency_Counter(object):
	"""
	Class to calculate the frequencies of words.
	"""

	def __init__(self, dir_list, total_file_count, ngram):
		"""
		Initialize the Frequency_Counter class.
		"""
		self.dir_list = dir_list
		self.total_file_count = total_file_count
		self.ngram = ngram

		self.frequencies = [{}, {}] # [total_words_dict, word_document_dict]

		self.stop_words = []
		for filename in STOPWORDS_GLOSSARY_LIST:			
			self.stop_words = self.stop_words + read_to_lines(filename, False)

		self.filenames = [CLASSIFIER_MODEL_DIR + '/word_' + str(ngram) + '/file_count_'+str(self.total_file_count)+'.bow',
						  CLASSIFIER_MODEL_DIR + '/doc_' + str(ngram) + '/file_count_'+str(self.total_file_count)+'.bow']


	def add_to_freq(self, grams, index):
		"""
		Adds the words to the frequency counts.
		"""
		for gram in grams:
			count = 0
			if (gram in self.stop_words):
				continue
			if (self.frequencies[index].has_key(gram)):
				count = self.frequencies[index][gram] + 1
			else:
				count = 1
			self.frequencies[index][gram] = count


	def form_grams(self, string):
		"""
		Parses the string and extracts grams.
		"""
		words = string.lower().split()
		grams = []
		length = len(words)
		for i in range(length):
			gram = []
			for n in range(self.ngram):
				if (i+n < length):
					gram.append(words[i+n].rstrip('\'\"-,.:;!?'))
					count = 0
					for word in gram:
						if word in self.stop_words:
							count = count + 1
					if (count < n+1):
						grams.append(' '.join(gram))
		return grams


	def traverse_dir(self):
		"""
		Walks the directories.
		"""
		for path in self.dir_list:
			count = 0
			for rootdir, _, files in os.walk(path):
				for filename in files:
					if (filename.endswith('.txt')):
						string = read_to_string(rootdir+'/'+filename, True)
						grams = self.form_grams(string)
						self.add_to_freq(grams, 0)
						grams = list(set(grams))
						self.add_to_freq(grams, 1)

						count = count + 1
						if (count >= self.total_file_count):
							break
				if (count >= self.total_file_count):
					break


	def write(self):
		"""
		Write to the bag of words file.
		"""
		for index in range(len(self.frequencies)):
			lines = []
			lines.append('# positive_directory: ' + self.dir_list[0])
			lines.append('# negative_directory: ' + self.dir_list[1])
			lines.append('# total_file_count: ' + str(self.total_file_count))
			lines.append('# ngram: ' + str(self.ngram))
			lines.append('# length: ' + str(len(self.frequencies[index].keys())))
			frequency = sorted(self.frequencies[index].items(), key=lambda x: x[1], reverse=True)
			for key, val in frequency:
				lines.append(str(key) + ':=' + str(val))
			write_string(self.filenames[index], '\n'.join(lines), False)


def main(positive_directory, # = '/home/manish/Dropbox/Thesis/MGSeCor/data/raw/positive/cve/',
	 negative_directory, # = '/home/manish/Dropbox/Thesis/MGSeCor/data/raw/negative/wikipedia/computer_science/',
	 total_file_count, ngram):
	fc = Frequency_Counter([positive_directory, negative_directory], total_file_count, ngram)
	fc.traverse_dir()
	fc.write()


if __name__ == "__main__":
	"""
	Entry point.
	"""
	nargs = len(sys.argv)
	args = sys.argv
	if nargs < 5:
		print "Usage: python form_bag_of_words.py <positive-directory> <negative-directory> <# file_count> <n-gram>"
	else:
		main(args[1], args[2], eval(args[3]), eval(args[4]))
