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

from lxml import html


class main:
	def __init__(self, q):
		""" google.com image search engine
			q     : Query for search
		"""
		self.framework = main.framework
		self.q = q
		self.agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
		self.xpath_name_original = {
			'results': '//div[@class="isv-r PNCib MSM1fd BUooTd"]',
			'results_content': './/img',
			'results_title': './/h3',
			'results_a': './/a',
			'results_cite': './/div[@class="dmeZbb"]'
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

	def run_crawl(self):
		payload = {'ie': 'utf-8', 'oe': 'utf-8', 'q': self.q, 'filter': '0', 'tbm': 'isch'}
		self.framework.verbose(f"[GOOGLE Images] Searching...", end='\r')
		try:
			req = self.framework.request(
				url=self.url,
				params=payload,
				headers={'user-agent': self.agent},
				allow_redirects=True)
		except Exception as e:
			self.framework.error(f"ConnectionError: {e}", 'util/google_images', 'run_crawl')
			self.framework.error('Google is missed!', 'util/google_images', 'run_crawl')
		else:
			if req.status_code in (503, 429):
				self.framework.error('Google CAPTCHA triggered.', 'util/google_images', 'run_crawl')
				return
			if req.status_code in (301, 302):
				redirect = req.headers['location']
				req = self.framework.request(url=redirect, allow_redirects=False)

			self._pages += req.text

	@property
	def results(self):
		tree = html.fromstring(self._pages)
		output = []
		results = []
		results = tree.xpath(self.xpath_name_original['results'])
		for i in results:
			a = i.xpath(self.xpath_name_original['results_content'])
			b = i.xpath(self.xpath_name_original['results_title'])
			c = i.xpath(self.xpath_name_original['results_a'])
			d = i.xpath(self.xpath_name_original['results_cite'])
			roler = {}
			if all([a,b,c,d]):
				if 'https://' not in a[0].values()[0]:
					continue
				roler['i'] = a[0].values()[0]
				roler['t'] = b[0].text_content()
				roler['a'] = c[1].get('href')
				roler['d'] = d[0].text_content()
			output.append(roler)
		return output

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
