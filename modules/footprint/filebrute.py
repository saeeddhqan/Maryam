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


meta = {
	'name': 'File Brute Force',
	'author': 'Saeed',
	'version': '1.0',
	'description': 'File/Directory brute force attack, supports cocurrency.',
	'comments': ('The wordlist option can be an url.',),
	'options': (
		('domain', None, False, 'Domain name without https?://', '-d', 'store', str),
		('count', None, False, 'Number of payloads len(max=count of payloads). default is max',
							 '-c', 'store', int),
		('wordlist', 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/RobotsDisallowed-Top500.txt', False, 
							'wordlist address. default is dnsnames.txt in data folder', '-w', 'store', str),
		('thread', 8, False, 'The number of links that open per round(default=8)', '-t', 'store', int),
		('wordlists', False, False, 'List of most common DNS wordlists', '-l', 'store_true', bool),
		('status_codes', '200,201,204', False, 'List of good status codes(default="200,201,204")', '-s', 'store', str),
		('redirect', True, False, 'Allow redirection(default=True)', '-r', 'store_true', bool),
	),
	'examples': ('filebrute -d <DOMAIN> --output',
				'filebrute -d <DOMAIN> -w <WORDLIST>')
}

URLS = []

LISTS = {"https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/CMS/wp-plugins.fuzz.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/CMS/wp-themes.fuzz.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/CMS/wordpress.fuzz.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/tests.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/jboss.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/PHP.fuzz.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/IIS.fuzz.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/RobotsDisallowed-Top10.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/RobotsDisallowed-Top100.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/RobotsDisallowed-Top500.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/RobotsDisallowed-Top1000.txt": 'small',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/CMS/sitemap-magento.txt": 'medium',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/LinuxFileList.txt": 'large',
		 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/SVNDigger/all.txt": 'large',
}
def thread(self, function, hostname, wordlist, thread_count, status_codes):
	threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
	futures = (threadpool.submit(function, self, hostname, word, status_codes) for word in wordlist if not word.startswith("#"))
	counter = 1
	for _ in concurrent.futures.as_completed(futures):
		print(f"Checking payload {counter}, hits: {len(URLS)}", end='\r')
		counter += 1
	print(os.linesep)

def request_checker(self, hostname, word, status_codes):
	hostname_join = self.urlib(hostname).join(word)
	try:
		req = self.request(hostname_join, allow_redirects=self.options['redirect'])
	except Exception as e:
		if 'timed out' in str(e.args):
			self.verbose(f"{hostname_join} => Timed out", 'O')
		else:
			self.debug(f"{list(e.args)[0]}:'{hostname_join}'", 'O')
	else:
		if 'Location' in req.headers:
			location = req.headers['Location']
			join = self.urlib(hostname).join(location)
			try:
				req = self.request(join)
			except:
				return
		if req.status_code in status_codes:
			URLS.append(hostname_join)
			self.output(f"{hostname_join}{' '*50}", 'G')

def remote_list(self, addr):
	req = self.request(addr)
	headers = req.headers
	keys = list(map(str.lower, list(headers.keys())))
	cond1 = 'content-type' in keys and 'text/plain' in str(headers).lower()
	cond2 = 'githubusercontent.com' in addr.lower()
	if cond1 or cond2:
		wordlist = req.text.split('\n')
		if '' in wordlist:
			wordlist.pop(wordlist.index(''))
		return wordlist
	else:
		self.error(f"{addr} value is not text/plain", 'filebrute', 'remote_list')
	return []

def module_api(self):
	if self.options["wordlists"]:
		return {'lists': LISTS}

	domain = self.options['domain']
	wordlist = self.options['wordlist']
	if not domain or not wordlist:
		return {'error': 'Arguments are incorrect'}
	urlib = self.urlib(domain)
	domain = urlib.sub_service('http')
	domain = domain.replace('www.', '')
	status_codes = list(map(int, self.options['status_codes'].split(',')))
	count = self.options['count']
	if '://' in wordlist:
		dlist = remote_list(self, wordlist)
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

	self.heading(f"Starting File/Dir brute force with {count} payload", level=0)
	thread(self, request_checker, domain, dlist[:count], self.options['thread'], status_codes)
	output = {'urls': URLS}
	self.save_gather(output, 'footprint/filebrute', domain, output=self.options['output'])
	return output

def module_run(self):
	if self.options["wordlists"]:
		self.alert('common DNS wordlists')
		self.table(LISTS.items(), header=('list', 'scale'))
		return
	self.alert_results(module_api(self))
