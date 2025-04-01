import pandas as pd
from lxml import etree
import matplotlib.pyplot as plt
import numpy as np
import re
from unidecode import unidecode
import os

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

def clean_description(text):
    # Remove whitespace between .,;!?
    text = re.sub(r'(\S)\s*(?=[.,;!?])', r'\1', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove extra Punctuations
    text = re.sub(r'\.{2,}', '.', text)
    # Insert Whitespace after .,;!? if missing
    text= re.sub(r'([.,;!?])(?=\S)', r'\1 ', text)
    # Split concatenated words --> EasyTuesday -> Easy. Tuesday
    text = re.sub(r'(?<=[a-z])(?=[A-Z])(?=[a-zA-Z])', '. ', text)
    # replace special characters
    text = unidecode(text)

    return text


def load_data_basiccleanup():
    # Load XML files and create dataframe
    PATH_DEV = os.path.join(os.getcwd(), 'origdata', 'BlurbGenreCollection_EN_dev.txt')
    PATH_TEST = os.path.join(os.getcwd(), 'origdata', 'BlurbGenreCollection_EN_test.txt')
    PATH_TRAIN = os.path.join(os.getcwd(), 'origdata', 'BlurbGenreCollection_EN_train.txt')
    df = pd.concat([read_xml(PATH_TRAIN), read_xml(PATH_TEST), read_xml(PATH_DEV)]).reset_index(drop=True)

    # Reduced topics - Sorted in ascending order by frequency of occurrence (lowest first)
    reduced_topics_sorted = ['Poetry', 'Humor', 'Young Adult', 'Classics', 'Children’s Books', 'Fiction', 'Nonfiction']
    df['TOPICS_SPLIT'] = df['TOPICS'].apply(lambda x: sorted(list(set(i.strip() for i in re.split(r'[,\s]{2,}', x)))))
    def assign_primary_topic(topic_string):
        # label will be the first match --> topic has a lower frequency of occurence
        for reduced_topic in reduced_topics_sorted:
            for t in topic_string:
                if reduced_topic.lower() in t.lower():
                    return reduced_topic
        return 'Others'
    df['TOPIC_MAIN'] = df['TOPICS_SPLIT'].apply(assign_primary_topic)
    if not df[df['TOPIC_MAIN'] == 'Other'].empty:
        raise Exception('TOPIC_MAIN is somewhere empty!!!')

    ## Prepreprocessing Blurbs
    # Applying basic clean up to the blurbs.
    df['DESCRIPTION'] = df['DESCRIPTION'].fillna('').apply(clean_description)
    if (df['DESCRIPTION'].str.strip() == '').any():
        print("Warning: One row was deleted, because 'DESCRIPTION' is empty.")
        df = df[df['DESCRIPTION'].str.strip() != '']

    return df[['TOPIC_MAIN', 'DESCRIPTION']]
