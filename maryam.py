#!/usr/bin/env python3
from maryam import __main__
import argparse
import sys

if __name__ == '__main__':
	desc = 'maryam -h'
	parse = argparse.ArgumentParser(description=desc)
	parse.add_argument('-e', help='execute a command and exit', metavar='execute', dest='execute', action='store')
	parse.add_argument('-s', help='run a command without exit', metavar='start', dest='start', action='store')
	parse.add_argument('-v', help='show version and exit', action='version', 
			version=f"OWASP MARYAM V.{__main__.__VERSION__}")
	format_help = parse.format_help()
	argv = [f'"{arg}"' if ' ' in arg else arg for arg in sys.argv[1:]]
	__main__.cui(argv, format_help)
