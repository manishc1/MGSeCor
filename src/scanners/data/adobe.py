#! /usr/bin/python

"""
Scanner for adobe security blogs. (http://blogs.adobe.com/security/)
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
		self.urls = ADOBE_BLOG_URL
		self.corpus_dir = POSITIVE_CORPUS_DIR + '/blog/adobe'
		self.raw_dir = POSITIVE_RAW_DATA_DIR + '/blog/adobe'
		self.count = 0


	def scan(self):
		"""
		Scans the url.
		"""
		try:
			for blog, (url, max_page) in self.urls.items():
				page = 1
				while(page <= max_page):
					html = urllib2.urlopen(url + str(page)).read()
					soup = BeautifulSoup(html)
					title_urls = []
					h2_s = soup.findAll('h2', {'class': 'entry-title'})
					for h2 in h2_s:
						title_urls.append(h2.find('a').get('href').strip())

					try:
						for title_url in title_urls:
							date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
							entry_src = 'adobe'
							entry_type = blog
							entry_id = 'blog_' + date

							entry_date = date
							entry_date_div = soup.findAll('div', {'class': 'entry-left-text'})
							if not (entry_date_div is None):
								for div in entry_date_div:
									if (len(div.text.strip()) > 0):
										entry_date = asciify(div.text.strip())
										break

							html = urllib2.urlopen(title_url).read()
							soup = BeautifulSoup(html)
							content_div = soup.find('div', {'id': 'content'})							

							entry_title = content_div.find('h2', {'class': 'entry-title'})
							if (entry_title is None):
								entry_title = 'Adobe_' + entry_date
							else:
								entry_title = entry_title.text.strip()

							entry_desc = ''
							article_div = soup.find('div', {'class': 'entry-content'})
							if (article_div is None):
								print 'description not found'
								continue
							paras = article_div.findAll('p')
							for para in paras:
								entry_desc = entry_desc + para.text.strip() + ' '

							if (entry_desc != ''):
								xml_string = bundle_xml(entry_src, entry_type, entry_id, entry_title, entry_date, clean(entry_desc))
			
								write_string(self.corpus_dir + '/' + asciify(entry_type).lower().replace(' ', '_') + '/' + asciify(entry_title).replace(' ', '_') + '.xml', xml_string, False)
								write_string(self.raw_dir + '/' + asciify(entry_type).lower().replace(' ', '_') + '/' + asciify(entry_title).replace(' ', '_') + '.txt', entry_desc, True)

								self.count = self.count + 1
								if (self.count % 100 == 0):
									print 'Scanned ' + str(self.count) + ' files from ' + blog

					except Exception as e:
						print 'Read more url error in <' + title_url + '> [' + str(e) + ']'

					page = page + 1

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

