"""
OWASP Maryam!

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import flask
from flask import request, jsonify
from json import dumps

framework = None
app = flask.Flask('OWASP Maryam')

@app.route('/', methods=['GET', 'POST'])
def home():
	page = '<pre>current pages:<br>/api/modules => running modules<br>/api/framework => framework commands</pre>'
	return page


@app.route('/api/', methods=['GET', 'POST'])
def api():
	page = '<pre>current pages:<br>/api/modules => running modules<br>/api/framework => framework commands'\
		   '<br><b>/api/modules?_module=<module-name>&options[short or long]...</b>'\
		   '<br>["meta"]: api metadata'\
		   '<br>["meta"]["error"]: error messages. None if no error occurs'\
		   '<br>["meta"]["command"]: input command'\
		   '<br>["output"]: module output'\
		   '<br>["output"]["running_errors]: error messages that occurs during running the module'\
		   '<br><b>/api/framework?command=<command></b>'\
		   '<br>["meta"]: api metadata'\
		   '<br>["meta"]["error"]: error messages. None if no error occurs'\
		   '<br>["meta"]["command"]: input command'\
		   '</pre>'
	return page

@app.route('/api/framework')
def api_framework():
	error = None
	command = None
	page = {'meta': {'error': error, 'command': command}}
	if 'command' in request.args:
		invalid_commands = ['workspaces', 'set', 'unset', 'history', 'report', 'update']
		command = request.args['command']
		if command != '':
			if command.split(' ')[0] in invalid_commands:
				framework.onecmd(command)
				command = request.args['command']
			else:
				error = 'Invalid command.'
		else:
			error = 'No command specified.'
	else:
		error = 'no command specified.'
	page['meta']['command'] = command
	page['meta']['error'] = error
	return jsonify(page)

@app.route('/api/modules')
def api_modules():
	page = {'meta': {'error': None, 'command': None}, 'output': {}}

	# If no module specified
	args_dict = request.args.to_dict()
	if '_module' not in args_dict:
		page['meta']['error'] = 'No module specified.'
		return jsonify(page)

	module_name = args_dict.pop('_module')
	# If module doesn't exist
	if module_name not in framework._loaded_modules:
		page['meta']['error'] = f"Module name '{module_name}' not found."
		return jsonify(page)
	
	# Validating and Setting framework options	
	framework_option_error= framework.set_framework_options(module_name, args_dict) 
	if(framework_option_error):
		page['meta']['error'] = framework_option_error
		return jsonify(page)

	# Executing Module
	result = framework.run_module_api(module_name)
	page['meta']['error'] = result.get('error', None)
	page['output'] = result.get('output', None)
	page['meta']['command'] = result.get('command', None)
	return jsonify(page)

@app.errorhandler(404)
def page_not_found(e):
    return "<pre>404</pre>", 404

def run_app(core_obj, host='127.0.0.1', port=1313):
	global framework
	framework = core_obj
	app.run(host=host, port=port)
