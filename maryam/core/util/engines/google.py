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
		"""
		self.framework = main.framework
		self.q = q
		self.agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
		self.xpath_name_original = {
			'results': '//div[@class="g"]|//div[@class="g tF2Cxc"]',
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
	def google_card(self):
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
		card_xpath_second = {
			'card': '//div[@class="SzZmKb"]',
			'card_img': './/g-img/@data-lpage',
			'card_name': './/h2[@class="qrShPb kno-ecr-pt PZPZlf mfMhoc"]',
			'card_known_as': './/div[@data-attrid="subtitle"]'
		}
		xpath2 = {
			card_xpath_second['card']: [
				card_xpath_second['card_img'],
				card_xpath_second['card_name'],
				card_xpath_second['card_known_as']
			]
		}
		card_xpath_social = {
			'card': '//g-link[@class="fl"]',
			'card_href': './/a',
		}
		xpath3 = {
			card_xpath_social['card']: [
				card_xpath_social['card_href']
			]
		}
		parser = self.framework.page_parse(self._first_page)
		xpath_results = parser.html_fromstring(xpath)
		xpath_results2 = parser.html_fromstring(xpath2)
		xpath_results3 = parser.html_fromstring(xpath3)
		output = {'content': '', 'info': []}
		root = xpath_results[card_xpath_name['card']]
		root2 = xpath_results2[card_xpath_second['card']]
		root3 = xpath_results3[card_xpath_social['card']]
		if root[card_xpath_name['card_content']]:
			output['content'] = root[card_xpath_name['card_content']][0].text_content()
		else:
			card_xpath_name = {
				'card': '//div[@class="LuVEUc B03h3d P6OZi V14nKc ptcLIOszQJu__wholepage-card wp-ms"]',
				'card_content': './/div[@class="kno-rdesc"]',
				'card_info': './/div[@class="rVusze"]'
			}
			xpath = {
				card_xpath_name['card']: [
					card_xpath_name['card_content'],
					card_xpath_name['card_info']
				]
			}
			xpath_results = parser.html_fromstring(xpath)
			root = xpath_results[card_xpath_name['card']]
			if root[card_xpath_name['card_content']]:
				output['content'] = root[card_xpath_name['card_content']][0].text_content()
			else:
				output['content'] = ''
		img = root2[card_xpath_second['card_img']]
		name = root2[card_xpath_second['card_name']]
		known_as = root2[card_xpath_second['card_known_as']]
		if img:
			output['img'] = img[0]
		if name:
			output['name'] = name[0].text_content()
		if known_as:
			output['known_as'] = known_as[0].text_content()
		for piece in root[card_xpath_name['card_info']]:
			output['info'].append(piece.text_content())
		social = root3[card_xpath_social['card_href']]
		output['social'] = []
		for piece in social:
			output['social'].append(piece.get('href'))
		return output

	@property
	def results(self):
		parser = self.framework.page_parse(self._pages)
		results = parser.get_engine_results(self.xpath_original, self.xpath_name_original)
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
