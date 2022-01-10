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
def get_file(fname, origin, loc):
    datadir = os.path.join(loc)
    fpath = os.path.join(datadir, fname)
    # print('datadir: ', datadir)
    print('File path: ', fpath)
    if os.path.exists(fpath):
        print('already exist')
        return False
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

    return True

# download latest dump and add an entry in log.txt
def get_dump(dump_loc, dump_name, dump_index, dump_date):
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

    # download latest dump and index file
    origin = 'https://dumps.wikimedia.org/enwiki/'
    if dump_date is None:
        origin += 'latest/'
        dump_date = latest_dump_date
    else:
        dump_date += '/'
        origin += dump_date


    # this is first 100 pages and index
    if dump_name is None and dump_index is None:
        dump = 'enwiki-latest-pages-articles-multistream1.xml-p1p41242.bz2'
        index = 'enwiki-latest-pages-articles-multistream-index1.txt-p1p41242.bz2'

        # this is full pages and index
        # dump = 'enwiki-latest-pages-articles-multistream.xml.bz2'
        # index = 'enwiki-latest-pages-articles-multistream-index.txt.bz2'
    else:
        dump, index = dump_name, dump_index

    log_path = dump_loc + '/log.txt'
    if not os.path.exists(log_path):
        # create log file if it doesn't exist
        with open(log_path, 'w'):
            pass

    with open(log_path, 'r') as log:
        if dump_date is None and latest_dump_date + dump in log.read():
            print('target dump already exist')
            return dump, index  # already exist
        elif dump_date + dump in log.read():
            print('target dump already exist')
            return dump, index

    dump_output = get_file(dump, origin + dump, dump_loc)
    index_output = get_file(index, origin + index, dump_loc)

    # add to log with today's date
    if dump_output and index_output:
        with open(log_path, 'a') as log:
            today = str(date.today())
            if dump_date is None:
                log.write(today + ': ' + latest_dump_date + dump + '\n')
            else:
                log.write(today + ': ' + dump_date + dump + '\n')

    return dump, index