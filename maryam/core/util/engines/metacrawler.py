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

	def __init__(self, q, limit=1):
		""" metacrawler.com search engine

			q 		  : query for search
			limit	  : count of pages
		"""
		self.framework = main.framework
		self.q = self.framework.urlib(q).quote
		self.xpath_name = {
			'results': '//div[@class="web-bing"]',
			'results_content': './/span[@class="web-bing__description"]',
			'results_title_and_a': './/a[@class="web-bing__title"]',
			'results_cite': './/span[@class="web-bing__url"]'
		}
		self.xpath = {
			self.xpath_name['results']: [
				self.xpath_name['results_content'],
				self.xpath_name['results_title_and_a'],
				self.xpath_name['results_cite']
			]
		}
		self.limit = limit
		self._pages = ''
		self.metacrawler = 'https://www.metacrawler.com/serp'

	def run_crawl(self):
		page = 1
		payload = {'q': self.q, 'page': 1}
		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) \
					AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15',
			'Accept-Language': 'en-US,en;q=0.5'
		}

		while True:
			self.framework.verbose(f"[METACRAWLER] Searching in {page} page...")
			try:
				req = self.framework.request(url=self.metacrawler, params=payload, headers=headers)
			except Exception as err:
				self.framework.error('ConnectionError', 'util/engines/metacrawler', 'run_crawl')
				self.framework.error('Metacrawler is missed!', 'util/engines/metacrawler', 'run_crawl')
				break
			else:
				text = self.framework.to_str(req.text)
				if 'To continue, please respond below:' in text:
					self.framework.error('CaptchaError', 'util/enginesmetacrawler', 'run_crawl')
					self.framework.error('Metacrawler is missed!', 'util/engines/metacrawler', 'run_crawl')
					break
				self._pages += text
				if 'Next »' not in text or page >= self.limit:
					break
				page += 1
				payload['page'] += 1

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		links = self.framework.page_parse(self._pages).findall(\
			r'<a class="web-bing__title" href="(.*)"\sdata-thash')
		return links

	@property
	def results(self):
		parser = self.framework.page_parse(self._pages)
		xpath_results = parser.html_fromstring(self.xpath)
		results = []
		if xpath_results:
			root = xpath_results[self.xpath_name['results']]
			for i in range(len(root[self.xpath_name['results_title_and_a']])):
				t_and_a = root[self.xpath_name['results_title_and_a']][i]
				a = t_and_a.get('href')
				t = t_and_a.text_content()
				result = {
					't': t,
					'a': a,
					'c': root[self.xpath_name['results_cite']][i].text_content(),
					'd': root[self.xpath_name['results_content']][i].text_content(),
				}
				results.append(result)
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
