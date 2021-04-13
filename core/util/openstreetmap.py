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

    def __init__(self, q):
        """
        openstreetmap search engine for places
        q       :   query
        limit   :   max result count
        """

        self.framework = main.framework
        self.q = self.framework.urlib(q).quote
        self._places = []
        self._pages = ''

    def run_crawl(self):
        urls = [f'https://www.openstreetmap.org/geocoder/search_geonames?query={self.q}',
                f'https://www.openstreetmap.org/geocoder/search_osm_nominatim?query={self.q}']
        self.framework.verbose('Searching openstreetmap...')

        for url in urls:
            try:
                req = self.framework.request(url=url)
            except Exception as e:
                self.framework.error('ConnectionError', 'util/openstreetmap', 'run_crawl')
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
        soup = bs(self.pages, 'html.parser')
        items = soup.find_all('li', class_='list-group-item search_results_entry')
        for item in items:
            if item.a.get('data-zoom') is None:
                category = item.contents[0]
            else:
                category = ''
            anchor = item.a
            location = anchor.get_text()
            link = f"https://www.openstreetmap.org{anchor.get('href')}"
            latitude = anchor.get('data-lat')
            longitude = anchor.get('data-lon')

            result = {
                'category': category,
                'location': location,
                'latitude': latitude,
                'longitude': longitude,
                'link': link
            }
            results.append(result)

        return results
