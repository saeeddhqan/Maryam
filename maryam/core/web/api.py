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
	page = '<pre>current pages:<br>/api/modules => running modules<br>/api/framework => framework commands<br>/api/iris_cluster => iris search and cluster module'
	return page


@app.route('/api/', methods=['GET', 'POST'])
def api():
	page = '<pre>current pages:<br>/api/modules => running modules<br>/api/framework => framework commands<br>/api/iris_cluster => iris search and cluster module'\
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
		   '<br><b>/api/iris_cluster?options[short or long]...</b>'\
		   '<br>["meta"]: api metadata'\
		   '<br>["meta"]["error"]: error messages. None if no error occurs'\
		   '<br>["output"]: module output'\
		   '<br>["output"]["iris_search_result]: search results by iris module'\
		   '<br>["output"]["cluster_result]: search results by cluster module'\
		   '<br>["output"]["running_errors]: error messages that occurs during running the module'\
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

@app.route('/api/iris_cluster')
def api_iris_cluster():
	page = {'meta': {'error': None}, 'output': {}}
	args_dict = request.args.to_dict()

	module_name = 'iris'
	# Validating and Setting framework options for Iris Module	
	framework_option_error= set_framework_options(module_name, args_dict) 
	if(framework_option_error):
		page['meta']['error'] = framework_option_error
		return jsonify(page)
	# Executing Iris Module 
	iris_search_result = run_module_api(module_name)
	if('error' in iris_search_result.keys()):
		page['meta']['error'] = iris_search_result.get('error', None)
		return jsonify(page)
	page['output']['iris_search_result'] = iris_search_result.get('output', None)	
	
	module_name = 'cluster'
	# Validating and Setting framework options for Cluster Module	
	cluster_user_options = {
		'data': dumps(iris_search_result.get('output', None))
	}
	framework_option_error= set_framework_options(module_name, cluster_user_options) 
	if(framework_option_error):
		page['meta']['error'] = framework_option_error
		return jsonify(page)
	# Executing Cluster Module 
	cluster_result = run_module_api(module_name)
	page['output']['cluster_result'] = cluster_result.get('output', None)
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
	framework_option_error= set_framework_options(module_name, args_dict) 
	if(framework_option_error):
		page['meta']['error'] = framework_option_error
		return jsonify(page)

	# Executing Module
	result = run_module_api(module_name)
	page['meta']['error'] = result.get('error', None)
	page['output'] = result.get('output', None)
	page['meta']['command'] = result.get('command', None)
	return jsonify(page)

@app.errorhandler(404)
def page_not_found(e):
    return "<pre>404</pre>", 404


def set_framework_options(module_name, user_options):
	if user_options == {}:
		return f"No option specified."
	
	module = framework._loaded_modules[module_name]
	options = module.meta['options']
	true_options = ('true', 'on', 'yes', '1', True)
	framework.options = {}

	# Add framework options
	if 'output' in user_options:
		if user_options['output'] in true_options:
			framework.options['output'] = True
		else:
			framework.options['output'] = False
	else:
		framework.options['output'] = False

	# Setting options
	for option in options:
		option_name = option[0]
		default_option_value = option[1]
		option_required = option[2] # OPTION REQUIRED CHECK
		option_type = option[6]
		option_name_short = option[4][1:]
		option_action = option[5]
		if option_name in user_options:
			option_value = user_options[option_name]
		elif option_name_short in user_options:
			option_value = user_options[option_name_short]
		else:
			option_value = default_option_value

		if option_action == 'store':
			if option_value == default_option_value or isinstance(option_value, option_type):
				framework.options[option_name] = option_value
			else:
				return f"Need {option_type}. got invalid type for {option_name}."
		else:
			if option_value in true_options:
				framework.options[option_name] = True
	


def run_module_api(module_name):
	result = {}
	try:
		output = framework.mod_api_run(module_name)
	except Exception as e:
		framework.print_exception()
		output = False
	if output == False:
		result['error'] = 'Something went wrong'
	else:
		result['output'] = output
		if result['output']['running_errors'] != []:
			result['error'] = 'Runting error'
	result['command'] = framework.options 
	return result
	

def run_app(core_obj, host='127.0.0.1', port=1313):
	global framework
	framework = core_obj
	app.run(host=host, port=port)
