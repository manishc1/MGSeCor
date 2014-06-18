#! /usr/bin/python

"""
Scanner for microsoft security bulletins. (https://technet.microsoft.com/en-us/library/security/)
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


class Microsoft_Bulletin_Scanner(object):
	"""
	Class for scanning the microsoft security bulletins.
	"""

	def __init__(self):
		"""
		Initializes the class.
		"""
		self.urls = MICROSOFT_BULLETIN_URL
		self.corpus_dir = POSITIVE_CORPUS_DIR + '/bulletin/microsoft'
		self.raw_dir = POSITIVE_RAW_DATA_DIR + '/bulletin/microsoft'
		self.count = 0


	def scan(self):
		"""
		Scans the url.
		"""
		try:
			year = MICROSOFT_BASE_YEAR
			for bulletin, url_template in self.urls.items():
				while(year <= MICROSOFT_LAST_YEAR):
					page = 1
					while(page <= MICROSOFT_PAGES[year]):
						year_str = str(year)[-2:len(str(year))]
						page_str = str(page).zfill(3)
						url = url_template.replace('<YEAR>', year_str).replace('<PAGE>', page_str)
						html = urllib2.urlopen(url).read()
						soup = BeautifulSoup(html)

						date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
						entry_src = 'microsoft'
						entry_type = bulletin
						entry_id = 'MS' + year_str + '-' + page_str

						div = soup.find('div', {'id': 'mainBody'})

						entry_title = div.find('h2', {'class': 'subheading'})
						if (entry_title is None):
							entry_title = 'Krebsonsecurity_' + date
						else:
							entry_title = entry_title.text.strip()

						entry_date = str(year)
						entry_date_div = div.find('div', {'id': 'pubInfo'})
						if not (entry_date_div is None):
							paras = entry_date_div.findAll('p')
							for para in paras:
								if ('pub' in para.text.lower()):
									entry_date = para.text.split(' ', 1)[1]

						entry_desc = ''
						paras = div.findAll('p', recursive=True)
						para_lines = []
						for para in paras:
							# hacks
							if (len(para.text.split(' ')) < 10 or
								'for additional' in para.text.lower() or
								'the information provided' in para.text.lower() or
								'built at' in para.text.lower()):
								continue
							para_lines.append(para.text)

						entry_desc = '\n'.join(para_lines)

						if (''.join(entry_desc.split()) != ''):
							xml_string = bundle_xml(entry_src, entry_type, entry_id, entry_title, entry_date, clean(entry_desc))

							write_string(self.corpus_dir + '/' + entry_id.lower() + '.xml', xml_string, False)
							write_string(self.raw_dir + '/' + entry_id.lower() + '.txt', entry_desc, True)

							self.count = self.count + 1
							if (self.count % 100 == 0):
								print 'Scanned ' + str(self.count) + ' files from ' + bulletin

						page = page + 1

					year = year + 1

		except Exception as e:
			print 'Scanning error in <' + url + '>! [' + str(e) + ']'


def main():
	"""
	Main function.
	"""
	mbs = Microsoft_Bulletin_Scanner()
	mbs.scan()


if __name__ == "__main__":
	"""
	Entry point.
	"""
	main()

