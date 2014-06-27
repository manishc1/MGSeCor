#! /usr/bin/python

"""
Script to create .arff and svm input file
"""

import sys
import os

COMMON_DIR = os.path.abspath(__file__ + '/../../common/')

sys.path.insert(0, COMMON_DIR)
from constants import *

sys.path.insert(0, UTILS_DIR)
from file_utils import *


class Instance_Creator(object):
	"""
	Class to form the instance.
	"""

	def __init__(self, bow_File, feature_length):
		"""
		Initialize the class.
		"""
		self.grams = []
		lines = read_to_lines(bow_File, False)
		for line in lines:
			if (':=' in line and not (line.startswith('#'))):
				self.grams.append(line.split(':=')[0])
		if (feature_length == -1):
			self.length = len(self.grams)
		else:
			self.length = min(len(self.grams), feature_length)
		self.grams = self.grams[0:self.length]


	def create(self, filename):
		"""
		Create the instance.
		"""
		arff_instance = [0] * self.length
		svm_instance = []
		words = read_to_string(filename, False).split()
		for word in words:
			if (word in self.grams):
				index = self.grams.index(word)
				arff_instance[index] = 1
		for index in range(len(arff_instance)):
			svm_instance.append(str(index+1) + ':' + str(arff_instance[index]))
		return arff_instance, svm_instance


class Feature_Vector_Creator(object):
	"""
	Class to for the .arff and svm input file
	"""

	def __init__(self, bow_file, bow_type, ngram, feature_length):
		"""
		Initialize the class.
		"""
		self.bow_file = bow_file
		self.ic = Instance_Creator(self.bow_file, feature_length)
		self.feature_file = CLASSIFIER_MODEL_DIR + '/'+bow_type+'_' + str(ngram) + '/feature_vector_'+str(self.ic.length)


	def get_attribute_str(self):
		"""
		Creates attribute_str for arff.
		"""
		lines = []
		for i in range(self.ic.length):
			lines.append("@attribute 'word" + str(i+1) + "' {0 , 1}")
		lines.append("@attribute 'class' {1 , -1}")
		return lines


	def create(self, dir_list, total_instances):
		"""
		Create the .arff file
		"""
		arff_instances = []
		arff_instances.append('@relation sec_classify')
		arff_instances = arff_instances + self.get_attribute_str()
		arff_instances.append('@data')
		svm_instances_train = []
		svm_instances_test = []
		for path, label_str in dir_list:
			count = 0
			label = 0
			if label_str == 'positive':
				label = 1
			elif label_str == 'negative':
				label = -1
			for rootdir, _, files in os.walk(path):
				for filename in files:
					if (filename.endswith('.txt')):
						arff_instance, svm_instance = self.ic.create(str(rootdir) + '/' + filename)
						arff_instances.append(','.join(str(i) for i in arff_instance) + ',' + str(label))
						if (count < 0.9*total_instances):
							svm_instances_train.append(str(label) + ' ' + ' '.join(svm_instance))
						else:
							svm_instances_test.append(str(label) + ' ' + ' '.join(svm_instance))
						count = count + 1
						if (count >= total_instances):
							break
				if (count >= total_instances):
					break

		write_string(self.feature_file+'.arff', '\n'.join(arff_instances), False)
		write_string(self.feature_file+'_train.data', '\n'.join(svm_instances_train), False)
		write_string(self.feature_file+'_test.data', '\n'.join(svm_instances_test), False)


def main(positive_directory, # = '/home/manish/Dropbox/Thesis/MGSeCor/data/raw/positive/cve/',
	 negative_directory, # = '/home/manish/Dropbox/Thesis/MGSeCor/data/raw/negative/wikipedia/computer_science/',
	 total_instances, ngram, bow_type, total_file_count, feature_length):
	"""
	Entry point.
	"""
	fvc = Feature_Vector_Creator(CLASSIFIER_MODEL_DIR + '/' + bow_type+'_'+str(ngram) + '/file_count_'+str(total_file_count)+'.bow', bow_type, ngram, feature_length)
	fvc.create([tuple([positive_directory, 'positive']), tuple([negative_directory, 'negative'])], total_instances)


if __name__=="__main__":
	"""
	Entry point.
	"""
	nargs = len(sys.argv)
	args = sys.argv
	if nargs < 8:
		print "Usage: python form_instances.py <positive-directory> <negative-directory> <# instances> <n-gram> <bow_type> <file_count> <feature_length>"
	else:
		main(args[1], args[2], eval(args[3]), eval(args[4]), args[5], eval(args[6]), eval(args[7]))
