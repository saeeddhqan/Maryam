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
	'name': 'Etools Search',
	'author': 'Saeed',
	'version': '0.1',
	'description': 'Search your query in the etools.ch and show the results.',
	'sources': ('etools',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
	),
	'examples': ('etools -q <QUERY>',)
}

def module_api(self):
	query = self.options['query']
	run = self.etools(query)
	run.run_crawl()
	results = run.results
	output = {'results': results}
	self.save_gather(output, 'search/etools', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
