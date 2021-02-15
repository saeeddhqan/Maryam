from flask import Flask, cli, render_template
from core import base
import os

cli.show_server_banner = lambda *x: None

def create_app():

    # setting the static_url_path to blank serves static files from the web root
    app = Flask(__name__, static_url_path='')
    app.config.from_object(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app