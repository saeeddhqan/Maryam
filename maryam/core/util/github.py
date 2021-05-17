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
	def __init__(self, q, limit=10, cookie=''):
		""" github.com search
			
			q	  : The query for search
			cookie	  : Your GitHub cookie
			limit	  : The number of pages
			count	  : The number of links
		"""
		self.framework = main.framework
		self.q = q
		self.cookie = cookie
		self.limit = limit
		self._pages = 10
		self._page = []
		self._links = ''
		self._emails = {}
		self.github_api = 'api.github.com'
		self.types = ['users', 'repositories']
		self.urls = [
			f"https://{self.github_api}/search/{self.types[0]}?q={self.q}&per_page={self.limit}",
			f"https://{self.github_api}/search/{self.types[1]}?q={self.q}&per_page={self.limit}&page={self._pages}"
			]
	
	def run_crawl(self):
		users = ''
		repo =  {'Github':[]}
		max_attempt = len(self.urls)
		for page in range(max_attempt):
			try:
				self.framework.verbose(f"[GITHUB] Searching in {page} page...")
				req = self.framework.request(url=self.urls[page], headers={'Cookie': self.cookie, 'Accept': 'application/vnd.github.v3.text-match+json'}, allow_redirects=True)
				result_json = req.json()
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/github', 'run_crawl')
			else:
				for results in result_json['items']:
					if 'fork' not in results:
						users = users + ''.join(results['html_url']).replace("https://", " ")
					else:
						repo['Github'].append(results['html_url'])
				self._page = repo['Github']
				self._links = users.split(' ')
		

		self.framework.verbose("[GITHUB] Searching for emails...")
		for user in self._links:
			user = user.replace('github.com/', '')
			try:
				req = self.framework.request(url=f"https://api.github.com/users/{user}/events/public", headers={'Cookie': self.cookie, 'Accept': 'application/vnd.github.v3.text-match+json'}, allow_redirects=True)
				self._emails[user] = req.json()
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/github', 'run_crawl')

	@property
	def links(self):
		return self._links

	@property
	def users(self):
		return self._links

	@property
	def repositories(self):
		return self._page
		
	@property
	def emails(self):
		result = set()
		for user, email_data in self._emails.items():
			for i in email_data:
				try:
					result.add(i['payload']['commits'][0]['author']['email'])
				except Exception as e:
			        	continue
		return list(result)
