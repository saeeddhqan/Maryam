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
	'name': 'Duckduckgo d.js',
	'author': 'Vikas Kundu',
	'version': '0.2',
	'description': 'Search for a query using the d.js file of duckduckgo',
	'sources': ('Google Pagespeed API', 'DuckDuckGo'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
	),
	'examples': ('d_js -q <QUERY>',)
}


def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	run = self.duckduckgo(query, limit)
	run.d_js_run_crawl()
	results = run.d_js_results
	output = {'results': results}
	self.save_gather(output, 'search/d_js', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
