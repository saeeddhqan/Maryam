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
import concurrent.futures


class Module(BaseModule):
	
	meta = {
		'name': 'Youtube Search',
		'author': 'Aman Rawat',
		'version': '0.5',
		'description': 'Search your query in the youtube.com and show the results.',
		'sources': ('google', 'carrot2', 'bing', 'yippy', 'yahoo', 'millionshort', 'qwant', 'duckduckgo'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store'),
			('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store'),
			('engine', 'google,yippy', False, 'Engine names for search(default=google)', '-e', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('youtube -q <QUERY> -l 15 --output',)
	}

	links = []
	pages = ''

	def set_data(self, urls):
		for url in urls:
			self.links.append(url)

	def thread(self, function, thread_count, engines, q, q_formats, limit, count):
		threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
		futures = (threadpool.submit(
			function, name, q, q_formats, limit, count) for name in engines if name in self.meta['sources'])
		for _ in concurrent.futures.as_completed(futures):
			pass

	def search(self, name, q, q_formats, limit, count):
		engine = getattr(self, name)
		name = engine.__name__

		q = f"{name}_q" if f"{name}_q" in q_formats else q_formats['default_q']

		varnames = engine.__code__.co_varnames

		if 'limit' in varnames and 'count' in varnames:
			attr = engine(q, limit, count)
		elif 'limit' in varnames:
			attr = engine(q, limit)
		else:
			attr = engine(q)

		attr.run_crawl()
		self.set_data(attr.links)
		self.pages += attr.pages

		if name == 'google':
			attr.q = q_formats['ch_q']
			attr.run_crawl()
			self.set_data(attr.links)

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engine = self.options['engine'].split(',')
		q_formats = {
			'ch_q': f"site:youtube.com inurl:/c/ OR inurl:/user/ {query}",
			'default_q': f"site:youtube.com {query}",
			'yippy_q': f"www.youtube.com {query}",
			'qwant_q': f"site:www.youtube.com {query}",
			'millionshort_q': f'site:www.youtube.com "{query}"',
		}

		channels = []
		usernames = []
		videos = []
		self.thread(self.search, self.options['thread'], engine, query, q_formats, limit, count)

		links = self.reglib().filter(lambda x: '/feed/' not in
			x and 'youtube.com' in x, list(set(self.links)))
		if not links:
			self.output('Without result')
		else:
			search = self.page_parse(self.pages).get_networks
			self.alert('usernames')
			for user in set(search['Youtube user']):
				self.output(f'\t{user}', 'G')
				usernames.append(user)
			self.alert('channels')
			for chan in set(search['Youtube channel']):
				self.output(f'\t{chan}', 'G')
				channels.append(chan)

			self.alert('videos and playlists')
			for video in self.reglib().filter(lambda x: '/watch?' in x.lower() or '/playlist?' in x.lower(), links):
				self.output(f'\t{video}', 'G')
				videos.append(video)

		self.save_gather({'videos': videos, 'channels': channels, 'usernames':
			usernames}, 'search/youtube', query, output=self.options.get('output'))
