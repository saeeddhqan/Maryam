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

	def __init__(self, framework, q):
		""" yippy.com search engine

			framework : core attribute
			q 		  : query for search
		"""
		self.framework = framework
		self.q = q
		self.limit = limit
		self.count = count
		self._pages = ''
		self._links = []
		self.yippy = 'yippy.com'

	def run_crawl(self):
		reg = r"<a href=\"(https://?[^\"]+)\" class=\"title\""
		geturl = f"http://{self.yippy}/search?query={self.q}"
		self.framework.verbose('Opening the yippy.com domain...', end='\r')
		try:
			req = self.framework.request(url=geturl)
		except:
			self.framework.error('[YIPPY] ConnectionError')
			self.framework.error('Yippy is missed!')
			return

		txt = req.text
		self._links = [x.replace('<a href="', '') for x in re.findall(reg, txt)]
		self._pages = txt
		root = re.search(r'(root-[\d]+-[\d]+%7C[\d]+)">next</', txt)
		if root:
			root = root.group()
			file = re.search(r'%3afile=([A-z0-9_\-\.]+)&amp', txt)
			if not file:
				self.framework.error('Yippy is missed!')
				return
			file = file.group()
			root = re.sub(r'[\d]+-[\d]+', '0-8000', root)
			newurl = f"https://yippy.com/ysa/cgi-bin/query-meta?v{file};v:state=root|" + root.replace('">next</', '')
			self.framework.verbose('Making next page link...', end='\r')
			try:
				req = self.framework.request(url=newurl)
			except:
				self.framework.error('[YIPPY] ConnectionError')
				self.framework.error('Yippy is missed!')
				return
			self._pages += req.text
			self._links.extend([x.replace('<a href="', '').replace(' class="title"', '') for x in re.findall(reg, self._pages)])
	
	def crawl_with_response_filter(self, policy):
		policies = {'webpages': 'https://www.yippy.com/oauth/bing_yxml_api.php',
					'images': 'https://www.yippy.com/oauth/bing_yxml_api_images.php',
					'news': 'https://www.yippy.com/oauth/bing_yxml_api_news.php',
					'video': 'https://www.yippy.com/oauth/bing_yxml_api_video.php'}
		policy = policy.lower()
		if policy not in policies:
			baseurl = policies['webpages']
		else:
			baseurl = policies[policy]

		url = f"{baseurl}?safeSearch=off&textDecorations=true&count=1000&offset=0&mkt=en-US&textFormat=HTML&q={self.q}"
		req = self.framework.request(url=url)
		if req.status_code == 429:
			self.framework.error('Rate limit is exceeded. Try again in 26 seconds.')
			return
		self._pages += req.text
		links = re.findall(r"<!\[CDATA\[([^\]]+)\]\]>", req.text)
		self._links.extend(links)

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		return self._links
	
	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
