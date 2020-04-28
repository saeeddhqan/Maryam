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
		'name': 'Millionshort Search',
		'author': 'Saeeddqn',
		'version': '0.1',
		'description': 'Million Short started out as an experimental web search engine that allows you to filter and refine your search results set',
		'sources': ('millionshort',),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('millionshort -q <QUERY> -l 15 --output',)
	}

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		run = self.millionshort(query, limit)
		run.run_crawl()
		links = run.links_with_title
		if links == {}:
			self.output('Nothing to declare')
		else:
			for item in links:
				self.output(f"\t{item.replace('<b>','').replace('</b>', '')}", 'C')
				self.output(f"\t\t{links[item]}")
				print('')

		self.save_gather(links, 'search/millionshort', query, output=self.options['output'])
