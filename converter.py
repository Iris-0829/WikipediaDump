import bz2
from bs4 import BeautifulSoup
import os
import re
import timeit


def decompress(dump, index):
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
                    print("page_index = ", page_index, "   page_title = ", page_titles[page_index],
                          '   Math expressions: ',
                          exist_math)  # true for there exist math expression

                    target = pages[page_index].prettify(formatter="html")

                    # convert target to html file with parsoid
                    target = target.replace('"', '\\"').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;',
                                                                                                          '&')
                    l1 = (m.start() for m in re.finditer('begin\{align\}', target))
                    l2 = (n.start() for n in re.finditer('\\\end\{align\}', target))

                    total_occur = 0
                    for a, b in zip(l1, l2):
                        a += total_occur
                        b += total_occur

                        occur = target[a:b - 1].count('\\')
                        total_occur += occur
                        target = target[:a] + target[a:b - 1].replace('\\', '\\\\') + target[b - 1:]

                    # os.system('var="'+target+'" && printf \'%s\n\' \"$var\"')
                    page_title = re.sub(r'[^A-Za-z0-9 ]+', '', page_titles[page_index])
                    page_title = page_title.replace(' ', '_')

                    print('page_title = ', page_title)

                    print(target)

                    with open('temp.txt', 'w') as temp:
                        temp.write(target)

                    start2 = timeit.default_timer()
                    os.system('cat temp.txt | node node_modules/parsoid/bin/parse.js > result/' + page_title + '.html')
                    end2 = timeit.default_timer()

                    # print('target = ', target)
                    # os.system(
                    #        'var2="' + target + '" && printf \'%s\n\' \"$var2\" | node node_modules/parsoid/bin/parse.js')

                    # clean html file
                    with open('result/' + page_title + '.html', 'r') as f:
                        content = f.read(-1)

                    content = content.replace('&lt;', '<')
                    content = re.sub(r'<ns>.*?</format>', r'', content, flags=re.DOTALL)
                    with open('result/' + page_title + '.html', 'w') as f:
                        f.write(content)

                    end1 = timeit.default_timer()

                    print((end2 - start2) / (1.0 * (end1 - start1)))

