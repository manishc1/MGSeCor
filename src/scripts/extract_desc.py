#! /usr/bin/python


import sys
import os

COMMON_DIR = os.path.abspath(__file__ + '/../../common/')

sys.path.insert(0, COMMON_DIR)
from constants import *

sys.path.insert(0, UTILS_DIR)
from file_utils import *

import xml.etree.ElementTree as ET


def read_desc(filename):
    """
    Parse the .xml
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root:
        docDesc = ''
        if (child.tag == 'Description'):
            docDesc = clean(child.text)
            if (docDesc is None):
                docDesc = ''
    return docDesc.lower()


def extract(src_path, dest_path):
    """
    Traverse the dir.
    """
    for rootdir, _, files in os.walk(src_path):
        for filename in files:
            if (filename.endswith('.xml')):
				desc = read_desc(str(rootdir) + '/' + filename)
				write_string(dest_path + '/' + filename.replace('.xml', '.txt'), desc, True)


def main(src_path, dest_path):
    extract(src_path, dest_path)


if __name__ == "__main__":
	"""
	Entry point.
	"""
	nargs = len(sys.argv)
	args = sys.argv
	if nargs < 3:
		print "Usage: python extract_desc.py <src_path> <dest_path>"
	else:
		main(args[1], args[2])
