# -*- coding: u8 -*-
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
# Based on the Recon-ng: https://github.com/lanmaster53/recon-ng

from __future__ import print_function
import cmd
import codecs
import json
import os
import re
import subprocess
import sys
import signal
import traceback
import time
import argparse
from multiprocessing import Process
from core.util import request
try:
	from StringIO import StringIO
except (NameError, ImportError):
	from io import StringIO
# =================================================
# SUPPORT CLASSES
# =================================================


class FrameworkException(Exception):
	pass

class Colors(object):
	N = '\033[m'  # native
	R = '\033[31m'  # red
	G = '\033[32m'  # green
	O = '\033[33m'  # orange
	B = '\033[34m'  # blue
	P = '\033[35m'  # purple
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
		return {"true": True, "false": False}[value.lower()]

	def _autoconvert(self, value):
		if value in (None, True, False):
			return value
		elif (isinstance(value, str)) and value.lower() in ("none", '\'\'', '\"\"'):
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
	_history_file =''

	def __init__(self, params):
		cmd.Cmd.__init__(self)
		self._modulename = params
		self.ruler = '-'
		self.spacer = '  '
		self.time_format = "%Y-%m-%d %H:%M:%S"
		self.nohelp = "%s[!] No help on %%s%s" % (Colors.R, Colors.N)
		self.do_help.__func__.__doc__ = '''Displays this menu'''
		self.doc_header = "Commands (type [help|?] <topic>):"
		self.rpc_cache = []
		self._exit = 0
		self.module_args = []
	
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
			print('%s' % (line))
		if Framework._record:
			recorder = codecs.open(Framework._record, 'ab', encoding="utf-8")
			recorder.write('%s\n' % line)
			recorder.flush()
			recorder.close()
		if Framework._spool:
			Framework._spool.write("%s%s\n" % (self.prompt, line))
			Framework._spool.flush()
		return line

	def onecmd(self, line):
		line = self.to_unicode(line)
		# Log commant into the history file if 'history' is true
		if self._global_options["history"]:
			self._log_commands(line)
		cmd, arg, line = self.parseline(line)
		if not line:
			return self.emptyline()
		if line == "EOF":
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
				return self.run_tool(cmd, arg)
			else:
				try:
					func = getattr(self, "do_" + cmd)
				except AttributeError:
					return self.default(line)
				return func(arg)

	# make help menu more attractive
	def print_topics(self, header, cmds, cmdlen, maxcol):
		if cmds:
			self.stdout.write("%s\n" % str(header))
			if self.ruler:
				self.stdout.write("%s\n" % str(self.ruler * len(header)))
			for cmd in cmds:
				self.stdout.write("%s %s\n" % (
					cmd.ljust(15), getattr(self, "do_" + cmd).__doc__))
			self.stdout.write('\n')

	# ==================================================
	# SUPPORT METHODS
	# ==================================================

	def to_unicode(self, obj, encoding="utf-8"):
		# checks if obj is a string and converts if not
		try:
			if not isinstance(obj, basestring):
				obj = str(obj)

			if not isinstance(obj, unicode):
				obj = unicode(obj, encoding)
			return obj
		except NameError:
			if isinstance(obj, bytes):
				obj = str(obj, encoding)
			else:
				obj = str(obj)
			return obj

	def _is_readable(self, filename, flag="r"):
		try:
			with open(filename, flag) as fp:
				return fp
		except IOError as e:
			self.error("IOError: " + str(e))
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

	def save_gather(self, value, module, target, method=[], output=True):
		if not output:return
		gather_file = os.path.join(self.workspace, "gather.dat")
		# create the file if one doesn't exist
		if not os.path.exists(gather_file):
			open(gather_file, 'a')
			data = {}
		else:
			with open(gather_file) as file:
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
							data[module][target].update({i : value[i]})
			else:
				data[module].update({target : value})
		else:
			data.update({module : {target : value}})
		# update gather file
		with open(gather_file, 'w') as file:
			json.dump(data, file, indent=4)

	def json2xml(self, json_obj, line_padding=""):
		result_list = list()

		json_obj_type = type(json_obj)

		if json_obj_type is list:
			for sub_elem in json_obj:
				result_list.append(self.json2xml(sub_elem, line_padding))

			return "\n".join(result_list)

		if json_obj_type is dict:
			for tag_name in json_obj:
				sub_obj = json_obj[tag_name]
				result_list.append("%s<%s>" % (line_padding, tag_name))
				result_list.append(self.json2xml(sub_obj, "\t" + line_padding))
				result_list.append("%s</%s>" % (line_padding, tag_name))

			return "\n".join(result_list)

		return "%s%s" % (line_padding, json_obj)

	def json2txt(self, json_obj, line_padding=""):
		result_list = list()

		json_obj_type = type(json_obj)

		if json_obj_type is list:
			for sub_elem in json_obj:
				result_list.append(self.json2txt(sub_elem, line_padding))

			return "\n".join(result_list)

		if json_obj_type is dict:
			for tag_name in json_obj:
				sub_obj = json_obj[tag_name]
				result_list.append("%s" %tag_name)
				result_list.append(self.json2txt(sub_obj, "\t" + line_padding))

			return "\n".join(result_list)

		return "%s%s" % (line_padding, json_obj)

	def json_output(self, filename, value):
		file = os.path.join(self.workspace, filename)
		try:
			with open(file, 'w') as f:
				json.dump(value, f, indent=4) 
			return True
		except Exception:
			self.print_exception()

		return False

	def xml_output(self, filename, value):
		value = self.json2xml(value)
		try:
			with open(filename, 'w') as f:
				f.write(value)
			return True
		except Exception:
			self.print_exception()

		return False

	def txt_output(self, filename, value):
		value = self.json2txt(value)
		try:
			with open(filename, 'w') as f:
				f.write(value)
			return True
		except Exception:
			self.print_exception()

		return False

	def print_exception(self, line=''):
		stack_list = [x.strip()
					  for x in traceback.format_exc().strip().splitlines()]
		line = ' '.join([x for x in [stack_list[-1], line] if x])
		if self._global_options["verbosity"] == 1:
			if len(stack_list) > 3:
				line = os.linesep.join((stack_list[-1], stack_list[-3]))
		elif self._global_options["verbosity"] == 2:
			print('%s%s' % (Colors.R, '-' * 60))
			traceback.print_exc()
			print('%s%s' % ('-' * 60, Colors.N))
		self.error(line)

	def error(self, line):
		'''Formats and presents errors.'''
		# print(tuple(line))
		if not re.search(r'[.,;!?]$', line):
			line += '.'
		line = line[:1].upper() + line[1:]
		print("%s[!] %s%s" % (Colors.R, self.to_unicode(line), Colors.N))

	def output(self, line, color='N'):
		'''Formats and presents normal output.'''
		line = self.to_unicode(line)
		print("%s[*]%s %s\033[m" % (Colors.B, getattr(Colors, color.upper()), line))

	def alert(self, line):
		'''Formats and presents important output.'''
		print("%s[*]%s %s" % (Colors.G, Colors.N, self.to_unicode(line)))

	def verbose(self, line, color='N'):
		'''Formats and presents output if in verbose mode.'''
		if self._global_options["verbosity"] >= 1:
			self.output(line, color)

	def debug(self, line):
		'''Formats and presents output if in debug mode (very verbose).'''
		if self._global_options["verbosity"] >= 2:
			self.output(line)

	def heading(self, line, level=1):
		'''Formats and presents styled header text'''
		line = self.to_unicode(line)
		print('')
		if level == 0:
			print(self.ruler * len(line))
			print(line.upper())
			print(self.ruler * len(line))
		if level == 1:
			print("%s%s" % (self.spacer, line.title()))
			print("%s%s" % (self.spacer, self.ruler * len(line)))

	def table(self, data, header, title=''):
		'''Accepts a list of rows and outputs a table.'''
		tdata = list(data)
		if header:
			tdata.insert(0, header)
		if len(set([len(x) for x in tdata])) > 1:
			raise FrameworkException('Row lengths not consistent.')
		lens = []
		cols = len(tdata[0])
		# create a list of max widths for each column
		for i in range(0,cols):
			lens.append(len(max([self.to_unicode(x[i]) if x[i] != None else '' for x in tdata], key=len)))
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
			separator_str = '%s+-%s%%s-+' % (self.spacer, '%s---'*(cols-1))
			separator_sub = tuple(['-'*x for x in lens])
			separator = separator_str % separator_sub
			data_str = '%s| %s%%s |' % (self.spacer, '%s | '*(cols-1))
			# top of ascii table
			print('')
			print(separator)
			# ascii table data
			if title:
				print('%s| %s |' % (self.spacer, title.center(tdata_len)))
				print(separator)
			if header:
				rdata = tdata.pop(0)
				data_sub = tuple([rdata[i].center(lens[i]) for i in range(0,cols)])
				print(data_str % data_sub)
				print(separator)
			for rdata in tdata:
				data_sub = tuple([self.to_unicode(rdata[i]).ljust(lens[i]) if rdata[i] != None else ''.ljust(lens[i]) for i in range(0,cols)])
				print(data_str % data_sub)
			# bottom of ascii table
			print(separator)
			print('')

	# ==================================================
	# ADD METHODS
	# ==================================================

	def _display(self, data, rowcount, pattern=None, keys=None):
		display = self.alert if rowcount else self.verbose
		if pattern and keys:
			values = tuple([data[key] or "<blank>" for key in keys])
			display(pattern % values)
		else:
			for key in sorted(data.keys()):
				display("%s: %s" % (key.title(), data[key]))
			display(self.rutooller * 50)

	# ==================================================
	# HISTORY METHODS
	# ==================================================

	def _init_history(self, reborn=False):
		history = os.path.join(self.workspace, "history.dat")
		# initialize history file
		if not os.path.exists(history):
			self._history_file = open(history, 'w')
		else:
			self._history_file = open(history, 'a+')
		# Reborn history file
		if reborn:self._history_file.truncate()

	def _get_history(self):
		self._init_history()
		commands = self._history_file.read().split("\n")
		commands = ["%d  %s" %(num,name) for num,name in enumerate(commands) if name]
		return commands

	def _log_commands(self, cmd):
		if cmd and cmd != "EOF":
			self._history_file.write("\n%s" %cmd)
			self._init_history()

	# ==================================================
	# OPTIONS METHODS
	# ==================================================

	def opt_proc(self, tool_name, args=None, output=None):
		mod = self._loaded_modules[self._module_names[tool_name]]
		meta = mod.meta
		opts = meta["options"]
		description = '%s(%s) - \tdescription: %s\n' % (tool_name, meta["author"], meta["description"])
		parser = argparse.ArgumentParser(prog=tool_name, description=description, version=meta["version"])
		for option in opts:
			try:
				name, val, req, desc, op, act = option
			except ValueError as e:
				self.error("%sCodeError: options is too short. need more than %d option" % (tool_name, len(option)))
				return
			name = "--%s" % name if not name.startswith("-") else name
			try:
				parser.add_argument(op, name, help=desc, dest=name, default=val, action=act, required=req)
			except argparse.ArgumentError as e:
				self.error("ModuleException: %s" % e)


		# Initialize help menu
		format_help = parser.format_help()
		if "sources" in meta:
			format_help += "\nSources:\n\t%s"%("\n\t".join(meta["sources"]))
		if "examples" in meta:
			format_help += "\nExamples:\n\t%s"%("\n\t".join(meta["examples"]))

		# If args is nothing
		if not args:
			print(format_help)
		else:
			# Initialite args
			if isinstance(args, unicode):
				args = args.split(" ")
			args = parser.parse_args(args)
			args = vars(args)
			# Set options
			for option in args:
				mod.options[option[2:]] = args[option]
			# Run the tool
			spool_flag = 0
			try:
				if output:
					output = "start " + output
					self.do_spool(output)
					spool_flag = 1
				mod._validate_options()
				mod.module_pre()
				mod.module_run()
				mod.module_post()
			except KeyboardInterrupt:
				return
			except Exception:
				self.print_exception()
			finally:
				if spool_flag:
					self.do_spool("stop")


	def run_tool(self, name, args=None):
		p = Process(target=self.opt_proc, args=(name, args))
		try:
			p.start()
			p.join()
		except KeyboardInterrupt:
			return
		except Exception:
			self.print_exception()

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
						"Value required for the \"%s\" option." %
						(option.upper()))
		return

	def _load_config(self):
		config_path = os.path.join(self.workspace, "config.dat")
		# don't bother loading if a config file doesn't exist
		if os.path.exists(config_path):
			# retrieve saved config data
			with open(config_path) as config_file:
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
		config_path = os.path.join(self.workspace, "config.dat")
		# create a config file if one doesn't exist
		if not os.path.exists(config_path):
			open(config_path, 'a').close()
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

	def request(self, url, **kwargs):
		kwargs_tmp = {}
		for i in kwargs:
			if kwargs[i] != None:
				kwargs_tmp[i] = kwargs[i]
		kwargs = kwargs_tmp
		req = request.main(framework=self)
		cond1 = self._global_options["agent"] == None
		cond2 = "agent" not in kwargs
		if not cond2:
			req.user_agent = kwargs["agent"]
		if not cond1:
			req.user_agent = self._global_options["agent"]
		req.debug = True if self._global_options['verbosity'] >= 2 else False
		req.proxy = kwargs["proxy"] if "proxy" in kwargs else self._global_options["proxy"]
		req.timeout = kwargs["timeout"] if "timeout" in kwargs else self._global_options["timeout"]
		req.redirect = kwargs["redirect"] if "redirect" in kwargs else True
		req.rand_agent = kwargs["rand_agent"] if "rand_agent" in kwargs else self._global_options["rand_agent"]
		method = kwargs["method"] if "method" in kwargs else "GET"
		payload = kwargs["payload"] if "payload" in kwargs else {}
		headers = kwargs["headers"] if "headers" in kwargs else {}
		cookie = kwargs["cookie"] if "cookie" in kwargs else None
		auth = kwargs["auth"] if "auth" in kwargs else ()
		content = kwargs["content"] if "content" in kwargs else ''
		return req.send(
			url=url,
			method=method,
			payload=payload,
			headers=headers,
			cookie=cookie,
			auth=auth,
			content=content)

	# ==================================================
	# SHOW METHODS
	# ==================================================

	def show_modules(self, param):
		# process parameter according to type
		if isinstance(param, list):
			modules = param
		elif param:
			modules = [
				x for x in Framework._loaded_modules if x.startswith(param)]
			if not modules:
				self.error("Invalid module category.")
				return
		else:
			modules = Framework._loaded_modules
		if not modules:
			self.error("no modules to display.")
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
			print('%s%s' % (self.spacer * 2, module))
		print('')

	def show_options(self, options=None):
		'''Lists options'''
		if options is None:
			options = self.options
		if options:
			pattern = "%s%%s  %%s  %%s  %%s" % (self.spacer)
			key_len = len(max(options, key=len))
			if key_len < 4:
				key_len = 4
			val_len = len(max([self.to_unicode(options[x])
							   for x in options], key=len))
			if val_len < 13:
				val_len = 13
			print('')
			print(pattern % ("Name".ljust(key_len), "Current Value".ljust(
				val_len), "Required", "Description"))
			print(
				pattern %
				(self.ruler *
				 key_len,
				 (self.ruler *
				  13).ljust(val_len),
				 self.ruler *
				 8,
				 self.ruler *
				 11))
			for key in sorted(options):
				value = options[key] if options[key] is not None else ''
				reqd = "no" if options.required[key] is False else "yes"
				desc = options.description[key]
				print(
					pattern %
					(key.upper().ljust(key_len),
					 self.to_unicode(value).ljust(val_len),
					 self.to_unicode(reqd).ljust(8),
					 desc))
			print('')
		else:
			print('')
			print("%sNo options available for this module." % (self.spacer))
			print('')

	def show_var(self):
		self.do_var("list")

	def _get_show_names(self):
		# Any method beginning with "show_" will be parsed
		# and added as a subcommand for the show command.
		prefix = "show_"
		return [x[len(prefix):]
				for x in self.get_names() if x.startswith(prefix)]

	# ==================================================
	# COMMAND METHODS
	# ==================================================

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
			print("%s => %s" % (name.upper(), value))
			self._save_config(name)
		else:
			self.error("Invalid option.")

	def do_unset(self, params):
		'''Unsets module options'''
		self.do_set('%s %s' % (params, "None"))

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
		self.output("Searching for \"%s\"..." % (text))
		modules = [x for x in Framework._loaded_modules if text in x]
		if not modules:
			self.error("No modules found containing \"%s\"." % (text))
		else:
			self.show_modules(modules)

	def do_shell(self, params):
		'''Executes shell commands'''
		proc = subprocess.Popen(params, shell=True, stdout=subprocess.PIPE,
								stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		self.output("Command: %s" % (params))
		stdout = proc.stdout.read()
		stderr = proc.stderr.read()
		if stdout:
			stdout = self.to_unicode(stdout)
			print("%s%s%s" % (Colors.O, stdout, Colors.N), end='')
		if stderr:
			stderr = self.to_unicode(stderr)
			print("%s%s%s" % (Colors.R, stderr, Colors.N), end='')

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
				self.error("Script file \"%s\" not found." % (params))

	def do_var(self, params):
		'''Variable define'''
		if not params:
			self.help_var()
			return
		params = params.split()
		arg = params[0].lower()
		if arg[:1] == '$':
			if len(params) == 2:
				if self.add_var(arg[1:], params[1]):
					self.output("Variable \'%s\' added." % (arg[1:]))
				else:
					self.output("Invalid variable name \'%s\'." % (arg[1:]), "r")
			else:
				print("\nUsage: var <name> <value>\n")
		elif arg == "list":
			self._list_var()
		elif arg == "delete":
			if len(params) == 2:
				if params[1] in ["limit", "proxy", "target", "timeout", "agent", "verbosity", "history"]:
					self.error("You can't delete default variable \'%s\'." % params[1])
				else:
					if self.delete_var(params[1]):
						self.output("Var \'%s\' deleted." % (params[1]))
					else:
						self.error("No such var was found for deletion \'%s\'" % params[1])
			else:
				print("\nUsage: var delete <name>\n")
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
					if not self._is_readable(filename):
						self.output('Cannot record commands to \'%s\'.' % (filename))
					else:
						Framework._record = filename
						self.output('Recording commands to \'%s\'.' % (Framework._record))
				else: self.help_record()
			else: self.output('Recording is already started.')
		elif arg == 'stop':
			if Framework._record:
				self.output('Recording stopped. Commands saved to \'%s\'.' % (Framework._record))
				Framework._record = None
			else: self.output('Recording is already stopped.')
		elif arg == 'status':
			status = 'started' if Framework._record else 'stopped'
			self.output('Command recording is %s.' % (status))

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
						self.output('Cannot spool output to \'%s\'.' % (filename))
					else:
						Framework._spool = codecs.open(filename, 'ab', encoding='utf-8')
						self.output('Spooling output to \'%s\'.' % (Framework._spool.name))
				else: self.help_spool()
			else: self.output('Spooling is already started.')
		elif arg == 'stop':
			if Framework._spool:
				self.output('Spooling stopped. Output saved to \'%s\'.' % (Framework._spool.name))
				Framework._spool = None
			else: self.output('Spooling is already stopped.')
		elif arg == 'status':
			status = 'started' if Framework._spool else 'stopped'
			self.output('Output spooling is %s.' % (status))
		else:
			self.help_spool()

	def do_report(self, params):
		'''Get report from the Gathers and save it to the other formats'''
		if not params:
			self.help_report()
			return
		arg = params.lower().split(" ")
		gather_file = os.path.join(self.workspace, "gather.dat")
		# open gather file
		with open(gather_file) as gf:
			try:
				gdata = json.loads(gf.read())
			except ValueError:
				self.error("Gather data is incorrect. gather is missed!") 
				return

		if arg[0] == "saved":
			for mod in gdata:
				self.heading(mod)
				for q in gdata[mod]:
					print("\t"+q)
			print()
			return

		if len(arg) < 3 or len(arg) > 4:
			self.error("Please select the your module name")
			self.help_report()
			return

		if arg[0] in ["json", "txt", "xml"]:
			form = getattr(self, "%s_output" % arg[0])
		else:
			self.error("Format \'%s\' doesn't found." % arg[0])
			return
		filename = "%s.%s" % (arg[1], arg[0])
		output_file = os.path.join(self.workspace, filename)
		mod_name = arg[2]

		if mod_name in gdata:
			output = gdata[mod_name]
		else:
			self.error("Module \'%s\' does not have any data" % mod_name)
			return

		if len(arg) == 4:
			tar_name = arg[3]
			if tar_name in output:
				output = output[tar_name]
			else:
				self.error("Query name \'%s\' is not found." % tar_name)
				return

		if form(output_file, output):
			self.output("Report saved at %s" % output_file)

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
				self.error("Invalid module name.")
			else:
				self.output("Multiple modules match \"%s\"." % params)
				self.show_modules(modules)
			return
		# compensation for stdin being used for scripting and loading
		if Framework._script:
			end_string = sys.stdin.read()
		else:
			end_string = "EOF"
			Framework._load = 1
		sys.stdin = StringIO("load %s\n%s" % (modules[0], end_string))
		return True

	do_use = do_load

	#==================================================
	# VARIABLE METHODS
	#==================================================

	def get_var(self, name):
		if name in self.variables:
			return self.variables[name]
		else:
			self.error("Variable name \'%s\' not found.Enter `var list`" % name)

	def add_var(self, name, value):
		if re.search(r"[a-zA-Z_][a-zA-Z0-9_]*", name):
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
		tdata = []
		for var in sorted(variables):
			tdata.append(var)
		if tdata:
			self.table(tdata, header=["Name", "Value"])

	def _init_var(self, vals=None):
		vars_path = os.path.join(self.workspace, "var.dat")
		# default variables define
		default_vars = {"limit": self._global_options["limit"],
						"proxy": self._global_options["proxy"],
						"target": self._global_options["target"],
						"timeout": self._global_options["timeout"],
						"agent": self._global_options["agent"],
						"verbosity": self._global_options["verbosity"],
						"history": self._global_options["history"]}

		# create a var file if one doesn't exist
		if not os.path.exists(vars_path):
			open(vars_path, 'a').close()
			vars_data = {}
		else:
			with open(vars_path) as vars_file:
				try:
					vars_data = json.loads(vars_file.read())
				except ValueError:
					# file is empty or corrupt, nothing to load
					vars_data = {}

		# add default variables if doesn't exist
		if "agent" not in vars_data:
			for i in default_vars.keys():
				if i not in vars_data:
					vars_data[i] = default_vars[i]


		if vals != None or vals == {}:
			self.variables = vals
		else:
			self.variables = vars_data

		# Update var.dat
		with open(vars_path, 'w') as vars_file:
			json.dump(self.variables, vars_file, indent=4)

	# ==================================================
	# HELP METHODS
	# ==================================================

	def help_load(self):
		print(getattr(self, "do_load").__doc__)
		print('')
		print("Usage: [load|use] <module>")
		print('')

	help_use = help_load

	def help_resource(self):
		print(getattr(self, "do_resource").__doc__)
		print('')
		print("Usage: resource <filename>")
		print('')

	def help_var(self):
		print(getattr(self, "do_var").__doc__)
		print('')
		print("Usage: var <$name> <value> || var [delete] <name> || var [list]")
		print('')

	def help_record(self):
		print(getattr(self, 'do_record').__doc__)
		print('')
		print('Usage: record [start <filename>|stop|status]')
		print('')

	def help_spool(self):
		print(getattr(self, 'do_spool').__doc__)
		print('')
		print('Usage: spool [start <filename>|stop|status]')
		print('')

	def help_report(self):
		print(getattr(self, 'do_report').__doc__)
		print('')
		print('Usage: report [<format> <filename> [<module_name> or <module_name> <query(hostname,domain name, keywords,etc)>]]')
		print('or   :    report [saved] => for show queries')
		print('\nExample: report json pdf_docs(without extention) osint/docs_search company.com')
		print('\n       : report xml pdf_docs(without extention) osint/docs_search')
		print('')

	def help_search(self):
		print(getattr(self, "do_search").__doc__)
		print('')
		print("Usage: search <string>")
		print('')

	def help_set(self):
		print(getattr(self, "do_set").__doc__)
		print('')
		print("Usage: set <option> <value>")
		self.show_options()

	def help_unset(self):
		print(getattr(self, "do_unset").__doc__)
		print('')
		print("Usage: unset <option>")
		self.show_options()

	def help_shell(self):
		print(getattr(self, "do_shell").__doc__)
		print('')
		print("Usage: [shell|!] <command>")
		print("...or just type a command at the prompt.")
		print('')

	def help_show(self):
		options = sorted(self._get_show_names())
		print(getattr(self, "do_show").__doc__)
		print('')
		print("Usage: show [%s]" % ('|'.join(options)))
		print('')

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

