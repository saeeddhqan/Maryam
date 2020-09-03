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
		'name': 'Documentations Search',
		'author': 'Saeeddqn',
		'version': '0.8',
		'description': 'Search in open-sources to find relevant documents. filetypes[pdf,doc,docx,ppt,pptx,xlsx,txt,..].',
		'sources': ('bing', 'google', 'yahoo', 'yandex', 'metacrawler', 'ask',
			'startpage', 'exalead', 'carrot2', 'searchencrypt', 'qwant', 'millionshort'),
		'options': (
			('query', BaseModule._global_options['target'], True, 'Host Name, Company Name, keyword, query, etc', '-q', 'store'),
			('file', 'pdf', True, 'Filetype [pdf,doc,docx,ppt,pptx,xlsx,txt,..]', '-f', 'store'),
			('limit', 2, False, 'Search limit(number of pages, default=2)', '-l', 'store'),
			('count', 50, False, 'number of results per page(min=10)', '-c', 'store'),
			('site', False, False, 'If this is set, search just limited to the site', '-s', 'store_false'),
			('engines', 'exalead,bing', True, 'Search engines with comma separator', '-e', 'store'),
			('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('docs_search -q amazon -f pdf -e google,bing,metacrawler --thread 3',
			'docs_search -q amazon -f pdf -e google,bing,metacrawler -l 3')
	}
	
	docs = []

	def thread(self, function, thread_count, engines, q, limit, count):
		threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
		futures = (threadpool.submit(function, name, q, limit, count) for name in engines if name in self.meta['sources'])
		for _ in concurrent.futures.as_completed(futures):
			pass

	def search(self, name, q, limit, count):
		try:
			engine = getattr(self, name)
		except:
			self.verbose(f"Search engine {name} not found.")
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
			self.docs.extend(attr.docs)

	def module_run(self):
		q = self.options['query']
		_type = self.options['file'].lower()
		limit = self.options['limit']
		count = self.options['count']
		engines = self.options['engines'].lower().split(',')
		# Make dork
		if self.options['site']:
			dork = self.urlib(f"filetype:{_type} site:{self.options['site']} {q}").quote
		else:
			dork = f"{q} filetype:{_type}"

		self.thread(self.search, self.options['thread'], engines, dork, limit, count)

		self.docs = list(set(self.docs))
		self.alert(_type.upper())
		if self.docs != []:
			for doc in self.docs:
				self.output(f'\t{doc}')
		else:
			self.output('\tNothing to declare')
		self.save_gather({_type : self.docs}, 'osint/docs_search', q, [_type], output=self.options['output'])
