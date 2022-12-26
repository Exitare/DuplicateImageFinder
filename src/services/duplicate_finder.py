from pathlib import Path
from src.globals.statics import Statics
import os, hashlib
from src.entities.image import Image
from src.entities.duplicate import Duplicate

file_extensions = ("jpg", "jpeg", "png", "gif", "img", "raw", "nef")


class DuplicateFinder:

    @staticmethod
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
                    Statics.duplicates[file_hash] = duplicate
                else:
                    # Create image entity and append to duplicates
                    image = Image(path=Path(subdir, file).absolute())
                    Statics.duplicates[file_hash].images.append(image)

        # Only keep real duplicates
        Statics.duplicates = [duplicate for duplicate in Statics.duplicates.values() if len(duplicate.images) > 1]
