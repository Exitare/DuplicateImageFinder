from Globals import Globals
import os
from pathlib import Path
from random import randrange


def prepare_static_folder():
    path = Globals.static_path
    if path.exists():
        for subdir, dirs, files in os.walk(path):
            for file in files:
                try:
                    os.unlink(Path(path, file))
                except:
                    continue
    else:
        os.mkdir(path)


def create_symbolic_links():
    for duplicate in Globals.duplicates:
        for image in duplicate.images:
            source_path = image.path
            try:
                os.symlink(source_path, Path(Globals.static_path, os.path.basename(source_path)))
                image.symlink = Path(Globals.static_path, os.path.basename(source_path))
            except FileExistsError:
                rand = randrange(1000)
                extension = os.path.splitext(os.path.basename(source_path))[1]
                name = os.path.splitext(os.path.basename(source_path))[0]
                os.symlink(source_path, Path(Globals.static_path, f"{name}_{rand}{extension}"))
                image.symlink = Path(Globals.static_path, f"{name}_{rand}{extension}")
                continue

            except KeyError:
                print("Could not extract key from dictionary. Skipping...")
                continue


def split_path(path: str):
    return os.path.split(path)

