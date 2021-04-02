from flask import Blueprint, current_app, request, jsonify, abort
from flask_restful import Resource, Api
from core import initial
from core import core
import json
import os
from pathlib import Path

core_obj = core.core()
base_obj = initial.initialize(core_obj)

home = str(Path.home())

resources = Blueprint('resources', __name__, url_prefix='/api')
API = Api()
API.init_app(resources)

class WorkspaceSummary(Resource):
    def post(self):
        workspace = request.json['workspace']
        base_obj._init_workspace(workspace)
        current_app.config['WORKSPACE'] = workspace
        WORKSPACE = base_obj.workspace.split('/')[-1]
        print((f" * Workspace initialized: {WORKSPACE}"))
        try:
            filename = os.path.join(home, base_obj._config['workspaces_directory_name'], workspace, 'gather.dat')
            file = open(filename)
            data = json.loads(file.read())
        except:
            data = {}
        return data

API.add_resource(WorkspaceSummary, '/workspaces/')


class RunModules(Resource):
    def get(self):
        meta = {}
        modules = []
        module_path = os.path.abspath(os.path.join(os.getcwd(), 'modules'))
        for mod_type in os.listdir(module_path):
            for module in os.listdir(os.path.join(module_path,mod_type)): 
                if module.split('.')[-1] == 'py' :
                    modules.append(mod_type + '/' + module.split('.')[0])

        for module in modules:
            meta[module.split('/')[-1]] = base_obj.opt_proc(module.split('/')[-1], args=None, output=None)

        meta = json.dumps(meta, default=lambda o: o.__name__, sort_keys=True, indent=4)
        meta = json.loads(meta)

        return {
            'modules': modules,
            'meta': meta
        }

    def post(self):
        cmd = request.json['cmd']
        args = cmd.split(' ');
        ret = base_obj.onecmd(cmd)
        workspace = current_app.config['WORKSPACE']
        try:
            filename = os.path.join(home, base_obj._config['workspaces_directory_name'], workspace, 'gather.dat')
            file = open(filename)
            data = json.loads(file.read())
        except:
            data = {}

        output = []
        for module in data:
            if args[0] in module:
                for target in data[module]:
                    if args[2] in target:
                        output = data[module][target]
                        break
                break

        return {
            'output': output,
            'workspace': workspace,
            'cmd': cmd
        }

API.add_resource(RunModules, '/run/')


class PlotGraph(Resource):
    def get(self):
        workspace = current_app.config['WORKSPACE']
        try:
            filename = os.path.join(home, '.maryam/workspaces/', workspace, 'gather.dat')
            file = open(filename)
            data = json.loads(file.read())
        except:
            data = {}

        dataPoints = {"modules" : [] , "targets": [], "name": []}
        for modules in sorted(list(data.keys())):
            dataPoints['modules'].append(modules.split('/')[1])
            dataPoints['targets'].append(len(data[modules]))
            dataPoints['name'].append(', '.join(data[modules].keys()))

        return dataPoints

API.add_resource(PlotGraph, '/graph/')