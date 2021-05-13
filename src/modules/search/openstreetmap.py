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
	'name': 'Openstreetmap',
	'author': 'Kunal Khandelwal',
	'version': '0.1',
	'description': "OpenStreetMap is the free wiki world map",
	'sources': ('openstreetmap',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
	),
	'examples': ('openstreetmap -q <QUERY>',)
}


def module_api(self):
	query = self.options['query']
	run = self.openstreetmap(query)
	run.run_crawl()
	results = run.results
	output = {'results': results}
	self.save_gather(output, 'search/openstreetmap', query, output=self.options['output'])
	return output

def module_run(self):
	output = module_api(self)['results']
	for item in output:
		print()
		if item['category'] != '':
			self.output(item['category'])
		self.output(item['location'])
		coordinates = f"{item['latitude']}, {item['longitude']}"
		self.output(coordinates)
		self.output(item['link'])
