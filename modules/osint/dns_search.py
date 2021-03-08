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
import json
from socket import gethostbyaddr

class Module(BaseModule):

	meta = {
		'name': 'DNS Searcher',
		'author': 'Saeeddqn',
		'version': '2.5',
		'description': 'Search in the open-sources to find subdomans.',
		'sources': ('bing', 'google', 'yahoo', 'yandex', 'metacrawler', 'ask', 'baidu', 'startpage',
					'netcraft', 'threatcrowd', 'virustotal', 'yippy', 'otx', 'carrot2', 'crt',
					'qwant', 'millionshort', 'threatminer', 'jldc', 'bufferover', 'rapiddns', 'certspotter',
					'sublist3r', 'riddler', 'sitedossier', 'duckduckgo'),
		'options': (
			('domain', BaseModule._global_options['target'],
			 False, 'Domain name without https?://', '-d', 'store'),
			('limit', 3, False, 'Search limit(number of pages, default=3)', '-l', 'store'),
			('count', 30, False, 'number of results per page(min=10, max=100, default=30)', '-c', 'store'),
			('engines', 'otx', False, 'Search engine names. e.g bing,google,...[otx by default]', '-e', 'store'),
			('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store'),
			('max', False, False, 'Using all of sources(max limit=15, max count=50)', '--max', 'store_true'),
			('validate', False, False, 'Validate the domains(Remove dead subdomains) \
				found and display their IP(default=False)', '--validate', 'store_true'),
			('silent', False, False, 'Output without any color and message([Warn]This sets the \
				value of verbosity to zero!, default=False)', '--silent', 'store_true'),
			('reverse', None, False, 'Use reverse DNS search. \
				Input could be a list of ip addresses(with comma separator)\
				 or could be a filename that contains ip addresses', '-r', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true')
		),
		'examples': ('dns_search -d example.com --output', 'dns_search -d example.com -e \
			google,bing,yahoo -l 3 -t 3 --output', 
					 'dns_search -d example.com --max --validate --silent --output',
					 'dns_search --reverse 1.1.1.1,2.2.2.2,3.3.3.3',
					 'dns_search --reverse ips.txt')
	}

	hostnames = []

	def set_data(self, lst):
		for sub in lst:
			if '%' not in sub:
				self.hostnames.append(sub)		

	def riddler(self, q):
		self.verbose('[RIDDLER] Searching in reddler...')
		try:
			req = self.request(
				f"https://riddler.io/search?q=pld:{q}&view_type=data_table")
		except Exception as e:
			self.error('Riddler is missed!')
		else:
			j = self.page_parse(req.text).get_dns(q) or []
			self.hostnames.extend(j)
		return 'riddler'

	def sitedossier(self, q):
		self.verbose('[SITEDOSSIER] Searching in reddler...')
		next_page = ''
		while True:
			try:
				req = self.request(
					f"http://www.sitedossier.com/parentdomain/{q}/{next_page}")
			except Exception as e:
				self.error('Sitedossier is missed!')
				break
			else:
				text = req.text
				if 'We apologise for any inconvenience this may cause.' in text:
					self.verbose('[SITEDOSSIER] Unusual Activity!')
					break
				next_page = re.search(r'<a href="/parentdomain/[\w\.\-]+/([\d]+)">', req.text)
				if next_page:
					next_page = next_page.group(1)
				j = self.page_parse(req.text).get_dns(q) or []
				self.hostnames.extend(j)
				if next_page == None:
					break
				self.output(f"[SITEDOSSIER] Searching in the {next_page} page...")
		return 'sitedossier'

	def threatcrowd(self, q):
		self.verbose('[THREATCROWD] Searching in threatcrowd...')
		try:
			req = self.request(
				'https://threatcrowd.org/searchApi/v2/domain/report/?domain=' + q)
		except Exception as e:
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
		self.verbose('[THREATMINER] Searching in threatminer...')
		try:
			req = self.request(
				f"https://api.threatminer.org/v2/domain.php?q={q}&rt=5")
		except Exception as e:
			self.error('ThreatMiner is missed!')
		else:
			j = req.json()['results'] or []
			self.hostnames.extend(j)
		return 'threatminer'

	def rapiddns(self, q):
		self.verbose('[RAPIDDNS] Searching in rapiddns...')
		try:
			req = self.request(
					'https://rapiddns.io/subdomain/' + q + '?full=1')
		except Exception as e:
			self.error('Rapiddns is missed!')
		else:
			j = self.page_parse(req.text).get_dns(q) or []
			self.hostnames.extend(j)
		return 'rapiddns'

	def certspotter(self, q):
		self.verbose('[CERTSPOTTER] Searching in certspotter...')
		try:
			req = self.request(
				f"https://api.certspotter.com/v1/issuances?domain=\
				{q}&include_subdomains=true&expand=dns_names")
		except Exception as e:
			self.error('CERTSPOTTER is missed!')
		else:
			text = req.text
			if "rate_limit" in text:
				self.error('[CERTSPOTTER] Too many request please try again later')
				return "certspotter"
			j = self.page_parse(req.text).get_dns(q) or []
			self.hostnames.extend(j)
		return 'certspotter'

	def sublist3r(self, q):
		self.verbose('[SUBLIST3R] Searching in sublist3r...')
		try:
			req = self.request(
				'https://api.sublist3r.com/search.php?domain=' + q)
		except Exception as e:
			self.error('SUBLIST3R is missed!')
		else:
			text = json.loads(req.text)
			self.hostnames.extend(text)
		return 'SUBLIST3R'

	def jldc(self, q):
		self.verbose('[JLDC] Searching in jldc.me...')
		try:
			req = self.request(
				'https://jldc.me/anubis/subdomains/' + q)
		except Exception as e:
			self.error('JLDC is missed!')
		else:
			if 'Too many request' in req.text:
				self.error('[JLDC] Too many request please try again later')
				return 'jldc'
			j = list(req.json()) or []
			self.hostnames.extend(j)
		return 'jldc'

	def bufferover(self, q):
		self.verbose('[BUFFEROVER] Searching in bufferover.run...')
		try:
			req = self.request(
				f'https://dns.bufferover.run/dns?q=.{q}')
		except Exception as e:
			self.error('BufferOver is missed!')
		else:
			j = list(req.json()['FDNS_A']) or []
			self.hostnames.extend([(x.split(',')[1] if len(x.split(',')) == 2 else x) for x in j])
		return 'bufferover'

	def otx(self, q):
		self.verbose('[OTX] Searching in otx.alienvault...')
		try:
			req = self.request(
				f"https://otx.alienvault.com/api/v1/indicators/domain/{q}/passive_dns")
		except Exception as e:
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
		engine = getattr(self, name)
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

	def reverse_dns(self, ips):
		reg_ip = self.reglib().ip_m
		if not re.search(reg_ip, ips):
			r = self._is_readable(ips)
			if not r:
				self.output("Invalid filename: " + ips)
				return
			ips = [x.replace('\n', '') for x in r.readlines() if re.search(reg_ip, x)]
		else:
			ips = ips.split(',')

		data = []
		titles = ['hostnames', 'ip_address_list', 'alias_list']
		for i, ip in enumerate(ips):
			tire = ()
			try:
				hostname, alias_list, addr_list = gethostbyaddr(ip)
				tire += (hostname,)
				tire += (','.join(addr_list),)
				tire += (','.join(alias_list),) if alias_list else ('-',)
				data.append(tire)
			except: 
				self.output('Invalid IP address: ' + ip)
				continue
		self.table(data, header=titles, title='REVERSE DNS')

	def module_run(self):
		domain = self.options['domain']
		reverse = self.options['reverse']
		if reverse:
			self.reverse_dns(reverse)
			return
		if not domain:
			self.output('Domain name has not been set.', 'R')
			return
		domain_attr = self.urlib(domain)
		domain = domain_attr.sub_service('http')
		domain_name = self.urlib(domain).netloc
		MAX = self.options['max']
		limit = 15 if MAX else self.options['limit']
		count = 50 if MAX else self.options['count']
		engines = self.options['engines']
		verb = self._global_options['verbosity']
		if self.options['silent']:
			self._global_options['verbosity'] = 0
		if engines == None:
			engines = 'otx'
		engines = self.meta['sources'] if MAX else self.options['engines'].lower().split(',')
		self.thread(self.search, self.options['thread'], engines, domain_name, limit, count)
		self.hostnames = list(set(self.hostnames))

		if self.options['validate']:
			validate_hosts = []
			for sub in self.hostnames:
				sub = re.sub(r'^\*\.', '', sub)
				if re.search(r'[^\w\d\.\-]+', sub):
					continue
				try:
					ip = self.urlib("http://" + sub).ip
				except:
					pass
				else:
					sub = f"{sub} {ip}"
					validate_hosts.append(sub)
			self.hostnames = list(set(validate_hosts))

		if not self.options['output']:
			if self.hostnames == []:
				self.output('No hostname found', 'O')
			else:
				for host in self.hostnames:
					print(f"{host}")

		self._global_options['verbosity'] = verb
		self.save_gather(self.hostnames, 'osint/dns_search', domain_name,\
		 output=self.options['output'])
