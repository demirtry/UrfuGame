import os
import shutil


def clear_directory(direct_path: str = 'images/dynamic'):
    shutil.rmtree(direct_path)
    os.mkdir(direct_path)

