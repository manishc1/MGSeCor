"""
Basic xml functional utilities.
"""

from lxml import etree
import lxml.builder as lb

XML_HEAD = '<?xml version="1.0" encoding="ASCII"?>\n'


def bundle_xml(entry_src, entry_type, entry_id, entry_title, entry_date, entry_desc):
    """
    Bundles the data in xml.
    """
    document = lb.E.Document(
        lb.E.Title(entry_title),
        lb.E.Date(entry_date),
        lb.E.Description(entry_desc),
        src=entry_src, id=entry_id, type=entry_type)		
    document_string = etree.tostring(document, pretty_print=True)
    return XML_HEAD + document_string
