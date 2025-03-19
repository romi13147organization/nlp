import pandas as pd
from lxml import etree

def read_xml(path_file):
    with open(path_file, 'r', encoding='utf-8') as file:
        content = file.read()
    content = '<books>' + content + '</books>'  # Add Wrapper

    parser = etree.XMLParser(recover=True)
    tree = etree.XML(content, parser=parser)
    books = tree.xpath('//book')
    data = []
    for book in books:
        book_data = {
            'TITLE': book.find('title').text,
            'AUTHOR': book.find('.//author').text,
            'PUBLISHED': book.find('.//published').text,
            'ISBN': book.find('.//isbn').text,
            'PAGE_NUM': book.find('.//page_num').text,
            'URL': book.find('.//url').text,
            'TOPICS': ', '.join([topic.text for topic in book.xpath('.//topics/*')]),
            'COPYRIGHT': book.find('copyright').text,
            'DESCRIPTION': book.find('body').text,
            'DATE': book.attrib.get('date'),
            'LANGUAGE': book.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
        }
        data.append(book_data)

    # Erstelle ein DataFrame mit den gesammelten Daten
    df = pd.DataFrame(data)
    return df