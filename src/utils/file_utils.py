"""
Basic file functional utilities.
"""

from string_utils import *

import os


def read_to_lines(filename, is_clean):
    """
    Return list of lines from the file.
    """
    try:
        f = open(filename, 'r')
        lines = [line for line in f]
        f.close()
        newlines = []
        for line in lines:
            line = line.strip()
            if (len(line) != 0):
                if (is_clean):
                    line = clean(line)
                newlines.append(line)
        return newlines
    except Exception as e:
        print 'File read error! [' + str(e) + ']'
        exit(-1)


def read_to_string(filename, is_clean):
    """
    Read string from the file.
    """
    try:
        with open (filename, "r") as f:
            string = f.read()
        if (is_clean):
            string = clean(string)
        return string
    except Exception as e:
        print 'File read error! [' + str(e) + ']'
        exit(-1)


def put_string(filename, mode, string, is_clean):
    """
    Write the string to file in given mode.
    """
    try:
        if(is_clean):
            string = clean(string)
        parent_dir = os.path.abspath(filename + '/../')
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        f = open(filename, mode)
        f.write(string)
        f.close()
    except Exception as e:
        print 'File write error! [' + str(e) + ']'
        exit(-1)


def write_string(filename, string, is_clean):
    """
    Write string to the file.
    """
    put_string(filename, 'w', string, is_clean)


def append_string(fileName, string, is_clean):
    """
    Appends string to the file.
    """
    put_string(filename, 'a', string, is_clean)
