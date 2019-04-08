import sys
from time import sleep
import os
import shutil

from collect_files import filter_tex_files

def extract_preamble(tex_paths):
    preamble = []
    titles = []
    contents = ['\\begin{document}\n']
    exceptions = ['\\hypersetup{\n']
    for path in tex_paths:
        f = open(path, "r")
        lines = f.readlines()
        
        for index, line in enumerate(lines):
            #Check for the end of the preamble
            if line == "\\begin{document}\n":
                doc_start = index + 1
                break
            #Check for titles to add to sections
            elif line[:7] == "\\title{":
                titles.append(line[7:-2])
            #Add any new packages/lines to the preamble that aren't already in it
            elif line not in preamble:
                if (line not in exceptions) and (line[1:4] != 'pdf'):
                    preamble.append(line)

        for line in lines[doc_start:-1]:
                contents.append(line)

    contents.append('\\end{document}\n')
    return titles, preamble, contents

def insert_titles_as_sections(contents, titles):
    insertAtIndex = 0
    titleIndexes = []
    for lineNumber, line in enumerate(contents):
        if line == '\\tableofcontents\n':
            titleIndexes.append(lineNumber)

    for i, title in enumerate(titles):
        contents.insert(titleIndexes[i], ("\\section{" + title + "}\n"))

    return contents


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

    titles, preamble, file_contents = extract_preamble(copies)

    file_contents = insert_titles_as_sections(file_contents, titles)

    output = open('output.tex', 'w')
    output.writelines(preamble)
    output.writelines("\\title{TEST}\n")
    output.writelines(file_contents)
    
    #Remove copied files
    for path in tex_files:
        os.remove(path[:-4] + "_COPY.tex")

if __name__ == '__main__':
    main()

