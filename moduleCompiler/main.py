import sys
from time import sleep
import os
import shutil

from collect_files import filter_tex_files

def main():
    try:
        path = sys.argv[1]
    except(IndexError):
        path = None

    tex_files = filter_tex_files(path)

    for path in tex_files:
        copy_path = path[:-4] + "COPY.tex"
        shutil.copyfile(path, copy_path)

    file_contents = []

    print(tex_files)

    sleep(5)
    print("Deleting")
    for path in tex_files:
        os.remove(path[:-4] + "COPY.tex")

if __name__ == '__main__':
    main()

