import subprocess
import sys


def convert_to_html(file_name: str):
    ps = subprocess.run(['cat', file_name], check=True, capture_output=True)
    processNames = subprocess.run(['node', 'node_modules/parsoid/bin/parse.js'], input=ps.stdout, capture_output=True)
    return processNames.stdout.decode('utf-8').replace('&lt;', '<')


if __name__ == "__main__":
    print(convert_to_html(sys.argv[1]))
