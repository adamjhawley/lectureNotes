import sys
from time import sleep
import os
import shutil

from collect_files import filter_tex_files

def extract_preamble(tex_paths):
    preamble = []
    contents = ['\\begin{document}\n']
    exceptions = ['\\hypersetup{\n']
    for path in tex_paths:
        f = open(path, "r")
        lines = f.readlines()
        
        for index, line in enumerate(lines):
            if line == "\\begin{document}\n":
                doc_start = index + 1
                break
            elif line not in preamble:
                if (line not in exceptions) and (line[1:4] != 'pdf'):
                    preamble.append(line)
                else:
                    print("pdf in line")

        for line in lines[doc_start:-1]:
                contents.append(line)

    contents.append('\\end{document}\n')
    return preamble, contents

def main():
    try:
        path = sys.argv[1]
    except(IndexError):
        path = None

    tex_files = filter_tex_files(path)
    copies = []

    for path in tex_files:
        copy_path = path[:-4] + "_COPY.tex"
        copies.append(copy_path)
        shutil.copyfile(path, copy_path)

    preamble, file_contents = extract_preamble(copies)

    output = open('output.tex', 'w')
    output.writelines(preamble)
    output.writelines(file_contents)
    
    #Remove copied files
    for path in tex_files:
        os.remove(path[:-4] + "_COPY.tex")

if __name__ == '__main__':
    main()

