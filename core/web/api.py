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

@app.route('/', methods=['GET'])
def home():
	page = '<pre>current pages:<br>/api/modules => running modules<br>/api/framework => framework commands</pre>'
	return page


@app.route('/api/', methods=['GET'])
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

@app.route('/api/framework', methods=['GET'])
def api_framework():
	page = {'meta': {'error': None, 'command': ''}}
	if 'command' in request.args:
		framework.onecmd(request.args['command'])
		page['meta']['command'] = request.args['command']
	else:
		page['meta']['error'] = 'no command specified.'
		page['meta']['command'] = None
	return jsonify(page)

@app.route('/api/modules', methods=['GET'])
def api_modules():
	page = {'meta': {'error': None, 'command': None}, 'output': {}}
	# If no module specified
	if '_module' not in request.args:
		page['meta']['error'] = 'No module specified.'
		return jsonify(page)
	module_name = request.args['_module']
	# If module doesn't exist
	if module_name not in framework._loaded_modules:
		page['meta']['error'] = f'Module name "{module_name}" not found.'
		return jsonify(page)

	module = framework._loaded_modules[module_name]
	options = module.meta['options']
	args = ''
	args_dict = request.args.to_dict()
	# Setting options
	for option in options:
		option_name = option[0]
		option_name_short = option[4][1:]
		option_action = option[5]
		prefix = '-'
		if option_name in args_dict:
			prefix = '--'
			option_value = args_dict[option_name]
		elif option_name_short in args_dict:
			option_value = args_dict[option_name_short]
			option_name = option_name_short
		else:
			continue
		if option_action == 'store':
			args += f"{prefix}{option_name} {option_value} "
		else:
			args += f"--{option_name} "
	# If no command specified.
	if args == '':
		page['meta']['error'] = 'No command found.'
		return jsonify(page)
	# Remove last space
	if args[-1:] == ' ':
		args = args[:-1]

	command = f"{module_name} {args}"
	page['output'] = framework.opt_proc(module_name, args, 'web_api')
	if page['output']['running_errors'] != []:
		page['meta']['error'] = 'Runtime error.'
	page['meta']['command'] = command
	return jsonify(page)

@app.errorhandler(404)
def page_not_found(e):
    return "<pre>404</pre>", 404

def run_app(core_obj, host='127.0.0.1', port=1313):
	global framework
	framework = core_obj
	app.run(host=host, port=port)
