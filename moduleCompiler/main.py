import sys
from time import sleep
import os
import shutil

from collect_files import filter_tex_files

def extract_preamble(tex_paths):
    preamble = ["\\documentclass{article}"]
    titles = []
    contents = ['\\begin{document}\n', '\\tableofcontents\n']
    exceptions = ['\\hypersetup{\n', "\\documentclass{article}\n", "\\documentclass[11pt]{article}\n"]
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
    offset = 0
    for lineNumber, line in enumerate(contents):
        if line == '\\maketitle\n':
            titleIndexes.append(lineNumber+1)

    for i, title in enumerate(titles):
        contents[titleIndexes[i]] = ("\\section{" + title + "}\n")

    return contents

def decrease_level_of_section(contents):
    toBeSubbed = []
    toBePara = []
    for lineNumber, line in enumerate(contents):
        if line[:14] == "\\subsubsection":
            toBePara.append((lineNumber, line[14:]))
        if line[:9] == "\\section{":
            toBeSubbed.append((lineNumber, line))
        elif line[:4] == "\\sub":
            toBeSubbed.append((lineNumber, line))

    for i in toBeSubbed:
        contents[i[0]] = "\\sub" + i[1][1:]

    for i in toBePara:
        contents[i[0]] = "\\paragraph" + i[1]

    return contents

"""
def filter_toc_title(contents):
    to_be_removed = []
    for n,line in enumerate(contents):
       if (line == "\\tableofcontents\n") or (line == "\\maketitle\n"):
           to_be_removed.append(n)

    for i in to_be_removed[2:]:
        del contents[i]

    return contents
"""

def sort_file_paths(paths, path):
    croppedPaths = []
    sortedPaths = []
    for p in paths:
        cropped = p[::-1]
        cropped = cropped[9:]
        slash_index = 0
        for index, char in enumerate(cropped):
            if char == "/":
                slash_index = index
                break
        if slash_index != 0:
            cropped = cropped[:slash_index]
        cropped = int(cropped[::-1])
        croppedPaths.append(cropped)

    croppedPaths.sort()

    if path != None:
        for p in croppedPaths:
            sortedPaths.append(path + str(p) + "_COPY.tex")
    else:
        for p in croppedPaths:
            sortedPaths.append(str(p) + "_COPY.tex")

    return sortedPaths

def main():
    try:
        path = sys.argv[1]
    except(IndexError):
        path = None

    tex_files = filter_tex_files(path)
    copies = []

    for p in tex_files:
        copy_path = p[:-4] + "_COPY.tex"
        copies.append(copy_path)
        shutil.copyfile(p, copy_path)

    copies = sort_file_paths(copies, path)

    titles, preamble, file_contents = extract_preamble(copies)

    file_contents = decrease_level_of_section(file_contents)

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

