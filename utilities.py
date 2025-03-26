import pandas as pd
from lxml import etree
import matplotlib.pyplot as plt
import numpy as np

def read_xml(path_file):
    with open(path_file, 'r', encoding='utf-8') as file:
        content = file.read()
    content = '<books>' + content + '</books>'  # Add Wrapper

    parser = etree.XMLParser(recover=True)
    tree = etree.XML(content, parser=parser)
    books = tree.xpath('//book')
    data = []
    for book in books:
        description = book.find('body').text
        if description:
            description = description.replace('\xa0', ' ')  # Ersetze NBSP durch ein normales Leerzeichen

        book_data = {
            'TITLE': book.find('title').text,
            'AUTHOR': book.find('.//author').text,
            'PUBLISHED': book.find('.//published').text,
            'ISBN': book.find('.//isbn').text,
            'PAGE_NUM': book.find('.//page_num').text,
            'URL': book.find('.//url').text,
            'TOPICS': ', '.join([topic.text for topic in book.xpath('.//topics/*')]),
            'COPYRIGHT': book.find('copyright').text,
            'DESCRIPTION': description, #book.find('body').text,
            'DATE': book.attrib.get('date'),
            'LANGUAGE': book.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
        }
        data.append(book_data)

    # Erstelle ein DataFrame mit den gesammelten Daten
    df = pd.DataFrame(data)
    return df


def plot_three(data, title, bins, xlabel, xlim):
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].hist(data, bins=bins)
    ax[0].set_title(title)
    ax[0].set_xlabel(xlabel)

    ax[1].hist(data, bins=bins)
    ax[1].set_title(title)
    ax[1].set_xlabel(xlabel)
    ax[1].set_xlim(0, xlim)

    data_log = np.log(data)
    ax[2].hist(data_log, bins=bins)
    ax[2].set_title(title + ' - Log')
    ax[2].set_xlabel('Log(' + xlabel + ')')


def plot_two(data, title, bins, xlabel, xlim):
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].hist(data, bins=bins)
    ax[0].set_title(title)
    ax[0].set_xlabel(xlabel)

    ax[1].hist(data, bins=bins)
    ax[1].set_title(title)
    ax[1].set_xlabel(xlabel)
    ax[1].set_xlim(0, xlim)