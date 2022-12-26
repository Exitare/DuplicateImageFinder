from src.globals.statics import Statics
import os
from pathlib import Path
from random import randrange
from src.entities.image import Image


class FileService:

    @staticmethod
    def prepare_static_folder():
        path = Statics.static_path
        if path.exists():
            for subdir, dirs, files in os.walk(path):
                for file in files:
                    try:
                        os.unlink(Path(path, file))
                    except:
                        continue
        else:
            os.mkdir(path)

    @staticmethod
    def create_symbolic_links():
        for duplicate in Statics.duplicates:
            image: Image
            for image in duplicate.images:
                source_path = Path(image.path)

                try:
                    destination_path = Path(Statics.static_path, os.path.basename(Path(*source_path.parts[1:])))
                    os.symlink(source_path, destination_path)
                    image.symlink = Path("static", os.path.basename(Path(*source_path.parts[1:])))
                except FileExistsError:
                    rand = randrange(1000)
                    extension = os.path.splitext(os.path.basename(source_path))[1]
                    name = os.path.splitext(os.path.basename(source_path))[0]
                    destination_path = Path(Statics.static_path, f"{name}_{rand}{extension}")

                    os.symlink(source_path, destination_path)
                    image.symlink = Path("static", f"{name}_{rand}{extension}")

                except KeyError:
                    print("Could not extract key from dictionary. Skipping...")
                    continue

    @staticmethod
    def split_path(path: str):
        return os.path.split(path)
