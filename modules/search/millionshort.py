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
	'name': 'Millionshort Search',
	'author': 'Saeeddqn',
	'version': '0.1',
	'description': 'Million Short started out as an experimental \
	web search engine that allows you to filter and refine your search results set.',
	'sources': ('millionshort',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store'),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
	),
    'examples': ('millionshort -q <QUERY> -l 15 --output',)
}

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	run = self.millionshort(query, limit)
	run.run_crawl()
	output = {'titles' : [], 'links' : []}
	links = run.links_with_title
	
	for link, title in links.items():
		output['links'].append(link)
		output['titles'].append(title)


	self.save_gather(output, 'search/millionshort', query, output=self.options['output'])
	return output

def module_run(self):
	self.alert_results(module_api(self))