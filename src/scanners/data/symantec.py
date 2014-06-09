#! /usr/bin/python

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


class Symantec_Blog_Scanner(object):
	"""
	Class for scanning the symantec security blogs.
	"""

	def __init__(self):
		"""
		Initializes the class.
		"""
		self.urls = SYMANTEC_BLOG_URL
		self.corpus_dir = POSITIVE_CORPUS_DIR + '/blog/symantec'
		self.raw_dir = POSITIVE_RAW_DATA_DIR + '/blog/symantec'
		self.count = 0


	def scan(self):
		"""
		Scans the url.
		"""
		try:
			for blog, (url, max_page) in self.urls.items():
				page = 0
				while(page <= max_page):
					html = urllib2.urlopen(url + str(page)).read()
					soup = BeautifulSoup(html)
					read_more_urls = []
					a_s = soup.findAll('a')
					for a in a_s:
						if (a.text.strip() == 'Read more'):
							read_more_urls.append(SYMANTEC_DOMAIN + a.get('href').strip())

					try:
						for read_more_url in read_more_urls:
							entry_src = 'symantec'

							html = urllib2.urlopen(read_more_url).read()
							soup = BeautifulSoup(html)
							banner_div = soup.find('div', {'class': 'blog-brand-banner'})
							entry_type = None
							if (banner_div is not None):
								entry_type = banner_div.find('div', {'class': 'blog-brand-name'})
							if (entry_type is None):
								entry_type = blog
							else:
								entry_type = entry_type.text.strip()

							entry_id = 'blog_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')

							entry_title = soup.find('h1', {'itemprop': 'name', 'class': 'node-title'})
							if (entry_title is None):
								entry_title = ''
							else:
								entry_title = entry_title.text.strip()

							entry_date = soup.find('div', {'class': 'node-posted'})
							if (entry_date is None):
								entry_date = ''
							else:
								entry_date = asciify(entry_date.text.strip())

							entry_desc = ''
							article_div = soup.find('div', {'itemprop': 'articleBody', 'class': 'content clearfix'})
							if (article_div is None):
								print 'description not found'
								continue
							paras = article_div.findAll('p')
							for para in paras:
								entry_desc = entry_desc + para.text.strip()

							xml_string = bundle_xml(entry_src, entry_type, entry_id, entry_title, entry_date, entry_desc)
			
							write_string(self.corpus_dir + '/' + asciify(entry_type).replace(' ', '_') + '/' + asciify(entry_title).replace(' ', '_') + '.xml', xml_string, True)
							write_string(self.raw_dir + '/' + asciify(entry_type).replace(' ', '_') + '/' + asciify(entry_title).replace(' ', '_') + '.txt', entry_desc, True)

							self.count = self.count + 1
							if (self.count % 100 == 0):
								print 'Scanned ' + str(self.count) + ' files from ' + blog

					except Exception as e:
						print 'Read more url error in <' + read_more_url + '> [' + str(e) + ']'

					page = page + 1

		except Exception as e:
			print 'Scanning error in <' + url + '>! [' + str(e) + ']'


def main():
	"""
	Main function.
	"""
	sbs = Symantec_Blog_Scanner()
	sbs.scan()


if __name__ == "__main__":
	"""
	Entry point.
	"""
	main()

