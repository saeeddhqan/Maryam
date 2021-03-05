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

	def __init__(self, framework, q, limit=1, count=10):
		""" duckduckgo.com search engine
			framework  : Core attribute
			q          : Query for search
			limit      : Number of of pages
			count      : Number of of results
		"""
		self.framework = framework
		self.q = q
		self._pages = ''
		self.limit = limit + 1
		self.num = count
		self._links = []

	def run_crawl(self):
		url = 'https://lite.duckduckgo.com/lite/'
		payload = {'q': self.q, 's': 0, 'o': 'json', 'dc': '', 'api': '/d.js', 'kl': 'wt-wt'}	
		page = 1
		while True:
			self.framework.verbose(f"[DUCKDUCKGO] Searching in {page} page...", end='\r')
			try:
				req = self.framework.request(
						url=url,
						method='POST',
						params=payload,
						allow_redirects=False)
			except:
				self.framework.error('[DUCKDUCKGO] ConnectionError')
				return
			if req.status_code == 403:
				self.framework.error('[DUCKDUCKGO] 403 Forbidden (Too many requests.)')
				return
			self._pages += req.text
			# setting next page offset
			if payload['s'] == 0:
				# num of result per page
				payload['s'] = self.num
			else:
				payload['s'] += self.num
			# next page start
			payload['dc'] = payload['s'] + 1 
			
			page += 1
			if page > self.limit:
				break
		links = self.framework.page_parse(self._pages).findall(r'rel="nofollow" href="([^"]+)" class=\'result-link\'>')
		for link in links:
			cond1 = 'duckduckgo.com' not in link.lower()
			cond2 = '/lite/?' not in link.lower()
			cond3 = "://" in link
			if cond1 and cond2 and cond3:
				self._links.append(self.framework.urlib(link).unquote_plus)
	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		return self._links

	@property
	def links_with_title(self):
		parser = self.framework.page_parse(self._pages)
		parser.pclean
		results = parser.findall(r'''rel="nofollow" href="([^"]+)" class='result-link'>([^<]+)</a''')
		return results

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
