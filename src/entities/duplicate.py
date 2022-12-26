from src import Image


class Duplicate:

    def __init__(self, hash_sum: str):
        self.hash_sum = hash_sum
        self.images: [Image] = []
        self.is_duplicate = True
