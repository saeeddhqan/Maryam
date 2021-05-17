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
	# framework = None
	def __init__(self, q, limit=1):
		""" dogpile.com search engine

			q     : Query for search
			limit : Number of pages
		"""
		self.framework = main.framework
		self.q = q
		self.url = 'https://www.dogpile.com/serp'
		self.next_page_text = 'pagination__num pagination__num--next-prev pagination__num--next'
		self._pages = ''
		self.limit = limit
		self.xpath_name = {
			'results': '//div[@class="web-bing__result"]',
			'results_content': './/span[@class="web-bing__description"]',
			'results_title_a': './/a[@class="web-bing__title"]',
		}
		self.xpath = {
			self.xpath_name['results']: [
				self.xpath_name['results_content'],
				self.xpath_name['results_title_a'],
			]
		}

	def run_crawl(self):
		page = 1
		payload = {'page': page, 'q': self.q, 'sc': ''}
		while True:
			self.framework.verbose(f"[Dogpile] Searching in {page} page...", end='\r')
			try:
				req = self.framework.request(
					url=self.url,
					params=payload,
					allow_redirects=True)
			except Exception as e:
				self.framework.error(f"ConnectionError: {e}", 'util/dogpile', 'run_crawl')
			else:
				if req.status_code == 307:
					self.framework.error('Dogpile CAPTCHA triggered.', 'util/dogpile', 'run_crawl')
					break
				self._pages += req.text
				if page >= self.limit or self.next_page_text not in req.text:
					break
				page += 1
				payload['page'] = page
				sc = re.search(fr'page={page}&amp;sc=([\w]+)"', req.text)
				if not sc:
					break
				payload['sc'] = sc.group(1)

	@property
	def results(self):
		parser = self.framework.page_parse(self._pages)
		xpath_results = parser.html_fromstring(self.xpath)
		results = []
		if not xpath_results:
			return results
		root = xpath_results[self.xpath_name['results']]
		for i in range(len(root[self.xpath_name['results_title_a']])):
			a = root[self.xpath_name['results_title_a']][i].get('href')
			cite = self.framework.meta_search_util().make_cite(a)
			result = {
				't': root[self.xpath_name['results_title_a']][i].text_content(),
				'a': a,
				'c': cite,
				'd': root[self.xpath_name['results_content']][i].text_content(),
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
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
