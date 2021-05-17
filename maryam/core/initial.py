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

__version__ = 'v2.2.6'

import argparse
import imp
import os
import shutil
import sys
import shlex
import json
import concurrent.futures

from maryam.core import basedir
from multiprocessing import Pool,Process

class turn_off:
	def __enter__(self):
		self._original_stdout = sys.stdout
		sys.stdout = open(os.devnull, 'w')

	def __exit__(self, exc_type, exc_val, exc_tb):
		sys.stdout.close()
		sys.stdout = self._original_stdout

from .core import core

class initialize(core):

	def __init__(self, mode, section='*'):
		core.__init__(self)
		self._mode = mode
		self._config = {
				'name': 'maryam',
				'module_ext': '.py',
				'data_directory_name': 'data',
				'module_directory_name': 'modules',
				'workspaces_directory_name': '.maryam/workspaces'
			}
		self.section = section
		self._name = self._config['name']
		self._prompt_template = '%s[%s] > '
		self._base_prompt = self._prompt_template % ('', self._name)
		self.path = basedir.BASEDIR
		self.data_path = os.path.join(
			self.path, self._config['data_directory_name'])
		self.core_path = os.path.join(
			self.path, 'core')
		self.module_path = os.path.join(
			self.path, self._config['module_directory_name'])
		self.module_ext = self._config[
			'module_ext']
		self.module_dirname = self._config[
			'module_directory_name']
		self.workspaces_dirname = self._config['workspaces_directory_name']
		self._init_framework_options()
		self._init_home()
		self._init_workspace('default')
		self._init_util_classes(self.section)
		if mode != 'execute':
			self.__version__ = __version__
			self._check_version()
			self.show_banner()

	def _init_framework_options(self):
		self._global_options_['proxy'] = ('proxy', None, False,
							 'proxy server (address:port)')
		self._global_options_['agent'] = (
			'agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',\
			 True, 'user-agent')
		self._global_options_['rand_agent'] = ('rand_agent', False, True, 'setting random user-agent')
		self._global_options_['timeout'] = ('timeout', 10, True, 'socket timeout (seconds)')
		self._global_options_['verbosity'] = ('verbosity', 1, True, \
			'verbosity level (0 = minimal, 1 = verbose, 2 = debug)')
		self._global_options_['update_check'] = ('update_check', True, True,\
			'checking the framework version before running')
		self._global_options_['api_mode'] = ('api_mode', False, True,\
			'Activating API mode causes results will be shown in JSON format(warn: it doesnt show any other information)')
		for key in self._global_options_:
			self._global_options[key] = self._global_options_[key][1]

	def _init_home(self):
		self._home = os.path.expanduser('~')
		# initialize home folder
		if not os.path.exists(self._home):
			os.makedirs(self._home)

	def _init_util_classes(self, require='*'):
		util_path = os.path.join(self.core_path, 'util')
		for dirpath, _, files in os.walk(util_path, followlinks=True):
			if not dirpath.endswith(require) and require != '*' and util_path != dirpath: continue
			for file in filter(lambda f: f.endswith('.py')\
						and not f.startswith('__'), files):
				mod_name = file.split('.')[0]
				mod_path = os.path.join(dirpath, file)
				try:
					imp.load_source(mod_name, mod_path, open(mod_path)).main
				except Exception as e:
					self.error(f"Util class '{mod_name}' has been disabled due to this error: {e}", 'initial', '_init_util_classes')
				else:
					exec(f"self.{mod_name} = sys.modules['{mod_name}'].main")
					exec(f"self.{mod_name}.framework = self")

	def _load_modules(self, require='*'):
		self.loaded_category = {}
		self._loaded_modules = core._loaded_modules
		for dirpath, dirnames, _ in os.walk(self.module_path, followlinks=True):
			# Each Section
			for section in filter(lambda d: not d.startswith('__'), dirnames):
				category = section
				if require != category and require != '*': continue
				self._cat_module_names[category] = []
				section = os.path.join(dirpath, section)
				for _, _, files in os.walk(section):
					# Each File
					for file in filter(lambda f: f.endswith(self.module_ext) and not f.startswith('__'), files):
						mod_path = os.path.join(section, file)
						mod_load_name = f"__{file.split('.')[0]}"
						mod_disp_name = file.split('.')[0]
						try:
							imp.load_source(mod_load_name, mod_path, open(mod_path))
						except Exception as e:
							if not self._global_options['api_mode']:
								self.error(f"Module name '{mod_disp_name}' has been disabled due to this error: {e}", 'initial', '_load_modules')
						else:
							self._loaded_modules[mod_disp_name] = sys.modules[mod_load_name]
							self._cat_module_names[category].append(mod_disp_name)
							self._module_names.append(mod_disp_name)

	# ////////////////////////
	#          API 		    //
	# ////////////////////////

	def do_web(self, params):
		'''Manage web/api interface'''
		if not params:
			self.help_web()
			return
		params = params.lower().split(' ')
		if 'api' not in sys.modules:
			from .web import api
		if params[0] == 'api':
			api_mode = self._global_options['api_mode']
			_mode = self._mode
			self._mode = 'api'
			if not api_mode:
				self._global_options['api_mode'] = True
			if len(params) == 3:
				host = params[1]
				port = params[2]
			else:
				host = '127.0.0.1'
				port = 1313

			api.run_app(self, host, port)
			self._global_options['api_mode'] = api_mode
			self._mode = _mode

	def help_web(self):
		print(getattr(self, 'do_web').__doc__)
		print('\tweb api => running api on 127.0.0.1:1313')
		print('\tweb api <HOST> <PORT> => running api')

	# ////////////////////////////////
	#           WORKSPACE 		    //
	# ////////////////////////////////

	def _init_workspace(self, workspace):
		if not workspace:
			return
		workspace = os.path.join(self._home, self.workspaces_dirname, workspace)
		if not os.path.exists(workspace):
			os.makedirs(workspace)
		self.workspace = core.workspace = workspace
		self.prompt = self._prompt_template % (self._base_prompt[:-3], self.workspace.split('/')[-1])
		self._load_config()
		self._load_modules(self.section)
		return True

	def remove_workspaces(self, workspace):
		path = os.path.join(self._home, self.workspaces_dirname, workspace)
		try:
			shutil.rmtree(path)
		except OSError:
			return False
		if workspace == self.workspace.split('/')[-1]:
			self._init_workspace('default')
		return True

	def _get_workspaces(self):
		dirnames = []
		path = os.path.join(self._home, self.workspaces_dirname)
		dirnames = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
		return dirnames

	def show_banner(self):
		print(f"OWASP Maryam({__version__}): Open-source Intelligence Framework.\
			\nTo show the framework help, run 'help' command.")

	def show_workspaces(self):
		self.do_workspaces('list')

	def help_workspaces(self):
		print(getattr(self, 'do_workspaces').__doc__)
		print(f'{os.linesep}Usage: workspaces [add|select|delete|list]{os.linesep}')

	def do_reload(self, params=None):
		'''Reloads all modules'''
		self.output(f"Reloading...")
		if params:
			params = params.split()
			if params[0] == '*':
				self._init_util_classes(params[0])
			section = params[0]
		else:
			section = self.section
		self._load_modules(section)

	def do_workspaces(self, params):
		'''Manages workspaces'''
		if not params:
			self.help_workspaces()
			return
		params = params.split()
		arg = params.pop(0).lower()
		if arg == 'list':
			header = '\nWorkspaces\n'
			print(f"{header}{self.ruler * len(header[2:])}")
			for i in self._get_workspaces():
				print(''.ljust(5) + i)
			print('')
		elif arg in ['add', 'select']:
			if len(params) == 1:
				if not self._init_workspace(params[0]):
					self.output(f"Unable to initialize '{params[0]}' workspace.")
			else:
				print('Usage: workspace [add|select|delete] <name>')
		elif arg == 'delete':
			if len(params) == 1:
				if not self.remove_workspaces(params[0]):
					self.output(f"Unable to delete '{params[0]}' workspace.")
			else:
				print('Usage: workspace delete <name>')
		else:
			self.help_workspaces()

	# ////////////////////////////////
	#           MODULES 			//
	# ////////////////////////////////

	def alert_results(self, output, prefix='\t', depth=0, color='N'):
		if output == [] or output == {}:
			if depth != 0:
				self.output('Without result')
		if isinstance(output, dict):
			for key, value in output.items():
				if isinstance(value, list) or isinstance(value, dict):
					self.alert(f"{prefix*depth}{key.upper()}")
					self.alert_results(value, prefix=prefix, depth=depth + 1, color='G')
				else :
					value = value.strip().replace('\n', ' ').replace('\\x', ' ') if isinstance(value, str) else value
					self.alert(f"{prefix*depth}{key.upper()}")
					self.output(f"{prefix*(depth+1)}{value}", color)
			print('')
		elif isinstance(output, list):
			for key in output:
				self.alert_results(key, prefix='\t', depth=depth, color='G')
		else:
			output = output.strip().replace('\n', ' ').replace('\\x', ' ')
			self.output(f"{prefix*depth}{output}", color)

	def search_engine_results(self, output):
		for i in output['results']:
			self.output(i['t'])
			self.output(i['a'])
			self.output(i['c'])
			self.output(i['d'])
			print()

	def thread(self, *args):
		""" self, function, thread_count, engines, {...all args}, sources"""
		with concurrent.futures.ThreadPoolExecutor(max_workers=args[1]) as executor:
			[executor.submit(args[0], self, name, *args[3:-1]) for name in args[2] if name in args[-1]]

	def opt_proc(self, tool_name, args=None, output=None):
		""" processing the module name and its options to run"""
		mod = self._loaded_modules[tool_name]
		meta = mod.meta
		opts = meta['options']
		self.options = {}
		# Add default options
		opts += (('output', False, False, 'Save the output to the workspace', '--output', 'store_true', bool),)
		opts += (('api', False, False, 'Show results in the JSON format', '--api', 'store_true', bool),)
		opts += (('format', False, False, 'Beautifying JSON output if --api is used', '--format', 'store_true', bool),)
		description = f"{tool_name} {meta['version']}({meta['author']}) - \tdescription: {meta['description']}\n"
		parser = argparse.ArgumentParser(prog=tool_name, description=description)
		for option in opts:
			try:
				name, val, req, desc, op, act, typ = option
			except ValueError as e:
				self.error(f"{tool_name.title()}CodeError: options is too short. need more than {len(option)} option")
				return False
			name = f"--{name}" if not name.startswith('-') else name
			try:
				if act == 'store':
					parser.add_argument(op, name, help=desc, default=val, action='store', type=typ, required=req)
				else:
					parser.add_argument(op, name, help=desc, default=val, action=act, required=req)
			except argparse.ArgumentError as e:
				self.output(f"ModuleException: {str(e)}")
		# Initialize help menu
		format_help = parser.format_help()
		# Add comments
		if 'comments' in meta:
			format_help += 'Comments:'
			for comment in meta['comments']:
				prefix = '* '
				if comment.startswith('\t'):
					prefix = self.spacer + '- '
					comment = comment[1:]
				format_help += self.textwrapping(self.spacer, comment, 100)
			format_help += '\n'
		if 'sources' in meta:
			format_help += '\nSources:\n\t' + '\n\t'.join(meta['sources'])
		if 'examples' in meta:
			format_help += '\nExamples:\n\t' + '\n\t'.join(meta['examples'])
		if 'contributors' in meta:
			format_help += f"\nContributors:\n\t{meta['contributors']}"
		# If args is nothing
		if not args:
			print(format_help)
			return False
		else:
			# Initialite args
			if self._mode == 'execute':
				if self.section != '*':
					argv = sys.argv[4:]
				else:
					argv = sys.argv[3:]
				args = parser.parse_args(argv)
			else:
				lexer = shlex.split(args)
				args = parser.parse_args(lexer)
			args = vars(args)
			# Set options
			self.options = args
			try:
				if self.options['api'] or self._global_options['api_mode']:
					# Turn off framework prints till the executing of module
					with turn_off():
						results = mod.module_api(self)
						results['running_errors'] = self._error_stack
					if output == 'web_api':
						return results
					elif self.options['format']:
						print(json.dumps(results, indent=4))
					else:
						print(results)
					self._reset_error_stack()
				else:
					mod.module_run(self)
			except KeyboardInterrupt:
				pass
			except Exception as e:
				self.print_exception(where=tool_name, which_func='opt_proc')

	def mod_api_run(self, module):
		mod = self._loaded_modules[module]
		try:
			# with turn_off():
			results = mod.module_api(self)
			results['running_errors'] = self._error_stack
			self._reset_error_stack()
			return results
		except KeyboardInterrupt:
			pass
		except Exception as e:
			self.print_exception()
		return False

	def run_tool(self, func, tool_name, args, output=None):
		try:
			proc = Process(target=getattr(self, func), args=(tool_name, args, output))
			proc.start()
			proc.join()
			if proc.is_alive():
				proc.kill()
			return
		except KeyboardInterrupt as e:
			print(f"\nStopping {tool_name} module...")
			if proc.is_alive():
				proc.kill()
		except Exception as e:
			self.print_exception()
