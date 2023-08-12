import os
import sys


WIN = sys.platform == 'win32'
WORKING = os.path.abspath(os.path.join(os.path.curdir))


def build_files_list(root_dir):
    """Build a list containing relative paths to the generated files."""
    file_list = []
    for dirpath, subdirs, files in os.walk(root_dir):
        for file_path in files:
            file_list.append(os.path.join(dirpath[len(root_dir):], file_path))

    return file_list