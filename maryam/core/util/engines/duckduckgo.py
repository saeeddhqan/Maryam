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

	def __init__(self, q, limit=1):
		""" duckduckgo.com search engine

			q          : Query for search
			limit      : Number of of pages
			count      : Number of of results
		"""
		self.framework = main.framework
		self.q = q
		self._pages = ''
		self.limit = 1
		self._links = []
		self._d_js_results = []
		self._d_js_xpath_name = {}
		self.d_js_xpath_name = {
				'results': '//div[@class="result results_links results_links_deep web-result "]',
				'results_content': './/a[@class="result__snippet"]',
				'results_title': './/a[@class="result__a"]',
				'results_a': './/a[@class="result__a"]/@href',
			}
		self.d_js_xpath = {
			self.d_js_xpath_name['results']: [
				self.d_js_xpath_name['results_content'],
				self.d_js_xpath_name['results_title'],
				self.d_js_xpath_name['results_a'],
			]
		}

	def run_crawl(self):
		page = 1
		set_page = lambda x: (x - 1) * 10 + 1
		payload = {'s': set_page(page), 'q': self.q, 'dc': 10, 'v': 'l', 'o': 'json'}
		duck_url = 'https://duckduckgo.com/html'
		self._pages = ''
		while True:
			self.framework.verbose(f"[DuckDuckGo] Searching in {page} page...", end='\r')
			try:
				req = self.framework.request(
					url=duck_url,
					params=payload)
			except Exception as e:
				self.framework.error(f"ConnectionError: {e}", 'util/duckduckgo', 'run_crawl')
				self.framework.error('DuckDuckGo is missed!', 'util/duckduckgo', 'run_crawl')
			else:
				if req.status_code != 200:
					self.framework.error(f"{req.status_code} Forbidden", 'util/duckduckgo', 'run_crawl')
					self.framework.error('DuckDuckGo is missed!', 'util/duckduckgo', 'run_crawl')
					break

				text = req.text
				self._pages += text

				if page == 1:
					vqd = re.search(r'"vqd" value="([\d\-]+)" />', text)
					if vqd:
						duck_url = f"https://links.duckduckgo.com/d.js"
						payload['vqd'] = vqd.group(1)
						payload['api'] = '/d.js'
						payload['s'] = set_page(page)
				else:
					try:
						self._d_js_results.extend(req.json()['results'])
					except Exception as e:
						pass
					else:
						pass

				page += 1
				if page >= self.limit:
					break

	@property
	def results(self):
		results = []
		parser = self.framework.page_parse(self._pages)
		xpath_results = parser.html_fromstring(self.d_js_xpath)
		root = xpath_results[self.d_js_xpath_name['results']]
		for i in range(len(root[self.d_js_xpath_name['results_a']])):
			a = root[self.d_js_xpath_name['results_a']][i]
			try :
				results.append({
					't': root[self.d_js_xpath_name['results_title']][i].text_content(),
					'a': a,
					'c': self.framework.meta_search_util().make_cite(a),
					'd': root[self.d_js_xpath_name['results_content']][i].text_content(),
				})
			except Exception as e:
				pass

		return results + [{'a': x['u'], 't': x['t'], 'd': x['a'], 'c': self.meta_search_util.make_cite(x['u'])}\
			for x in self._d_js_results]

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
		results = [{ 'link': a, 'title': b } for a,b in parser.findall(r'''rel="nofollow" href="([^"]+)" class='result-link'>([^<]+)</a''')]

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
