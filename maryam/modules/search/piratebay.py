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
	'name': 'Piratebay',
	'author': 'Kaushik',
	'version': '0.1',
	'description': "Piratebay is the world's most persistent torrenting site. \
		 Please refrain from abusive usage.",
	'sources': ('piratebay',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('count', 15, False, 'Max result count (default=15)', '-c', 'store', int),
	),
	'examples': ('piratebay -q <QUERY> -l 15 --output',)
}

def module_api(self):
	query = self.options['query']
	count = self.options['count']
	run = self.piratebay(query, count)
	run.run_crawl()
	output = {'results': []}
	links = run.results

	for item in links:
		output['results'].append(item)

	self.save_gather(output, 'search/piratebay', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
