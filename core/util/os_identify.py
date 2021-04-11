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

from re import search, I

class main:

	def __init__(self, content, headers):
		""" Detect operation system

			content 	: Web page content
			headers		: Web page headers
		"""
		self.content = content
		self.headers = headers
		self._os = None

	def run_crawl(self):
		for attr in dir(self):
			con1 = not attr.startswith('__')
			con2 = not attr.endswith('__')
			con3 = attr not in ('_os', 'content', 'headers',
							 'framework', 'os', 'run_crawl')
			if con1 and con2 and con3:
				getattr(self, attr)()
		
	def windows(self):
		OSes = ('windows', 'win32')
		for os in OSes:
			for header in self.headers.items():
				if search(os, header[1], I):
					self._os = os.title()

	def bsd(self):
		for header in self.headers.items():
			if search(r'^bsd', header[1], I):
				self._os = 'BSD'

	def ibm(self):
		OSes = ('IBM', 'Lotus-Domino', 'WebSEAL')
		for os in OSes:
			for header in self.headers.items():
				if search(os, header[1], I):
					self._os = 'IBM'

	def linux(self):
		OSes = ('linux', 'ubuntu', 'gentoo', 'debian', 'dotdeb', 'centos', 'redhat', 'sarge', 'etch',
			  'lenny', 'squeeze', 'wheezy', 'jessie', 'red hat', 'scientific linux')
		for os in OSes:
			for header in self.headers.items():
				if search(os, header[1], I):
					self._os = os.title()

	def mac(self):
		for header in self.headers.items():
			if search(r'^mac|^macos', header[1], I):
				self._os = 'MacOS'

	def solaris(self):
		OSes = ('solaris', 'sunos', 'opensolaris', 'sparc64', 'sparc')
		for os in OSes:
			for header in self.headers.items():
				if search(os, header[1], I):
					self._os = os.title()

	def unix(self):
		for header in self.headers.items():
			if search(r'^unix', header[1], I):
				self._os = 'Unix'

	@property
	def os(self):
		return self._os
