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

	def __init__(self, q, count=10):
		""" wikipedia.org search 
			q          : Query for search
			count      : Number of results
		"""
		self.framework = main.framework
		self.q = q
		self.num = count
		self._links = []
		self._titles = []
		self._pids = []
		self.url = 'https://en.wikipedia.org/w/api.php'		
		self.headers = {'User-Agent' : 'OWASP Maryam(github.com/saeeddhqan/maryam)'}


	def run_crawl(self):
		self.framework.verbose('[WIKIPEDIA] Searching...', end='\r')
		payload = {
			'action': 'query',
			'list': 'search',
			'prop': '', 
			'srsearch': self.q, 
			'srlimit': self.num, 
			'utf8': '', 
			'format': 'json'
		}

		res = self.wiki_request(payload)
		if res is None:
			return 

		res = res.json()
		results = res['query']['search']

		for result in results:
			title = result['title']
			pid = result['pageid']
			link = 'https://en.wikipedia.org/wiki/' + '_'.join(title.split(' '))
			self._titles.append(title)
			self._links.append(link)
			self._pids.append(pid)


	def page(self):
		self.framework.verbose(f"[WIKIPEDIA] Getting page {self.q}...", end='\r')
		payload = {
			'action': 'query', 
			'pageids': self.q,
			'prop': 'info|extracts', 
			'inprop': 'url',  
			'explaintext': '',
			'exintro': '',
			'format': 'json'
		}

		res = self.wiki_request(payload)
		if not res:
			return

		res = res.json()
		return res['query']['pages'][str(self.q)]

	def wiki_request(self, payload):
		try:
			req = self.framework.request(
					url=self.url,
					params=payload,
					headers=self.headers,
					allow_redirects=False)
			return req
		except Exception as e:
			self.framework.error(f"ConnectionError: {e}", 'util/wikipedia', 'wiki_request')
			return None

	@property
	def links(self):
		return self._links

	@property
	def titles(self):
		return self._titles

	@property
	def pids(self):
		return self._pids

	@property
	def links_with_title(self):
		return zip(self._links, self._titles , self._pids)
