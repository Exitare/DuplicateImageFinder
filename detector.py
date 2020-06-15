import hashlib
# from scipy.misc import imread, imresize, imshow
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
import time
# import numpy as np
import argparse
import os
import hashlib
from pathlib import Path

duplicates = []
args = {}

def file_hash(filepath):
    with open(filepath, 'rb') as f:
        return md5(f.read()).hexdigest()

def handle_args():
    """
    Parse the given arguments
    :return:
    """
    global  args
    parser = argparse.ArgumentParser(description='Get the impact of tool features on it\'s runtime.',
                                     epilog='Accepts tsv and csv files')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store', required=False,
                        help="Enables the verbose mode. With active verbose mode additional information is shown in the console")
    parser.add_argument('-f', '--folder', dest='folder', default=False, required=False,
                        help="The folder which should be checked for duplicates")
    parser.add_argument('-r', '--remove', dest='remove', action='store', required=False,
                        help="Activates the removal of data for further evaluation of data sets")
    args = parser.parse_args()



def find_duplicates():
    global duplicates
    global args
    duplicates = []
    hash_keys = dict()

    print(args.folder)

    for path in Path(args.folder).iterdir():
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                filehash = hashlib.md5(f.read()).hexdigest()
                print(filehash)
            if filehash not in hash_keys:
                hash_keys[filehash] = path
            else:
                duplicates.append((path, hash_keys[filehash]))


    print(duplicates)



if __name__ == '__main__':
    handle_args()
    find_duplicates()