from flask_restful import MethodView
from flask import send_from_directory
from detector import app


class BaseController(MethodView):
    def get(self):
        return send_from_directory(app.static_folder, 'index.html')
