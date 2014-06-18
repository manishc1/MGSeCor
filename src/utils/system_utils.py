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
	try:
		download_filename = TMP_DIR + '/' + filename
		urllib.urlretrieve(url, download_filename)
		return download_filename
	except Exception as e:
		raise e


def pdf_to_txt(pdf_filename):
	"""
	Converts .pdf to .txt
	"""
	try:
		os.system('pdftotext %(pdf_filename)s' % locals())
		return pdf_filename.replace('.pdf', '.txt')
	except Exception as e:
		raise e


def remove(filename):
	"""
	Deletes the file.
	"""	
	try:
		os.system('rm %(filename)s' % locals())
	except Exception as e:
		raise e
