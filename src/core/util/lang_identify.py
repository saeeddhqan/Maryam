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

from re import search

class main:

	def __init__(self, content, headers):
		""" Detect web language

			content	  : web content
			headers	  : web headers
		"""
		self.content = content
		self.headers = headers
		self._lang = None

	def run_crawl(self):
		for attr in dir(self):
			con1 = not attr.startswith('__')
			con2 = not attr.endswith('__')
			con3 = attr not in ('_lang', 'content', 'headers',
							 'lang', 'run_crawl', 'framework')
			if con1 and con2 and con3:
				getattr(self, attr)()
		
	def ruby(self):
		if search(r'<a href\=\S*(\.rb|\.rhtml)', self.content):
			self._lang = 'Ruby'

	def asp(self):
		if search(r'<a href\=\S*(\.asp)', self.content):
			self._lang = 'ASP'

	def asp_net(self):
		if search(r'<a href\=\S*(\.aspx|\.axd|\.asx|\.asmx|\.ashx|\.asax|\.ascx|\.cshtml)', self.content):
			self._lang = 'ASP.NET'

	def cold_fusion(self):
		if search(r'<a href\=\S*(\.cfm|\.cfml)', self.content):
			self._lang = 'ColdFusion'

	def flash(self):
		if search(r'<a href\=\S*(\.swf)', self.content):
			self._lang = 'Flash'

	def perl(self):
		if search(r'<a href\=\S*(\.pl|\.cgi)', self.content):
			self._lang = 'Perl'

	def python(self):
		if search(r'<a href\=\S*(\.py)', self.content):
			self._lang = 'Python'

	def php(self):
		if search(r'<a href\=\S*(\.php|\.php2|\.php3|\.php4|\.php5|\.phtm|\.phtml)', self.content):
			self._lang = 'PHP'

	def java(self):
		if search(r'<a href\=\S*(\.do|\.jhtml|\.jsp|\.jspa|\.jspx|\.jws|\.wss|\.action)', self.content):
			self._lang = 'Java'

	@property
	def lang(self):
		return self._lang
