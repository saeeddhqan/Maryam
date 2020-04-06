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


class Module(BaseModule):

	meta = {
		'name': 'Carrot2 Search',
		'author': 'Saeeddqn',
		'version': '0.1',
		'description': 'Search your query in the carrot2.org and get result.',
		'sources': ('carrot2',),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('carrot2 -q <QUERY>',)
	}

	def module_run(self):
		query = self.options['query']
		run = self.carrot2(query)
		run.run_crawl()
		json_links = run.json_links
		out = 0
		for link in json_links:
			self.output(link.get('title'), 'C')
			self.output(f"\t{link.get('url')}")
			out = 1

		if not out:
			self.output('Without result')

		self.save_gather(json_links, 'search/carrot2', query, output=self.options['output'])
