import os

def filter_files(path, extension):
    files = os.listdir(path) 
    paths = []
    to_be_removed = []

    for f in files:
        if f[-4:] != extension:
            to_be_removed.append(f)

    for f in to_be_removed:
        files.remove(f)

    if path != ".":
        for fname in files:
            paths.append(path+fname)
        return paths
    else:
        return files


def filter_tex_files(path):
    if path == None:
        path = "."
    return filter_files(path, ".tex")
