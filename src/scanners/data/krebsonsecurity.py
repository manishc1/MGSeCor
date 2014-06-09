#! /usr/bin/python

"""
Scanner for krebs on security blogs. (http://krebsonsecurity.com/)
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
from datetime import datetime
import urllib2


class Adobe_Blog_Scanner(object):
	"""
	Class for scanning the symantec security blogs.
	"""

	def __init__(self):
		"""
		Initializes the class.
		"""
		self.urls = KREBS_BLOG_URL
		self.corpus_dir = POSITIVE_CORPUS_DIR + '/blog/krebsonsecurity'
		self.raw_dir = POSITIVE_RAW_DATA_DIR + '/blog/krebsonsecurity'
		self.count = 0


	def scan(self):
		"""
		Scans the url.
		"""
		try:
			year = KREBS_BASE_YEAR
			month = KREBS_BASE_MONTH
			for blog, url_template in self.urls.items():
				while((year < KREBS_LAST_YEAR) or (year == KREBS_LAST_YEAR and month <= KREBS_LAST_MONTH)):
					url = url_template.replace('<YEAR>', str(year)).replace('<MONTH>', str(month))
					html = urllib2.urlopen(url).read()
					soup = BeautifulSoup(html)
					items = soup.findAll('item')
					for item in items:
						date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
						entry_src = 'krebsonsecurity'
						entry_type = blog
						entry_date = date

						entry_id = item.find('guid')
						if (entry_id is None):
							entry_id = 'blog_' + entry_date
						else:
							entry_id = entry_id.text.split('=')[1]

						entry_title = item.find('title')
						if (entry_title is None):
							entry_title = 'Krebsonsecurity_' + date
						else:
							entry_title = entry_title.text.strip()

						entry_desc = item.find('content:encoded')
						if (entry_desc is None):
							print 'description not found'
							continue
						else:
							entry_desc = clean(entry_desc.text)
						
						xml_string = bundle_xml(entry_src, entry_type, entry_id, entry_title, entry_date, entry_desc)

						write_string(self.corpus_dir + '/' + asciify(entry_type).lower().replace(' ', '_') + '/' + asciify(entry_title).replace(' ', '_') + '.xml', xml_string, False)
						write_string(self.raw_dir + '/' + asciify(entry_type).lower().replace(' ', '_') + '/' + asciify(entry_title).replace(' ', '_') + '.txt', entry_desc, True)

						self.count = self.count + 1
						if (self.count % 100 == 0):
							print 'Scanned ' + str(self.count) + ' files from ' + blog

					if (month == 12):
						month = 1
						year = year + 1
					else:
						month = month + 1

		except Exception as e:
			print 'Scanning error in <' + url + '>! [' + str(e) + ']'


def main():
	"""
	Main function.
	"""
	abs = Adobe_Blog_Scanner()
	abs.scan()


if __name__ == "__main__":
	"""
	Entry point.
	"""
	main()

