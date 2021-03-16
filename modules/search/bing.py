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
	'name': 'Bing Search',
	'author': 'Saeeddqn',
	'version': '0.1',
	'description': 'Search your query in the bing.com and show the results.',
	'sources': ('bing',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store'),
		('limit', 1, False, 'Search limit(count of pages, default=1)', '-l', 'store'),
		('count', 50, False, 'The number of results per page(min=10, max=100, default=50)', '-c', 'store'),
	),
    'examples': ('bing -q <QUERY> -l 15 --output',)
}

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	run = self.bing(query, limit, count)
	run.run_crawl()
	output = {'titles' : [], 'links' : []}
	results = run.links_with_title
	
	for link, title in results:
		output['links'].append(link)
		output['titles'].append(title)

	self.save_gather(output, 'search/bing', query, output=self.options['output'])
	return output

def module_run(self):
	self.alert_results(module_api(self))
