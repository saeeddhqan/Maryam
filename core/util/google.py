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
	def __init__(self, q, limit=1, count=10, mode='original'):
		""" google.com search engine
			q     : Query for search
			limit : Number of pages
			count : Number of results
		"""
		self.framework = main.framework
		self.q = q
		self.mode = mode
		if self.mode == 'legacy':
			self.agent = 'Lynx/2.8.5rel.1 libwww-FM/2.15FC SSL-MM/1.4.1c OpenSSL/0.9.7e-dev'
			self.xpath_name_legacy = {
				'results': '//div[@class="ezO2md"]',
				'results_content': './/div[@class="YgS6de"]//span[@class="fYyStc"]',
				'results_title': './/span[@class="CVA68e qXLe6d"]',
				'results_a': './/a[@class="fuLhoc ZWRArf"]',
				'results_cite': './/span[@class="qXLe6d dXDvrc"]/span[@class="fYyStc"]'
			}
			self.xpath_legacy = {
				self.xpath_name_legacy['results']: [
					self.xpath_name_legacy['results_content'],
					self.xpath_name_legacy['results_title'],
					self.xpath_name_legacy['results_a'],
					self.xpath_name_legacy['results_cite']
				]
			}
		else:
			self.agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
			self.xpath_name_original = {
				'results': '//div[@class="g"]',
				'results_content': './/div[@class="IsZvec"]',
				'results_title': './/h3[1]',
				'results_a': './/div[@class="yuRUbf"]/a',
				'results_cite': './/div[@class="yuRUbf"]/a//cite'
			}
			self.xpath_original = {
				self.xpath_name_original['results']: [
					self.xpath_name_original['results_content'],
					self.xpath_name_original['results_title'],
					self.xpath_name_original['results_a'],
					self.xpath_name_original['results_cite']
				]
			}
		self.url = 'https://www.google.com/search'
		self._pages = ''
		self._first_page = ''
		self.limit = limit + 1
		self.count = count

	def run_crawl(self):
		page = 1
		set_page = lambda x: (x - 1) * self.count
		payload = {'num': self.count, 'start': set_page(page), 'ie': 'utf-8', 'oe': 'utf-8', 'q': self.q, 'filter': '0'}
		max_attempt = 0
		while True:
			self.framework.verbose(f"[GOOGLE] Searching in {page} page...", end='\r')
			try:
				req = self.framework.request(
					url=self.url,
					params=payload,
					headers={'user-agent': self.agent},
					allow_redirects=True)
			except Exception as e:
				self.framework.error(f"ConnectionError: {e}", 'util/google', 'run_crawl')
				max_attempt += 1
				if max_attempt == self.limit:
					self.framework.error('Google is missed!', 'util/goolge', 'run_crawl')
					break
			else:
				if req.status_code in (503, 429):
					self.framework.error('Google CAPTCHA triggered.', 'util/google', 'run_crawl')
					break

				if req.status_code in (301, 302):
					redirect = req.headers['location']
					req = self.framework.request(url=redirect, allow_redirects=False)

				self._pages += req.text
				if page == 1:
					self._first_page += req.text
				page += 1
				payload['start'] = set_page(page)
				if page >= self.limit:
					break

	@property
	def google_card_original(self):
		card_xpath_name = {
			'card': '//div[@id="wp-tabs-container"]',
			'card_content': './/div[@class="kno-rdesc"]',
			'card_info': './/div[@class="rVusze"]'
		}
		xpath = {
			card_xpath_name['card']: [
				card_xpath_name['card_content'],
				card_xpath_name['card_info']
			]
		}
		parser = self.framework.page_parse(self._first_page)
		xpath_results = parser.html_fromstring(xpath)
		output = {'content': '', 'info': []}
		root = xpath_results[card_xpath_name['card']]
		output['content'] = root[card_xpath_name['card_content']][0].text_content()
		for piece in root[card_xpath_name['card_info']]:
			output['info'].append(piece.text_content())
		return output

	@property
	def results_original(self):
		parser = self.framework.page_parse(self._pages)
		xpath_results = parser.html_fromstring(self.xpath_original)
		results = []
		if not xpath_results:
			return results
		root = xpath_results[self.xpath_name_original['results']]
		for i in range(len(root[self.xpath_name_original['results_a']])):
			result = {
				't': root[self.xpath_name_original['results_title']][i].text_content(),
				'a': root[self.xpath_name_original['results_a']][i].get('href'),
				'c': root[self.xpath_name_original['results_cite']][i].text_content(),
				'd': root[self.xpath_name_original['results_content']][i].text_content(),
			}
			results.append(result)
		return results

	@property
	def google_card_legacy(self):
		card_xpath_name = {
			'card': '//div[@class="ezO2md"]',
			'card_content': './/span[@class="qXLe6d FrIlee"]',
			'card_info': './/div[@class="tRBhqc"]'
		}
		xpath = {
			card_xpath_name['card']: [
				card_xpath_name['card_content'],
				card_xpath_name['card_info']
			]
		}
		parser = self.framework.page_parse(self._first_page)
		xpath_results = parser.html_fromstring(xpath)
		output = {'content': '', 'info': []}
		root = xpath_results[card_xpath_name['card']]
		output['content'] = root[card_xpath_name['card_content']][0].text_content().strip()
		for piece in root[card_xpath_name['card_info']]:
			output['info'].append(piece.text_content().strip())
		return output

	@property
	def results(self):
		parser = self.framework.page_parse(self._pages)
		xpath_results = parser.html_fromstring(self.xpath_legacy)
		results = []
		if not xpath_results:
			return results
		root = xpath_results[self.xpath_name_legacy['results']]
		for i in range(len(root[self.xpath_name_legacy['results_cite']])):
			a = root[self.xpath_name_legacy['results_a']][i].get('href')
			a = a[7:a.find('&sa=U&ved=')]
			result = {
				't': root[self.xpath_name_legacy['results_title']][i].text_content(),
				'a': a,
				'c': root[self.xpath_name_legacy['results_cite']][i].text_content(),
				'd': root[self.xpath_name_legacy['results_content']][i].text_content().strip(),
			}
			results.append(result)
		return results

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		if self.mode == 'legacy':
			links = [x['a'] for x in self.results]
		else:
			links = [x['a'] for x in self.results_original]
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
