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

from bs4 import BeautifulSoup as bs

class main:

		def __init__(self, query=None, id=None, limit=15):
			""" Sanctionsearch.ofac.treas.gov search engine
					name     : Mame to search
					id       : Id to search
					limit	 : Number of results (only applicable for name search)
			"""
			self.framework = main.framework
			self._query = query
			self._listid = 'ALL'
			self._max = limit
			self._id = id
			self._json = ''
			self.sanctionsearch = 'https://sanctionssearch.ofac.treas.gov/'
			self._rows = []
			self._data = [] if self._query is not None else {}

		def name_crawl(self):
			self._query = self.framework.urlib(self._query).quote
			self.framework.verbose('Searching sanctionsearch...')
			headers = {
				'Content-Type': 'application/x-www-form-urlencoded',
				}

			try:
				# First request to get viewstate from input tag
				req = self.framework.request(url=self.sanctionsearch)
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/sanctionsearch', 'name_crawl')
				self.framework.error('Sanctionsearch is missed!', 'util/sanctionsearch', 'name_crawl')
				return

			soup = bs(req.text, 'html.parser')
			viewstate = soup.find('input',
				{'type': 'hidden',
				'name': '__VIEWSTATE',
				'id': '__VIEWSTATE'})['value']

			data = {'__VIEWSTATE': viewstate,
				'ctl00$MainContent$txtLastName': self._query,
				'ctl00$MainContent$btnSearch': 'Search'}
			try:
				req = self.framework.request(
						url=self.sanctionsearch,
						method='POST',
						data=data,
						headers=headers)
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/sanctionsearch', 'name_crawl')
				self.framework.error('Sanctionsearch is missed!', 'util/sanctionsearch', 'name_crawl')
				return

			soup = bs(req.text, 'html.parser')
			table = soup.find('table', {'id': 'gvSearchResults'})

			self._rows = table.find_all('tr') if table is not None else None

			if self._rows is not None:
				for count, row in enumerate(self._rows):
					if count  >= self._max:
						break

					name = row.find('a').text
					address = row.find_all('td')[1].text
					link = row.find('a')['href']

					self._data.append({
						'name': name,
						'address': address,
						'link': self.sanctionsearch+link
						})

		def id_crawl(self):
			self.framework.verbose('Searching sanctionsearch...')
			url = f"{self.sanctionsearch}Details.aspx?id={self._id}"
			req = self.framework.request(url=url)
			soup = bs(req.text, 'html.parser')

			# DETAILS
			details_table = soup.find('table', {'class': 'MainTable'})

			if details_table is not None:
				details_fields = map(lambda x: x.text, 
					details_table.find_all('tr'))
				details = list(filter(lambda x: len(x) > 0, 
					(''.join(details_fields)).split('\n')))

				self._data['details'] = {}
				for x,y in zip(details, details[1:]):
					if x.endswith(':') and not y.endswith(':'):
						self._data['details'][x] = y

			# IDENTIFICATION
			id_table = soup.find('table', {'id': 'ctl00_MainContent_gvIdentification'})

			if id_table is not None:
				id_th = list(map(lambda x: x.text,
					id_table.find_all('th', {'class': 'borderline'})))
				id_td = list(map(lambda x: x.text,
					id_table.find_all('td')))

				self._data['identification'] = {}
				for i in range(len(id_th)):
					if len(id_td[i].strip()) > 0:
						self._data['identification'][id_th[i]] = id_td[i]

			# AlIASES
			al_table = soup.find('table', {'id': 'ctl00_MainContent_gvAliases'})

			if al_table is not None:
				al_th = list(map(lambda x: x.text,
					al_table.find_all('th', {'class': 'borderline'})))
				al_td = list(map(lambda x: x.text,
					al_table.find_all('td')))

				self._data['aliases'] = {}
				for i in range(len(al_th)):
					if len(al_td[i].strip()) > 0:
						self._data['aliases'][al_th[i]] = al_td[i]

			# ADDRESS
			address_table_div = soup.find('div', {'id': 'ctl00_MainContent_pnlAddress'})

			if address_table_div is not None:
				address_table = address_table_div.find('table')
				address_th = list(map(lambda x: x.text, 
					address_table.find_all('th')))
				address_rows = list(filter(lambda x:len(''.join(x.text).strip()) > 0, 
					address_table.find_all('tr')))[1:]

				self._data['addresses'] = {}
				for i,row in enumerate(address_rows, 1):
					cols = list(map(lambda x: x.text.strip(),
						row.find_all('td')))
					self._data['addresses'][str(i)] = {}
					for j in range(len(cols)):
						if len(cols[j]) > 0:
							self._data['addresses'][str(i)][address_th[j]] = cols[j]

		@property
		def rows(self):
			return self._rows

		@property
		def data(self):
			return self._data
