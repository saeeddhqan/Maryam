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
		'name': 'DNS Searcher',
		'author': 'Saeeddqn',
		'version': '1.8',
		'description': 'Search in the open-sources to find subdomans.',
		'sources': ('bing', 'google', 'yahoo', 'yandex', 'metacrawler', 'ask', 'baidu', 'startpage',
					'netcraft', 'threatcrowd', 'virustotal', 'yippy', 'otx', 'carrot2', 'crt',
					'searchencrypt', 'qwant', 'millionshort', 'threatminer', 'jldc', 'bufferover'),
		'options': (
			('domain', BaseModule._global_options['target'],
			 True, 'Domain name without https?://', '-d', 'store'),
			('limit', 3, False, 'Search limit(number of pages, default=3)', '-l', 'store'),
			('count', 30, False, 'number of results per page(min=10, max=100, default=30)', '-c', 'store'),
			('engines', None, True, 'Search engine names. e.g bing,google,..', '-e', 'store'),
			('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('dns_search -d example.com --output', 'dns_search -d example.com -e google,bing,yahoo -l 3 -t 3 --output')
	}

	hostnames = []

	def set_data(self, lst):
		for sub in lst:
			if '%' not in sub:
				self.hostnames.append(sub)

	def threatcrowd(self, q):
		self.verbose('Searching in threatcrowd...')
		try:
			req = self.request(
				'https://threatcrowd.org/searchApi/v2/domain/report/?domain=' + q)
		except:
			self.error('ThreatCrowd is missed!')
		else:
			txt = re.sub(r'[\t\n ]+', '', req.text)
			txt = re.findall(
				r'"subdomains":(\[["\.A-z0-9_\-,]+\])', txt)
			hosts = list(set(txt[0][1:-1].split(',')))
			for host in hosts:
				host = host[1:-1]
				if host.startswith('.'):
					host = host[1:]
				self.hostnames.append(host)
		return 'threatcrowd'

	def threatminer(self, q):
		self.verbose('Searching in threatminer...')
		try:
			req = self.request(
				f'https://api.threatminer.org/v2/domain.php?q={q}&rt=5')
		except:
			self.error('ThreatMiner is missed!')
		else:
			j = req.json()['results'] or []
			self.hostnames.extend(j)
		return 'threatminer'

	def jldc(self, q):
		self.verbose('[JLDC] Searching in jldc.me...')
		try:
			req = self.request(
				f'https://jldc.me/anubis/subdomains/{q}')
		except:
			self.error('JLDC is missed!')
		else:
			if 'Too many request' in req.text:
				self.error('[JLDC] Too many request please try again later')
				return 'jldc'
			j = list(req.json()) or []
			self.hostnames.extend(j)
		return 'jldc'

	def bufferover(self, q):
		self.verbose('Searching in bufferover.run...')
		try:
			req = self.request(
				f'https://dns.bufferover.run/dns?q=.{q}')
		except:
			self.error('BufferOver is missed!')
		else:
			j = list(req.json()['FDNS_A']) or []
			self.hostnames.extend([x.replace(',', ', ') for x in j])
		return 'bufferover'

	def otx(self, q):
		self.verbose('Searching in otx.alienvault...')
		try:
			req = self.request(f'https://otx.alienvault.com/api/v1/indicators/domain/{q}/passive_dns')
		except:
			self.error("OTX is missed!")
		else:
			parser = self.page_parse(req.text).get_dns(q)
			for host in list(set(parser)):
				if host.startswith('.'):
					host = host[1:]
				self.hostnames.append(host)
		return 'otx'

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
			if attr not in ('otx', 'threatcrowd'):
				attr.run_crawl()
				self.set_data(attr.dns)

	def module_run(self):
		domain = self.options['domain']
		domain_attr = self.urlib(domain)
		domain = domain_attr.sub_service('http')
		domain_name = self.urlib(domain).netloc
		limit = self.options['limit']
		count = self.options['count']
		engines = self.options['engines'].lower().split(',')

		self.thread(self.search, self.options['thread'], engines, domain_name, limit, count)
		self.hostnames = list(set(self.hostnames))
		if not self.options['output']:
			self.alert('Hostnames')
			if self.hostnames == []:
				self.output('\tNo hostname found', 'O')
			else:
				for host in self.hostnames:
					self.output(f"\t{host}")

		self.save_gather(self.hostnames, 'osint/dns_search', domain_name, output=self.options['output'])
