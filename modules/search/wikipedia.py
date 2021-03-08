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

from core.module import BaseModule
from pprint import pprint

class Module(BaseModule):
	meta = {
		'name': 'Wikipedia Search',
		'author': 'Tarunesh Kumar',
		'version': '0.1',
		'description': 'Search your query in the Wikipedia and show the results.',
		'sources': ('wikipedia',),
		'options': (
			('query', None, True, 'Query String', '-q', 'store'),
			('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('wikipedia -q <QUERY> -c 15 --output',)
	}

	def module_run(self):
		query = self.options['query']
		count = self.options['count']
		wiki = self.wikipedia(query, count)
		target = ""
		output = {}
		
		if isinstance(query,str):
			wiki.search()
			links_with_title = wiki.links_with_title

			self.alert('Links')
			for link, title, pid in links_with_title:
				self.output(f'{title}[{pid}]','G')
				self.output(f'\t{link}')

			target = query
			output['Titles'] = wiki.titles
			output['Links'] = wiki.links

		else:
			output = wiki.page()
			page = {**output}
			target = page.pop('title',query)
			description = page.pop('extract')
			header = ['Key','Value']
			self.table(page.items(),header, title=target)
			self.heading('Description')
			pprint(description,width=80)
		

		self.save_gather(output, 'search/wikipedia', target, output=self.options.get('output'))		




