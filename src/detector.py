from flask import Flask, send_from_directory, render_template
from flask_restful import Api
import argparse
import os
import hashlib
from pathlib import Path
from random import randrange
from Globals import Globals
from Entities.Image import Image
from Entities.Duplicate import Duplicate
from Services import FileService
import sys

app = Flask(__name__, static_folder='static')
api = Api(app)

file_extensions = ("jpg", "jpeg", "png", "gif", "img", "raw", "nef")


@app.route('/')
def root():
    return render_template("index.html", duplicates=Globals.duplicates)


def file_hash(file_path: str):
    with open(file_path, 'rb') as f:
        return md5(f.read()).hexdigest()


def handle_args():
    """
    Parse the given arguments
    :return:
    """
    parser = argparse.ArgumentParser(description='Get the impact of tool features on it\'s runtime.',
                                     epilog='Accepts tsv and csv files')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store', required=False,
                        help="Enables the verbose mode. With active verbose mode additional information is shown in the console")
    parser.add_argument('-f', '--folder', dest='folder', default=False, required=True,
                        help="The folder which should be checked for duplicates")
    Globals.args = parser.parse_args()


def find_duplicates():
    # duplicates = dict()
    hash_keys = dict()

    folder = Path(Globals.args.folder)
    # walk the dirs and find duplicates
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if not file.endswith(file_extensions):
                continue

            with open(Path(subdir, file), 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash not in hash_keys:
                hash_keys[file_hash] = subdir

                # Create image entity and append to duplicates
                image = Image(Path(subdir, file))
                duplicate = Duplicate(file_hash)
                duplicate.images.append(image)
                Globals.duplicates.append(duplicate)
            else:
                # Create image entity and append to duplicates
                image = Image(Path(subdir, file))
                duplicate = find_duplicate(file_hash)
                duplicate.images.append(image)

    # Remove images which do not have duplicates
    for duplicate in Globals.duplicates:
        # TODO: Remove symlinks if no duplicates found
        if len(duplicate.images) <= 1:
            duplicate.valid = False

    Globals.duplicates = [duplicate for duplicate in Globals.duplicates if duplicate.valid]


def find_duplicate(hash_sum: str):
    for duplicate in Globals.duplicates:
        if duplicate.hash_sum == hash_sum:
            return duplicate


if __name__ == '__main__':
    Globals.static_path = Path(FileService.split_path(sys.argv[0]))
    print(Globals.static_path)
    input()
    FileService.prepare_static_folder()

    handle_args()
    find_duplicates()
    FileService.create_symbolic_links()

    app.run(use_reloader=False)
