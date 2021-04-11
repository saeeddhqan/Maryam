from flask import Blueprint, current_app, request, jsonify, abort
from flask_restful import Resource, Api
from core import initial
from core import core
import requests
import json
import os
from pathlib import Path

core_obj = core.core()
base_obj = initial.initialize(core_obj)

home = str(Path.home())

resources = Blueprint('resources', __name__, url_prefix='/api')
API = Api()
API.init_app(resources)

class ShowModules(Resource):
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

API.add_resource(ShowModules, '/framework/')

class RunModules(Resource):
    def get(self):
        print(request.args)
        args = request.args
        data = requests.get('http://localhost:5000/api/framework/').json()
        module_data = data['meta'][args['module']]
        cmd = args['module']
        for option in module_data['options']:
            try:
                if(option[5]=='store'):
                    if(args[option[0]]): #checking if user has supplied the parameter
                        cmd+= ' ' + option[4] + ' ' + args[option[0]]
                    else: #if the user has not supplied a mandatory parameter then use default
                        cmd+= ' ' + option[4] + ' ' + option[1]
                else:
                    if(args[option[0]]):
                        cmd+= ' ' + option[4]
            except Exception as e:
                continue

        base_obj.onecmd(cmd)
        workspace = current_app.config['WORKSPACE']
        try:
            filename = os.path.join(home, base_obj._config['workspaces_directory_name'], workspace, 'gather.dat')
            file = open(filename)
            data = json.loads(file.read())
        except:
            data = {}

        output = []
        for module in data:
            if args['module'] in module:
                for target in data[module]:
                    if args[module_data['options'][0][0]] == target:
                        output = data[module][target]
                        break
                break

        return {
            'meta': {
                'workspace': workspace,
                'cmd': cmd,
                'module': module_data
                },
            'output': output
        }

API.add_resource(RunModules, '/modules/')