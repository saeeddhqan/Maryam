from flask import Blueprint, current_app, request, jsonify, abort
from flask_restful import Resource, Api
import json
import os
from pathlib import Path


home = str(Path.home())

resources = Blueprint('resources', __name__, url_prefix='/api')
API = Api()
API.init_app(resources)

class WorkspaceSummary(Resource):
    def post(self):
        workspace = request.json['workspace']
        current_app.config['WORKSPACE'] = workspace
        try:
            filename = os.path.join(home, '.maryam/workspaces/', workspace, 'gather.dat')
            file = open(filename)
            data = json.loads(file.read())
        except:
            data = {}
        return data

API.add_resource(WorkspaceSummary, '/workspaces/')
