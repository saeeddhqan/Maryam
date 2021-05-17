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

import re
import json
from socket import gethostbyaddr

meta = {
	'name': 'DNS Searcher',
	'author': 'Saeed',
	'version': '2.5',
	'description': 'Search in the open-sources to find subdomans.',
	'sources': ('securitytrails', 'bing', 'google', 'yahoo', 'yandex', 'metacrawler', 'ask', 'baidu', 'startpage',
				'netcraft', 'threatcrowd', 'virustotal', 'otx', 'carrot2', 'crt',
				'qwant', 'millionshort', 'threatminer', 'jldc', 'bufferover', 'rapiddns', 'certspotter',
				'sublist3r', 'riddler', 'sitedossier', 'duckduckgo', 'dnsdumpster', 'yougetsignal', 'pastebin',
				'urlscan', 'gigablast', 'dogpile'),
	'options': (
		('domain', None,
		 False, 'Domain name without https?://', '-d', 'store', str),
		('limit', 3, False, 'Search limit(number of pages, default=3)', '-l', 'store', int),
		('count', 30, False, 'number of results per page(min=10, max=100, default=30)', '-c', 'store', int),
		('engines', 'otx,securitytrails', False, 'Search engine names. e.g bing,google,...[otx by default]', '-e', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
		('max', False, False, 'Using all of sources(max limit=15, max count=50)', '--max', 'store_true', bool),
		('validate', False, False, 'Validate the domains(Remove dead subdomains) \
			found and display their IP(default=False)', '--validate', 'store_true', bool),
		('silent', False, False, 'Output without any color and message([Warn]This sets the \
			value of verbosity to zero!, default=False)', '--silent', 'store_true', bool),
		('reverse', None, False, 'Use reverse DNS search. \
			Input could be a list of ip addresses(with comma separator)\
			 or could be a filename that contains ip addresses', '-r', 'store', str),
	),
	'examples': ('dns_search -d example.com --output', 'dns_search -d example.com -e\
		google,bing,yahoo -l 3 -t 3 --output', 
				 'dns_search -d example.com --max --validate --silent --output',
				 'dns_search --reverse 1.1.1.1,2.2.2.2,3.3.3.3',
				 'dns_search --reverse ips.txt')
}

HOSTNAMES = []

def set_data(lst):
	global HOSTNAMES
	for sub in lst:
		if '%' in sub:
			sub = sub.split('%')[0]
		if sub.startswith('.'):
			sub = sub[1:]
		if sub.count('.') < 2:
			continue
		HOSTNAMES.append(sub)

def search(self, name, q, q_format, limit, count):
	inside_func = 0
	if hasattr(self, name):
		engine = getattr(self, name)
		varnames = engine.__init__.__code__.co_varnames
	else:
		inside_func = 1
		engine = eval(name)
		varnames = engine.__code__.co_varnames
	if 'limit' in varnames and 'count' in varnames:
		if not inside_func:
			attr = engine(q, limit, count)
		else:
			attr = engine(self, q, limit, count)
	elif 'limit' in varnames:
		if not inside_func:
			attr = engine(q, limit)
		else:
			attr = engine(q, limit)
	else:
		if not inside_func:
			attr = engine(q)
		else:
			attr = engine(self, q)
	if not inside_func:
		attr.run_crawl()
		set_data(attr.dns)

def riddler(self, q):
	self.verbose('[RIDDLER] Searching in riddler...')
	try:
		req = self.request(
			f"https://riddler.io/search?q=pld:{q}&view_type=data_table")
	except Exception as e:
		self.error('Riddler is missed!', 'dns_search', 'riddler')
	else:
		j = self.page_parse(req.text).get_dns(q) or []
		set_data(j)

def sitedossier(self, q):
	self.verbose('[SITEDOSSIER] Searching in reddler...')
	next_page = ''
	while True:
		try:
			req = self.request(
				f"http://www.sitedossier.com/parentdomain/{q}/{next_page}")
		except Exception as e:
			self.error('Sitedossier is missed!', 'dns_search', 'sitedossier')
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
			set_data(j)
			if next_page == None:
				break
			self.output(f"[SITEDOSSIER] Searching in the {next_page} page...")

def threatcrowd(self, q):
	global HOSTNAMES
	self.verbose('[THREATCROWD] Searching in threatcrowd...')
	try:
		req = self.request(
			'https://threatcrowd.org/searchApi/v2/domain/report/?domain=' + q)
	except Exception as e:
		self.error('ThreatCrowd is missed!', 'dns_search', 'threatcrowd')
	else:
		txt = re.sub(r'[\t\n ]+', '', req.text)
		txt = re.findall(
			r'"subdomains":(\[["\.A-z0-9_\-,]+\])', txt)
		hosts = list(set(txt[0][1:-1].split(',')))
		for host in hosts:
			host = host[1:-1]
			if host.startswith('.'):
				host = host[1:]
			HOSTNAMES.append(host)

def threatminer(self, q):
	self.verbose('[THREATMINER] Searching in threatminer...')
	try:
		req = self.request(
			f"https://api.threatminer.org/v2/domain.php?q={q}&rt=5")
	except Exception as e:
		self.error('ThreatMiner is missed!', 'dns_search', 'threatminer')
	else:
		j = req.json()['results'] or []
		set_data(j)

def rapiddns(self, q):
	self.verbose('[RAPIDDNS] Searching in rapiddns...')
	try:
		req = self.request(
				f"https://rapiddns.io/subdomain/{q}?full=1")
	except Exception as e:
		self.error('Rapiddns is missed!', 'dns_search', 'rapiddns')
	else:
		j = self.page_parse(req.text).get_dns(q) or []
		set_data(j)

def dnsdumpster(self, q):
	self.verbose('[DNSDUMPSTER] Searching in dnsdumpster...')
	init_res = self.request('https://dnsdumpster.com/', method='GET')  # initial response from dnsdumpster
	set_cookie = init_res.headers.get('Set-Cookie')  # getting crsftoken from cookie field
	cookie = set_cookie[:set_cookie.index(';') + 1]
	headers = {
		'authority': 'dnsdumpster.com',
		'origin': 'https://dnsdumpster.com',
		'content-type': 'application/x-www-form-urlencoded',
		'sec-fetch-dest': 'document',
		'referer': 'https://dnsdumpster.com/',
		'cookie': cookie
	}
	try:
		# using regex to search for the csrfmiddlewaretoken (64 characters)
		i = re.search(r'name="csrfmiddlewaretoken" value="', init_res.text).end()
		csrf_token = init_res.text[i:i + 64]
		data = {'csrfmiddlewaretoken': csrf_token, 'targetip': q}
		req = self.request('https://dnsdumpster.com/', method='POST', headers=headers, data=data)
	except Exception:
		self.error('DNSdumpster is missed!', 'dns_search', 'dnsdumpster')
	else:
		j = self.page_parse(req.text).get_dns(q) or []
		set_data(j)

def yougetsignal(self, q):
	self.verbose('[YOUGETSIGNAL] Searching in yougetsignal...')
	headers = {
		'authority': 'domains.yougetsignal.com',
		'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
		'origin': 'https://www.yougetsignal.com',
		'referer': 'https://www.yougetsignal.com/',
	}
	data = {'remoteAddress': q}
	try:
		req = self.request('https://domains.yougetsignal.com/domains.php', method='POST', headers=headers, data=data).json()
	except Exception as e:
		self.error('YouGetSignal is missed!', 'dns_search', 'yougetsignal')
	else:
		j = [x[0] if len(x)>1 else '' for x in req.get('domainArray')]
		set_data(j)

def certspotter(self, q):
	self.verbose('[CERTSPOTTER] Searching in certspotter...')
	try:
		req = self.request(
			f"https://api.certspotter.com/v1/issuances?domain={q}&include_subdomains=true&expand=dns_names")
	except Exception as e:
		self.error('CERTSPOTTER is missed!', 'dns_search', 'certspotter')
	else:
		text = req.text
		if "rate_limit" in text:
			self.error('Too many request please try again later', 'dns_search', 'certspotter')
			return "certspotter"
		j = self.page_parse(req.text).get_dns(q) or []
		set_data(j)

def sublist3r(self, q):
	global HOSTNAMES
	self.verbose('[SUBLIST3R] Searching in sublist3r...')
	try:
		req = self.request(
			'https://api.sublist3r.com/search.php?domain=' + q)
	except Exception as e:
		self.error('SUBLIST3R is missed!', 'dns_search', 'sublist3r')
	else:
		j = json.loads(req.text)
		set_data(j)

def jldc(self, q):
	self.verbose('[JLDC] Searching in jldc.me...')
	try:
		req = self.request(
			f"https://jldc.me/anubis/subdomains/{q}")
	except Exception as e:
		self.error('JLDC is missed!', 'dns_search', 'jldc')
	else:
		if 'Too many request' in req.text:
			self.error('Too many request please try again later', 'dns_search', 'jldc')
			return 'jldc'
		j = list(req.json()) or []
		set_data(j)

def bufferover(self, q):
	self.verbose('[BUFFEROVER] Searching in bufferover.run...')
	try:
		req = self.request(
			f'https://dns.bufferover.run/dns?q=.{q}')
	except Exception as e:
		self.error('BufferOver is missed!', 'dns_search', 'bufferover')
	else:
		j = list(req.json()['FDNS_A']) or []
		set_data([(x.split(',')[1] if len(x.split(',')) == 2 else x) for x in j])

def otx(self, q):
	self.verbose('[OTX] Searching in otx.alienvault...')
	try:
		req = self.request(
			f"https://otx.alienvault.com/api/v1/indicators/domain/{q}/passive_dns")
	except Exception as e:
		self.error('OTX is missed!', 'dns_search', 'otx')
	else:
		j = self.page_parse(req.text).get_dns(q)
		set_data(j)

def securitytrails(self, q):
	sectrail_url = 'securitytrails.com'
	enu_url = f"https://{sectrail_url}/list/apex_domain/{q}"
	trim = ['<script id="__NEXT_DATA__" type="application/json">','</script><script nomodule=""']
	domains = []
	self.verbose('[SECTRAILS] Enumerating dns records...')
	try:
		req = self.request(enu_url)
	except Exception as e:
		self.error('Sectrails is missed!', 'dns_search', 'securitytrails')
	else:
		result = req.text.split(trim[0])[1].split(trim[1])[0]
		req_json = json.loads(result)
		for x in req_json['props']['pageProps']['apexDomainData']['data']['records']:
			domains.append(x['hostname'])
		set_data(domains)

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

def module_api(self):
	domain = self.options['domain']
	reverse = self.options['reverse']
	if reverse:
		self.reverse_dns(reverse)
		return
	if not domain:
		self.output('Domain name has not been set.', 'R')
		return
	query = domain
	domain_attr = self.urlib(domain)
	domain = domain_attr.sub_service('http')
	domain_name = self.urlib(domain).netloc
	MAX = self.options['max']
	limit = 15 if MAX else self.options['limit']
	count = 50 if MAX else self.options['count']
	engines = self.options['engines']
	verb = self._global_options['verbosity']
	output = {'hostnames': []}
	if self.options['silent']:
		self._global_options['verbosity'] = 0
	if engines == None:
		engines = 'otx,duckduckgo'
	engines = meta['sources'] if MAX else self.options['engines'].lower().split(',')
	self.thread(search, self.options['thread'], engines, query, {}, limit, count, meta['sources'])
	output['hostnames'] = list(set(HOSTNAMES))
	if self.options['validate']:
		validate_hosts = []
		for sub in HOSTNAMES:
			sub = re.sub(r'^\*\.', '', sub)
			if re.search(r'[^\w\d\.\-]+', sub):
				continue
			try:
				ip = self.urlib("http://" + sub).ip
			except Exception as e:
				pass
			else:
				sub = f"{sub} {ip}"
				validate_hosts.append(sub)
		output['hostnames'] = list(set(validate_hosts))

	self._global_options['verbosity'] = verb
	self.save_gather(output, 'osint/dns_search', domain_name, output=self.options['output'])
	return output

def module_run(self):
	self.alert_results(module_api(self))
