from pathlib import Path
from src.globals.statics import Statics
import os, hashlib
from src.entities.image import Image
from src.entities.duplicate import Duplicate
from typing import Dict

file_extensions = ("jpg", "jpeg", "png", "gif", "img", "raw", "nef")


class DuplicateFinder:

    @staticmethod
    def find_duplicates():
        hash_keys: Dict = {}
        Statics.duplicates = {}

        for folder in Statics.search_paths:
            folder = Path(folder)

            # walk the dirs and find duplicates
            for subdir, dirs, files in os.walk(folder):
                for file in files:
                    if not file.endswith(file_extensions):
                        continue

                    with open(Path(subdir, file), 'rb') as f:
                        file_hash: str = hashlib.md5(f.read()).hexdigest()

                    if file_hash not in hash_keys:
                        hash_keys[file_hash] = [subdir]

                        # Create image entity and append to duplicates
                        image = Image(path=Path(subdir, file).absolute())
                        duplicate = Duplicate(file_hash)
                        duplicate.images.append(image)
                        Statics.duplicates[file_hash] = duplicate
                    else:
                        if subdir in hash_keys[file_hash]:
                            continue

                        hash_keys[file_hash].append(subdir)
                        # Create image entity and append to duplicates
                        image = Image(path=Path(subdir, file).absolute())
                        Statics.duplicates[file_hash].images.append(image)

        # Only keep real duplicates
        Statics.duplicates = {key: duplicate for (key,duplicate) in Statics.duplicates.items() if len(duplicate.images) > 1}