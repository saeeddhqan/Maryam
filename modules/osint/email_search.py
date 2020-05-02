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
		'name': 'Email Searcher',
		'author': 'Saeeddqn',
		'version': '0.5',
		'description': 'Search in open-sources to find emails.',
		'sources': ('bing', 'google', 'yahoo', 'yandex', 'metacrawler', 
					'ask', 'baidu', 'startpage', 'hunter', 'yippy', 'qwant'),
		'options': (
			('query', BaseModule._global_options['target'], True, 'Domain name or company name', '-q', 'store'),
			('limit', 3, False, 'Search limit(number of pages, default=3)', '-l', 'store'),
			('count', 50, False, 'number of results per page(min=10, max=100, default=50)', '-c', 'store'),
			('engines', 'google,metacrawler', True, 'Search engine names. e.g bing,google,..', '-e', 'store'),
			('key', None, False, 'hunter.io api key', '-k', 'store'),
			('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store'),
			('output', False, False, 'Save output to  workspace', '--output', 'store_true'),
		),
		'examples': ('email_search -q microsoft.com -e bing --output',
			'email_search -q owasp.org -e google,bing,yahoo -l 20 -t 3 --output')
	}

	emails = []

	def thread(self, function, thread_count, engines, domain, q, limit, count, key):
		threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
		futures = (threadpool.submit(function, name, domain, q, limit, count, key) for name in engines if name in self.meta['sources'])
		for _ in concurrent.futures.as_completed(futures):
			pass

	def search(self, name, domain, q, limit, count, key=None):

		try:
			engine = getattr(self, name)
		except:
			self.debug(f"Search engine {name} not found.")
			return
		else:
			varnames = engine.__code__.co_varnames
			if name == 'ask':
				q = q.replace('"', '')
			if 'key' in varnames:
				if not key:
					self.error('--key option is require to search for hunter.io')
					return
				attr = engine(domain, key)
				attr.run_crawl()
				self.emails.extend(attr.json_emails)
				return
			if 'limit' in varnames and 'count' in varnames:
				attr = engine(q, limit, count)
			elif 'limit' in varnames:
				attr = engine(q, limit)
			else:
				attr = engine(q)
			attr.run_crawl()
			self.emails.extend(attr.emails)

	def module_run(self):
		domain = self.options['query'].replace('@', '')
		urlib = self.urlib(domain)
		domain = self.urlib(domain).netroot if '/' in domain else domain
		limit = self.options['limit']
		count = self.options['count']
		engines = self.options['engines'].split(',')
		q = f'"%40{domain}"'

		self.thread(self.search, self.options['thread'], engines, domain, q, limit, count, self.options.get('key'))

		self.alert('Emails')
		emails = list(set(self.emails))
		if emails == []:
			self.output('Nothing to declare', 'O')
		for email in emails:
			self.output(f"\t{email}")

		self.save_gather(emails, 'osint/email_search', domain, output=self.options['output'])
