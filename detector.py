from flask import Flask, render_template, request
from flask_restful import Api
import argparse
import os
import hashlib
from pathlib import Path
from src import FileService, Statics, DuplicateFinder
import sys

template_path = Path("src", "templates").absolute()
static_path = Path("src", "static").absolute()

app = Flask(__name__, template_folder=template_path, static_folder=f"{static_path}")
api = Api(app)


@app.route('/', methods=["get", "post"])
def root():
    if request.method == 'POST':
        print(request)

        new_path = request.form['new_path']
        print("Path", new_path)

        if new_path:
            Statics.search_paths.append(new_path)

        if len(Statics.search_paths) > 0:
            DuplicateFinder.find_duplicates()
            FileService.create_symbolic_links()

        return render_template("index.html", duplicates=Statics.duplicates, search_paths=Statics.search_paths)

    return render_template("index.html", duplicates=Statics.duplicates)


if __name__ == '__main__':
    Statics.static_path = Path(FileService.split_path(sys.argv[0])[0], "src/static")
    print(Statics.static_path)
    FileService.prepare_static_folder()

    print("searching duplicates...")
    # DuplicateFinder.find_duplicates()
    # file_service.create_symbolic_links()

    app.run(use_reloader=False)
