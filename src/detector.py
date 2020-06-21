from flask import Flask, send_from_directory, render_template
from flask_restful import Api
import argparse
import os
import hashlib
from pathlib import Path
from random import randrange

app = Flask(__name__, static_folder='static')
api = Api(app)

duplicates = []
args = {}
file_extensions = ("jpg", "jpeg", "png", "gif", "img", "raw", "nef")


@app.route('/')
def root():
    global duplicates
    return render_template("index.html", duplicates=duplicates)


def file_hash(file_path: str):
    with open(file_path, 'rb') as f:
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
    parser.add_argument('-f', '--folder', dest='folder', default=False, required=True,
                        help="The folder which should be checked for duplicates")
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
                file
                duplicates[file_hash].append(Path(subdir, file))

    # Remove images which do not have duplicates
    for image_name, paths in list(duplicates.items()):
        if len(paths) <= 1:
            del duplicates[image_name]

    print(duplicates)


def generate_symbolic_link(path: Path):
    try:
        os.symlink(path, Path("src", "static", os.path.basename(path)))
    except FileExistsError:
        rand = randrange(1000)
        extension = os.path.splitext(os.path.basename(path))[1]
        name = os.path.splitext(os.path.basename(path))[0]
        os.symlink(path, Path("src", "static", f"{name}_{rand}{extension}"))


def symbol_links():
    global duplicates
    for key, images in list(duplicates.items()):
        for image in images:
            try:
                os.symlink(image, Path("src", "static", os.path.basename(image)))
            except FileExistsError:
                rand = randrange(1000)
                extension = os.path.splitext(os.path.basename(image))[1]
                name = os.path.splitext(os.path.basename(image))[0]
                os.symlink(image, Path("src", "static", f"{name}_{rand}{extension}"))


def clean_folder(path: Path):
    pass


if __name__ == '__main__':
    path = Path("src", "static")
    if path.exists():
        for subdir, dirs, files in os.walk(path):
            for file in files:
                print(file)
                try:
                    print("in here")
                    os.unlink(Path(path, file))
                except:
                    continue
    else:
        os.mkdir(path)

    handle_args()
    find_duplicates()
    symbol_links()
    app.run(use_reloader=False)
