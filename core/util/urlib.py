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
try:
	from urllib import parse as urlparse
	from urllib.parse import quote
except:
	import urlparse
	from urllib import quote

import re
from socket import gethostbyname, gethostbyaddr

class main:

	def __init__(self, url):
		self.url = url

	def join(self, urjoin):
		return urlparse.urljoin(self.url, urjoin)

	def parse(self):
		return urlparse.urlparse(self.url)

	def unparse(self, urparse):
		return urlparse.urlunparse(urparse)

	def sub_service(self, serv):
		serv = re.sub(r"://", '', serv)
		urparse = re.split(r"://", self.url)
		if len(urparse) == 2:
			del urparse[0]
			if serv != '':
				url = "%s://%s" % (serv, "".join(urparse))
			else:
				url = ''.join(urparse)
		else:
			url = "%s://%s" % (serv, urparse[0])
		return url
	
	@property
	def quote(self):
		if "%" not in self.url:
			return quote(self.url)
		else:
			return self.url
			
	@property
	def unquote(self):
		return urlparse.unquote(self.url)

	@property
	def ip(self):
		return gethostbyname(self.netloc)

	@property
	def host(self):
		return gethostbyaddr(self.parse().netloc)[0]

	@property
	def scheme(self):
		return self.parse().scheme

	@property
	def netloc(self):
		return self.parse().netloc

	@property
	def netroot(self):
		loc = self.parse().netloc
		# Replace subdomains
		reg = re.search(r"^[A-z0-9\-.]+\.([A-z0-9\-]+\.[A-z0-9]+)$", loc)
		if reg:
			loc = reg.group(1)
		return loc

	@property
	def path(self):
		return self.parse().path

	@property
	def query(self):
		return self.parse().query

	@property
	def params(self):
		return self.parse().params

	@property
	def fragment(self):
		return self.parse().fragment
