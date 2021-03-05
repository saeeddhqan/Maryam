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
import re

class Module(BaseModule):
	meta = {
		'name': 'Business Linkedin Search',
		'author': 'Dimitrios Papageorgiou',
		'version': '0.1',
		'description': 'Search your query in the Business Linkedin and show the results.',
		'sources': ('google', 'yahoo', 'bing', 'yippy', 'metacrawler', 'millionshort', 'carrot2', 'qwant'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store'),
			('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('business_linkedin -q <QUERY> -l 15 --output',)
	}

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engine = self.options['engine'].split(',')
		q = f"site:business.linkedin.com {query}"
		meta_q = f'"business.linkedin.com" {query}'

		run = self.google(q, limit, count)
		run.run_crawl()
		links = run.links

		if 'bing' in engine:
			run = self.bing(q, limit, count)
			run.run_crawl()
			links.extend(run.links)

		if 'yahoo' in engine:
			run = self.yahoo(q, limit, count)
			run.run_crawl()
			links.extend(run.links)

		if 'yippy' in engine:
			run = self.yippy(meta_q)
			run.run_crawl()
			links.extend(run.links)

		if 'metacrawler' in engine:
			run = self.metacrawler(meta_q, limit)
			run.run_crawl()
			links.extend(run.links)

		if 'millionshort' in engine:
			run = self.millionshort(q, limit)
			run.run_crawl()
			links.extend(run.links)

		if 'carrot2' in engine:
			run = self.carrot2(q)
			run.run_crawl()
			links.extend(run.links)

		if 'qwant' in engine:
			run = self.qwant(q, limit)
			run.run_crawl()
			links.extend(run.links)

		regex = re.compile(r"https?:\/\/business\.linkedin\.com/")
		links = filter(regex.match, links)
		links = list(set(links))
		if links == []:
			self.output('Without result')
		else:
			for link in links:
				self.output(f"\t{link}", "G")

		self.save_gather({'links': links},
						 'search/business_linkedin', query, output=self.options.get('output'))