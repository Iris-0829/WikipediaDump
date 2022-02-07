import argparse
import os
from auto_download import get_dump
from convert_math import decompress_math

def main():
    parser = argparse.ArgumentParser(
        description='Crawl all Wikipedia pages from the Wikipedia dump which contain math expressions and convert them to html files')
    parser.add_argument('-v', '--verbose', help='Show more informative output', required=False)
    parser.add_argument('-l', '--location', help='Set location of dump files', required=False)
    parser.add_argument('-r', '--result', help='Set location of result files', required=False)
    parser.add_argument('-n', '--name', help='Set name and index of the dump file', required=False, nargs=2)
    parser.add_argument('-d', '--date', help='Set date of dump files', required=False)

    args = vars(parser.parse_args())
    print(args)

    dump_path = "dump" if args['location'] is None else args['location']
    result_path = "result" if args['result'] is None else args['result']

    # create directory for dump and result
    if not os.path.exists(dump_path):
        os.mkdir(dump_path)
    if not os.path.exists(result_path):
        os.mkdir(result_path)


    # download latest dump
    if args['name'] is None:
        dump, index = get_dump(dump_path, None, None, args['date'])
    else:
        dump, index = get_dump(dump_path, args['name'][0], args['name'][1], args['date'])

    print('dump: ', dump)
    print('index: ', index)

    # decompress dump and convert to html files
    decompress_math(dump_path + '/' + dump, dump_path + '/' + index, result_path, args['verbose'])


if __name__ == "__main__":
    main()
