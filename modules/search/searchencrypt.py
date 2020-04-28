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
		'name': 'searchencrypt Search',
		'author': 'Saeeddqn',
		'version': '0.1',
		'description': 'Search your query in the searchencrypt.com and get result.',
		'sources': ('searchencrypt',),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('method', 'webpages', False, 'Searchencrypt methods("webpages", "images", "news"). default=None', '-m', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('searchencrypt -q <QUERY>', 'searchencrypt -q <QUERY> -m images')
	}

	def module_run(self):
		query = self.options['query']
		run = self.searchencrypt(query)
		method = self.options['method'].lower()
		if method not in ('webpages', 'images', 'news'):
			self.error(f'Method name "{method}" is incurrect!')
			self.verbose('Running with "webpages" method...')
			method = 'webpages'
		run.run_crawl(method)
		links = run.links_with_title

		if links == {}:
			self.output('Nothing to declare')
		else:
			for item in links:
				self.output(f"\t{item.replace('<b>','').replace('</b>', '')}", 'C')
				self.output(f"\t\t{links[item]}")
				print('')

		self.save_gather(links, 'search/searchencrypt', query, output=self.options['output'])
