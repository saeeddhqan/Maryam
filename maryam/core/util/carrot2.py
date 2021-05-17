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
import webbrowser

class main:

	def __init__(self, q):
		""" carrot2.org search engine

			q 		  : Query for search
		"""
		self.framework = main.framework
		self.q = q
		self._pages = ''
		self._json = {}
		self.etools = 'https://www.etools.ch/partnerSearch.do'

	def run_crawl(self):
		params = {'country': 'web', 'dataSourceResults': 40, 
				'dataSources': 'all', 'language': 'en', 'maxRecords': 200, 'partner': 'Carrot2Json', 
				'query': self.q, 'safeSearch': 'false'}
		headers = {'Host': 'www.etools.ch', 
				   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0',
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
				   'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br', 
				   'Connection': 'keep-alive', 'Cookie': 'JSESSIONID=6120E7C52197190DE5126DCBF47D38B0', 
				   'Upgrade-Insecure-Requests': '1', 'Cache-Control': 'max-age=0'}
		self.framework.debug(f"[eTOOLS] Searching in 'etools.ch'...")
		try:
			req = self.framework.request(url=self.etools, params=params, headers=headers, allow_redirects=True)
		except:
			self.framework.error('ConnectionError.', 'util/carrot2', 'run_crawl')
			self.framework.error('eTOOLS is missed!', 'util/carrot2', 'run_crawl')
		else:
			self._pages = req.text
			try:
				self._json = req.json()
			except:
				self.framework.error('eTOOLS is missed!', 'util/carrot2', 'run_crawl')

	@property
	def pages(self):
		return self._pages

	@property
	def results(self):
		resp = self._json.get('response')
		results = []
		if resp:
			merged_records = resp.get('mergedRecords')
			for result in merged_records:
				print(result)
				results.append({
					't': result['title'], 
					'a': result['url'], 
					'c': self.framework.meta_search_util().make_cite(result['url']),
					'd': result['text']})
		return results

	@property
	def links(self):
		self._links = []
		resp = self._json.get('response')
		if resp:
			resp = resp.get('mergedRecords')
			for link in resp:
				self._links.append(link.get('url'))
		return self._links

	@property
	def json(self):
		return self._json

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q)
