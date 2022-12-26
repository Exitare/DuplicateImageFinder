from flask import Flask, render_template
from flask_restful import Api
import argparse
import os
import hashlib
from pathlib import Path
from src import file_service, duplicate_finder, Image, Duplicate, Statics
import sys

template_path = Path("src", "templates").absolute()
static_path = Path("src", "static").absolute()

app = Flask(__name__, template_folder=template_path, static_folder=f"{static_path}")
api = Api(app)

file_extensions = ("jpg", "jpeg", "png", "gif", "img", "raw", "nef")


@app.route('/')
def root():
    return render_template("index.html", duplicates=Statics.duplicates)


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
    Statics.args = parser.parse_args()


def find_duplicates():
    # duplicates = dict()
    hash_keys = dict()

    folder = Path(Statics.args.folder)
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
                image = Image(path=Path(subdir, file).absolute())
                duplicate = Duplicate(file_hash)
                duplicate.images.append(image)
                Statics.duplicates.append(duplicate)
            else:
                # Create image entity and append to duplicates
                image = Image(path=Path(subdir, file).absolute())
                duplicate = compare_hash_sum(file_hash)
                duplicate.images.append(image)

    # Remove images which do not have duplicates
    duplicate: Duplicate
    for duplicate in Statics.duplicates:
        if len(duplicate.images) <= 1:
            duplicate.is_duplicate = False

    Statics.duplicates = [duplicate for duplicate in Statics.duplicates if duplicate.is_duplicate]

def compare_hash_sum(hash_sum: str):
    for duplicate in Statics.duplicates:
        if duplicate.hash_sum == hash_sum:
            return duplicate


if __name__ == '__main__':
    Statics.static_path = Path(file_service.split_path(sys.argv[0])[0], "src/static")
    print(Statics.static_path)
    file_service.prepare_static_folder()

    handle_args()
    print("searching duplicates...")
    find_duplicates()
    file_service.create_symbolic_links()


    app.run(use_reloader=False)
