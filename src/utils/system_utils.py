"""
Basic pdf functional utilities.
"""


import sys
import os
import urllib

COMMON_DIR = os.path.abspath(__file__ + '/../../../common/')

sys.path.insert(0, COMMON_DIR)
from constants import *


def download(url, filename):
	"""
	Donloads the file at url.
	"""
	download_filename = TMP_DIR + '/' + filename
	urllib.urlretrieve(url, download_filename)
	return download_filename


def pdf_to_txt(pdf_filename):
	"""
	Converts .pdf to .txt
	"""
	os.system('pdftotext %(pdf_filename)s' % locals())
	return pdf_filename.replace('.pdf', '.txt')


def remove(filename):
	"""
	Deletes the file.
	"""	
	os.system('rm %(filename)s' % locals())
