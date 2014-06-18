"""
Basic pdf functional utilities.
"""

from file_utils import *
from system_utils import *


def pdf_url_to_string(url, filename):
	try:
		pdf_filename = download(url, filename)
		txt_filename = pdf_to_txt(pdf_filename)
		remove(pdf_filename)
		if (os.path.exists(txt_filename)):
			string = read_to_string(txt_filename, False)
			remove(txt_filename)
			return string
		else:
			raise
	except Exception as e:
		raise e

