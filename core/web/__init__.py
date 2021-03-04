from flask import Flask, cli, render_template
from flasgger import Swagger
from core import base
import os

cli.show_server_banner = lambda *x: None

base_obj = base.Base()

SWAGGER = {
	'title': 'Swagger',
	'info': {
		'title': 'Maryam-Api',
		'description': 'A RESTful API for Maryam'
	},
	'specs_route': '/api/'
}

WORKSPACE = base_obj.workspace.split('/')[-1]
print((f" * Workspace initialized: {WORKSPACE}"))

headings = ('Type', 'Modules', 'Targets', 'Results')
def create_app():

    # setting the static_url_path to blank serves static files from the web root
    app = Flask(__name__, static_url_path='')
    app.config.from_object(__name__)

    Swagger(app)

    @app.route('/')
    def index():
        return render_template('index.html', workspaces=base_obj._get_workspaces(), headings=headings)

    @app.route('/run')
    def run():
        return render_template('run.html', workspaces=base_obj._get_workspaces(), headings=headings)

    from core.web.api import resources
    app.register_blueprint(resources)

    return app
