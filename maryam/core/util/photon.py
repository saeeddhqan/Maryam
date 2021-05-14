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

	def __init__(self, q, limit):
		"""
		photon uses osm data for locations and reverse geolocation
		q       :   query
		limit   :   max result count
		"""

		self.framework = main.framework
		self.q = q.split('_')[0]
		self.lat = q.split('_')[1]
		self.lon = q.split('_')[2]
		self._pages = ''
		self._json = {}
		self.ph = 'https://photon.komoot.io/'

	def run_crawl(self):
		urls = [f"{self.ph}api/?",f"{self.ph}reverse?"]
		if self.q and self.lat and self.lon:
			if self.q == 'q':
				url = urls[1]
				payloads = {'lat': self.lat, 'lon': self.lon}
			else:
				url = urls[0]
				payloads = {'q': self.q, 'lat': self.lat, 'lon': self.lon}
		else:
			url = urls[0]
			payloads = {'q': self.q}
		self.framework.verbose("[PHOTON]Searching in photon.komoot.io...")
		try:
			req = self.framework.request(
				url = url,
				params = payloads
			)
			result = req.text
			result_json = req.json()
		except:
			self.framework.error('ConnectionError', 'util/photon', 'run_crawl')
		else:
			if 'message' in req.text:
				self.framework.verbose(f"[PHOTON] Search ended with the message: {req.json()['message'].split(',')[0]}")
		self._pages = result
		self._json = result_json

	@property
	def pages(self):
		return self._pages

	@property
	def json(self):
		return self._json