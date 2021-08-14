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
	def __init__(self, q, limit=1, count=10):
		""" bing.com search engine
			q     : Query for search
			limit : Number of pages
			count : Number of results
		"""
		self.framework = main.framework
		self.q = q
		self.agent = 'Lynx/2.8.5rel.1 libwww-FM/2.15FC SSL-MM/1.4.1c OpenSSL/0.9.7e-dev'
		self.xpath_name = {
			'results': '//li[@class="b_algo"]',
			'results_content_and_cite': './/div[@class="b_caption"]',
			'results_links': './/h2/a',
		}
		self.xpath = {
			self.xpath_name['results']: [
				self.xpath_name['results_content_and_cite'],
				self.xpath_name['results_links']
			]
		}
		self.url = 'https://www.bing.com/search'
		self._pages = ''
		self._first_page = ''
		self.limit = limit + 1
		self.count = count

	def run_crawl(self):
		page = 1
		set_page = lambda x: (x - 1) * 10 + 1
		payload = {'count': self.count, 'first': set_page(page), 'form': 'QBLH', 'pq': self.q.lower(), 'q': self.q}
		max_attempt = 0
		while True:
			self.framework.verbose(f"[BING] Searching in {page} page...", end='\r')
			try:
				req = self.framework.request(
					url=self.url,
					params=payload,
					headers={'user-agent': self.agent},
					allow_redirects=True)
			except Exception as e:
				self.framework.error(f"ConnectionError: {e}", 'util/engines/bing', 'run_crawl')
				max_attempt += 1
				if max_attempt == self.limit:
					self.framework.error('Bing is missed!', 'util/engines/bing', 'run_crawl')
					break
			else:
				self._pages += req.text
				if page == 1:
					self._first_page += req.text
				page += 1
				payload['first'] = set_page(page)
				if page >= self.limit or 'title="Next page"' not in req.text:
					break
	# TODO: Finish it
	@property
	def bing_card(self):
		card_xpath_name = {
			'card': '//div[@class="lite-entcard-main"]',
			'card_names': '//div[@class="l_ecrd_hero"]',
			'card_description': './/span[@class="l_ecrd_txt_pln"]',
			'card_description_link': './/a[@class=" l_ecrd_txt_lnk l_ecrd_txt_hover"]',
			'card_social_nets': '//div[@class="l_ecrd_hero"]/div[@class="l_ecrd_webicons"]/div/a',
			'card_facts': '//div[@class="l_ecrd_qfi4_fcts"]/div[@class="l_ecrd_qfi4_fct"]',
		}
		xpath = {
			card_xpath_name['card']: [
				card_xpath_name['card_description'],
				card_xpath_name['card_description_link'],
				card_xpath_name['card_social_nets'],
				card_xpath_name['card_facts'],
			]
		}
		parser = self.framework.page_parse(self._first_page)
		xpath_results = parser.html_fromstring(xpath)
		output = {'content': '', 'source': '', 'networks': [], 'facts': []}
		root = xpath_results[card_xpath_name['card']]
		if root[card_xpath_name['card']]:
			output['content'] = root[card_xpath_name['card_names']][0].text_content().strip()
			output['content'] += '\n' + root[card_xpath_name['card_description']][0].text_content().strip()
			output['source'] = root[card_xpath_name['card_description_link']][0].get('href')
			output['networks'] = []
			output['facts'] = []
			for i in root[card_xpath_name['card_social_nets']]:
				output['networks'].append(i.get('href'))
			for i in root[card_xpath_name['card_facts']]:
				output['facts'].append(i.text_content())
		return output

	@property
	def results(self):
		parser = self.framework.page_parse(self._pages)
		xpath_results = parser.html_fromstring(self.xpath)
		results = []
		if not xpath_results:
			return results
		root = xpath_results[self.xpath_name['results']]
		for i in range(len(root[self.xpath_name['results_content_and_cite']])):
			try:
				link = root[self.xpath_name['results_links']][i]
				title = link.text_content()
				a = link.get('href')
				c_and_c = root[self.xpath_name['results_content_and_cite']][i]
				desc = c_and_c.xpath('.//p')[0].text_content()
				cite = c_and_c.xpath('.//div[@class="b_attribution"]/cite')[0].text_content().strip()
				cite = self.framework.meta_search_util().make_cite(cite)
				result = {
					't': title,
					'a': a,
					'c': cite,
					'd': desc,
				}
				results.append(result)
			except:
				pass
		return results

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		return [x['a'] for x in self.results]

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q, self.links)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
