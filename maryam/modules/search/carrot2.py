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
	'name': 'Carrot2 Search',
	'author': 'Saeed',
	'version': '0.1',
	'description': 'Search your query in the carrot2.org and show the results.',
	'sources': ('carrot2',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
	),
	'examples': ('carrot2 -q <QUERY>',)
}

def module_api(self):
	query = self.options['query']
	run = self.carrot2(query)
	run.run_crawl()
	results = run.results
	output = {'results': results}
	self.save_gather(output, 'search/carrot2', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
