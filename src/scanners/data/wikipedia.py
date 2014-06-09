"""
Fetches wikipedia articles for the nist glossary terms.
"""

import sys
import os

COMMON_DIR = os.path.abspath(__file__ + '/../../../common/')

sys.path.insert(0, COMMON_DIR)
from constants import *

sys.path.insert(0, UTILS_DIR)
from datetime import datetime
from file_utils import *
from glossary_utils import *
from xml_utils import *

from wikiapi import WikiApi


class Wikipedia_Scanner(object):
	"""
	Class to Scann wikipedia articles.
	"""

	def __init__(self, add_gloss_list, del_gloss_list, category, label):
		"""
		Initialize the class.
		"""
		self.add_phrases = get_phrases(add_gloss_list)
		self.del_phrases = get_phrases(del_gloss_list)
		self.category = category
		self.corpus_dir = CORPUS_DIR + '/' + label + '/wikipedia/' + category
		self.raw_dir = RAW_DATA_DIR + '/' + label + '/wikipedia/' + category
		self.wiki = WikiApi({})
		self.visited_results = self.get_results(self.del_phrases)


	def get_results(self, phrases):
		"""
		Return dictionary of wiki results corresponding to phrases.
		"""
		visited_results = {}
		for phrase in phrases:
			results = self.wiki.find(phrase)
			for result in results:
				if (not visited_results.has_key(result)):
					visited_results[result] = True
		return visited_results


	def get_articles(self):
		"""
		Fetches articles and puts in data directory.
		"""
		for phrase in self.add_phrases:
			try:
				results = self.wiki.find(phrase)
				for result in results:
					if (not self.visited_results.has_key(result)):
						self.visited_results[result] = True

						article = self.wiki.get_article(result)
						entry_src = 'wikipedia_' + self.category
						entry_type = 'article'
						entry_id = 'wikipedia_' + result.replace(' ', '_')
						entry_title = article.heading
						entry_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
						entry_desc = clean(article.summary)

						xml_string = bundle_xml(entry_src, entry_type, entry_id, entry_title, entry_date, entry_desc)
			
						write_string(self.corpus_dir + '/' + entry_id + '.xml', xml_string, False)
						write_string(self.raw_dir + '/' + entry_id + '.txt', entry_desc, True)

			except Exception as e:
				print 'Wiki Api Error! [' + str(e) + ']'


def main(category, label):
	"""
	Main function.
	"""
	if (category == 'security' and label == 'positive'):
		ws = Wikipedia_Scanner(SECURITY_GLOSSARY_LIST, [], category, label)
		ws.get_articles()
	elif (category == 'computer_science' and label == 'negative'):
		ws = Wikipedia_Scanner(COMPUTER_SCIENCE_GLOSSARY_LIST, [], category, label)
		ws.get_articles()
	elif (category == 'words' and label == 'negative'):
		ws = Wikipedia_Scanner(WORD_GLOSSARY_LIST, [], category, label)
		ws.get_articles()
	else:
		print 'Invalid arguments!'
 

if __name__=="__main__":
	"""
	Entry point.
	"""
	nargs = len(sys.argv)
	args = sys.argv
	if nargs < 3:
		print "Usage: python wikipedia.py <category> <'positive'/'negative'>"
	else:
		main(args[1], args[2])
