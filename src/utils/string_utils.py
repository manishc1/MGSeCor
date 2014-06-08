"""
Basic string functional utilities.
"""

def asciify(string):
    """
    Removes non-ascii characters from the string.
    """
    new_string = ''
    for c in string:
        if ((32 <= ord(c)) and (ord(c) <= 126)):
            new_string = new_string + c
    return new_string


def detag(string):
    """
    Remove words of type '&xxx;' from the string.
    """
    words = string.split(' ')
    new_words = []
    for word in words:
        if (word[0] == '&' and word[-1] == ';'):
            continue
        new_words.append(word)
    return ' '.join(new_words)


def replace_abbrv(string):
    """
    Replace abbrv like & -> and in the string.
    """
    return string.replace('&', 'and')


def depunctuate(string):
    """
    Extract alphanumeric words from the string.
    """
    return re.findall("[\w']+", string)


def dedigit(string):
    """
    Remove digits from the string.
    """
    words = string.split(' ')
    new_words = []
    for word in words:
        if (word.isdigit()):
            continue
        new_words.append(word)
    return ' '.join(new_words)


def clean(string):
    """
    Cleans the string to have ascii characters and somewhat valid words.
    """
    if (string in ['', None]):
        return ''
    string = string.strip()
    string = asciify(string)
    string = detag(string)
    string = replace_abbrv(string)
    string = depunctuate(string)
    string = dedigit(string)
    return string
