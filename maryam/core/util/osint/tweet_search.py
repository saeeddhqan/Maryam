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

from requests.exceptions import Timeout

class main:

	def __init__(self, q, limit=15, verbose=False):
		""" tweet search engine

				q         : query for search
				limit     : maximum result count
				verbose   : print entire json 
		"""
		self.framework = main.framework
		self.q = q
		self.max = limit
		self._json = {}
		self._tweets = []
		self._verbose = verbose

	def run_crawl(self):
		self.framework.verbose('[TWEETSEARCH] Searching the twitter domain...')
		self.header = {
			'authorization': ('Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNw'
					'IzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq1'
					'6cHjhLTvJu4FA33AGWWjCpTnA'),
			'x-twitter-client-language': 'en'
			}

		guest_url = 'https://api.twitter.com/1.1/guest/activate.json'
		for _ in range(5):
			try:
				res = self.framework.request(
						guest_url,
						headers=self.header, 
						method='POST',
						timeout=5)
				break

			except Timeout:
				self.framework.error('Hit timeout on guest activation, trying again', 
						'util/osint/twitter', 'run_crawl')

			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/osint/twitter', 'run_crawl')
				self.framework.error('Twitter is missed!', 'util/osint/twitter', 'run_crawl')
				return

		self.header['x-guest-token'] = res.json()['guest_token']
		search_url = f'https://twitter.com/i/api/2/search/adaptive.json'
		payload = {
			'simple_quoted_tweet': 'true',
			'q': self.q, 
			'count': self.max, 
			'query_source': 'typed_query'
			}

		for _ in range(5):
			try:
				res = self.framework.request(
						search_url, 
						params=payload,
						headers=self.header,
						timeout=5)
				break

			except Timeout:
				self.framework.error('Hit timeout on search endpoint, trying again', 
						'util/osint/twitter', 'run_crawl')

			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/osint/twitter', 'run_crawl')
				self.framework.error('Twitter is missed!', 'util/osint/twitter', 'run_crawl')
				return

		self._json = res.json()['globalObjects']['tweets']

	def lookup_id(self, uid):
		'''Can accept upto 100 uids
		'''
		if isinstance(uid, list):
			uid = ','.join(uid)

		user = self.framework.request(
				'https://api.twitter.com/1.1/users/lookup.json',
				params={'user_id': uid},
				headers=self.header).json()
		return user

	@property
	def tweets(self):
		if not self._verbose:
			for tweet in self._json.values():
				tweet = tweet.get('text').replace('\n\n', '\n')
				self._tweets.append(tweet)
			return self._tweets
		else:
			return self._json
