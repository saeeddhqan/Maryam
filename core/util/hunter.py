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
import json
class main:

	def __init__(self, framework, q, key, limit=10):
		""" hunter.io search engine

			framework : core attribute
			q 		  : query for search
			key 	  : hunter.io api key
			limit	  : max number of email addresses (Limited to 10 on Free Plan)
		"""
		self.framework = framework
		self.q = q
		self.limit = limit
		self.key = key
		self.check = ''
		self._pages = ''
		self._json_pages = ''
		self.hunter_api = f"https://api.hunter.io/v2/domain-search?domain={self.q}&api_key={self.key}"
		self.acceptable = False
	def run_crawl(self):
		self.framework.verbose('[HUNTER] Searching in hunter...')
		try:
			req = self.framework.request(self.hunter_api)
		except:
			self.framework.debug('[HUNTER] ConnectionError')
			self.framework.error('Hunter is missed!')
			return
		self._pages = req.text
		#print(self._pages)
		self._json_pages = req.json()
		print(self._json_pages)
        # Key validation
		if 'errors' in self._json_pages:
			self.check = self._json_pages['details']
			self.framework.error(f"[HUNTER] email extraction error:{self.log}")
			self.acceptable = False
			return

		# Request validation
		if not self._json_pages.get('data').get('accept_all'):
			self.framework.verbose('[HUNTER] request was not accepted!')
		else:
			self.acceptable = True

	@property
	def pages(self):
		return self._pages
	
	@property
	def json_pages(self):
		return self._json_pages

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def json_emails(self):
		emails = []
		if self.acceptable:
			for email in self._json_pages.get('data')['emails']:
				emails.append(email.get('value'))
			return emails
		return []
	
	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)
