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
		'name': 'Youtube Search',
		'author': 'Aman Rawat',
		'version': '0.5',
		'description': 'Search your query in the youtube.com and show the results.',
		'sources': ('google', 'carrot2', 'bing', 'yippy', 'millionshort', 'qwant'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store'),
			('engine', 'google,yippy', False, 'Engine names for search(default=google)', '-e', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('youtube -q <QUERY> -l 15 --output',)
	}

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engine = self.options['engine'].split(',')
		ch_q = f"site:youtube.com inurl:/c/ OR inurl:/user/ {query}"
		q = f"site:youtube.com {query}"
		yippy_q = f"www.youtube.com {query}"
		qwant_q = f"site:www.youtube.com {query}"
		millionshort_q = f'site:www.youtube.com "{query}"'
		run = self.google(q, limit, count)
		run.run_crawl()
		links = run.links
		if links:
			run.q = ch_q
			run.run_crawl()
		pages = run.pages
		channels = []
		usernames = []
		videos = []

		if 'bing' in engine:
			run = self.bing(q, limit, count)
			run.run_crawl()
			pages += run.pages
			for item in run.links_with_title:
				link,title = item
				self.verbose(title, 'G')
				self.verbose(f'\t{link}')
				self.verbose('')
				links.append(link)

		if 'carrot2' in engine:
			run = self.carrot2(q)
			run.run_crawl()
			pages += run.pages
			for item in run.json_links:
				link = item.get('url')
				self.verbose(item.get('title'), 'G')
				self.verbose(f"\t{link}")
				links.append(link)

		if 'yippy' in engine:
			run = self.yippy(yippy_q)
			run.run_crawl()
			pages += run.pages
			links += run.links

		if 'metacrawler' in engine:
			run = self.metacrawler(yippy_q, limit)
			run.run_crawl()
			pages += run.pages
			links += run.links

		if 'millionshort' in engine:
			run = self.millionshort(millionshort_q, limit)
			run.run_crawl()
			pages += run.pages
			links += run.links

		if 'qwant' in engine:
			run = self.qwant(qwant_q, limit)
			run.run_crawl('webpages')
			pages += run.pages
			links += run.links

		links = self.reglib().filter(lambda x: '/feed/' not in \
			x and 'youtube.com' in x, list(set(links)))
		if links == []:
			self.output('Without result')
		else:
			search = self.page_parse(pages).get_networks
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

		self.save_gather({'videos': videos, 'channels': channels, 'usernames':\
			usernames}, 'search/youtube', query, output=self.options.get('output'))
