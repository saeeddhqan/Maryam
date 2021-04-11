from flask import Flask, cli, render_template
from flasgger import Swagger
from core import initial
from core import core
import os
import requests
import json

cli.show_server_banner = lambda *x: None

core_obj = core.core()
base_obj = initial.initialize(core_obj)

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

def create_app():

    app = Flask(__name__, static_url_path='')
    app.config.from_object(__name__)

    Swagger(app)

    from core.web.api import resources
    app.register_blueprint(resources)

    return app
