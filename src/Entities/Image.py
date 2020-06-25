from pathlib import Path


class Image:

    def __init__(self, path: Path):
        self.path = path
        self.symlink = None
