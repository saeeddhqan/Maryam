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

import os
import concurrent.futures
from socket import gethostbyname

from maryam.core.basedir import BASEDIR

meta = {
	'name': 'DNS Brute Force',
	'author': 'Saeeddqn',
	'version': '1.1',
	'description': 'DNS brute force attack, supports concurrency.',
	'comments': ('The wordlist option can be an url',),
	'options': (
		('domain', None, False, 'Domain name without https?://', '-d', 'store', str),
		('count', None, False, 'Number of payloads len(max=count of payloads). default is max',
							 '-c', 'store', int),
		('wordlist', os.path.join(BASEDIR, 'data', 'dnsnames.txt'), False, 
			   'wordlist address. default is dnsnames.txt in data folder', '-w', 'store', str),
		('thread', 8, False, 'The number of links that open per round(default=8)', '-t', 'store', int),
		('wordlists', False, False, 'List of most common DNS wordlists', '-l', 'store_true', bool),
		('ips', False, False, 'Show ip addresses', '-i', 'store_true', bool),
	),
	'examples': ('dnsbrute -d <DOMAIN> --output',
				'dnsbrute -d <DOMAIN> -w <WORDLIST>')
}

HOSTNAMES = []
LISTS = {"https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/fierce-hostlist.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/namelist.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-20000.txt": 'medium',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-110000.txt": 'large',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/deepmagic.com-prefixes-top50000.txt": 'large',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/shubs-subdomains.txt": 'large'
}

def thread(self, function, hostname, wordlist, thread_count):
	threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
	futures = (threadpool.submit(function, self, hostname, word) for word in wordlist if not word.startswith("#"))
	counter = 1
	for _ in concurrent.futures.as_completed(futures):
		print(f"Checking payload {counter}, hits: {len(HOSTNAMES)}", end='\r')
		counter += 1
	print(os.linesep)

def request_checker(self, hostname, word):
	hostname = f"{word}.{hostname}".lower()
	try:
		req = self.request(f"http://{hostname}")
	except Exception as e:
		if 'timed out' in str(e.args):
			self.verbose(f"{hostname} => Timed out", 'O')
		else:
			self.debug(f"{list(e.args)[0]}:'{hostname}'", 'O')
	else:	
		if self.options['ips']:
			try:
				ip = gethostbyname(hostname)
			except:
				ip = '-'
			hostname = f"{hostname} : {ip}"
		HOSTNAMES.append(hostname)
		self.output(f"{hostname}{' '*50}", 'G')

def remote_list(self, addr):
	req = self.request(addr)
	headers = req.headers
	keys = list(map(str.lower, list(headers.keys())))
	cond1 = 'content-type' in keys and 'text/plain' in str(headers).lower()
	cond2 = 'githubusercontent.com' in addr.lower()
	cond3 = '<' not in req.text
	if cond1 or cond2 or cond3:
		wordlist = req.text.split('\n')
		if '' in wordlist:
			wordlist.pop(wordlist.index(''))
		return wordlist
	else:
		self.error(f"{addr} value is not text/plain", 'dnsbrute', 'remote_list')
	return []

def module_api(self):
	domain = self.options['domain']
	urlib = self.urlib(domain)
	domain = urlib.sub_service('http')
	domain = domain.replace('www.', '')
	hostname = urlib.netloc
	wordlist = self.options['wordlist']
	count = self.options['count']
	if '://' in wordlist:
		dlist = remote_list(wordlist)
	else:
		dlist = self._is_readable(wordlist)
		if dlist:
			dlist = dlist.read().split()
		else:
			dlist = []

	dlen = len(dlist)
	if not count:
		count = dlen
	else:
		count = dlen if count > dlen else count

	self.heading(f"Starting DNS brute force with {count} payload", level=0)
	thread(self, request_checker, hostname, dlist[:count], self.options['thread'])

	self.save_gather({'hostnames': HOSTNAMES}, 'footprint/dnsbrute', hostname, output=self.options['output'])
	return HOSTNAMES

def module_run(self):
	if self.options["wordlists"]:
		self.alert('common DNS wordlists')
		self.table(LISTS.items(), header=('list', 'scale'))
		return
	self.alert('hostname')
	self.alert_results(module_api(self))
