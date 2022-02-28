import re
import subprocess
import sys


def convert_to_html(file_name: str):
    with open(file_name) as f:
        content = f.read().replace('&lt;', '<').replace('&gt;', '>')

    l1 = (m.start() for m in re.finditer('<math', content))
    l2 = (n.start() for n in re.finditer('</math>', content))

    total_occur = 0

    for a, b in zip(l1, l2):
        a += total_occur
        b += total_occur
        latex_str = ""
        mathml = content[a:b + 7]

        for i in range(a, b):
            if content[i:i + 7] == "alttext":
                latex_str = "<math>" + content[i + 9:content.find("\"", i + 9)] + "</math>"

        total_occur += len(latex_str) - len(mathml)
        content = content[:a] + latex_str + content[b + 7:]

    ps = subprocess.run(['echo', content], check=True, capture_output=True)
    processNames = subprocess.run(['node', 'node_modules/parsoid/bin/parse.js'], input=ps.stdout, capture_output=True)
    result = processNames.stdout.decode('utf-8').replace('&lt;', '<').replace('&gt;', '>')
    result = re.sub('<ns>.*?</format>', '\n', result, flags=re.DOTALL)
    return result


if __name__ == "__main__":
    print(convert_to_html(sys.argv[1]))
