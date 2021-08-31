import os
from auto_download import get_dump
# from converter import decompress
from convert_math import decompress_math

def main():
    dump, index = get_dump()
    print('dump: ', dump)
    print('index: ', index)

    if not os.path.exists("result/"):
        os.mkdir("result")

    decompress_math('dumps/' + dump, 'dumps/' + index)



if __name__ == "__main__":
    main()