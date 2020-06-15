import hashlib
# from scipy.misc import imread, imresize, imshow
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
import time
# import numpy as np
from Controllers import BaseController
from flask import Flask, escape, request, jsonify, send_from_directory, render_template
from flask_restful import Resource, Api
from waitress import serve
import argparse
import os
import hashlib
from pathlib import Path

app = Flask(__name__, static_folder='./HTML')
api = Api(app)

duplicates = []
args = {}
file_extensions = ("jpg", "jpeg", "png", "gif", "img", "raw", "nef")


@app.route('/')
def root():
    global duplicates
    return render_template("index.html", duplicates=duplicates)


def file_hash(filepath):
    with open(filepath, 'rb') as f:
        return md5(f.read()).hexdigest()


def handle_args():
    """
    Parse the given arguments
    :return:
    """
    global args
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
    duplicates = dict()
    hash_keys = dict()

    folder = Path(args.folder)
    # walk the dirs and find duplicates
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            print(file)
            if not file.endswith(file_extensions):
                continue

            with open(Path(subdir, file), 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
                print(file_hash)
            if file_hash not in hash_keys:
                print("Not in")
                hash_keys[file_hash] = subdir
                duplicates[file_hash] = [Path(subdir, file)]
            else:
                print("in")
                duplicates[file_hash].append(Path(subdir, file))

    # Remove images which do not have duplicates
    for image_name, paths in list(duplicates.items()):
        if len(paths) <= 1:
            del duplicates[image_name]

    print(duplicates)


if __name__ == '__main__':
    handle_args()
    find_duplicates()
    app.run(use_reloader=True)
