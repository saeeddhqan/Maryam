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
	'author': 'Saeeddqn',
	'version': '0.1',
	'description': 'Search your query in the carrot2.org and show the results.',
	'sources': ('carrot2',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store'),
	),
    'examples': ('carrot2 -q <QUERY>',)
}


def module_api(self):
	query = self.options['query']
	run = self.carrot2(query)
	run.run_crawl()
	output = {'titles' : [], 'links' : []}
	json_links = run.json_links

	for raw_data in json_links:
		output['titles'].append(raw_data.get('title',''))
		output['links'].append(raw_data.get('url',''))

	self.save_gather(json_links, 'search/carrot2', query, output=self.options['output'])
	return output


def module_run(self):
	self.alert_results(module_api(self))