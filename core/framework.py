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
# Based on the Recon-ng core(https://github.com/lanmaster53/recon-ng)

import cmd
import codecs
import json
import os
import re
import subprocess
import sys
import signal
import traceback
import requests
import shlex
from core.util import rand_uagent
from io import StringIO

class FrameworkException(Exception):
	def __init__(self, message):
		Exception.__init__(self, message)

class Colors(object):
	N = '\033[m'  # native
	R = '\033[91m'  # red
	G = '\033[92m'  # green
	O = '\033[93m'  # orange
	B = '\033[94m'  # blue
	P = '\033[95m'  # purple
	C = '\033[0;1;36m'  # cyan


class Options(dict):

	def __init__(self, *args, **kwargs):
		self.required = {}
		self.description = {}

		super(Options, self).__init__(*args, **kwargs)

	def __setitem__(self, name, value):
		super(Options, self).__setitem__(name, self._autoconvert(value))

	def __delitem__(self, name):
		super(Options, self).__delitem__(name)
		if name in self.required:
			del self.required[name]
		if name in self.description:
			del self.description[name]

	def _boolify(self, value):
		# designed to throw an exception if value is not a string
		# representation of a boolean
		return {'true': True, 'false': False, 'yes': True, 'no': False}[value.lower()]

	def _autoconvert(self, value):
		if value in (None, True, False):
			return value
		elif (isinstance(value, str)) and value.lower() in ('none', '\'\'', '\"\"'):
			return None
		orig = value
		for fn in (self._boolify, int, float):
			try:
				value = fn(value)
				break
			except (ValueError, KeyError, AttributeError):
				pass
		if isinstance(value, int) and '.' in str(orig):
			return float(orig)
		return value

	def init_option(self, name, value=None, required=False, description=''):
		self[name] = value
		self.required[name] = required
		self.description[name] = description

	def serialize(self):
		data = {}
		for key in self:
			data[key] = self[key]
		return data

# =================================================
# FRAMEWORK CLASS
# =================================================


class Framework(cmd.Cmd):
	prompt = ">>>"
	# mode flags
	_script = 0
	_load = 0
	# framework variables
	_global_options = Options()
	_loaded_modules = {}
	_module_names = {}
	app_path = ''
	data_path = ''
	core_path = ''
	module_path = ''
	module_dirname = ''
	workspace = ''
	module_ext = ''
	variables = {}
	_home = ''
	_record = None
	_spool = None
	_summary_counts = {}
	Colors = Colors
	_history_file = ''
	def __init__(self, params):
		cmd.Cmd.__init__(self)
		self._modulename = params
		self.ruler = '-'
		self.spacer = '  '
		self.nohelp = f'{Colors.R}[!] No help on %s{Colors.N}'
		self.do_help.__func__.__doc__ = '''Displays this menu'''
		self.doc_header = 'Commands (type [help|?] <topic>):'
		self._exit = 0

	# ==================================================
	# CMD OVERRIDE METHODS
	# ==================================================

	def default(self, line):
		self.do_shell(line)

	def emptyline(self):
		# disables running of last command when no command is given
		# return flag to tell interpreter to continue
		return 0

	def precmd(self, line):
		line = self.to_unicode(line)
		if Framework._load:
			print('\r', end='')
		if Framework._script:
			print(f'{line}')
		if Framework._record:
			recorder = codecs.open(Framework._record, 'ab', encoding='utf-8')
			recorder.write(f'{line}{os.linesep}')
			recorder.flush()
			recorder.close()
		if Framework._spool:
			Framework._spool.write(f'{self.prompt}{line}{os.linesep}')
			Framework._spool.flush()
		return line

	def onecmd(self, line):
		line = self.to_unicode(line)
		# Log commant into the history file if 'history' is true
		if self._global_options['history']:
			self._log_commands(line)
		cmd, arg, line = self.parseline(line)
		if not line:
			return self.emptyline()
		if line == 'EOF':
			# reset stdin for raw_input
			sys.stdin = sys.__stdin__
			Framework._script = 0
			Framework._load = 0
			return 0
		if cmd is None:
			return self.default(line)
		self.lastcmd = line
		if cmd == '':
			return self.default(line)
		else:
			if cmd in self._module_names:
				return self.run_tool('opt_proc', cmd, arg)
			else:
				try:
					func = getattr(self, 'do_' + cmd)
				except AttributeError:
					return self.default(line)
				try:
					return func(arg)
				except Exception as e:
					self.print_exception()

	# make help menu more attractive
	def print_topics(self, header, cmds, cmdlen, maxcol):
		if cmds:
			self.stdout.write(f"{header}{os.linesep}")
			if self.ruler:
				self.stdout.write(f"{self.ruler * len(header)}{os.linesep}")
			for cmd in cmds:
				self.stdout.write(f"{cmd.ljust(15)} {getattr(self, 'do_' + cmd).__doc__}{os.linesep}")
			self.stdout.write(os.linesep)

	# ==================================================
	# SUPPORT METHODS
	# ==================================================

	def to_unicode_str(self, obj, encoding='utf-8'):
		# converts non-stringish types to unicode
		if type(obj) not in (str, bytes):
			obj = str(obj)
		obj = self.to_unicode(obj, encoding)
		return obj

	def to_unicode(self, obj, encoding='utf-8'):
		# checks if obj is a string and converts if not
		if isinstance(obj, bytes):
			obj = str(obj, encoding)
		else:
			obj = str(obj)
		return obj

	def _is_readable(self, filename, flag='r'):
		try:
			return open(filename, flag)
		except IOError as e:
			self.error('IOError: ' + str(e))
			return False

	def _parse_rowids(self, rowids):
		xploded = []
		rowids = [x.strip() for x in rowids.split(',')]
		for rowid in rowids:
			try:
				if '-' in rowid:
					start = int(rowid.split('-')[0].strip())
					end = int(rowid.split('-')[-1].strip())
					xploded += range(start, end + 1)
				else:
					xploded.append(int(rowid))
			except ValueError:
				continue
		return sorted(list(set(xploded)))

	# ==================================================
	# OUTPUT METHODS
	# ==================================================

	def print_exception(self, line=''):
		stack_list = [x.strip() for x in traceback.format_exc().strip().splitlines()]
		message = stack_list[-1]
		if self._global_options['verbosity'] == 0:
			return
		elif self._global_options['verbosity'] == 1:
			line = ' '.join([x for x in [message, line] if x])
			self.error(stack_list[-3])
			self.error(line)
		elif self._global_options['verbosity'] == 2:
			print(f"{Colors.R}{'-'*60}")
			traceback.print_exc()
			print(f"{'-'*60}{Colors.N}")

	def error(self, line):
		'''Formats and presents errors.'''
		if not re.search(r'[.,;!?]$', line):
			line += '.'
		line = line[:1].upper() + line[1:]
		print(f"{Colors.R}[!] {line}{Colors.N}")

	def output(self, line, color='N', end='', linesep=True):
		'''Formats and presents normal output.'''
		line = self.to_unicode(line)
		line = f'{Colors.B}[*]{getattr(Colors, color.upper())} {line}\033[m'
		if not line.endswith(os.linesep) and linesep:
			line += os.linesep
		print(line, end=end)

	def alert(self, line):
		'''Formats and presents important output.'''
		print(f"{Colors.G}[*]{Colors.N} {line}")

	def verbose(self, line, color='n', end=''):
		'''Formats and presents output if in verbose mode.'''
		if self._global_options['verbosity'] >= 1:
			self.output(line, color, end)

	def debug(self, line, end='', linesep=True):
		'''Formats and presents output if in debug mode (very verbose).'''
		if self._global_options['verbosity'] >= 2:
			line = f'{Colors.C}[~] {Colors.N}{self.to_unicode(line)}'
			if not line.endswith(os.linesep) and linesep:
				line += os.linesep
			print(line, end=end)

	def heading(self, line, level=1):
		'''Formats and presents styled header text'''
		line = line
		print('')
		if level == 0:
			print(self.ruler*len(line))
			print(line.upper())
			print(self.ruler*len(line))
		if level == 1:
			print(f"{self.spacer}{line.title()}")
			print(f"{self.spacer}{self.ruler*len(line)}")

	def table(self, data, header, title='', linear=False, sep='-'):
		'''Accepts a list of rows and outputs a table.'''
		tdata = list(data)
		if header:
			tdata.insert(0, header)
		if len(set([len(x) for x in tdata])) > 1:
			raise FrameworkException('Row lengths not consistent.')
		lens = []
		cols = len(tdata[0])
		# create a list of max widths for each column
		for i in range(0, cols):
			lens.append(len(max([self.to_unicode_str(x[i]) if x[i] != None else '' for x in tdata], key=len)))
		# calculate dynamic widths based on the title
		title_len = len(title)
		tdata_len = sum(lens) + (3*(cols-1))
		diff = title_len - tdata_len
		if diff > 0:
			diff_per = diff / cols
			lens = [x+diff_per for x in lens]
			diff_mod = diff % cols
			for x in range(0, diff_mod):
				lens[x] += 1
		# build ascii table
		if len(tdata) > 0:
			separator_str = f"{self.spacer}+{sep}{f'%s{sep*3}'*(cols-1)}%s{sep}+"
			separator_sub = tuple([sep*x for x in lens])
			separator = separator_str % separator_sub
			data_str = f"{self.spacer}| {'%s | '*(cols-1)}%s |"
			# top of ascii table
			print('')
			print(separator)
			# ascii table data
			if title:
				print(f"{self.spacer}| {title.center(tdata_len)} |")
				print(separator)
			if header:
				rdata = tdata.pop(0)
				data_sub = tuple([rdata[i].center(lens[i]) for i in range(0,cols)])
				print(data_str % data_sub)
				print(separator)
			for rdata in tdata:
				data_sub = tuple([self.to_unicode_str(rdata[i]).ljust(lens[i]) if rdata[i] != None else ''.ljust(lens[i]) for i in range(0,cols)])
				print(data_str % data_sub)
				if linear:
					print(separator)
			if not linear:
				# bottom of ascii table
				print(separator)
			print('')

	# ==================================================
	# EXPORT METHODS
	# ==================================================

	def save_gather(self, value, module, target, method=[], output=True):
		if not output:
			return
		self.debug('Saving data to the gather file...')
		gather_file = os.path.join(self.workspace, 'gather.dat')
		# create the file if one doesn't exist
		if not os.path.exists(gather_file):
			open(gather_file, 'a').close()
			data = {}
		else:
			file =self._is_readable(gather_file)
			try:
				data = json.loads(file.read())
			except ValueError:
				# file is empty or corrupt, nothing to load
				data = {}
		# update data
		if module in data:
			if target in data[module]:
				if method == []:
					data[module][target] = value
				else:
					for i in method:
						if i in data[module][target]:
							data[module][target][i] = value[i]
						else:
							data[module][target].update({i: value[i]})
			else:
				data[module].update({target: value})
		else:
			data.update({module: {target: value}})
		# update gather file
		file = self._is_readable(gather_file, 'w')
		json.dump(data, file, indent=4)
		self.debug(f"{file.name} => Done")

	def json2xml(self, json_obj, line_padding=''):
		result_list = list()

		json_obj_type = type(json_obj)

		if json_obj_type is list:
			for sub_elem in json_obj:
				result_list.append(self.json2xml(sub_elem, line_padding))
			return os.linesep.join(result_list)

		if json_obj_type is dict:
			for tag_name in json_obj:
				sub_obj = json_obj[tag_name]
				tag_name = re.sub(r"[\W]+", '_', tag_name)
				result_list.append(f"{line_padding}\t<{tag_name}>")
				result_list.append(self.json2xml(sub_obj, '\t' + line_padding))
				result_list.append(f"{line_padding}\t</{tag_name}>")

			return f"{os.linesep}{os.linesep.join(result_list)}{os.linesep}"

		return f'\t{line_padding}{json_obj}'

	def json2csv(self, json_obj, separator=';', parent='.'):
		titles = list(json_obj.keys())
		resp = {}
		if isinstance(json_obj[titles[0]], list):
			for title in titles:
				resp[f"{parent}/{title}"] = json_obj[title]
			return resp
		else:
			for title in titles:
				obj = json_obj[title]
				if isinstance(obj, list):
					resp[f"{parent}/{title}"] = obj
				elif isinstance(obj, dict):
					tmp = self.json2csv(obj, separator, parent+'/'+title)
					resp.update(tmp)
			return resp

	def csv2text(self, json_obj, separator=';'):
		get_titles = list(json_obj.keys())
		first = f"{separator.join(get_titles)}\n"
		for tup in range(len(json_obj[max(json_obj, key=len)])):
			line = []
			for atom in get_titles:
				atom = json_obj[atom]
				atom = atom[tup] if tup < len(atom) else False
				if atom:
					line.append(atom)
			first += f"{separator.join(line)}\n"
		first = first[:-1]
		return first

	def exporter(self, datasets, filename, method):
		"""Export the results."""

		# Initialize filename
		if '/' not in filename:
			filename = os.path.join(self.workspace, filename)
			if f'.{method}' not in filename.lower():
				filename = f'{filename}.{method}'
		self.debug(f'Making a report with {method} format and save to the {filename}')
		file = self._is_readable(filename, 'w+')
		if file:
			if method == 'json':
				# Convert json_dict to a JSON styled string
				json_string = json.dumps(datasets, indent=4)
				file.write(json_string)
			elif method == 'csv':
				csv = self.json2csv(datasets)
				text = self.csv2text(csv)
				file.write(text)
			elif method == 'xml':
				text = self.json2xml(datasets)
				file.write(text)
			else:
				# Default method is txt
				json_string = json.dumps(datasets, indent=4)
				json2txt = re.sub(r"[\"']+", '', str(json_string))
				file.write(json2txt)

			file.close()
			return filename
		return False

	# ==================================================
	# ADD METHODS
	# ==================================================

	def _display(self, data, rowcount):
		display = self.alert if rowcount else self.verbose
		for key in sorted(data.keys()):
			display(f"{key.title()}: {data[key]}")
		display(self.ruler*50)

	# ==================================================
	# HISTORY METHODS
	# ==================================================

	def _init_history(self, reborn=False, write=True):
		history = os.path.join(self.workspace, 'history.dat')
		# initialize history file
		if not os.path.exists(history):
			self._is_readable(history,'w').close()
		if write:
			mode = 'a+'
		else:
			mode = 'r'
		self._history_file = self._is_readable(history, mode)
		# Reborn history file
		if reborn:
			self._history_file.truncate()

	def _get_history(self):
		self._init_history(write=False)
		commands = self._history_file.read().split('\n')
		print(self._history_file.read())
		commands = [f'{num}  {name}' for num,name in enumerate(commands) if name]
		return commands

	def _log_commands(self, cmd):
		self._init_history(True)
		if cmd and cmd != 'EOF':
			self._history_file.write(f"\n{cmd}")
			self._history_file.close()
			self._init_history(False)

	# ==================================================
	# OPTIONS METHODS
	# ==================================================

	def register_option(self, name, value, required, description):
		self.options.init_option(
			name=name.lower(),
			value=value,
			required=required,
			description=description)
		# needs to be optimized rather than ran on every register
		self._load_config()

	def _validate_options(self):
		for option in self.options:
			# if value type is bool or int, then we know the options is set
			if not type(self.options[option]) in [bool, int]:
				if self.options.required[option] is True and not self.options[option]:
					raise FrameworkException(
						f"Value required for the '{option.upper()}' option.")
		return

	def _load_config(self):
		config_path = os.path.join(self.workspace, 'config.dat')
		# don't bother loading if a config file doesn't exist
		if os.path.exists(config_path):
			# retrieve saved config data
			config_file = self._is_readable(config_path)
			try:
				config_data = self.config_data = json.loads(config_file.read())
			except ValueError:
				# file is corrupt, nothing to load, exit gracefully
				pass
			else:
				# set option values
				for key in self.options:
					try:
						self.options[key] = config_data[self._modulename][key]
					except KeyError:
						# invalid key, contnue to load valid keys
						continue

	def _save_config(self, name):
		config_path = os.path.join(self.workspace, 'config.dat')
		# create a config file if one doesn't exist
		if not os.path.exists(config_path):
			self._is_readable(config_path, 'a').close()
			config_data = {}
		else:
			# retrieve saved config data
			with open(config_path) as config_file:
				try:
					config_data = json.loads(config_file.read())
				except ValueError:
					# file is empty or corrupt, nothing to load
					config_data = {}
		# create a container for the current module
		if self._modulename not in config_data:
			config_data[self._modulename] = {}
		# set the new option value in the config
		config_data[self._modulename][name] = self.options[name]
		# remove the option if it has been unset
		if config_data[self._modulename][name] is None:
			del config_data[self._modulename][name]
		# remove the module container if it is empty
		if not config_data[self._modulename]:
			del config_data[self._modulename]
		# write the new config data to the config file
		with open(config_path, 'w') as config_file:
			json.dump(config_data, config_file, indent=4)

	# ==================================================
	# REQUEST METHODS
	# ==================================================

	def _print_prepared_request(self, prepared):
		self.debug(f"{'='*25} REQUEST {'='*25}{os.linesep}")
		print(f"url:    {prepared.url}")
		print(f"method: {prepared.method} {prepared.path_url}")
		for k, v in prepared.headers.items():
			print(f"header: {k}: {v}")
		if prepared.body:
			print(f"body: {prepared.body}")

	def _print_response(self, resp):
		self.debug(f"{'='*25} RESPONSE {'='*25}{os.linesep}")
		print(f"status: {resp.status_code} {resp.reason}")
		for k, v in resp.headers.items():
			print(f"header: {k}: {v}")

	def request(self, url, method='GET', **kwargs):
		if '://' not in url:
			url = f'https://{url}'
		# process socket timeout
		kwargs['timeout'] = kwargs.get('timeout') or self._global_options['timeout']
		# process headers
		headers = kwargs.get('headers') or {}
		# set the User-Agent header
		if self._global_options['rand_agent']:
			headers['user-agent'] = rand_uagent.main().get
		else:
			headers['user-agent'] = headers.get('user_agent', False) or self._global_options['agent']
		# normalize capitalization of the User-Agent header
		headers = {k.title(): v for k, v in headers.items()}
		kwargs['headers'] = headers
		# process proxy
		proxy = self._global_options['proxy']
		if proxy:
			proxies = {
				'http': f"http://{proxy}",
				'https': f"http://{proxy}",
			}
			kwargs['proxies'] = proxies
		# disable TLS validation and warning
		kwargs['verify'] = False
		requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
		# send the request
		resp = getattr(requests, method.lower())(url, **kwargs)
		if self._global_options['verbosity'] < 2:
			return resp
		# display request data
		self._print_prepared_request(resp.request)
		# display response data
		self._print_response(resp)
		return resp

	# ==================================================
	# SHOW METHODS
	# ==================================================

	def show_history(self):
		self.do_history('list')

	def show_modules(self, param):
		# process parameter according to type
		if isinstance(param, list):
			modules = param
		elif param:
			modules = [
				x for x in Framework._loaded_modules if x.startswith(param)]
			if not modules:
				self.error('Invalid module category.')
				return
		else:
			modules = Framework._loaded_modules
		if not modules:
			self.error('no modules to display.')
			return
		# display the modules
		last_category = ''
		for module in sorted(modules):
			category = module.split('/')[0]
			if category != last_category:
				# print header
				last_category = category
				self.heading(last_category)
			# print module
			print(f'{self.spacer * 2}{module}')
		print('')

	def show_options(self, options=None):
		'''Lists options'''
		if options is None:
			options = self.options
		if options:
			pattern = f'{self.spacer}%s  %s  %s  %s'
			key_len = len(max(options, key=len))
			if key_len < 4: key_len = 4
			val_len = len(max([self.to_unicode_str(options[x]) for x in options], key=len))
			if val_len < 13: val_len = 13
			print('')
			print(pattern % ('Name'.ljust(key_len), 'Current Value'.ljust(val_len), 'Required', 'Description'))
			print(pattern % (self.ruler*key_len, (self.ruler*13).ljust(val_len), self.ruler*8, self.ruler*11))
			for key in sorted(options):
				value = options[key] if options[key] != None else ''
				reqd = 'no' if options.required[key] is False else 'yes'
				desc = options.description[key]
				print(pattern % (key.ljust(key_len), self.to_unicode_str(value).ljust(val_len), self.to_unicode_str(reqd).ljust(8), desc))
			print('')
		else:
			print(f'{os.linesep}{self.spacer}No options available for this module.{os.linesep}')

	def show_var(self):
		self.do_var('list')

	def _get_show_names(self):
		# Any method beginning with "show_" will be parsed
		# and added as a subcommand for the show command.
		prefix = 'show_'
		return [x[len(prefix):]
				for x in self.get_names() if x.startswith(prefix)]

	# ==================================================
	# COMMAND METHODS
	# ==================================================

	def do_history(self, params):
		'''Manage history of commands'''
		if not params:
			self.help_history()
			return
		params = params.split()
		arg = params.pop(0).lower()
		cmds = self._get_history()
		if arg == 'list':
			if len(cmds) > 50:
				cmds = cmds[:50]
			header = '\nCommands:\n'
			print(header + self.ruler * len(header[2:]))
			for i in cmds:
				print(''.ljust(5) + i)
			print('')
		elif arg == 'clear':
			self._init_history(reborn=True)
		elif (arg == 'from' and params) or arg == "all":
			try:
				if params:
					to = int(params[0])
				else:
					# Show all commands
					to = 0
			except TypeError:
				print('Usage: history from <num>')
			else:
				header = '\nCommands:\n'
				print(header + self.ruler * len(header[2:]))
				# Limit the show commands
				if len(cmds) > to:
					cmds = cmds[to:]
				for i in cmds:
					print(''.ljust(5) + i)
				print('')
		elif arg == 'status':
			print(f'History logger: {self._global_options["history"]}')
		elif arg == 'on':
			self._global_options['history'] = True
		elif arg == 'off':
			self._global_options['history'] = False
		else:
			self.help_history()

	def do_exit(self, params):
		'''Exits the framework'''
		self._exit = 1
		return True

	# alias for exit
	def do_back(self, params):
		'''Exits the current context'''
		return True

	def do_set(self, params):
		'''Sets module options'''
		options = params.split()
		if len(options) < 2:
			self.help_set()
			return
		name = options[0].lower()
		if name in self.options:
			value = ' '.join(options[1:])
			if value[:1] == '$':
				value = self.get_var(value[1:])
			self.options[name] = value
			print(f'{name.upper()} => {value}')
			self._save_config(name)
		else:
			self.error('Invalid option.')

	def do_unset(self, params):
		'''Unsets module options'''
		self.do_set(f'{params} {None}')

	def do_show(self, params):
		'''Shows various framework items'''
		if not params:
			self.help_show()
			return
		_params = params
		params = params.lower().split()
		arg = params[0]
		params = ' '.join(params[1:])
		if arg in self._get_show_names():
			func = getattr(self, "show_" + arg)
			if arg == "modules":
				func(params)
			else:
				func()
		else:
			self.help_show()

	def do_search(self, params):
		'''Searches available modules'''
		if not params:
			self.help_search()
			return
		text = params.split()[0]
		self.output(f"Searching for '{text}'...")
		modules = [x for x in Framework._loaded_modules if text in x]
		if not modules:
			self.error(f"No modules found containing '{text}'.")
		else:
			self.show_modules(modules)

	def do_shell(self, params):
		'''Executes shell commands'''
		if not params:
			self.help_shell()
			return
		proc = subprocess.Popen(params, shell=True, stdout=subprocess.PIPE,
								stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		self.output(f'Command: {params}{os.linesep}')
		stdout = proc.stdout.read()
		stderr = proc.stderr.read()
		if stdout:
			print(f'{Colors.O}{self.to_unicode(stdout)}{Colors.N}', end='')
		if stderr:
			print(f'{Colors.R}{self.to_unicode(stderr)}{Colors.N}', end='')

	def do_resource(self, params=None, code=False):
		'''Executes commands from a resource file'''
		if not params and not code:
			self.help_resource()
			return
		if code:
			print(code)
			sys.stdin = code
			Framework._script = 1
		else:
			if os.path.exists(params):
				sys.stdin = open(params)
				Framework._script = 1
			else:
				self.error(f"Script file '{params}' not found.")

	def do_var(self, params):
		'''Variable define'''
		if not params:
			self.help_var()
			return
		params = params.split()
		arg = params[0].lower()
		if arg[:1] == '$':

			if self.add_var(arg[1:], " ".join(params[1:])):
				self.output(f"Variable '{arg[1:]}' added.")
			else:
				self.output(f"Invalid variable name '{arg[1:]}'.", 'r')
		elif arg == 'list':
			self._list_var()
		elif arg == 'delete':
			if len(params) == 2:
				if params[1] in ["limit", "proxy", "target", "timeout", "agent", "verbosity", "history"]:
					self.error(f"You cannot delete default variable '{params[1]}'.")
				else:
					if self.delete_var(params[1][1:]):
						self.output(f"Var '{params[1]}' deleted.")
					else:
						self.error(f"No such var was found for deletion '{params[1]}'.")
			else:
				print(f"Usage: var delete <name>{os.linesep}")
		else:
			self.help_var()

	def do_record(self, params):
		'''Records commands to a resource file'''
		if not params:
			self.help_record()
			return
		arg = params.lower()
		if arg.split()[0] == 'start':
			if not Framework._record:
				if len(arg.split()) > 1:
					filename = ' '.join(arg.split()[1:])
					if not self._is_readable(filename, 'w'):
						self.output(f'Cannot record commands to \'{filename}\'.')
					else:
						Framework._record = filename
						self.output(f'Recording commands to \'{Framework._record}\'.')
				else: self.help_record()
			else: self.output('Recording is already started.')
		elif arg == 'stop':
			if Framework._record:
				self.output(f'Recording stopped. Commands saved to \'{Framework._record}\'.')
				Framework._record = None
			else: self.output('Recording is already stopped.')
		elif arg == 'status':
			status = 'started' if Framework._record else 'stopped'
			self.output(f'Command recording is {status}.')

	def do_spool(self, params):
		'''Spools output to a file'''
		if not params:
			self.help_spool()
			return
		arg = params.lower()
		if arg.split()[0] == 'start':
			if not Framework._spool:
				if len(arg.split()) > 1:
					filename = ' '.join(arg.split()[1:])
					if not self._is_readable(filename):
						self.output(f"Cannot spool output to \'{filename}\'.")
					else:
						Framework._spool = codecs.open(filename, 'ab', encoding='utf-8')
						self.output(f'Spooling output to \'{Framework._spool.name}\'.')
				else: self.help_spool()
			else: self.output('Spooling is already started.')
		elif arg == 'stop':
			if Framework._spool:
				self.output(f'Spooling stopped. Output saved to \'{Framework._spool.name}\'.')
				Framework._spool = None
			else: self.output('Spooling is already stopped.')
		elif arg == 'status':
			status = 'started' if Framework._spool else 'stopped'
			self.output(f'Output spooling is {status}.')
		else:
			self.help_spool()

	def do_report(self, params):
		'''Get report from the Gathers and save it to the other formats'''
		if not params:
			self.help_report()
			return
		arg = params.lower().split(" ")
		gather_file = os.path.join(self.workspace, "gather.dat")
		if not os.path.exists(gather_file):
			self.alert("No data found.")
			return
		# open gather file
		with open(gather_file) as gf:
			try:
				gather_data = json.loads(gf.read())
			except ValueError:
				self.error("Gather data is incorrect. gather is missed!") 
				return

		if arg[0] == "saved":
			if gather_data:
				for mod in gather_data:
					self.alert(mod)
					for q in gather_data[mod]:
						print(f'\t{q}')
			else:
				self.output('No result found.')
			print('')
			return

		if len(arg) < 3 or len(arg) > 4:
			self.error("Module name not found")
			self.help_report()
			return
		_format = arg[0]
		if _format not in ('json', 'txt', 'xml', 'csv'):
			self.error(f"Format \'{_format}\' doesn't found.")
			return
		mod_name = arg[2].lower()
		# Not supperted csv export
		if mod_name in ('footprint/entry_points',) and _format == 'csv':
			self.error('CSV format doesn\'t support entry_points output data.')
			return
			
		if mod_name in gather_data:
			output = gather_data[mod_name]
		else:
			self.error(f"Module \'{mod_name}\' does not have any data.")
			return

		if len(arg) == 4:
			tar_name = arg[3]
			if tar_name in output:
				output = output[tar_name]
			else:
				self.error(f"Query name \'{tar_name}\' is not found.")
				return

		output_file = os.path.join(self.workspace, arg[1])
		get_export = self.exporter(output, f"{output_file}.{_format}", _format)
		if get_export:
			self.output(f"Report saved at {get_export}")

	def do_load(self, params):
		'''Loads selected module'''
		if not params:
			self.help_load()
			return
		# finds any modules that contain params
		modules = [params] if params in Framework._loaded_modules else [
			x for x in Framework._loaded_modules if params in x]
		# notify the user if none or multiple modules are found
		if len(modules) != 1:
			if not modules:
				self.error('Invalid module name.')
			else:
				self.output(f"Multiple modules match '{params}'.")
				self.show_modules(modules)
			return
		# compensation for stdin being used for scripting and loading
		if Framework._script:
			end_string = sys.stdin.read()
		else:
			end_string = 'EOF'
			Framework._load = 1
		sys.stdin = StringIO(f'load {modules[0]}\n{end_string}')
		return True

	do_use = do_load

	#==================================================
	# VARIABLE METHODS
	#==================================================

	def get_var(self, name):
		self._init_var()
		if name in self.variables:
			return self.variables[name]
		else:
			self.error(f'Variable name \'{name}\' not found. enter `var list`')

	def add_var(self, name, value):
		if re.search(r'[a-zA-Z_][a-zA-Z0-9_]*', name):
			self.variables[name] = value
			self._init_var(self.variables)
			return True

	def delete_var(self, name):
		if name in self.variables:
			self.variables.pop(name)
			self._init_var(self.variables)
			return True

	def _list_var(self):
		self._init_var()
		variables = self.variables.items()
		tdata = sorted(variables)
		self.table(tdata, header=['Name', 'Value'])

	def _init_var(self, vals=None):
		vars_path = os.path.join(self.workspace, 'var.dat')
		# create a var file if one doesn't exist
		if os.path.exists(vars_path):
			v = open(vars_path, 'a')
			o = open(vars_path, 'r')
			r = o.read() or '{}'
			o.close()
		else:
			r = '{}'
			v = open(vars_path, 'w')

		try:
			vars_data = json.loads(r)
		except ValueError:
			vars_data = {}

		if vals:
			vars_data = vals
		else:
			# add default variables if doesn't exist
			if 'agent' not in vars_data:
				for opt in self._global_options.keys():
					if opt not in vars_data:
						vars_data[opt] = self._global_options[opt]

		self.variables = vars_data
		open(vars_path, 'w').close()
		# Update var.dat
		json.dump(self.variables, v, indent=4)

	# ==================================================
	# HELP METHODS
	# ==================================================

	def help_history(self):
		print(getattr(self, 'do_history').__doc__)
		print(f'{os.linesep}Usage: history [list|from <num>|off|on|status|all]')
		print('\thistory list\tshow 50 first commands')
		print('\thistory from <num>\tShow the last <num> commands')
		print('\thistory off\toff the history logger')
		print('\thistory on\ton the history logger')
		print('\thistory status\tfor show history status')
		print('\thistory all\tshow all of commands')
		print(f'Note: If \'from <num>\' is not set, only the last 50 commands will be shown.{os.linesep}')

	def help_load(self):
		print(getattr(self, 'do_load').__doc__)
		print(f'{os.linesep}Usage: [load|use] <module>{os.linesep}')

	help_use = help_load

	def help_resource(self):
		print(getattr(self, 'do_resource').__doc__)
		print(f'{os.linesep}Usage: resource <filename>{os.linesep}')

	def help_var(self):
		print(getattr(self, 'do_var').__doc__)
		print(f'{os.linesep}Usage: var <$name> <value> || var [delete] <name> || var [list]{os.linesep}')


	def help_record(self):
		print(getattr(self, 'do_record').__doc__)
		print(f'{os.linesep}Usage: record [start <filename>|stop|status]{os.linesep}')

	def help_spool(self):
		print(getattr(self, 'do_spool').__doc__)
		print(f'{os.linesep}Usage: spool [start <filename>|stop|status]{os.linesep}')

	def help_report(self):
		print(getattr(self, 'do_report').__doc__)
		print(f'{os.linesep}Usage    : report [<format> <filename> [<module_name> or <module_name> <query(hostname,domain name, keywords,etc)>]]')
		print('or       : report [saved] => for show queries')
		print('Example  : report json pdf_docs(without extention) osint/docs_search company.com')
		print(f'         : report xml pdf_docs(without extention) osint/docs_search')
		print(f'formats  : xml,json,csv and txt{os.linesep}')

	def help_search(self):
		print(getattr(self, "do_search").__doc__)
		print(f'{os.linesep}Usage: search <string>{os.linesep}')

	def help_set(self):
		print(getattr(self, "do_set").__doc__)
		print(f'{os.linesep}Usage: set <option> <value>')
		self.show_options()

	def help_unset(self):
		print(getattr(self, "do_unset").__doc__)
		print(f'{os.linesep}Usage: unset <option>')
		self.show_options()

	def help_shell(self):
		print(getattr(self, "do_shell").__doc__)
		print(f'{os.linesep}Usage: [shell|!] <command>')
		print(f'   or: just type a command at the prompt.{os.linesep}')

	def help_show(self):
		options = sorted(self._get_show_names())
		print(getattr(self, "do_show").__doc__)
		print(f'{os.linesep}Usage: show [{"|".join(options)}]{os.linesep}')

	# ==================================================
	# COMPLETE METHODS
	# ==================================================

	def complete_load(self, text, *ignored):
		return [x for x in Framework._loaded_modules if x.startswith(text)]

	complete_use = complete_load

	def complete_set(self, text, *ignored):
		return [x.upper()
				for x in self.options if x.upper().startswith(text.upper())]

	complete_unset = complete_set

	def complete_record(self, text, *ignored):
		return [x for x in ['start', 'stop', 'status'] if x.startswith(text)]

	complete_spool = complete_record

	def complete_show(self, text, line, *ignored):
		args = line.split()
		if len(args) > 1 and args[1].lower() == 'modules':
			if len(args) > 2:
				return [
					x for x in Framework._loaded_modules if x.startswith(
						args[2])]
			else:
				return [x for x in Framework._loaded_modules]
		options = sorted(self._get_show_names())
		return [x for x in options if x.startswith(text)]

	def complete_options(self, text, line, *ignored):
		arg, params = self._parse_params(line.split(' ', 1)[1])
		subs = self._parse_subcommands('options')
		if arg in subs:
			return getattr(self, '_complete_options_'+arg)(text, params)
		return [sub for sub in subs if sub.startswith(text)]
