#!/usr/bin/env python

import os
from collections import defaultdict


def check_by_file_size(path):
    files_by_size = defaultdict(list)
    files_by_size_tmp = defaultdict(list)

    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                full_path = os.path.realpath(full_path)
                file_size = os.path.getsize(full_path)
            except OSError:
                # not accessible (permissions, etc) - pass on
                continue
            files_by_size_tmp[file_size].append(full_path)
        for size in files_by_size_tmp:
            if (len(files_by_size_tmp[size]) > 1):
                files_by_size[size] = files_by_size_tmp[size]

    return files_by_size


def find_identical_files_by_bytes(open_files):
    # Comparing byte by byte with recursion
    file_by_byte = defaultdict(list)
    result = []
    for file in open_files:
        b = file.read(1)
        file_by_byte[b].append(file)

    for key in file_by_byte:
        if len(file_by_byte[key]) > 1 and (key == " " or key == ""):
            result.append(file_by_byte[key])
        elif len(file_by_byte[key]) > 1:
            result = result + find_identical_files_by_bytes(file_by_byte[key])
    return result


def check_for_duplicates(path):
    # get all file with same size
    files_by_size = check_by_file_size(path)
    for file_size, files in files_by_size.items():
        open_files = []

        for filename in files:
            f = open(filename, "rb")

            open_files.append(f)
        result = []
        results_of = find_identical_files_by_bytes(open_files)
        for group in results_of:
            for file in group:
                result.append(file.name)
        for file in open_files:
            file.close()
        print (str(result))


if __name__ == "__main__":
    # Getting folder path from env
    folder_path = os.environ['ENV_FOLDER_PATH']
    print("Going to check for file duplication on folder_path: {0}".format(folder_path))
    check_for_duplicates(folder_path)
