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

class main:

	def __init__(self, framework, q, cookie, _type='Repositories', limit=1):
		""" github.com search
			
			framework : Core attribute
			q 		  : The query for search
			cookie	  : Your GitHub cookie
			limit	  : The number of pages
			count	  : The number of links
		"""
		self.framework = framework
		self.q = self.framework.urlib(q).quote
		self.cookie = cookie
		self.limit = limit
		self._pages = ''
		self.github = 'github.com'
		self.type = _type
		self.types = ['users', 'Repositories']

	def run_crawl(self):
		if self.type not in self.types:
			self.type = 'Repositories'
		urls = [f"https://{self.github}/search?q={self.q}&p={i}&type={self.type}" for i in range(1, self.limit+1)]
		max_attempt = len(urls)
		for url in range(max_attempt):
			self.framework.verbose(f"[GITHUB] Searching in {url} page...")
			try:
				req = self.framework.request(url=urls[url], headers={'Cookie': self.cookie}, allow_redirects=True)
			except:
				self.framework.error('[GITHUB] ConnectionError')
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error('Github is missed!')
					break
			else:
				page = req.text
				if f"We couldn’t find any {self.type.lower()} matching '{self.q}'</h3>" in page:
					break
				if f"https://github.com/search?q={self.q}&p={url+1}&type={self.type}" not in page:
					self._pages += page
					break 
				self._pages += page
	@property
	def pages(self):
		return self._pages

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		emails = self.page_parse(",".join(self.all_emails)).get_emails(self.q)
		return emails

	@property
	def all_emails(self):
		parser = self.framework.page_parse(self._pages)
		parser.pclean
		emails = [("".join([chr(int(char[1:3], 16)) for char in email.split('&#')[1:]]))\
					for email in parser.findall(r"(&#x\w+;)+")]
		return list(set(emails))

	@property
	def repositories(self):
		parser = self.framework.page_parse(self._pages)
		parser.pclean
		links = [f"https://github.com/{x}" for x in parser.findall(r'data-hydro-click-hmac="[\w]+" href="([^"]+)">')]
		links_with_desc = parser.findall(r'([\w_\./]+)</a>[\w\W]{23}class="mb-1">\s+([^\n]+)\n\s+</p>')
		final_output = {}
		for i in links_with_desc:
			final_output[f"https://github.com{i[0]}"] = i[1]
		for i in links:
			if i not in final_output:
				final_output[i] = "<Withoud Description>"
		return final_output

	@property
	def users(self):
		parser = self.framework.page_parse(self._pages)
		parser.pclean
		links = [f"https://github.com/{x}" for x in parser.findall(r"Unfollow ([\w_\.]+)") if x != "this"]
		return list(set(links))
