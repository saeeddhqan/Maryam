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
import os
import concurrent.futures
from socket import gethostbyname

class Module(BaseModule):

	meta = {
		'name': 'File Brute Force',
		'author': 'Saeeddqn',
		'version': '1.0',
		'description': 'File/Directory brute force attack, supports cocurrency.',
		'comments': ('The wordlist option can be an url.',),
		'options': (
			('domain', BaseModule._global_options['target'],
			 False, 'Domain name without https?://', '-d', 'store'),
			('count', None, False, 'Count of payloads len(max=count of payloads). default is max',
								 '-c', 'store'),
			('wordlist', os.path.join(BaseModule.data_path, 'dnsnames.txt'), False, 
								'wordlist address. default is dnsnames.txt in data folder', '-w', 'store'),
			('thread', 8, False, 'The number of links that open per round(default=8)', '-t', 'store'),
			('wordlists', False, False, 'List of most common DNS wordlists', '-l', 'store_true'),
			('status_codes', '200,201,204', False, 'List of good status codes(default="200,201,204")', '-s', 'store_true'),
			('redirect', True, False, 'Allow redirection(default=True)', '-r', 'store_true'),
			('output', False, False, 'Save output to the workspace', '--output', 'store_true'),
		),
		'examples': ('fbrute -d <DOMAIN> --output',
					'fbrute -d <DOMAIN> -w <WORDLIST>')
	}

	hostnames = []

	def thread(self, function, hostname, wordlist, thread_count, status_codes):
		threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
		futures = (threadpool.submit(function, hostname, word, status_codes) for word in wordlist if not word.startswith("#"))
		counter = 1
		for _ in concurrent.futures.as_completed(futures):
			print(f"Checking payload {counter}, hits: {len(self.hostnames)}", end='\r')
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
				self.hostnames.append(hostname_join)
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
			self.error(f"{addr} value is not text/plain")
		return []

	def module_run(self):
		if self.options["wordlists"]:
			self.alert('common DNS wordlists')
			lists = {"https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/CMS/wp-plugins.fuzz.txt": 'small',
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
					 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/CMS/sitemap-magento.txt": 'mediom',
					 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/LinuxFileList.txt": 'large',
			}
			self.table(lists.items(), header=('list', 'scale'))
			return

		domain = self.options['domain']
		urlib = self.urlib(domain)
		domain = urlib.sub_service('http')
		domain = domain.replace('www.', '')
		wordlist = self.options['wordlist']
		status_codes = list(map(int, self.options['status_codes'].split(',')))
		count = self.options['count']
		if '://' in wordlist:
			dlist = self.remote_list(wordlist)
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
		self.thread(self.request_checker, domain, dlist[:count], self.options['thread'], status_codes)

		self.save_gather(self.hostnames, 'footprint/fbrute', domain, output=self.options['output'])
