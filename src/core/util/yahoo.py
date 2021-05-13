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

import re

class main:

	def __init__(self, q, limit=2, count=100):
		""" yahoo.com search engine

			framework : core attribute
			q 		  : query for search
			limit	  : Number of pages
			count	  : Number of links
		"""
		self.framework = main.framework
		self.q = self.framework.urlib(q).quote
		self.limit = limit
		self.count = count
		self.agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
		self.url = 'https://search.yahoo.com/search'
		self._pages = ''
		self.xpath_name = {
			'results': "//div[contains(concat(' ', normalize-space(@class), ' '), ' Sr ')]",
			'results_a': './/h3/a/@href',
			'results_title': './/h3/a',
			'results_content': './/div[contains(@class, "compText")]'
		}
		self.xpath = {
			self.xpath_name['results']: [
				self.xpath_name['results_content'],
				self.xpath_name['results_title'],
				self.xpath_name['results_a']
			]
		}

	def run_crawl(self):
		page = 1
		set_page = lambda x: (x*10)+1
		payload = {'p': self.q, 'b': set_page(page), 'pz': self.count, 'fl': 1}
		max_attempt = 0
		while True:
			self.framework.verbose(f"[YAHOO] Searching in {page} page...")
			try:
				req = self.framework.request(
					url=self.url,
					params=payload,
					headers={'user-agent': self.agent},
					allow_redirects=True)
			except:
				self.framework.error('ConnectionError', 'util/yahoo', 'run_crawl')
				max_attempt += 1
				if max_attempt == self.limit:
					self.framework.error('Yahoo is missed!', 'util/yahoo', 'run_crawl')
					break
			else:
				if 'unsafe-url">Next<' not in req.text or page == self.limit:
					self._pages += req.text
					break
				page += 1
				payload['b'] = set_page(page)
				self._pages += req.text

	@property
	def pages(self):
		return self._pages

	@property
	def results(self):
		parser = self.framework.page_parse(self._pages)
		xpath_results = parser.html_fromstring(self.xpath)
		results = []
		if not xpath_results:
			return results
		root = xpath_results[self.xpath_name['results']]
		for i in range(len(root[self.xpath_name['results_a']])):
			a = re.search(r"RU=(https?%3a%2f%2f[^/]+)/", root[self.xpath_name['results_a']][i])
			if a:
				a = a.group(1)
			else:
				a = root[self.xpath_name['results_a']][i]
			urlib = self.framework.urlib(a)
			a = urlib.unquote
			cite = self.framework.meta_search_util().make_cite(a)
			result = {
				't': root[self.xpath_name['results_title']][i].text_content(),
				'a': a,
				'c': cite,
				'd': root[self.xpath_name['results_content']][i].text_content(),
			}
			results.append(result)
		return results

	@property
	def links(self):
		reg = r"RU=(https?%3a%2f%2f[^/]+)/"
		tmp = self.framework.page_parse(self._pages).findall(reg)
		links = []
		for link in tmp:
			link = self.framework.urlib(link).unquote
			links.append(link)
		return links
	
	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
