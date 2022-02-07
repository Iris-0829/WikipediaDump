import argparse
import difflib
import os

def convert_test():
    parser = argparse.ArgumentParser(description='Test suite for dump conversion')

    parser.add_argument('dir', help='Actual and expected result', nargs=2)
    parser.add_argument('-v', '--verbose', help='Show more informative output', required=False, action="store_true")

    args = vars(parser.parse_args())

    actual_dir_path = args['dir'][0]
    expected_dir_path = args['dir'][1]

    actual_dir = os.fsencode(actual_dir_path)
    expected_dir = os.fsencode(expected_dir_path)

    expected = []
    num_pass = 0
    num_test = 0
    for expected_file in os.listdir(expected_dir):
        expected_filename = os.fsdecode(expected_file)
        if expected_filename.endswith('.html'):
            expected.append(expected_filename)
    for actual_file in os.listdir(actual_dir):
        actual_filename = os.fsdecode(actual_file)
        if actual_filename in expected:
            num_test += 1
            num_pass += compare(os.path.join(actual_dir_path, actual_filename), os.path.join(expected_dir_path, actual_filename), args['verbose'])

    print("Ran " + str(num_test) + " tests. ")
    print("Passed " + str(num_pass) + " tests. ")

def compare(actual_path, expected_path, verbose):
    with open(actual_path, 'r') as a:
        with open(expected_path, 'r') as e:
            actual = a.read().split('\n')
            expected = e.read().split('\n')

            actual[:] = (value for value in actual if value != '')
            expected[:] = (value for value in expected if value != '')

            if verbose:
                for diff in difflib.context_diff(actual, expected):
                    print(diff)

            return actual == expected

if __name__ == "__main__":
    convert_test()

