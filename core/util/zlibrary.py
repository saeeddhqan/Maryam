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
import math
from bs4 import BeautifulSoup

class main:

	def __init__(self, query, exact, start_year, end_year, lang, extension, count):
		""" Search in the Zlibrary for books and articles
		
			query		: query to seach for
			exact		: match exact string
			start_year	: year from which to search for
			end_year	: year till which to search for
			lang		: language to search in
			extension	: file extension i.e. pdf etc.
			count		: no. of results to show
		"""
		self.framework = main.framework
		self.query = query
		self.exact = exact
		self.start_year = start_year
		self.end_year = end_year
		self.lang = lang
		self.extension = extension
		self.count = count
		self.limit = math.ceil(count/50) # No. of pages to scrap. 50 entries per page so total = ceil of limit/50
		self._books_data = ''
		self._articles_data = ''
		self.original_rand_agent_val = self.framework._global_options['rand_agent']
		self.framework._global_options['rand_agent'] = True
	
	# Adding destructor to set global option to same as before
	def __del__(self):
		self.framework._global_options['rand_agent'] = self.original_rand_agent_val
				
	def search_all(self, url, payload, source):
		scrap_result = ''
		self.framework.verbose(f'[Zlibrary Search] Fetching query in {source}...')
		cookies = {'zlib-searchView':'table'} # Cookie needed for table view instead of list
		total_entries = 0
		
		for page_no in range(1, self.limit+1):
			if 'On your request nothing has been found' in scrap_result:
				self.framework.alert('[Zlibrary Search] No data found, moving to next task...')
				return scrap_result

			self.framework.verbose(f'[Zlibrary Search] Fetching page {page_no}...')
			total_entries += 50 # 50 table entries present per page

			try:
				scrap_result += self.framework.request(f"{url}{payload}&page={page_no}" , cookies=cookies).text
			except Exception as e:
				self.framework.error(f"Zlibrary {source}, page {page_no} is missed!", 'util/zlibrary', 'search_all')
	
		return scrap_result

	def search(self):
		self.framework.verbose('[Zlibrary Search] Fetching location of servers...')
		welcome_page_url = 'https://z-lib.org/'
		
		try:
			response = self.framework.request(welcome_page_url)
		except Exception as e:
			self.framework.error(f"Zlibrary is missed!", 'util/zlibrary', 'search')
			return False
		else:	
			parsed_html = BeautifulSoup(response.text, features='lxml')

			zlib_books_url = parsed_html.body.find('span', attrs={'class': 'domain-check-domain', 'data-mode': 'books'}).text
			zlib_articles_url = parsed_html.body.find('span', attrs={'class': 'domain-check-domain', 'data-mode': 'articles'}).text

			payload_books = f"/s/{self.query}/?e={int(self.exact)}&yearFrom={self.start_year}&"+\
			f"yearTo={self.end_year}&language={self.lang}&extension={self.extension}"
			payload_articles = f"/s/{self.query}/?e={int(self.exact)}&yearFrom={self.start_year}&yearTo={self.end_year}"
			# Language and extension options not present in article search so payloads different
			
			# Appending https:// else url invalid
			self._books_data = self.search_all(f"https://{zlib_books_url}", payload_books, 'books') 
			self._articles_data = self.search_all(f"https://{zlib_articles_url}", payload_articles, 'articles')

	@property
	def books_data(self):
		return self._books_data
			
	@property
	def articles_data(self):
		return self._articles_data
