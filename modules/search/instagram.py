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
		'name': 'Instagram Search',
		'author': 'Aman Singh',
		'version': '0.2',
		'description': 'Search your query in the Instagram and show the results.',
		'sources': ('google', 'carrot2', 'bing', 'yippy', 'yahoo', 'millionshort', 'qwant', 'duckduckgo'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store'),
			('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store'),
			('engine', 'google,carrot2', False, 'Engine names for search(default=google)', '-e', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('instagram -q <QUERY> -l 15 --output',)
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

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engine = self.options['engine'].split(',')

		q_formats = {
			'google_q': f"site:www.instagram.com inurl:{query}",
			'default_q': f"site:www.instagram.com {query}",
			'yippy_q': f"www.instagram.com {query}"
		}

		people = []
		hashtags = []
		posts = []
		self.thread(self.search, self.options['thread'], engine, query, q_formats, limit, count)

		usernames = self.page_parse(self.pages).get_networks
		self.alert('people')
		for _id in list(set(usernames.get('Instagram'))):
			if _id[-2:] == "/p" or _id[-8:] == '/explore':
				continue
			_id = f"@{_id[_id.find('/')+1:]}"

			if _id not in people:
				people.append(_id)
				self.output(f'\t{_id}', 'G')

		links = list(set(self.links))
		if not links:
			self.output('Without result')
		else:
			self.alert('hashtags')
			for link in self.reglib().filter(lambda x: '/explore/tags/' in x, links):
				tag = re.sub(r'https?://(www\.)?instagram\.com/explore/tags/', '', link)
				if re.search(r'^[\w\d_\-\/]+$', tag):
					tag = tag.rsplit('/')
					hashtags.append(tag[0])
					self.output(f"\t#{tag[0]}", 'G')

			self.alert('posts')
			for link in self.reglib().filter(r'https?://(www\.)?instagram\.com/p/[\w_\-0-9]+/', links):
				post = re.sub(r'https?://(www\.)?', '', link)
				posts.append(post)
				self.output(f'\t{post}', 'G')

		self.save_gather({'posts': posts, 'people': people, 'hashtags': hashtags},
						 'search/instagram', query, output=self.options.get('output'))
