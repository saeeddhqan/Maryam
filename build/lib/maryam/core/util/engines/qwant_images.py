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

	def __init__(self, q, limit=1, count=50):
		""" qwant.com image search engine

			q 	  : Query for search
			limit	  : Number of pages
			count	  : Number of results
		"""
		self.framework = main.framework
		self.q = q
		self.limit = 10 if limit > 10 else limit
		self.count = 50 if count > 50 else count
		self._pages = ''
		self._json = []
		self.qwant = 'https://api.qwant.com/v3/search/images'

	def run_crawl(self):
		page = 1
		set_page = lambda x: (x-1)*10
		payload = {'t': 'images', 'q': self.q, 'offset': set_page(page), 'count': '10', \
			'safesearch': '0', 'device': 'desktop', 'locale': 'en_GB', 'device': 'desktop'}
		while True:
			self.framework.verbose(f"[QWANT] Searching in {page+1} page...")
			try:
				req = self.framework.request(url=self.qwant, params=payload)
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/engines/qwant_images', 'run_crawl')
				self.framework.error('Qwant is missed!', 'util/engines/qwant_images', 'run_crawl')
				break
			else:
				if req.status_code == 429 and "I can't let you do that..." in req.text and '<div class="error-code">' in req.text:
					self.framework.error('429 Too Many Requests', 'util/engines/qwant_images', 'run_crawl')
					return
				self._pages += req.text
				try:
					self._json.append(req.json())
				except Exception as e:
					self.framework.error('429 Too Many Requests', 'util/engines/qwant_images', 'run_crawl')
					return
				else:
					if req.json() == {'status': 'error', 'data': {'error_code': 22}}:
						self.framework.error('429 Too Many Requests', 'util/engines/qwant_images', 'run_crawl')
						return
					else:
						if page == self.limit:
							break
						page += 1
						payload['offset'] = set_page(page)

	@property
	def pages(self):
		return self._pages

	@property
	def json(self):
		return self._json

	@property
	def results(self):
		results = []
		for page in self._json:
			items = page.get('data', {}).get('result', {})
			if items:
				items = items.get('items', [])
			for item in items:
				results.append({
					"a": item.get("url"),
					"i": item.get("media"),
					"t": item.get("title"),
					"d": f"{item.get('width')}*{item.get('height')} {item.get('size')}B"}
				)

		return results

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q, self.links)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)

