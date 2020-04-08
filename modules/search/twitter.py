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
		'name': 'Twitter Search',
		'author': 'Saeeddqn',
		'version': '0.1',
		'description': 'Search your query in the twitter.com and get result.',
		'sources': ('google','carrot2','bing'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(count of pages)', '-l', 'store'),
			('count', 50, False, 'Number of links per page(min=10, max=100)', '-c', 'store'),
			('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('twitter -q <QUERY> -l 15 --output',)
	}

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engine = self.options['engine'].split(',')
		q = f"{query} site:twitter.com"
		run = self.google(q, limit, count)
		run.run_crawl()
		links = run.links

		if 'bing' in engine:
			run = self.bing(q, limit, count)
			run.run_crawl()
			for item in run.links_with_title:
				link,title = item
				self.output(f'\t{title}', 'C')
				self.output(f'\t\t{link}')
				print('')
				links.append(link)

		if 'carrot2' in engine:
			run = self.carrot2(q)
			run.run_crawl()
			for item in run.json_links:
				link = item.get('url')
				self.output(item.get('title'), 'C')
				self.output(f"\t{link}")
				links.append(link)

		if links == []:
			self.output('Without result')
		else:
			for link in links:
				self.output(f'\t{link}')

		self.save_gather(links, 'search/twitter', query, output=self.options.get('output'))
