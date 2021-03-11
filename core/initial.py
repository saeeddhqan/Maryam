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

__version__ = "v2.0.0"
import argparse
import errno
import imp
import os
import re
import shutil
import sys
import shlex
import textwrap
import signal
from multiprocessing import Pool,Process

from core.core import core

class initialize(core):

	def __init__(self):
		core.__init__(self)
		self._history_file = ''
		self._mode = 0
		self._config = {
				'name': 'maryam',
				'module_ext': '.py',
				'data_directory_name': 'data',
				'module_directory_name': 'modules',
				'workspaces_directory_name': '.maryam/workspaces'
			}
		self._name = self._config['name']
		self._prompt_template = '%s[' + core.Colors.Y + '%s' + core.Colors.N + '] > '
		self._base_prompt = self._prompt_template % ('', self._name)
		# establish dynamic paths for framework elements
		self.path = sys.path[0]
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
		self._init_var()
		self._init_util_classes()
		self._check_version()
		self.show_banner()

	def _init_framework_options(self):
		self._global_options_['target'] = ('target', 'example.com', True,
							 'target for default hostname')
		self._global_options_['proxy'] = ('proxy', None, False,
							 'proxy server (address:port)')
		self._global_options_['agent'] = (
			'agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',\
			 True, 'user-agent')
		self._global_options_['rand_agent'] = ('rand_agent', False, True, 'setting random user-agent')
		self._global_options_['timeout'] = ('timeout', 10, True, 'socket timeout (seconds)')
		self._global_options_['verbosity'] = ('verbosity', 1, True, \
			'verbosity level (0 = minimal, 1 = verbose, 2 = debug)')
		self._global_options_['history'] = ('history', True, False, 'logging all console inputs')
		self._global_options_['update_check'] = ('update_check', True, False,\
			'checking the framework version before running')
		for key in self._global_options_:
			self._global_options[key] = self._global_options_[key][1]

	def _init_home(self):
		self._home = core._home = os.path.expanduser('~')
		# initialize home folder
		if not os.path.exists(self._home):
			os.makedirs(self._home)

	def _init_util_classes(self):
		util_path = os.path.join(self.core_path, 'util')
		for dirpath, _, files in os.walk(util_path, followlinks=True):
			for file in filter(lambda f: f.endswith('.py')\
						and not f.startswith('__'), files):
				mod_name = file.split('.')[0]
				mod_path = os.path.join(dirpath, file)
				try:
					imp.load_source(mod_name, mod_path, open(mod_path)).main
				except Exception as e:
					self.output(f"Module name '{mod_name}' has been disabled due to this error: {e}", 'O')
				else:
					exec(f"self.{mod_name} = sys.modules['{mod_name}'].main")
					exec(f"self.{mod_name}.framework = self")

	def _check_version(self):
		if self._global_options.get('update_check'):
			self.debug('Checking version...')
			pattern = r"__VERSION__ = '(\d+\.\d+\.\d+[^']*)'"
			remote = 0
			local = 0
			try:
				remote = re.search(pattern, self.request(\
					'https://raw.githubusercontent.com/saeeddhqan/maryam/master/maryam').text).group(1)
				local = re.search(pattern, open('maryam').read()).group(1)
			except Exception as e:
				self.error(f"Version check failed ({type(e).__name__}).")
			if remote != local:
				self.alert('Your version of Maryam does not match the latest release')
				self.output(f"Remote version:  {remote}")
				self.output(f"Local version:   {local}")

	def _load_modules(self):
		self.loaded_category = {}
		self._loaded_modules = core._loaded_modules
		for dirpath, dirnames, _ in os.walk(self.module_path, followlinks=True):
			# Each Section
			for section in filter(lambda d: not d.startswith('__'), dirnames):
				category = section
				self._cat_module_names[category] = []
				section = os.path.join(dirpath, section)
				for _, _, files in os.walk(section):
					# Each File
					for file in filter(lambda f: f.endswith(self.module_ext), files):
						mod_path = os.path.join(section, file)
						mod_disp_name = file.split('.')[0]

						try:
							imp.load_source(mod_disp_name, mod_path, open(mod_path))
						except Exception as e:
							self.output(f"Module name '{mod_disp_name}' has been disabled due to this error: {e}", 'O')
						else:
							self._loaded_modules[mod_disp_name] = sys.modules[mod_disp_name]
							self._cat_module_names[category].append(mod_disp_name)
							self._module_names.append(mod_disp_name)
	
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
		self._init_history()
		self._load_config()
		self._load_modules()
		return True

	def remove_workspace(self, workspace):
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
				self._init_util_classes()
		self._load_modules()

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
				if not self.remove_workspace(params[0]):
					self.output(f"Unable to delete '{params[0]}' workspace.")
			else:
				print('Usage: workspace delete <name>')
		else:
			self.help_workspaces()

	# ////////////////////////////////
	#           MODULES 			//
	# ////////////////////////////////

	def alert_results(self, output):
		if isinstance(output, dict):
			for key in output:
				self.alert(key.upper())
				for value in output[key]:
					self.output(f"\t{value}", 'G')
		elif isinstance(output, list):
			for value in output:
				self.output(f"\t{value}", 'G')
		else:
			self.output(output)

	def opt_proc(self, tool_name, args=None, output=None):
		mod = self._loaded_modules[tool_name]
		meta = mod.meta
		opts = meta['options']
		self.options = {}
		# Add default options
		opts += (('output', False, False, 'Save the output to the workspace', '--output', 'store_true'),)
		opts += (('api', False, False, 'Show results in the JSON format', '--api', 'store_true'),)
		description = f"{tool_name} {meta['version']}({meta['author']}) - \tdescription: {meta['description']}\n"
		parser = argparse.ArgumentParser(prog=tool_name, description=description)
		for option in opts:
			try:
				name, val, req, desc, op, act = option
			except ValueError as e:
				self.error(f"{tool_name.title()}CodeError: options is too short. need more than {len(option)} option")
				return
			name = f"--{name}" if not name.startswith('-') else name
			try:
				parser.add_argument(op, name, help=desc, dest=name, default=val, action=act, required=req)
			except argparse.ArgumentError as e:
				self.error(f"ModuleException: {str(e)}")
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
				format_help += f"\n{self.spacer}{textwrap.fill(prefix + comment, 100, subsequent_indent=self.spacer)}"
			format_help += '\n'
		if 'sources' in meta:
			format_help += '\nSources:\n\t' + '\n\t'.join(meta['sources'])
		if 'examples' in meta:
			format_help += '\nExamples:\n\t' + '\n\t'.join(meta['examples'])

		# If args is nothing
		if not args:
			print(format_help)
		else:
			# Initialite args
			clean_args = []
			for arg in args.split(' '):
				if arg.startswith('$'):
					arg = self.get_var(arg[1:])
				clean_args.append(arg)
			clean_args = ' '.join(clean_args)
			args = parser.parse_args(shlex.split(clean_args))
			args = vars(args)
			# Set options
			for option in args:
				self.options[option[2:]] = args[option]

			try:
				if self.options['api']:
					verb = self._global_options['verbosity']
					self._global_options['verbosity'] = 0
					results = mod.module_api(self)
					self._global_options['verbosity'] = verb
					print(results)
				else:
					mod.module_run(self)
			except Exception as e:
				self.print_exception()

	def run_tool(self, func, tool_name, args, output=None):
		# try:
		proc = Process(target=getattr(self, func), args=(tool_name, args, output))
		proc.start()
		proc.join()
		def signal_handler(signum, frame):  
			print(f"\nStopping {tool_name} module(press enter to continue)...")
			if 'kill' in dir(proc):
				proc.kill()
		signal.signal(signal.SIGINT, signal_handler)
		if 'kill' in dir(proc):
			proc.kill()
		# except KeyboardInterrupt:
			# return
		# except:
			# self.print_exception()
