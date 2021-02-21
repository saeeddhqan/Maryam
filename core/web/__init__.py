from flask import Flask, cli, render_template
from flasgger import Swagger
from core import base
import os

cli.show_server_banner = lambda *x: None

recon = base.Base()

SWAGGER = {
	'title' : "Swagger",
	'info' : {
		'title': 'Maryam-Api',
		'description': 'A RESTful API for Maryam'
	},
	'specs_route': '/api/'
}

WORKSPACE = recon.workspace.split('/')[-1]
print((f" * Workspace initialized: {WORKSPACE}"))

headings = ("Type","Modules","Targets","Results")
def create_app():

    # setting the static_url_path to blank serves static files from the web root
    app = Flask(__name__, static_url_path='')
    app.config.from_object(__name__)

    Swagger(app)

    @app.route('/')
    def index():
        return render_template('index.html', workspaces=recon._get_workspaces(),headings=headings)

    from core.web.api import resources
    app.register_blueprint(resources)

    return app
