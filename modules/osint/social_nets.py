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
import concurrent.futures

class Module(BaseModule):

	meta = {
		'name': 'Get Usernames in Social Networks',
		'author': 'Saeeddqn',
		'version': '1.0',
		'description': 'Search to find Usernames in social networks.',
		'sources': ('bing', 'google', 'yahoo', 'yandex', 'metacrawler', 'ask', 'startpage'),
		'options': (
			('query', BaseModule._global_options['target'], True, 'Company Name or Query', '-q', 'store'),
			('engines', 'google,bing', False, 'Search engine names. e.g `bing,google,..`', '-e', 'store'),
			('limit', 5, False, 'Search limit(number of pages, default=5)', '-l', 'store'),
			('count', 100, False, 'number of results per page(min=10, max=100, default=100)', '-c', 'store'),
			('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store'),
			('output', False, False, 'Save output to  workspace', '--output', 'store_true'),
		),
		'examples': ('social_nets -n microsoft -e google,bing,yahoo -c 50 -t 3 --output',
			'social_nets -n microsoft -e google')
	}

	pages = ''

	def thread(self, function, thread_count, engines, q, limit, count):
		threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
		futures = (threadpool.submit(function, name, q, limit, count) for name in engines if name in self.meta['sources'])
		for _ in concurrent.futures.as_completed(futures):
			pass

	def search(self, name, q, limit, count):
		try:
			engine = getattr(self, name)
		except:
			self.debug(f"Search engine {name} not found.")
			return
		else:
			varnames = engine.__code__.co_varnames
			if 'limit' in varnames and 'count' in varnames:
				attr = engine(q, limit, count)
			elif 'limit' in varnames:
				attr = engine(q, limit)
			else:
				attr = engine(q)
			attr.run_crawl()
			self.pages += attr.pages

	def module_run(self):
		query = '@' + self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engines = self.options['engines'].lower().split(',')
		try:
			page = self.request(query).text
		except:
			page = ''
		self.pages += page
		if engines != []:
			self.thread(self.search, self.options['thread'], engines, query, limit, count)
		usernames = self.page_parse(self.pages).get_networks
		links = []
		for net in usernames:
			lst = list(set(usernames[net]))
			if lst != []:
				self.alert(net)
				for atom in lst:
					links.append(atom)
					self.output(f"\t{atom}", 'G')

		self.save_gather({'links': links}, 'osint/social_nets', query, output=self.options['output'])
