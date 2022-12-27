from flask import Flask, render_template, request, redirect
from waitress import serve
from pathlib import Path
from src import FileService, Statics, DuplicateFinder
import sys, os

template_path = Path("src", "templates").absolute()
static_path = Path("src", "static").absolute()

app = Flask(__name__, template_folder=template_path, static_folder=f"{static_path}")


@app.route('/duplicates', methods=["post"])
def duplicates():
    if request.method == "POST":
        for data in request.form:
            data = data.split("||")
            image_path = str(data[0])
            hash_sum = str(data[1]).strip()

            if hash_sum not in Statics.duplicates.keys():
                print("Hash sum not found")
                continue

            duplicate = Statics.duplicates[hash_sum]
            Statics.duplicates[hash_sum].images = [image for image in duplicate.images if
                                                   str(image.path) != str(image_path)]

            if os.path.exists(image_path):
                os.remove(image_path)

    return redirect('/')


@app.route('/', methods=["get", "post"])
def index():
    if request.method == 'POST':

        new_path = request.form['new_path']
        if new_path and new_path not in Statics.search_paths:
            Statics.search_paths.append(new_path)

        if len(Statics.search_paths) > 0:
            DuplicateFinder.find_duplicates()
            FileService.create_symbolic_links()

        return render_template("index.html", duplicates=Statics.duplicates, search_paths=Statics.search_paths)

    return render_template("index.html", duplicates=Statics.duplicates, search_path=Statics.search_paths)


if __name__ == '__main__':
    Statics.static_path = Path(FileService.split_path(sys.argv[0])[0], "src/static")
    print(Statics.static_path)
    FileService.prepare_static_folder()

    print("searching duplicates...")
    # DuplicateFinder.find_duplicates()
    # file_service.create_symbolic_links()

    # app.run(use_reloader=False)
    serve(app, host="0.0.0.0", port=5000)
