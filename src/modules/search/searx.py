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
	'name': 'Searx Search',
	'author': 'Aman Singh',
	'version': '0.1',
	'description': 'Searx is a Privacy-respecting metasearch engine.',
	'sources': ('searcx',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
	),
	'examples': ('searx -q <QUERY> -l 5 --output',)
}

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	run = self.searx(query, limit)
	run.run_crawl()
	results = run.results
	output = {'results': results}
	self.save_gather(output, 'search/searx', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
