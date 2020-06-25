from flask import Flask, send_from_directory, render_template
from flask_restful import Api
import argparse
import os
import hashlib
from pathlib import Path
from random import randrange
from Globals import Globals
from Entities.Image import Image

app = Flask(__name__, static_folder='static')
api = Api(app)

duplicates = []
args = {}
file_extensions = ("jpg", "jpeg", "png", "gif", "img", "raw", "nef")


@app.route('/')
def root():
    global duplicates
    return render_template("index.html", duplicates=Globals.duplicates)


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
            if not file.endswith(file_extensions):
                continue

            with open(Path(subdir, file), 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash not in hash_keys:
                hash_keys[file_hash] = subdir

                # Create image entity and append to duplicates
                image = Image(Path(subdir, file))
                Globals.duplicates.append(image)
            else:
                # Create image entity and append to duplicates
                image = Image(Path(subdir, file))
                Globals.duplicates.append(image)

    # Remove images which do not have duplicates
    for  in list(Globals.duplicates):
        # TODO: Remove symlinks if no duplicates found
        if len(paths) <= 1:
            del duplicates[image_name]


def generate_symbolic_link(path: Path):
    """
    Generates a symbolic link for each image
    :param path:
    :return:
    """
    try:
        sym_path = Path("src", "static", os.path.basename(str(path)))
        os.symlink(str(path), sym_path)
        return sym_path
    except FileExistsError:
        rand = randrange(1000)
        extension = os.path.splitext(os.path.basename(str(path)))[1]
        name = os.path.splitext(os.path.basename(str(path)))[0]
        sym_path = Path("src", "static", f"{name}_{rand}{extension}")
        os.symlink(str(path), sym_path)
        return sym_path


def symbol_links():
    global duplicates
    for key, images in list(duplicates.items()):
        for path in images:
            source_path = path.get('OriginalPath')
            try:

                os.symlink(source_path, Path("src", "static", os.path.basename(source_path)))
            except FileExistsError:
                rand = randrange(1000)
                extension = os.path.splitext(os.path.basename(source_path))[1]
                name = os.path.splitext(os.path.basename(source_path))[0]
                os.symlink(source_path, Path("src", "static", f"{name}_{rand}{extension}"))
                continue

            except KeyError:
                print("Could not extract key from dictionary. Skipping...")
                continue
    print(duplicates)


def clean_folder(path: Path):
    pass


if __name__ == '__main__':
    path = Path("src", "static")
    if path.exists():
        for subdir, dirs, files in os.walk(path):
            for file in files:
                print(file)
                try:
                    os.unlink(Path(path, file))
                except:
                    continue
    else:
        os.mkdir(path)

    handle_args()
    find_duplicates()
    symbol_links()

    app.run(use_reloader=False)
