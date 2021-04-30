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

meta = {
	'name': 'Photon Search',
	'author': 'Divya Goswami',
	'version': '1.0',
	'description': 'Search-as-you-type and typo tolerant geolocator. Works as reverse geocoder too.',
	'sources': ('photon.komoot.io',),
	'options': (
		('query', '', False, 'Enter a location name', '-q', 'store', str),
		('latitude', '', False, 'Enter latitude', '-lat', 'store', str),
		('longitude', '', False, 'Enter longitude', '-lon', 'store', str),
		('limit', 3, False, 'Search limit(number of results, default=not set)', '-l', 'store', int),
		('engine', 'photon', False, 'Engine used is photon', '-e', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
	'examples': ('photon -q berlin --output', 
				'photon -q berlin -lat 52 -lon 13',
				'photon -lat 10 -lon 52'
				)
	}

def module_api(self):
	global PAGES, JSON
	query = self.options['query']
	lat = self.options['latitude']
	lon = self.options['longitude']
	limit = self.options['limit']
	engine = self.options['engine']
	output = {}
	q_formats = {
		'detail': f"{query}_{lat}_{lon}",
		'reverse': f"q_{lat}_{lon}"
	}
	if query == '':
		query = q_formats['reverse']
	else:
		query = q_formats['detail']
	run = self.photon(query, limit)
	run.run_crawl()
	PAGES = run.pages
	JSON = run.json
	output = JSON
	self.save_gather(output, 'search/photon', query, output=self.options.get('output'))
	return output

def module_run(self):
	output = module_api(self)['features']
	final = []
	for item in range(len(output)):
		self.output(output[item]['properties']['type'].title())
		self.output(f"Coordinates: {output[item]['geometry']['coordinates']}")
		properties = output[item]['properties']
		prop_k = list(properties.keys())
		for x in prop_k:
			if x not in ['osm_id','osm_type','osm_key','osm_value','countrycode','type','extent','postcode']:
				final.append(properties[x])
		self.output(', '.join(set(final)))
		final = []
		print()
