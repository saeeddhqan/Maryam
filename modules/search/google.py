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
	'name': 'Google Search',
	'author': 'Saeed',
	'version': '0.5',
	'description': 'Search your query in the google.com and show the results.',
	'sources': ('google',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store', int),
	),
	'examples': ('google -q <QUERY> -l 15 --output --api',)
}

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	run = self.google(query, limit, count, 'legacy')
	run.run_crawl()
	results = run.results
	output = {'results': results}
	self.save_gather(output, 'search/google', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
