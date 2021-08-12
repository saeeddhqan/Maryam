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

import cmd
import json
import os
import re
import subprocess
import sys
import traceback
import requests
from .util.helpers import rand_uagent
from io import StringIO
from textwrap import wrap

class FrameworkException(Exception):
	def __init__(self, message):
		Exception.__init__(self, message)

class Colors:
	N = '\033[m'  # native
	R = '\033[91m'  # red
	G = '\033[92m'  # green
	O = '\033[93m'  # orange
	B = '\033[94m'  # blue
	P = '\033[95m'  # purple
	C = '\033[0;1;36m'  # cyan
	Y = '\u001b[38;5;226m'

class core(cmd.Cmd):
	prompt = '>>>'
	_global_options = {}
	_global_options_ = {}
	_loaded_modules = {}
	_cat_module_names = {}
	_module_names = []
	_error_stack = []
	workspace = ''
	Colors = Colors

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.ruler = '-'
		self.spacer = '  '
		self.nohelp = f"{Colors.R}[!] No help on %s{Colors.N}"
		self.do_help.__func__.__doc__ = 'Displays this menu'
		self.doc_header = 'Commands (type [help|?] <topic>):'
		self._exit = 0

	# ////////////////////////////////
	#             OVERRIDE          //
	# ////////////////////////////////

	def default(self, line):
		self.do_shell(line)

	def emptyline(self):
		return 0

	def precmd(self, line):
		line = self.to_str(line)
		return line

	def onecmd(self, line):
		line = self.to_str(line)
		cmd, arg, line = self.parseline(line)
		if not line:
			return self.emptyline()
		if line == 'EOF':
			sys.stdin = sys.__stdin__
			core._script = 0
			core._load = 0
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

	def print_topics(self, header, cmds, cmdlen, maxcol):
		if cmds:
			self.stdout.write(f"{header}{os.linesep}")
			if self.ruler:
				self.stdout.write(f"{self.ruler * len(header)}{os.linesep}")
			for cmd in cmds:
				self.stdout.write(f"{cmd.ljust(15)} {getattr(self, 'do_' + cmd).__doc__}{os.linesep}")
			self.stdout.write(os.linesep)

	# ////////////////////////////////
	#           SUPPORT             //
	# ////////////////////////////////

	def to_str(self, obj):
		if not isinstance(obj, str):
			if isinstance(obj, bytes):
				obj = str(obj, 'utf-8')
			else:
				obj = str(obj)
		return obj

	def _is_readable(self, filename, flag='r'):
		try:
			return open(filename, flag)
		except IOError as e:
			self.error('IOError: ' + str(e))
			return False

	def _check_version(self):
		if not self._global_options.get('update_check'):
			return
		self.debug('Checking version...')
		pattern = r"__VERSION__\s+=\s+'(\d+\.\d+\.\d+[^']*)'"
		remote = 0
		local = 0
		try:
			remote = re.search(pattern, self.request(\
				'https://raw.githubusercontent.com/saeeddhqan/maryam/master/maryam/__main__.py').text).group(1)
			local = self.__version__[1:]
		except Exception as e:
			self.error(f"Version check failed ({type(e).__name__}).")
		if remote != local:
			self.alert('Your version of Maryam does not match the latest release')
			self.output(f"Remote version:  {remote}")
			self.output(f"Local version:   {local}")

	# ////////////////////////////////
	#           OUTPUT              //
	# ////////////////////////////////

	def print_exception(self, line='', where='nil', which_func='nil'):
		stack_list = [x.strip() for x in traceback.format_exc().strip().splitlines()]
		message = stack_list[-1]
		if self._global_options['verbosity'] == 0:
			return
		elif self._global_options['verbosity'] == 1:
			line = ' '.join([x for x in [message, line] if x])
			self.error(stack_list[-3], where, which_func)
			self.error(line, where, which_func)
		elif self._global_options['verbosity'] >= 2:
			print(f"{Colors.R}{'-'*60}")
			traceback.print_exc()
			print(f"{'-'*60}{Colors.N}")

	def textwrapping(self, prefix, string, size=80):
		size -= len(prefix)
		if isinstance(string, bytes):
			string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
			if size % 2:
				size -= 1
		return '\n'.join([prefix + line for line in wrap(string, size)])

	def error(self, line, where='nil', which_func='nil'):
		'''Formats and presents errors.'''
		if not re.search(r'[.,;!?]$', line):
			line += '.'
		line = line[:1].upper() + line[1:]
		error = f"[{where}:{which_func}] {line}"
		print(f"{Colors.O}[!] {error}{Colors.N}")
		if error not in self._error_stack:
			self._error_stack.append(error)

	def output(self, line, color='N', end='', prep='', linesep=True, prefix='[*]'):
		'''Formats and presents normal output.'''
		line = self.to_str(line)
		line = f'{prep}{Colors.B}{prefix}{getattr(Colors, color.upper())} {line}\033[m'
		if not line.endswith(os.linesep) and linesep:
			line += os.linesep
		print(line, end=end, flush=True)

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
			line = f'{Colors.C}[~] {Colors.N}{self.to_str(line)}'
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
		tdata = list(data)
		if header:
			tdata.insert(0, header)
		if len(set([len(x) for x in tdata])) > 1:
			raise FrameworkException('Row lengths not consistent.')
		lens = []
		cols = len(tdata[0])
		for i in range(0, cols):
			lens.append(len(max([self.to_str(x[i]) if x[i] != None else '' for x in tdata], key=len)))
		title_len = len(title)
		tdata_len = sum(lens) + (3*(cols-1))
		diff = title_len - tdata_len
		if diff > 0:
			diff_per = diff // cols
			lens = [x+diff_per for x in lens]
			diff_mod = diff % cols
			for x in range(0, diff_mod):
				lens[x] += 1
		if len(tdata) > 0:
			separator_str = f"{self.spacer}+{sep}{f'%s{sep*3}'*(cols-1)}%s{sep}+"
			separator_sub = tuple([sep*x for x in lens])
			separator = separator_str % separator_sub
			data_str = f"{self.spacer}| {'%s | '*(cols-1)}%s |"
			print('')
			print(separator)
			if title:
				print(f"{self.spacer}| {title.center(tdata_len)} |")
				print(separator)
			if header:
				rdata = tdata.pop(0)
				data_sub = tuple([rdata[i].center(lens[i]) for i in range(0,cols)])
				print(data_str % data_sub)
				print(separator)
			for rdata in tdata:
				data_sub = tuple([self.to_str(rdata[i]).ljust(lens[i]) if rdata[i] != None else ''.ljust(lens[i]) for i in range(0,cols)])
				print(data_str % data_sub)
				if linear:
					print(separator)
			if not linear:
				print(separator)
			print('')

	# ////////////////////////////////
	#             EXPORT            //
	# ////////////////////////////////

	def save_gather(self, value, module, target, method=None, output=True):
		if method is None:
			method = []
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

		if isinstance(json_obj, list):
			for sub_elem in json_obj:
				result_list.append(self.json2xml(sub_elem, line_padding))
			return os.linesep.join(result_list)

		if isinstance(json_obj, dict):
			for tag_name in json_obj:
				sub_obj = json_obj[tag_name]
				tag_name = re.sub(r"[\W]+", '_', tag_name)
				result_list.append(f"{line_padding}\t<{tag_name}>")
				result_list.append(self.json2xml(sub_obj, '\t' + line_padding).replace('&','&amp;'))
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
				text = f'<?xml version="1.0" encoding="UTF-8"?>\n{text}'
				file.write(text)
			else:
				# Default method is txt
				json_string = json.dumps(datasets, indent=4)
				json2txt = re.sub(r"[\"']+", '', str(json_string))
				file.write(json2txt)

			file.close()
			return filename
		return False

	# ////////////////////////////////
	#           ERRORS   			//
	# ////////////////////////////////

	def _reset_error_stack(self):
		self._error_stack.clear()

	# ////////////////////////////////
	#           OPTIONS 			//
	# ////////////////////////////////

	def _load_config(self):
		config_path = os.path.join(self.workspace, 'config.dat')

		if os.path.exists(config_path):
			config_file = self._is_readable(config_path)
			try:
				config_data = self.config_data = json.loads(config_file.read())
			except ValueError:
				pass
			else:
				for key in self._global_options:
					try:
						self._global_options[key] = config_data[key]
					except KeyError:
						continue

	def _save_config(self, name):
		config_path = os.path.join(self.workspace, 'config.dat')
		if not os.path.exists(config_path):
			self._is_readable(config_path, 'a').close()
			config_data = {}
		else:
			with open(config_path) as config_file:
				try:
					config_data = json.loads(config_file.read())
				except ValueError:
					config_data = {}


		config_data[name] = self._global_options[name]

		if config_data[name] is None:
			del config_data[name]

		with open(config_path, 'w') as config_file:
			json.dump(config_data, config_file, indent=4)

	# ////////////////////////////////
	#           request             //
	# ////////////////////////////////

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
			url = f"{self._global_options['protocol']}://{url}"
		kwargs['timeout'] = kwargs.get('timeout') or self._global_options['timeout']
		headers = kwargs.get('headers') or {}
		if self._global_options['rand_agent']:
			headers['user-agent'] = rand_uagent.main().get
		else:
			headers['user-agent'] = headers.get('user-agent', False) or self._global_options['agent']
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
		kwargs['verify'] = False
		requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
		resp = getattr(requests, method.lower())(url, **kwargs)
		if self._global_options['verbosity'] < 2:
			return resp
		self._print_prepared_request(resp.request)
		self._print_response(resp)
		return resp

	# ////////////////////////////////
	#           SHOW                //
	# ////////////////////////////////

	def show_modules(self, param):
		for section in core._cat_module_names:
			self.heading(section)
			for module in core._cat_module_names[section]:
				print(f'{self.spacer * 2}{module}')
		print('')

	def show_options(self, options=None):
		'''Lists options'''
		if options is None:
			options = self._global_options_
		if options:
			pattern = f'{self.spacer}%s  %s  %s  %s'
			key_len = len(max(options, key=len))
			if key_len < 4:
				key_len = 4
			val_len = len(max([self.to_str(self._global_options[x]) for x in options], key=len))
			if val_len < 13:
				val_len = 13
			print('')
			print(pattern % ('Name'.ljust(key_len), 'Current Value'.ljust(val_len), 'Required', 'Description'))
			print(pattern % (self.ruler*key_len, (self.ruler*13).ljust(val_len), self.ruler*8, self.ruler*11))
			for key in sorted(options):
				option = options[key]
				value = self._global_options[key] if self._global_options[key] != None else ''
				reqd = 'no' if not option[2] else 'yes'
				desc = option[3]
				print(pattern % (key.ljust(key_len), \
					self.to_str(value).ljust(val_len), \
					self.to_str(reqd).ljust(8), desc.title()))
			print('')
		else:
			print(f'{os.linesep}{self.spacer}No options available for this module.{os.linesep}')

	def _get_show_names(self):
		prefix = 'show_'
		return [x[len(prefix):]
				for x in self.get_names() if x.startswith(prefix)]

	# /////////////////////
	#         DEV       //
	# ////////////////////

	def _dev_install_requirements(self, reqs):
		'''Install requirements with pip.'''
		well = []
		for req in reqs:
			well.append(not bool(self.do_shell(f"{sys.executable} -m pip install {req}")))
		return all(well)

	# ////////////////////////////////
	#           COMMANDS            //
	# ////////////////////////////////

	def do_exit(self, params):
		'''Exits the framework'''
		self._exit = 1
		return True

	def do_set(self, params):
		'''Sets module options'''
		options = params.split()
		if len(options) < 2:
			self.help_set()
			return
		name = options[0].lower()
		if name in self._global_options:
			value = ' '.join(options[1:])
			if self._global_options_[name][2] and (not value or value == 'None'):
				print(f"{name} is a required option.")
				return
			if isinstance(self._global_options[name], bool):
				if value.lower() in ('true', 'yes', 'on'):
					value = True
				elif value.lower() in ('false', 'no', 'off'):
					value = False
				else:
					print(f"{name} is a bool option. got {value}")
					return
				self._global_options[name] = value
			elif isinstance(self._global_options[name], int):
				if value.isdigit():
					self._global_options[name] = int(value)
				else:
					print(f"{name} is an int option. got {value}")
					return
			else:
				if value == 'None':
					value = None
				self._global_options[name] = value
			print(f"{name.upper()} => {value}")
			self._save_config(name)
		else:
			self.error('Invalid option.')

	def do_unset(self, params):
		'''Unsets module options'''
		self.do_set(f"{params} {None}")

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
			func = getattr(self, f"show_{arg}")
			if arg == 'modules':
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
		modules = [x for x in core._loaded_modules if text in x]
		if not modules:
			self.error(f"No modules found containing '{text}'.")
		else:
			for section in core._cat_module_names:
				self.heading(section)
				for mod in core._cat_module_names[section]:
					if text in mod:
						self.output(f"\tFound '{text}' under {section}: {mod}", prefix='')

	def do_shell(self, params):
		'''Executes shell commands'''
		if not params:
			self.help_shell()
			return
		proc = subprocess.Popen(params, shell=True, stdout=subprocess.PIPE,
								stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		self.output(f"Command: {params}{os.linesep}")
		stdout = proc.stdout.read()
		stderr = proc.stderr.read()
		if stdout:
			print(f"{Colors.O}{self.to_str(stdout)}{Colors.N}", end='')
		if stderr:
			print(f"{Colors.R}{self.to_str(stderr)}{Colors.N}", end='')
		return stderr

	def do_report(self, params):
		'''Get report from the Gathers and save it to the other formats'''
		temp_dic={}
		if not params:
			self.help_report()
			return
		arg = params.lower().split(' ')
		gather_file = os.path.join(self.workspace, 'gather.dat')
		if not os.path.exists(gather_file):
			self.alert('No data found.')
			return
		# open gather file
		with open(gather_file) as gf:
			try:
				gather_data = json.loads(gf.read())
			except ValueError:
				self.error('Gather data is incorrect. Gather is missed!') 
				return

		if arg[0] == 'saved':
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
			self.error(f"Format '{_format}' doesn't found.")
			return
		mod_name = arg[2].lower()
		# Not supperted csv export
		if mod_name in ('footprint/entry_points',) and _format == 'csv':
			self.error('CSV format does not support entry_points output data.')
			return
			
		if mod_name in gather_data:
			output = gather_data[mod_name]
		else:
			self.error(f"Module '{mod_name}' does not have any data.")
			return

		if len(arg) == 4:
			tar_name = arg[3]
			if tar_name in output:
				temp_dic[tar_name] = output[tar_name]
			else:
				self.error(f"Query name '{tar_name}' is not found.")
				return

		else:
			temp_dic[mod_name]=output

		output_file = os.path.join(self.workspace, arg[1])
		get_export = self.exporter(temp_dic, f"{output_file}.{_format}", _format)
		if get_export:
			self.output(f"Report saved at {get_export}")
	
	def do_update(self, params):
		'''Update modules via module name'''
		if not params:
			self.help_update()
			return
		check = False
		args = params.lower().split()
		if len(args) < 2 or args[0] not in ('module', 'check'):
			self.help_update()
			return

		if args[0] == 'check':
			check = True

		# Means all of modules
		if args[1] == '*':
			modules = self._module_names
		else:
			modules = args[1:]
		for module in modules:
			self.heading(module)
			if module not in self._loaded_modules:
				self.output(f"Module name {module} does not exist.")
				continue
			mod = self._loaded_modules[module]
			file = mod.__file__
			mod_version = mod.meta['version']
			url = f"https://raw.githubusercontent.com/saeeddhqan/Maryam/master/maryam/modules/{'/'.join(file.split('/')[-2:])}"
			text = self.request(url).text
			mod_remote_version = re.search(r"'version'\s*:\s*'([\d\.]+)'\s*,", text)
			if not mod_remote_version:
				self.output(f"Update/check failed ({e}).", prep='\t')
			else:
				mod_remote_version = mod_remote_version.group(1)
				if max(mod_version, mod_remote_version) == mod_remote_version\
					and mod_version != mod_remote_version:
					self.output(f"Remote version: {mod_remote_version}", prep='\t')
					self.output(f"Local version: {mod_version}", prep='\t')
					if not check:
						fopen = self._is_readable(file, 'w')
						if fopen:
							fopen.write(text)
							fopen.close()
							self.output(f"{module} has been updated to {mod_remote_version}.", prep='\t')
						else:
							self.output(f"Update/check failed.", prep='\t')
				else:
					self.output(f"{module} is up to date.", prep='\t')
		self.do_reload()

	# ////////////////////////////////
	#             HELP              //
	# ////////////////////////////////

	def help_report(self):
		print(getattr(self, 'do_report').__doc__)
		print(f'{os.linesep}Usage: report [<format> <filename> [<module_name> or <module_name> <query(hostname,domain name, keywords,etc)>]]')
		print('or       : report [saved] => for show queries')
		print('Examples : report json pdf_docs(without suffix) osint/docs_search company.com')
		print('           report xml pdf_docs(without suffix) osint/docs_search')
		print(f'Formats : xml,json,csv and txt{os.linesep}')

	def help_search(self):
		print(getattr(self, 'do_search').__doc__)
		print(f'{os.linesep}Usage: search <string>{os.linesep}')

	def help_set(self):
		print(getattr(self, 'do_set').__doc__)
		print(f'{os.linesep}Usage: set <option> <value>')
		self.show_options()

	def help_unset(self):
		print(getattr(self, 'do_unset').__doc__)
		print(f'{os.linesep}Usage: unset <option>')
		self.show_options()

	def help_shell(self):
		print(getattr(self, 'do_shell').__doc__)
		print(f"{os.linesep}Usage: [shell|!] <command>")
		print(f"\tor just type a command at the prompt.{os.linesep}")

	def help_show(self):
		options = sorted(self._get_show_names())
		print(getattr(self, 'do_show').__doc__)
		print(f"{os.linesep}Usage: show [{'|'.join(options)}]{os.linesep}")

	def help_update(self):
		print(getattr(self, 'do_update').__doc__)
		print(f"{os.linesep}Usage: update [module|check] <modules or * for all modules>")
		print(f"update check dns_search email_search")
		print(f"update module *")
		print(f"update check *")

	# ////////////////////////////////
	#         AUTOCOMPLETE          //
	# ////////////////////////////////

	def complete_set(self, text, line, begidx, endidx):
		return [x.upper()
				for x in self._global_options if x.upper().startswith(text.upper())]

	complete_unset = complete_set

	def complete_update(self, text, line, begidx, endidx):
		return [x for x in ['check', 'module'] if x.startswith(text.lower())]

	def complete_dev(self, text, line, begidx, endidx):
		return [x for x in ['extension', 'package'] if x.startswith(text.lower())]

	def complete_package(self, text, line, begidx, endidx):
		return [x for x in ['extension', 'repo'] if x.startswith(text.lower())]

	def complete_workspace(self, text, line, begidx, endidx):
		return [x for x in ['add', 'list', 'select'] if x.startswith(text.lower())]

	def complete_show(self, text, line, begidx, endidx):
		options = sorted(self._get_show_names())
		return [x for x in options if x.startswith(text)]
