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

	def __init__(self, q, limit=2):
		""" startpage.com search engine

			q 		  : Query for search
			limit	  : Number of pages
		"""
		self.framework = main.framework
		self.q = self.framework.urlib(q).quote
		self.limit = limit
		self.xpath_name = {
			'results': '/html/body/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/section[2]/div',
			'results_content': './/div[1]/p',
			'results_links': './/div[1]/div[2]/a',
			'results_title': './/div[1]/div[2]/a/h3'
		}
		self.xpath = {
			self.xpath_name['results']: [
				self.xpath_name['results_content'],
				self.xpath_name['results_links'],
				self.xpath_name['results_title']
			]
		}
		self._pages = ''
		self.startpage = 'startpage.com'

	def run_crawl(self):
		url = f"https://{self.startpage}/sp/search"

		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0',
			'Content-Type': 'application/x-www-form-urlencoded'
		}

		data = {
				'query': self.q
		}

		self.framework.verbose(f"[STARTPAGE] Searching in {self.startpage}...")

		for i in range(self.limit):
			data['page'] = i

			try:
				req = self.framework.request(
						url=url,
						method='POST',
						headers=headers,
						data=data
				)
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/startpage', 'run_crawl')
				self.framework.error('Startpage is missed!', 'util/startpage', 'run_crawl')
				return

			else:
				page = req.text
				self._pages += page

				if '> Next <' not in page:
					break


	@property
	def results(self):
		parser = self.framework.page_parse(self._pages)
		xpath_results = parser.html_fromstring(self.xpath)
		results = []
		if not xpath_results:
			return results
		root = xpath_results[self.xpath_name['results']]
		for i in range(len(root[self.xpath_name['results_links']])):
			link = root[self.xpath_name['results_links']][i].get('href')
			title = root[self.xpath_name['results_title']][i].text_content().strip()
			desc = root[self.xpath_name['results_content']][i].text_content().strip()
			cite = self.framework.meta_search_util().make_cite(link)
			result = {
				't': title,
				'a': link,
				'c': cite,
				'd': desc,
			}
			results.append(result)
		return results

	@property
	def pages(self):
		return self._pages

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q)
