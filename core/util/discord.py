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

	def __init__(self, q, limit=3):
		"""
		discord users and servers search

		q          : Query for search
		limit      : Number of pages
		"""

		self.framework = main.framework
		self.q = q
		self._pages = ''
		self.limit = limit
		self._links = []
		self.disboard = 'https://disboard.org/search?'
		self.discordhub = 'https://discordhub.com/user/search?'

	def run_crawl(self):
		query = self.q.split('_')[0]
		url_s = [f"{self.disboard}keyword={query}&page={i}" for i in range(1, self.limit+1)]
		url_u = [f"{self.discordhub}user_search_bar=%23{query}&page={i}" for i in range(1, self.limit+1)]
		if self.q.split('_')[1] == 's':
			max_attempt = len(url_s)
			urls = url_s
		if self.q.split('_')[1] == 'u':
			max_attempt = len(url_u)
			urls = url_u
		for url in range(max_attempt):
			self.framework.verbose(f"[DISCORD] Searching in {url} page...")
			try:
				req = self.framework.request(url=urls[url], allow_redirects=True)
			except Exception as e:
				self.framework.error('ConnectionError', 'util/discord', 'run_crawl')
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error('Discord is missed!', 'util/discord', 'run_crawl')
					break
			self._pages += req.text
	@property
	def pages(self):
		return self._pages
