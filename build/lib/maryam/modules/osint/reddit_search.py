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

from json import dumps

meta = {
	'name': 'Reddit Search',
	'author': 'Kaushik',
	'version': '0.1',
	'description': 'Search tweets from twitter',
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('count', 15, False, 'Max result count (default=15)', '-l', 'store', int),
		('sortby', 'relevance', False, 'Sort resuts by (relevance|hot|top|new|comments)', '-s', 'store', str),
		('verbose', False, False, 'Print all post details as json', '-v', 'store_true', bool),
	),
	'examples': ('reddit_search -q <QUERY> -l 15',
		'reddit_search -q <QUERY> -l 15')
}


def module_api(self):
	query = self.options['query']
	count = self.options['count']
	sortby = self.options['sortby']
	verbose = self.options['verbose']

	run = self.reddit(query, count, sortby, verbose)
	run.run_crawl()

	output = {'results': run.results}

	self.save_gather(output, 'osint/twitter', query, output=self.options['output'])
	return output

	

def module_run(self):
	output = module_api(self)
	self.search_engine_results(output)
