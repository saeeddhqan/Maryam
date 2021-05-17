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
	'name': 'Metacrawler Search',
	'author': 'Saeed',
	'version': '0.2',
	'description': 'Search your query in the metacrawler.com and show the results.',
	'sources': ('metacrawler',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
	),
	'examples': ('metacrawler -q <QUERY> -l 15 --output',)
}

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	run = self.metacrawler(query, limit)
	run.run_crawl()
	links = run.links
	output = {'links': links}
	self.save_gather(output, 'search/metacrawler', query, output=self.options['output'])
	return output

def module_run(self):
	self.alert_results(module_api(self))
