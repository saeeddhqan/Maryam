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
	'name': 'DuckDuckGo',
	'author': 'Tarunesh Kumar',
	'version': '0.1',
	'description': 'Search your query in the duckduckgo.com and show the results.',
	'sources': ('duckduckgo',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store', int),
	),
    'examples': ('duckduckgo -q <QUERY> -l 15 --output',)
}

def module_api(self):
	query = self.options['query']
	count = self.options['count']
	run = self.duckduckgo(query, count)
	run.run_crawl()
	results = run.results
	output = {'results': results}
	self.save_gather(output, 'search/duckduckgo', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
