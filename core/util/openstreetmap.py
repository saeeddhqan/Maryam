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

	def __init__(self, q):
		"""
		openstreetmap search engine for places
		q       :   query
		limit   :   max result count
		"""

		self.framework = main.framework
		self.q = self.framework.urlib(q).quote
		self._pages = ''
		self.xpath_name = {
			'results': '//li[@class="list-group-item search_results_entry"]',
			'results_a': './a',
		}
		self.xpath = {
			self.xpath_name['results']: [
				self.xpath_name['results_a']
			]
		}

	def run_crawl(self):
		urls = [f"https://www.openstreetmap.org/geocoder/search_geonames?query={self.q}",
				f"https://www.openstreetmap.org/geocoder/search_osm_nominatim?query={self.q}"]
		self.framework.verbose('Searching openstreetmap...')

		for url in urls:
			try:
				req = self.framework.request(url=url)
			except Exception as e:
				self.framework.error(f"ConnectionError {e}", 'util/openstreetmap', 'run_crawl')
				self.framework.error('Openstreetmap is missed!', 'util/openstreetmap', 'run_crawl')
				return
			else:
				self._pages += req.text

	@property
	def pages(self):
		return self._pages

	@property
	def results(self):
		results = []
		parser = self.framework.page_parse(self._pages)
		xpath_results = parser.html_fromstring(self.xpath)
		if not xpath_results:
			return results
		root = xpath_results[self.xpath_name['results']]
		for i in range(len(root[self.xpath_name['results_a']])):
			if root[self.xpath_name['results_a']][i].get('data-prefix') is not None:
				category = root[self.xpath_name['results_a']][i].get('data-prefix')
			else:
				category = ''
			link = f"https://www.openstreetmap.org{root[self.xpath_name['results_a']][i].get('href')}"
			result = {
				'category': category,
				'location': root[self.xpath_name['results_a']][i].get('data-name'),
				'latitude': root[self.xpath_name['results_a']][i].get('data-lat'),
				'longitude': root[self.xpath_name['results_a']][i].get('data-lon'),
				'link': link
			}
			results.append(result)

		return results
