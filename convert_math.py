import bz2

from bs4 import BeautifulSoup
import os
import re
import timeit
import html


def decompress_math(dump, index, result_path, verbose):
    # dump = 'dumps/enwiki-latest-pages-articles-multistream1.xml-p1p41242.bz2'
    # index = 'dumps/enwiki-latest-pages-articles-multistream-index1.txt-p1p41242.bz2'

    if verbose not in [0, 1, 2, 3]:
        raise ValueError('Invalid value for -v/--verbose')

    num_expr = 0


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

    tex_path = 'math_expression.tex'
    if not os.path.exists(tex_path):
        # create log file if it doesn't exist
        with open(tex_path, 'w') as f:
            f.write("\\documentclass{article}\n" +
                    "\\usepackage{amsmath}\n" +
                    "\\begin{document}\n" +
                    "$$ $$\n" +
                    "\\end{document}")

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
                    # start1 = timeit.default_timer()
                    # time_count = 0

                    print("page_index = ", page_index, "   page_title = ", page_titles[page_index],
                          '   Math expressions: ',
                          exist_math)  # true for there exist math expression

                    target = pages[page_index].prettify(formatter="html")
                    target = html.unescape(target)

                    page_title = re.sub(r'[^A-Za-z0-9 ]+', '', page_titles[page_index])
                    page_title = page_title.replace(' ', '_')

                    result = convert(target, tex_path)
                    num_expr += result[1]
                    target = result[0]

                    with open(result_path + '/' + page_title + '.html', 'w') as f:
                        f.write(target)

                    # end1 = timeit.default_timer()
                    # print(time_count / (1.0*(end1 - start1)))
    if verbose == 1:
        print("Number of math expressions: ", num_expr)

    if os.path.exists(tex_path):
        os.remove(tex_path)
    if os.path.exists("combined.html"):
        os.remove("combined.html")
    if os.path.exists("actual.tex"):
        os.remove("actual.tex")

def convert(target, tex_path):
    # convert target to html file with latexml and latexmlpost
    l1 = (m.start() for m in re.finditer('<math', target))
    l2 = (n.start() for n in re.finditer('</math>', target))

    total_occur = 0
    num_expr = 0
    for a, b in zip(l1, l2):
        a += total_occur
        b += total_occur

        if target[a + 5] == '>':
            latex_str = target[a + 6:b]
            is_block = False
        else:
            latex_str = target[a + 22:b]
            is_block = True

        # start2 = timeit.default_timer()
        latex_str_len = len(latex_str)

        latex_str = latex_str.replace('align', 'aligned')
        # print(latex_str)

        with open(tex_path, "r") as fin:
            with open("actual.tex", "w") as fout:
                contents = fin.read()
                fout.write(contents.replace('$$ $$', '$$ ' + latex_str + ' $$'))

        os.system(
            "latexml actual.tex 2>/dev/null | latexmlpost - --format=html5 --destination=combined.html --presentationmathml --contentmathml 2>/dev/null")

        num_expr += 1

        with open("combined.html", "r") as h:
            h_content = h.read().replace('\n', '')
            m = re.search('<math(.+?)</math>', h_content)
            mathml = ''
            if m:
                mathml = '<math' + m.group(1) + '</math>'

        # end2 = timeit.default_timer()
        # time_count += end2 - start2

        if not is_block:
            total_occur += len(mathml) - latex_str_len - 13
            target = target[:a] + mathml + target[b + 7:]
        else:
            total_occur += len(mathml) - latex_str_len - 29
            target = target[:a] + mathml + target[b + 7:]

    return target, num_expr
