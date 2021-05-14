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
	'author': 'Saeed',
	'version': '1.1',
	'description': 'TLD brute force attack, supports cocurrency.',
	'comments': ('wordlist option can be an url',),
	'options': (
		('domain', None, True, 'Domain name without https?://', '-d', 'store', str),
		('count', None, False, 'Number of payloads len(max=count of payloads). default is max',
							 '-c', 'store', int),
		('wordlist', os.path.join(BASEDIR, 'data', 'tlds.txt'), False, 
							'wordlist address. default is dnsnames.txt in data folder', '-w', 'store', str),
		('thread', 8, False, 'The number of links that open per round(default=8)', '-t', 'store', int),
		('ips', False, False, 'Show ip addresses', '-i', 'store_true', bool),
	),
	'examples': ('tldbrute -d <DOMAIN> --output',
				'tldbrute -d <DOMAIN> -w <WORDLIST>')
}

HOSTNAMES = []

def thread(self, function, hostname, wordlist, thread_count):
	threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
	futures = (threadpool.submit(function, self, hostname, word) for word in wordlist if not word.startswith('#'))
	counter = 1
	for _ in concurrent.futures.as_completed(futures):
		print(f"Checking payload {counter}, hits: {len(HOSTNAMES)}", end='\r')
		counter += 1
	print(os.linesep)

def request_checker(self, hostname, word):
	hostname = f"{hostname}.{word}".lower()
	try:
		req = self.request(hostname)
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

def module_api(self):
	domain = self.options['domain']
	urlib = self.urlib(domain)
	domain = urlib.sub_service('http')
	hostname = urlib.netroot
	hostname = hostname.split('.')[0]
	wordlist = self.options['wordlist']
	count = self.options['count']

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

	self.heading(f"Starting TLD brute force with {count} payload", level=0)
	thread(self, request_checker, hostname, dlist[:count], self.options['thread'])
	output = {'hostnames': HOSTNAMES}

	self.save_gather(output, 'footprint/tldbrute', domain, output=self.options['output'])
	return output

def module_run(self):
	module_api(self)
