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

	def __init__(self, title, author, limit, order):
		""" Search in the Worldcat API: http://classify.oclc.org/classify2/Classify
		
			title	: title of the book
			author	: author of the book
			limit	: maximum queries to show
			order	: order in which to show queries ascending or descending
		"""
		self.framework = main.framework
		self.title = title
		self.author = author
		self.limit = limit
		self.order = f"thold {order}"
		self._xml_data = ''
				
	def run_crawl(self):
		self.framework.verbose('[Worldcat Search] Fetching data for the query...')
		api_url = 'http://classify.oclc.org/classify2/Classify'
		url_with_payload = f'{api_url}?title={self.title}&author={self.author}&maxRecs={self.limit}&orderBy={self.order}'
		try:
			response = self.framework.request(url=url_with_payload)
		except Exception as e:
			self.framework.error('Worldcat is missed!', 'util/worldcat', 'search')
			return False
		else:
			self._xml_data = response.content

	@property
	def xml_data(self):
		return self._xml_data
