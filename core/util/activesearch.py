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
import urllib.parse
import html

class main:

		def __init__(self, q, limit=15):
			""" activesearchresults.com search engine

					q         : query for search
					limit     : maximum result count
			"""
			self.framework = main.framework
			self.q = q
			self._max = limit
			self._cookie = ''
			self._rawhtml = ''
			self._clubbedrows = []
			self._rows = []
			self._links = []
			self._links_with_data = []
			self._pageno = 0
			self.active_search = 'www.activesearchresults.com'
			

		def run_crawl(self):
			payload = { 
				'wordsall': self.q,
				'asrtech' : 'yes',
				'perpage' : '100',
				'adultfilter': '5',
				'buttonall': ''
				}
			header = {
				'Cookie' : f'{self._cookie}'
				}

			self.framework.verbose('Searching the activesearchresults domain...')

			while True:
				self._pageno += 1
				url = f'https://{self.active_search}/searchsubmit.php?pageno={self._pageno}'

				try:
					req = self.framework.request(url=url,
						method='POST',
						data=payload,
						headers=header
						)
				except:
					self.framework.error('[ACTIVESEARCH] ConnectionError')
					self.framework.error('activesearchresults is missed!')
					return

				self._rawhtml += req.text

				if self._pageno==1:
					max_pages = list(map(int, re.findall(
						r"<a href='/searchsubmit.php\?pageno=(\d*?)'>LAST",
						req.text)))

					if len(max_pages)==0:
						print(req.text)
						print(max_pages)
						print("Cant find max pages text")
						print(payload)
						break

					else:
						max_pages = max_pages[0]

					self._cookie = req.headers.get('Set-Cookie')


				if self._pageno > max_pages or self._pageno*100>self._max:
					break
					    
			self._clubbedrows = '\n'.join(re.findall(r'<small>(.*?)</small>',
				self._rawhtml,
				flags=re.DOTALL))

			self._rows = re.findall(r'<a.*?<hr>', 
				self._clubbedrows, 
				flags=re.DOTALL)

			self._links = re.findall(r"<a href='(.*?)'.*?>.*?<br>",
				self._clubbedrows)[:self._max]

		@property
		def raw(self):
			return self._rawhtml

		@property
		def rows(self):
			return self._rows

		@property
		def links(self):
			return self._links

		@property
		def dns(self):
			return self.framework.page_parse(self._rawhtml).get_dns(self.q)

		@property
		def emails(self):
			return self.framework.page_parse(self._rawhtml).get_emails(self.q)

		@property
		def docs(self):
			return self.framework.page_parse(self._rawhtml).get_docs(self.q, self.links)

		@property
		def links_with_data(self):
			findlink = lambda x: re.findall(r"<a href='(.*?)'.*?>.*?<br>", x)
			findtitle = lambda x: list(map(
				html.unescape,
				re.findall(r"<a href='.*?'.*?>(.*?)</a>.*?<br>", 
					x, 
					flags=re.DOTALL)))

			for count, row in enumerate(self._rows):
				if count>self._max:
					break

				self._links_with_data.append({
					'title': findtitle(row)[0],
					'link' : findlink(row)[0]
					})


			return self._links_with_data 
