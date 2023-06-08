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

from datetime import datetime

class main:

	def __init__(self, query, count=50, search='posts', username='', subreddit='', before='', after='', score='' ):
		""" Search in reddit using the pushshift api
		
			query		: query to seach for
			count		: no. of results to show
			search		: search in posts or comments
			username	: reddit username
			subreddit	: reddit subreddit
			before		: show data only before this timestamp
			after		: show data only after this timestamp
			score		: score of the posts or comments

		"""
		self.framework = main.framework
		self.query = query
		self.count = count
		self.search = search
		self.username = username
		self.subreddit = subreddit
		self.before = before
		self.after = after
		self.score = score
		self._usernames = set() # To ensure unique usernames
		self._links = set() # To ensure unique links
	
	def convert_to_epoch_time(self, date):
		try:		
			date_time_obj = datetime.strptime(date, '%d/%m/%y %H:%M:%S')
		except ValueError:
			self.framework.error("Reddit_pushshift timestamp format is wrong. It should be '%d/%m/%y %H:%M:%S' i.e. 7/6/21 12:0:0. This parameter is skipped!", \
			'util/reddit_pushshift', 'convert_to_epoch_time')
			return ''
		else:
			return int(date_time_obj.timestamp())
				
	def run_crawl(self):
		self.framework.verbose('[Reddit Pushshift] Searching...')
		self.before = self.convert_to_epoch_time(self.before) if self.before else self.before
		self.after = self.convert_to_epoch_time(self.after) if  self.after else self.after
		base_url = 'https://api.pushshift.io/reddit/submission/search?html_decode=true' if self.search == 'posts' \
		else 'https://api.pushshift.io/reddit/comment/search?html_decode=true'
		query_url = f"{base_url}&q={self.query}&author={self.username}&subreddit={self.subreddit}&size={self.count}&before={self.before}&after={self.after}&score={self.score}"
		
		try:
			response = self.framework.request(query_url, timeout=20) # Increased timeout for date based queries which take long
		except Exception as e:
			self.framework.error('Reddit_pushshift is missed!', 'util/reddit_pushshift', 'search')
			return False
		else:	
			data = response.json()
			for i in data['data']:
				self._usernames.add(i['author'])
				self._links.add(f"https://www.reddit.com{i['permalink']}")

	@property
	def usernames(self):
		return list(self._usernames)
			
	@property
	def links(self):
		return list(self._links)
