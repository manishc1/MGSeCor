"""
Contains all the constants.
"""

import os


# Directory Name Constants

"""
Directory Structure

--DySeCor
  |
  |--data
  |  |
  |  |--corpus
  |  |  |
  |  |  |--positive
  |  |  |
  |  |  |--negative
  |  |
  |  |--feature
  |  |
  |  |--raw
  |
  |--glossary
  |
  |--src
  |  |
  |  |--common
  |  |
  |  |--scanners
  |  |
  |  |--utils
  |
  |--tmp

"""

# Path to MGSeCor Home Directory
HOME_DIR              = os.path.abspath(__file__ + '/../../../')


DATA_DIR              = HOME_DIR     + '/data'

CORPUS_DIR            = DATA_DIR     + '/corpus'
POSITIVE_CORPUS_DIR   = CORPUS_DIR   + '/positive'
NEGATIVE_CORPUS_DIR   = CORPUS_DIR   + '/negative'

FEATURE_DIR           = DATA_DIR     + '/feature'

RAW_DATA_DIR          = DATA_DIR     + '/raw'
POSITIVE_RAW_DATA_DIR = RAW_DATA_DIR + '/positive'
NEGATIVE_RAW_DATA_DIR = RAW_DATA_DIR + '/negative'


GLOSSARY_DIR          = HOME_DIR     + '/glossary'


SRC_DIR               = HOME_DIR     + '/src'

UTILS_DIR             = SRC_DIR      + '/utils'


CLASSIFIERS_DIR       = SRC_DIR      + '/classifiers'
COMMON_DIR            = SRC_DIR      + '/common'
SCANNERS_DIR          = SRC_DIR      + '/scanners'
SCRIPTS_DIR           = SRC_DIR      + '/scripts'
UTILS_DIR             = SRC_DIR      + '/utils'


TMP_DIR               = HOME_DIR     + '/tmp'



# File Name Constants

COMPUTER_SCIENCE_GLOSSARY_LIST = [GLOSSARY_DIR + '/computer_science_terms-1.gloss', \
                                  GLOSSARY_DIR + '/computer_science_terms-2.gloss', \
                                  GLOSSARY_DIR + '/computer_science_terms-3.gloss', \
                                  GLOSSARY_DIR + '/computer_science_terms-4.gloss']
SECURITY_GLOSSARY_LIST         = [GLOSSARY_DIR + '/nist_glossary_of_key_information_security_terms.gloss', \
                                  GLOSSARY_DIR + '/security_terms.gloss']
STOPWORDS_GLOSSARY_LIST        = [GLOSSARY_DIR + '/stopwords.gloss']
WORD_GLOSSARY_LIST             = [GLOSSARY_DIR + '/words.gloss']



# URL Constants

NVD_BASE_YEAR      = 2002
NVD_LAST_YEAR      = 2014
NVD_YEAR_RSS_URL   = 'http://nvd.nist.gov/download/nvdcve-<YEAR>.xml'
NVD_RECENT_RSS_URL = 'http://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-recent.xml'


ARXIV_SEARCH_QUERY_URL = 'http://export.arxiv.org/api/query?search_query=cat:<CATEGORY>&start=<START>&max_results=<MAX>'


COMPUTER_HOPE_URL = 'http://www.computerhope.com/jargon/j<PAGE>.htm'
MANY_THINGS_URL   = 'http://www.manythings.org/vocabulary/lists/l/words.php?f=3esl.<PAGE>'


SYMANTEC_DOMAIN   = 'http://www.symantec.com/'
SYMANTEC_BLOG_URL = {'In_Defense_Of_Data': ('http://www.symantec.com/connect/symantec-blogs/in-defense-of-data?page=', 10),
					 'Website_Security_Solutions': ('http://www.symantec.com/connect/blogs/website-security-solutions?page=', 65),
					 'Authentication_(User)_Blog': ('http://www.symantec.com/connect/blogs/authentication-user?page=', 20),
					 'Encryption_Blog': ('http://www.symantec.com/connect/symantec-blogs/encryption-blog?page=', 15),
					 'Endpoint_Security_Blog': ('http://www.symantec.com/connect/symantec-blogs/endpoint-security-blog?page=', 5),
					 'Symantec_Connect_Blog': ('http://www.symantec.com/connect/symantec-blogs/symantec-connect?page=', 14),
					 'Mail_and_Web_Security_Blog': ('http://www.symantec.com/connect/symantec-blogs/mail-and-web-security-blog?page=', 3),
					 'Managed_Security_Services_Blog': ('http://www.symantec.com/connect/symantec-blogs/managed-security-services-blog?page=', 3),
					 'Symantec_Intelligence': ('http://www.symantec.com/connect/symantec-blogs/symantec-intelligence?page=', 17),
					 'Cyber_Readiness_&_Response': ('http://www.symantec.com/connect/symantec-blogs/cyber-readiness-and-response?page=', 9),
					 'Security Response Blog': ('http://www.symantec.com/connect/symantec-blogs/sr?page=', 246),
					 'The_Confident_SMB': ('http://www.symantec.com/connect/symantec-blogs/the-confident-smb?page=', 11)}

ADOBE_BLOG_URL = {'Security': ('http://blogs.adobe.com/security/page/', 31)}

KREBS_BASE_YEAR = 2009
KREBS_BASE_MONTH = 12
KREBS_LAST_YEAR = 2014
KREBS_LAST_MONTH = 6
KREBS_BLOG_URL = {'Security': 'http://krebsonsecurity.com/<YEAR>/<MONTH>/feed/'}



# Numeric Constants

WORD_LEN_THRESHOLD = 25
INSTANCE_FILE_LIMIT = 1000



# String Constants

XML_HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n'
