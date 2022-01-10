import bz2
import subprocess

from bs4 import BeautifulSoup
import os
import re
import timeit


def decompress_math(dump, index, flag=False):
    # dump = 'dumps/enwiki-latest-pages-articles-multistream1.xml-p1p41242.bz2'
    # index = 'dumps/enwiki-latest-pages-articles-multistream-index1.txt-p1p41242.bz2'

    with open(index, 'rb') as f:
        f.seek(0)
        readback = f.read()
        decomp = bz2.BZ2Decompressor()
        page_index = decomp.decompress(readback).decode()
        page_index = page_index.split('\n')

    start_bytes = [int(x.split(":")[0]) for x in page_index if x.split(":")[0] != '']
    start_bytes = set(start_bytes)
    start_bytes = list(start_bytes)
    start_bytes.sort()

    file_size = os.path.getsize(dump)
    start_bytes.append(file_size + 1)

    with open(dump, 'rb') as d:
        for start_byte in start_bytes:
            d.seek(start_byte)
            readback = d.read(-1)
            decomp = bz2.BZ2Decompressor()
            page_xml = decomp.decompress(readback).decode()

            soup = BeautifulSoup(page_xml, 'lxml')
            pages = soup.find_all('page')

            page_titles = [p.find('title').text for p in pages]

            for page_index in range(len(page_titles)):
                extract_text = pages[page_index].find(
                    'text').text  # if not .text, show as ;lt... if .text, show as <math>
                exist_math = extract_text.find('<math>') != -1

                if exist_math:
                    start1 = timeit.default_timer()
                    time_count = 0

                    print("page_index = ", page_index, "   page_title = ", page_titles[page_index],
                          '   Math expressions: ',
                          exist_math)  # true for there exist math expression

                    target = pages[page_index].prettify(formatter="html")

                    # convert target to html file with latexmlmath
                    target = target.replace('"', '\\"').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;',
                                                                                                          '&')
                    l1 = (m.start() for m in re.finditer('<math>', target))
                    l2 = (n.start() for n in re.finditer('</math>', target))

                    total_occur = 0
                    for a, b in zip(l1, l2):

                        a += total_occur
                        b += total_occur

                        latex_str = target[a + 6:b]
                        start2 = timeit.default_timer()
                        mathml = subprocess.run(['latexmlmath', latex_str, '--preload=amsmath.sty', '--preload=amssymb.sty', '--preload=amsfonts.sty'],
                                                stdout=subprocess.PIPE).stdout.decode('utf-8')
                        end2 = timeit.default_timer()
                        time_count += end2-start2

                        print(latex_str)
                        # print(mathml)
                        total_occur += len(mathml) - len(latex_str)
                        target = target[:a + 6] + mathml + target[b:]


                    page_title = re.sub(r'[^A-Za-z0-9 ]+', '', page_titles[page_index])
                    page_title = page_title.replace(' ', '_')

                    with open('result/' + page_title + '.html', 'w') as f:
                        f.write(target)

                    end1 = timeit.default_timer()
                    print(time_count / (1.0*(end1 - start1)))


