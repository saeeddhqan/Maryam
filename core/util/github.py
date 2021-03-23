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
	def __init__(self, q, cookie='', limit=10):
		""" github.com search
			
			q 		  : The query for search
			cookie	  : Your GitHub cookie
			limit	  : The number of pages
			count	  : The number of links
		"""
		self.framework = main.framework
		self.q = q
		self.cookie = cookie
		self.limit = limit
		self._pages = 10
		self._page = {"Github":[""]}
		self._links = ''
		self.github_api = 'api.github.com'
		self.types = ['users', 'repositories']
		self.urls = [f"https://{self.github_api}/search/{self.types[0]}?q={self.q}&per_page={self.limit}",
					f"https://{self.github_api}/search/{self.types[1]}?q={self.q}&per_page={self.limit}&page={self._pages}"
					]
	
	def run_crawl(self):
		max_attempt = len(self.urls)
		for page in range(max_attempt):
			try:
				self.framework.verbose(f"[GITHUB] Searching in {page} page...")
				req = self.framework.request(url=self.urls[page], headers={'Cookie': self.cookie, 'Accept': 'application/vnd.github.v3.text-match+json'}, allow_redirects=True)
				result = req.text
				result_json = req.json()
				for results in result_json["items"]:
					if 'fork' not in results:
						self._links = self._links + "".join(results['html_url']).replace("https://", " ")
					else:
						self._page['Github'].append(results['html_url'])
				repo = self._page['Github']
				users = self._links.split(' ')
			except:
				self.framework.error('[GITHUB] ConnectionError')
				return
		return

	@property
	def links(self):
		return self._links

	@property
	def users(self):
		return users

	@property
	def repositories(self):
		return repo
