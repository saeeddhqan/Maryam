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
	if args_dict == {}:
		page['meta']['error'] = f"No option specified."
		return jsonify(page)
	module = framework._loaded_modules[module_name]
	options = module.meta['options']
	true_options = ('true', 'on', 'yes', '1', True)
	framework.options = {}
	# Add framework options
	if 'output' in args_dict:
		if args_dict['output'] in true_options:
			framework.options['output'] = True
		else:
			framework.options['output'] = False
	else:
		framework.options['output'] = False

	# Setting options
	for option in options:
		option_name = option[0]
		option_required = option[2]
		option_type = option[6]
		option_name_short = option[4][1:]
		option_action = option[5]
		if option_name in args_dict:
			option_value = args_dict[option_name]
		elif option_name_short in args_dict:
			option_value = args_dict[option_name_short]
		else:
			option_value = option[1]

		if option_action == 'store':
			if isinstance(option_value, option_type):
				framework.options[option_name] = option_value
			else:
				page['meta']['error'] = f"Need {option_type}. got invalid type for {option_name}."
				return jsonify(page)
		else:
			if option_value in true_options:
				framework.options[option_name] = True
	try:
		output = framework.mod_api_run(module_name)
	except Exception as e:
		framework.print_exception()
		output = False
	if output == False:
		page['meta']['error'] = 'Something went wrong.'
	else:
		page['output'] = output
		if page['output']['running_errors'] != []:
			page['meta']['error'] = 'Runtime error.'
	page['meta']['command'] = framework.options
	return jsonify(page)

@app.errorhandler(404)
def page_not_found(e):
    return "<pre>404</pre>", 404

def run_app(core_obj, host='127.0.0.1', port=1313):
	global framework
	framework = core_obj
	app.run(host=host, port=port)
