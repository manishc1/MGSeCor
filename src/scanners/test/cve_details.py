#! /usr/bin/python

"""
Scans the Vulnerabilities from http://www.cvedetails.com/
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


class CVE_Details_Scanner(object):
	"""
	Class for scanning the vulnerabilites.
	"""

	def __init__(self):
		"""
		Initializes the class.
		"""
		self.url = CVE_DETAILS_RSS_URL
		self.test_dir = TEST_DIR + '/cve_cve/'
		self.count = 0


	def scan(self):
		"""
		Scans the url.
		"""
		try:
			for vuln_type, vuln_id in CVE_DETAILS_TYPES.items():
				html = urllib2.urlopen(self.url.replace('<TYPE>', vuln_id)).read()
				soup = BeautifulSoup(html)
				items = soup.findAll('item')
				vulnerabilites = []
				for item in items:
					vulnerabilites.append(item.find('description').text.rsplit('Last Update',1)[0].rsplit('CVSS',1)[0].rsplit(' ',1)[0])

				write_string(self.test_dir + '/' + vuln_type.lower() + '/' + vuln_type.lower() + '.txt', '\n# ----------\n'.join(vulnerabilites), False)

				for one in range(len(vulnerabilites)):
					for two in range(one+1, len(vulnerabilites)):
						write_string(self.test_dir + '/' + vuln_type.lower() + '/' + 'pair_'+str(one)+'_'+str(two)+'.txt', vulnerabilites[one]+'\n'+vulnerabilites[two], False)


		except Exception as e:
			print 'Scanning error in <' + self.url + '>! [' + str(e) + ']'


def main():
	"""
	Main function.
	"""
	cds = CVE_Details_Scanner()
	cds.scan()


if __name__ == "__main__":
	"""
	Entry point.
	"""
	main()

