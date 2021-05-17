#!/usr/bin/env python3
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

__VERSION__ = '2.2.6'

import sys

# Import framework
from maryam.core import initial

def cui(args):
	core = initial.initialize
	help_menu = 'usage: maryam [-h] [-e execute] [-s start] [-c category] [-v]'\
				  '\nmaryam -h\n'\
				  '\noptional arguments:'\
				  '\n	  -h, --help   show this help message and exit'\
				  '\n	  -e execute   execute a command and exit'\
				  '\n	  -s start     run a command without exit'\
				  '\n	  --footprint  select footprint category to speed up the framework'\
				  '\n	  --iris       select iris category to speed up the framework'\
				  '\n	  --osint      select osint category to speed up the framework'\
				  '\n	  --search     select search category to speed up the framework'\
				  '\n	  -v           show version and exit'
	if args:
		option = args.pop(0)
		section = '*'
		mode = 'run'
		if option in ['-v', '--version']:
			print(f"OWASP Maryam V.{__VERSION__}")
			exit(0)
		elif option in ['--iris', '--footprint', '--osint', '--search']:
			section = option[2:]
			if len(args) > 0:
				option = args.pop(0)
			else:
				option = 'run'
		if option == '-e':
			core = core('execute', section)
			core.onecmd(' '.join(args))
			exit(0)
		elif option == '-s':
			core = core('run', section)
			core.onecmd(' '.join(args))
		elif option == 'run':
			core = core('run', section)
		else:
			print(help_menu)
			exit(0)
	else:
		core = core('run')

	while True:
		try:
			core.cmdloop()
			break
		except KeyboardInterrupt:
			print('\n[!] Use exit command to exit')
		except Exception as e:
			raise e

if __name__ == '__main__':
	args = [f'"{arg}"' if ' ' in arg else arg for arg in sys.argv[1:]]
	cui(args)
