import os
import shutil


def clear_directory(direct_path: str = 'images/dynamic'):
    shutil.rmtree(direct_path)
    os.mkdir(direct_path)


def check_directory(direct_path: str = 'images/dynamic'):
    if not os.path.isdir(direct_path):
        os.mkdir(direct_path)
