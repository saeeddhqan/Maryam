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
import datetime

class main:

	def __init__(self, q, limit=20, verbose=False, daterange=-1):
		""" tweet search engine

				q         : query for search
				limit     : maximum result count
				verbose   : print entire json 
				daterange : time range to fetch tweets for
		"""
		self.framework = main.framework
		self.q = q
		self.max = limit
		self._json = {}
		self._tweets = {}
		self._verbose = verbose
		self._daterange = daterange

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

		else:
			return

		self.header['x-guest-token'] = str(res.json()['guest_token'])

		if self._daterange == -1:
			self._search()
		else:
			self._datewise()
	
	def _search(self, date=None):
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
		else:
			return

		if date is None:
			self._json.update(res.json()['globalObjects']['tweets'])
		else:
			self._json[date] = res.json()['globalObjects']['tweets']

	def _datewise(self):
		base = datetime.datetime.today()
		date_list = [(base - datetime.timedelta(days=x)).strftime('%Y-%m-%d') \
				for x in range(self._daterange+1)]
		suffix = lambda x,y: f" until:{x} since:{y}"
		orig_q = self.q\

		for x,y in zip(date_list, date_list[1:]):
			self.q = orig_q + suffix(x,y)
			self._search(date=x)

	def lookup_id(self, uid):
		'''Can accept upto 100 uids separated by ','
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
			if self._daterange == -1:
				self._tweets['all'] = []
				for tweet in self._json.values():
					tweet = tweet.get('text').replace('\n\n', '\n')
					self._tweets['all'].append(tweet)
			else:
				for day in self._json:
					self._tweets[day] = []
					for tweet in self._json[day]:
						tweet = self._json[day][tweet].get('text').replace('\n\n', '\n')
						self._tweets[day].append(tweet)
			return self._tweets
			
		else:
			return self._json
