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
		'name': 'Wikipedia Search',
		'author': 'Tarunesh Kumar',
		'version': '0.1',
		'description': 'Search your query in the Wikipedia and show the results.',
		'sources': ('google','duckduckgo', 'yahoo', 'bing', 'yippy', 'metacrawler', 'millionshort', 'carrot2', 'qwant'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store'),
			('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('wikipedia -q <QUERY> -l 15 --output',)
	}

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engine = self.options['engine'].split(',')
		q = f"site:en.wikipedia.org {query}"
		yippy_q = f'"en.wikipedia.org" {query}'
		millionshort_q = f'site:en.wikipedia.org "{query}"'

		run = self.google(q, limit, count)
		run.run_crawl()
		links = run.links
		titles = []

		if 'duckduckgo' in engine:
			run = self.duckduckgo(q,limit,count)
			run.run_crawl()
			links += run.links

		if 'bing' in engine:
			run = self.bing(q, limit, count)
			run.run_crawl()
			links += run.links

		if 'yahoo' in engine:
			run = self.yahoo(q, limit, count)
			run.run_crawl()
			links += run.links

		if 'yippy' in engine:
			run = self.yippy(yippy_q)
			run.run_crawl()
			links += run.links

		if 'metacrawler' in engine:
			run = self.metacrawler(yippy_q, limit)
			run.run_crawl()
			links += run.links

		if 'millionshort' in engine:
			run = self.millionshort(millionshort_q, limit)
			run.run_crawl()
			links += run.links

		if 'carrot2' in engine:
			run = self.carrot2(q)
			run.run_crawl()
			links += run.links

		if 'qwant' in engine:
			run = self.qwant(q, limit)
			run.run_crawl('webpages')
			links += run.links

		links = list(set(links))
		filtered_links = []
		if links == []:
			self.output('Without result')
		else:
			self.alert('Links')
			for link in links:
				if 'en.wikipedia.org/wiki' in link:
					filtered_links.append(link)
					title = link.replace('https://en.wikipedia.org/wiki/','').replace('/',' ')
					title = title.replace('_',' ')
					title = self.urlib(title).unquote
					titles.append(title)
					self.output(title,'G')
					self.output(f'\t{link}')
			

		self.save_gather({'titles':titles, 'links': filtered_links},
						 'search/wikipedia', query, output=self.options.get('output'))
