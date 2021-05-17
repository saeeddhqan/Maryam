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

from urllib import parse as urlparse
import re
from socket import gethostbyname, gethostbyaddr

class main:

	def __init__(self, url):
		""" url parser

			url 	: url string for parse
		"""
		self.url = url

	def join(self, urjoin):
		return urlparse.urljoin(self.url, urjoin)

	def parse(self):
		return urlparse.urlparse(self.url)

	def unparse(self, urparse):
		return urlparse.urlunparse(urparse)

	def sub_service(self, serv=None):
		'''Add protocol to url or replace it or clean it'''
		urparse = re.split(r'://', self.url)
		if not serv:
			# Clean protocol
			url = ''.join(urparse)
		else:
			# Add protocol
			serv = re.sub(r'://', '', serv)
			if len(urparse) == 2:
				del urparse[0]
				url = f"{serv}://{''.join(urparse)}"
			else:
				url = f"{serv}://{urparse[0]}"
		self.url = url
		return url

	def check_urlfile(self, file):
		reg = re.compile(r"\."+file+r"[^\w]")
		reg2 = re.compile(r"\."+file+r"[^\w]?$")
		if reg.search(self.url) or reg2.search(self.url):
			return True
		return False

	@property
	def quote(self):
		if '%' not in self.url:
			self.url = urlparse.quote(self.url)
		return self.url

	@property
	def quote_plus(self):
		if '%' not in self.url:
			self.url = urlparse.quote_plus(self.url)
		return self.url

	@property
	def unquote(self):
		self.url = urlparse.unquote(self.url)
		return self.url

	@property
	def unquote_plus(self):
		self.url = urlparse.unquote_plus(self.url)
		return self.url

	@property
	def ip(self):
		if re.match(r"^\d+.\d+.\d+.\d+$", self.url):
			return self.url
		else:	
			loc = self.netloc
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

	def self_params(self, url):
		url = urlparse.unquote(url)
		queries = urlparse.urlparse(url).query
		page = url.replace('?'+queries, '')
		params = {}
		params[page] = {}
		if not queries:
			return {}

		if '&' in queries:
			queries = queries.split('&')
		else:
			queries = [queries]
		for query in queries:
			if not query:continue
			query = query.split('=')+['']
			name=query[0]
			value=query[1]
			params[page][name] = value
		return params
