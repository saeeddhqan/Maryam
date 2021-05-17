#!/usr/bin/env python3

from maryam import __main__
import sys

if __name__ == '__main__':
	argv = [f'"{arg}"' if ' ' in arg else arg for arg in sys.argv[1:]]
	__main__.cui(argv)
