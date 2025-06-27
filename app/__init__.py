# app/__init__.py

from flask import Flask, render_template
from app.utils.loader import load_blueprints_from_folder

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html") 

    load_blueprints_from_folder(app, "app/routes")

    return app
