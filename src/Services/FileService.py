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
            source_path = Path(image.path.absolute())

            try:
                destination_path = Path(Globals.static_path, os.path.basename(Path(*source_path.parts[1:])))
                os.symlink(source_path, destination_path)
                image.symlink = Path("static", os.path.basename(Path(*source_path.parts[1:])))
            except FileExistsError:
                rand = randrange(1000)
                extension = os.path.splitext(os.path.basename(source_path))[1]
                name = os.path.splitext(os.path.basename(source_path))[0]
                destination_path = Path(Globals.static_path, f"{name}_{rand}{extension}")

                os.symlink(source_path, destination_path)
                image.symlink = Path("static", f"{name}_{rand}{extension}")

            except KeyError:
                print("Could not extract key from dictionary. Skipping...")
                continue


def split_path(path: str):
    return os.path.split(path)
