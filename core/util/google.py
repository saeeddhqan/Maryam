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
	# framework = None
	def __init__(self, q, limit=1, count=10):
		""" google.com search engine

			q     : Query for search
			limit : Number of pages
			count : Number of results
			autoproxy: Use rotating proxies
		"""
		self.framework.autoproxy = True#self.framework_global_options_['autoproxy']
		self.countip=0
		self.framework = main.framework
		self.q = q
		self.agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
		self.url = 'https://www.google.com/search'
		self._pages = ''
		self.limit = limit + 1
		self.count = count
		self.xpath_name = {
			'results': '//div[@class="g"]',
			'results_content': './/div[@class="IsZvec"]',
			'results_title': './/h3[1]',
			'results_a': './/div[@class="yuRUbf"]/a',
			'results_cite': './/div[@class="yuRUbf"]/a//cite'
		}
		self.xpath = {
			self.xpath_name['results']: [
				self.xpath_name['results_content'],
				self.xpath_name['results_title'],
				self.xpath_name['results_a'],
				self.xpath_name['results_cite']
			]
		}

	def run_crawl(self):
		page = 1
		set_page = lambda x: (x - 1) * self.count
		payload = {'num': self.count, 'start': set_page(page), 'ie': 'utf-8', 'oe': 'utf-8', 'q': self.q, 'filter': '0'}
		while True:
			self.framework.verbose(f"[GOOGLE] Searching in {page} page...", end='\r')
			if self.framework.autoproxy:
				ob=self.framework.proxy()
				ob.getproxy()
				ob.readip()
			proxy = ob.rotateip(k=self.countip) if self.framework.autoproxy else None

			try:
				req = self.framework.request(
					url=self.url,
					params=payload,
					headers={'user-agent': self.agent},
					allow_redirects=True,
     				proxies=proxy)
			except Exception as e:
				self.framework.error(f"ConnectionError: {e}", 'util/google', 'run_crawl')
			else:
				if req.status_code in (503, 429):
					self.framework.error('Google CAPTCHA triggered.', 'util/google', 'run_crawl')
					if self.autoproxy == True:
						self.countip += 1
						if ob.rotateip(k=self.countip) == -1:
							self.framework.output('[PROXY] End of proxy list. ')
							break
						else:
							continue
					else:
						break

				if req.status_code in (301, 302):
					redirect = req.headers['location']
					req = self.framework.request(url=redirect, allow_redirects=False)

				self._pages += req.text
				page += 1
				payload['start'] = set_page(page)
				if page >= self.limit:
					break

	@property
	def results(self):
		parser = self.framework.page_parse(self._pages)
		xpath_results = parser.html_fromstring(self.xpath)
		results = []
		if not xpath_results:
			return results
		root = xpath_results[self.xpath_name['results']]
		for i in range(len(root[self.xpath_name['results_a']])):
			result = {
				'title': root[self.xpath_name['results_title']][i].text_content(),
				'a': root[self.xpath_name['results_a']][i].get('href'),
				'cite': root[self.xpath_name['results_cite']][i].text_content(),
				'content': root[self.xpath_name['results_content']][i].text_content(),
			}
			results.append(result)
		return results

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		links = [x['a'] for x in self.results]
		return links

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q, self.links)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
