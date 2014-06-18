#! /usr/bin/python

"""
Scrape the pdf papers from the arxiv.
"""

import sys
import os

COMMON_DIR = os.path.abspath(__file__ + '/../../../common/')

sys.path.insert(0, COMMON_DIR)
from constants import *

sys.path.insert(0, UTILS_DIR)
from file_utils import *
from pdf_utils import *
from string_utils import *
from xml_utils import *

from bs4 import BeautifulSoup
import urllib2


class Arxiv_Scanner(object):
	"""
	Class for scanning the arxiv search query.
	"""

	def __init__(self, category, label):
		"""
		Initializes the class.
		"""
		self.url = ARXIV_SEARCH_QUERY_URL.replace('<CATEGORY>', category)
		self.corpus_dir = CORPUS_DIR + '/' + label + '/paper/arxiv/' + category
		self.raw_dir = RAW_DATA_DIR + '/' + label + '/paper/arxiv/' + category
		self.category = category
		self.max = 100
		self.count = 0


	def scan(self):
		"""
		Scans the url.
		"""
		self.start = 0
		while(True):
			xml = urllib2.urlopen(self.url.replace('<START>',str(self.start)).replace('<MAX>',str(self.max))).read()
			soup = BeautifulSoup(xml)
			entries = soup.findAll('entry')
			for entry in entries:
				entry_src = 'arxiv'
				entry_type = 'scholar_paper'
				entry_id = entry.find('id').text.strip().split('/')[-1]
				entry_title = entry.find('title').text.strip()
				entry_date = entry.find('published').text.strip()
				entry_pdf_url = entry.find('link', {'title':'pdf'}).get('href').strip() + '.pdf'
				try:
					entry_desc = clean(pdf_url_to_string(entry_pdf_url, entry_id + '.pdf'))
					entry_desc = paragraphify(entry_desc)
				except Exception as e:
					print 'PDF Conversion Error in <' + entry_pdf_url + '> [' + str(e) + ']'
					print 'description not found'
					continue

				if (''.join(entry_desc.split()) != ''):
					xml_string = bundle_xml(entry_src, entry_type, entry_id, entry_title, entry_date, entry_desc)
					write_string(self.corpus_dir + '/' + entry_id.lower() + '.xml', xml_string, False)
					write_string(self.raw_dir + '/' + entry_id.lower() + '.txt', entry_desc, False)

					self.count = self.count + 1
					if (self.count % 100 == 0):
						print 'Scanned ' + str(self.count) + ' papers from ' + self.category

			if (len(entries) < self.max):
				break

			self.start = self.start + self.max


def main(category, label):
	ars = Arxiv_Scanner(category, label)
	ars.scan()


if __name__ == "__main__":
	"""
	Entry point.
	"""
	# Refer config/arxiv_category_abbrv.txt for categoties.
	nargs = len(sys.argv)
	args = sys.argv
	if (nargs < 3):
		print 'Usage: arxiv.py <category> <positive/negative>'
	else:
		main(args[1], args[2])
