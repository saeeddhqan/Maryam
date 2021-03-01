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
		'name': 'Instagram Search',
		'author': 'Aman Singh',
		'version': '0.2',
		'description': 'Search your query in the Instagram and show the results.',
		'sources': ('google', 'carrot2', 'bing', 'yippy'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store'),
			('engine', 'google,carrot2', False, 'Engine names for search(default=google)', '-e', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('instagram -q <QUERY> -l 15 --output',)
	}

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engine = self.options['engine'].split(',')
		google_q = f"site:www.instagram.com inurl:{query}"
		bing_q = f"site:www.instagram.com {query}"
		yippy_q = f"www.instagram.com {query}"

		run = self.google(google_q, limit, count)
		run.run_crawl()
		links = run.links
		people = []
		hashtags = []
		posts = []
		pages = run.pages

		if 'bing' in engine:
			run = self.bing(bing_q, limit, count)
			run.run_crawl()
			pages += run.pages
			for item in run.links_with_title:
				link,title = item
				self.verbose(f"\t{title}", 'C')
				self.verbose(f"\t\t{link}")
				self.verbose('')
				links.append(link)

		if 'carrot2' in engine:
			run = self.carrot2(google_q)
			run.run_crawl()
			pages += run.pages
			for item in run.json_links:
				link = item.get('url')
				self.verbose(item.get('title'), 'C')
				self.verbose(f"\t{link}")
				links.append(link)

		if 'yippy' in engine:
			run = self.yippy(yippy_q)
			run.run_crawl()
			links += run.links

		usernames = self.page_parse(pages).get_networks
		self.alert('People')
		for _id in list(set(usernames.get('Instagram'))):
			if isinstance(_id, (tuple, list)):
				_id = _id[0]
				if _id[-2:] == "/p" or _id[-8:] == '/explore':
					continue
				_id = f"@{_id[_id.find('/')+1:]}"
			else:
				if _id[-2:] == "/p" or _id[-8:] == '/explore':
					continue
				_id = f"@{_id[_id.find('/')+1:]}"

			if _id not in people:
				people.append(_id)
				self.output(f'\t{_id}', 'G')

		links = list(set(links))
		if links == []:
			self.output('Without result')
		else:
			self.alert('Hashtags')
			for link in links:
				if '/explore/tags/' in link:
					tag = link.replace('https://www.instagram.com/explore/tags/', '').replace('/', '')
					if re.search(r'^[\w\d_\-\/]+$', tag):
						hashtags.append(tag)
						self.output(f"\t#{tag}", 'G')

			self.alert('Posts')
			for link in links:
				if re.search(r'instagram\.com/p/[\w_\-0-9]+/', link):
					post = link.replace('https://www.', '')
					posts.append(post)
					self.output(f'\t{post}', 'G')

		self.save_gather({'posts': posts, 'people': people, 'hashtags': hashtags}, 'search/instagram', query, output=self.options.get('output'))
