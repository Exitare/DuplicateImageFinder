from flask import Flask, render_template
from flask_restful import Api
import argparse
import os
import hashlib
from pathlib import Path
from src import file_service, Statics, DuplicateFinder
import sys

template_path = Path("src", "templates").absolute()
static_path = Path("src", "static").absolute()

app = Flask(__name__, template_folder=template_path, static_folder=f"{static_path}")
api = Api(app)



@app.route('/')
def root():
    return render_template("index.html", duplicates=Statics.duplicates)


def handle_args():
    """
    Parse the given arguments
    :return:
    """
    parser = argparse.ArgumentParser(description='Get the impact of tool features on it\'s runtime.',
                                     epilog='Accepts tsv and csv files')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store', required=False,
                        help="Enables the verbose mode. With active verbose mode additional information is shown in the console")
    parser.add_argument('-f', '--folder', dest='folder', default=False, required=True,
                        help="The folder which should be checked for duplicates")
    Statics.args = parser.parse_args()



if __name__ == '__main__':
    Statics.static_path = Path(file_service.split_path(sys.argv[0])[0], "src/static")
    print(Statics.static_path)
    file_service.prepare_static_folder()

    handle_args()
    print("searching duplicates...")
    DuplicateFinder.find_duplicates()
    file_service.create_symbolic_links()


    app.run(use_reloader=False)
