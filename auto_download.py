import urllib
from urllib.error import URLError
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import os
from six.moves.urllib.request import urlretrieve
from urllib.error import HTTPError
from datetime import date

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


# helper function to download dump
def get_file(fname, origin):
    datadir = os.path.join('dumps')
    fpath = os.path.join(datadir, fname)
    # print('datadir: ', datadir)
    print('File path: ', fpath)
    if os.path.exists(fpath):
        print('already exist')
    else:
        print('Downloading data from', origin)

        error_msg = 'URL fetch failure on {}: {} -- {}'
        try:
            try:
                urlretrieve(origin, fpath)
            except URLError as e:
                raise Exception(error_msg.format(origin, e.errno, e.reason))
            except HTTPError as e:
                raise Exception(error_msg.format(origin, e.code, e.msg))
        except (Exception, KeyboardInterrupt) as e:
            if os.path.exists(fpath):
                os.remove(fpath)
            raise

    return fpath


def get_dump():
    # read from website
    url = 'https://dumps.wikimedia.org/enwiki/'
    file = urllib.request.urlopen(url)
    html_doc = ''

    for line in file:
        decoded_line = line.decode("utf-8")
        html_doc += decoded_line

    # parse html
    soup = BeautifulSoup(html_doc, 'html.parser')

    latest_dump_date = soup.find_all('a')[-2].text  # latest dump date

    # open log.txt to check if latest dump already exist

    # download latest dump and index file
    origin = 'https://dumps.wikimedia.org/enwiki/latest/'

    # this is first 100 pages and index
    dump = 'enwiki-latest-pages-articles-multistream1.xml-p1p41242.bz2'
    index = 'enwiki-latest-pages-articles-multistream-index1.txt-p1p41242.bz2'

    # this is full pages and index
    # dump = 'enwiki-latest-pages-articles-multistream.xml.bz2'
    # index = 'enwiki-latest-pages-articles-multistream-index.txt.bz2'

    with open('dumps/log.txt', 'r') as log:
        if latest_dump_date in log.read():
            print('latest dump already exist')
            return dump, index  # already exist

    get_file(dump, origin + dump)
    get_file(index, origin + index)

    # add to log with today's date
    with open('dumps/log.txt', 'a') as log:
        today = str(date.today())
        log.write(today + ': ' + latest_dump_date + '\n')

    return dump, index

