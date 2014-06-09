#! /usr/bin/python

"""
Details to grab the NVD vulnerabilities.
"""

import sys
import os

COMMON_DIR = os.path.abspath(__file__ + '/../../../common/')

sys.path.insert(0, COMMON_DIR)
from constants import *

sys.path.insert(0, UTILS_DIR)
from file_utils import *
from xml_utils import *

from bs4 import BeautifulSoup
import urllib2


class NVD_Recent_Scanner(object):
	"""
	Class for scanning the nvd recent rss feed.
	"""

	def __init__(self):
		"""
		Initializes the class.
		"""
		self.url = NVD_RECENT_RSS_URL
		self.corpus_dir = POSITIVE_CORPUS_DIR + '/cve/recent'
		self.raw_dir = POSITIVE_RAW_DATA_DIR + '/cve/recent'
		self.count = 0


	def scan(self):
		"""
		Scans the url.
		"""
		xml = urllib2.urlopen(self.url).read()
		soup = BeautifulSoup(xml)
		entries = soup.findAll('entry')
		for entry in entries:
			entry_src = 'cve_recent'
			entry_type = 'vulnerability'
			entry_id = entry.find('vuln:cve-id').text.strip()
			entry_title = entry.get('id').strip()
			entry_date = entry.find('vuln:last-modified-datetime').text.strip()
			entry_desc = entry.find('vuln:summary').text.strip()

			xml_string = bundle_xml(entry_src, entry_type, entry_id, entry_title, entry_date, entry_desc)
			
			write_string(self.corpus_dir + '/' + entry_id + '.xml', xml_string, False)
			write_string(self.raw_dir + '/' + entry_id + '.txt', entry_desc, True)

			self.count = self.count + 1
			if (self.count % 1000 == 0):
				print 'Scanned ' + str(self.count) + ' files from recent'
			break
		

class NVD_Yearwise_Scanner(object):
	"""
	Class for scanning the nvd yearwise rss feed.
	"""

	def __init__(self):
		"""
		Initializes the class.
		"""
		self.url = NVD_YEAR_RSS_URL
		self.corpus_dir = POSITIVE_CORPUS_DIR + '/cve/<YEAR>'
		self.raw_dir = POSITIVE_RAW_DATA_DIR + '/cve/<YEAR>'
		self.count = 0


	def scan(self):
		"""
		Iterates for all the years.
		"""
		year = NVD_BASE_YEAR
		while(year <= NVD_LAST_YEAR):
			url = self.url.replace('<YEAR>', str(year))
			corpus_dir = self.corpus_dir.replace('<YEAR>', str(year))
			raw_dir = self.raw_dir.replace('<YEAR>', str(year))
			self.scan_helper(year, url, corpus_dir, raw_dir)
			year = year + 1
			break


	def scan_helper(self, year, url, corpus_dir, raw_dir):
		"""
		Scans the url.
		"""
		xml = urllib2.urlopen(url).read()
		soup = BeautifulSoup(xml)
		entries = soup.findAll('entry')
		for entry in entries:
			entry_src = 'cve_' + str(year)
			entry_type = 'vulnerability'
			entry_id = entry.get('name').strip()
			entry_title = entry_id
			entry_date = entry.get('published').strip()
			entry_desc = entry.find('desc').find('descript').text.strip()

			xml_string = bundle_xml(entry_src, entry_type, entry_id, entry_title, entry_date, entry_desc)

			write_string(corpus_dir + '/' + entry_id + '.xml', xml_string, False)
			write_string(raw_dir + '/' + entry_id + '.txt', entry_desc, True)

			self.count = self.count + 1
			if (self.count % 1000 == 0):
				print 'Scanned ' + str(self.count) + ' files from ' + str(year)
			break


def main():
	"""
	Main function.
	"""
	#nrs = NVD_Recent_Scanner()
	#nrs.scan()
	nys = NVD_Yearwise_Scanner()
	nys.scan()


if __name__ == "__main__":
	"""
	Entry point.
	"""
	main()
