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

import datetime

class main:

	def __init__(self, q, count=20, sortby='relevance', verbose=False):
		""" Reddit search engine

				q         : query for search
				count     : maximum result count
				verbose   : print entire json 
		"""
		self.framework = main.framework
		self.q = q
		self.count = count
		self.sortby = sortby
		self._json = {}
		self._posts = []
		self._verbose = verbose

	def run_crawl(self):
		self.framework.verbose('[REDDIT] Searching the reddit domain...')
		url = f'https://gateway.reddit.com/desktopapi/v1/search'
		payload = {
			'q': self.q,
			'sort': self.sortby,
			't': 'all'
		}

		for _ in range(self.count//25+1):
			try:
				res = self.framework.request(
						url, 
						params=payload,
				)

			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/osint/reddit', 'run_crawl')
				self.framework.error('Reddit is missed!', 'util/osint/reddit', 'run_crawl')

			else:
				self._json.update(res.json())
				self._posts.extend(list(self._json['posts'].values()))

	@property
	def json(self):
		return self._json

	@property
	def posts(self):
		return self._posts

	@property
	def results(self):
		results = []
		for count, post in enumerate(self._posts, 1):
			if count > self.count:
				break

			date = datetime.datetime.fromtimestamp(int(post['created'])//1000).strftime("%m/%d/%Y, %H:%M:%S")

			media = post['media']
			if media is not None:
				type = media['type']

				if type == 'embed':
					desc = media['content']

				elif type == 'text':
					desc = media.get('markdownContent')

				elif type == 'video':
					desc = 'Video description currently not supported'

				elif type == 'gallery':
					desc = []
					for item in media['gallery']['items']:
						id = item['mediaId']
						desc.append(media['mediaMetadata'][id]['s']['u'])
					desc = '\n'.join(desc)

				elif type == 'image':
					desc = media['content']

			elif post['source'] is not None:
				desc = post['source']['url']

			else:
				desc = 'Description not available'

			results.append({
				't': post['title'],
				'a': post['permalink'],
				'c': f"author: {post['author']} | date: {date}",
				'd': desc
			})

		return results

