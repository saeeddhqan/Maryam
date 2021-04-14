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
import concurrent.futures
import requests

meta = {
	'name': 'Domain Reputation',
	'author': 'Kunal Khandelwal',
	'version': '0.3',
	'description': 'Check domain reputation with different sources and provide a summary of combined results.',
	'sources': ('barracudacentral', 'mxtoolbox', 'multirbl', 'norton'),
	'options': (
		('domain', None, True, 'Domain name without https?://', '-d', 'store', str),
		('engines', 'barracudacentral,multirbl,mxtoolbox,norton', False, 'Search engine names(default=[barracudacentral,'
					'multirbl, mxtoolbox])'
		 , '-e', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
	'examples': ('domain_reputation -d example.com',
				 'domain_reputation -d 93.184.216.34'
				 )
}

BLACKLIST = []
OUTPUT = {}
LISTS = 0
RESULT = ''
OUTPUT = {'category': '', 'number': 0, 'blacklists': [], 'absence': 0, 'norton': ''}

def thread(self, function, thread_count, engines, q, sources):
	threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
	futures = (threadpool.submit(
		function, self, name, q) for name in engines if name in sources)
	for _ in concurrent.futures.as_completed(futures):
		pass

def search(self, name, q):
	engine = eval(name)
	engine(self, q)

def norton(self, q):
	global RESULT
	self.verbose('[NORTON] Scanning domain...')
	try:
		req = self.request(f'https://safeweb.norton.com/report/show?url={q}')
	except Exception as e:
		self.error(f"Norton could not scan! due to {e}", 'domain_reputation', 'norton')
	else:
		e_reg = 'is a known dangerous web page'
		s_reg = 'found no issues with'
		if e_reg in req.text:
			RESULT = f"Threat Report: {q} {e_reg}"
		elif s_reg in req.text:
			RESULT = f"Threat Report: {s_reg} {q}"
		else:
			RESULT = f"Threat Report: {q} not yet rated as dangerous."

def barracudacentral(self, q):
	global LISTS,OUTPUT
	self.verbose('[Barracuda] Searching in barracuda...')
	data = {
		'lookup_entry': q,
		'submit': 'Check Reputation'
	}
	try:
		req = self.request('https://www.barracudacentral.org/lookups/lookup-reputation', method='POST',
						   data=data)
	except Exception as e:
		self.error('Barracuda is missed!', 'domain_reputation', 'barracudacentral')
	else:
		reg = re.compile(r"categories: <strong>([\w\d\s-]+)")
		if 'listed as "poor"' not in req.text:
			category = reg.findall(req.text)[0]
			OUTPUT['category'] = category
		else:
			BLACKLIST.append('BARRACUDA')
		LISTS += 1

def mxtoolbox(self, q):
	global LISTS
	self.verbose('[MXTOOLBOX] Searching in mxtoolbox...')
	try:
		headers = {'TempAuthorization': 'ca1e3b2f-cd6c-4886-9446-88f4ff7a960d',
				   'Referer': f'https://mxtoolbox.com/SuperTool.aspx?action=blacklist:{q}&run=toolpage',
				   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
								 '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
				   }
		req = requests.get(f'http://mxtoolbox.com/api/v1/Lookup?command=blacklist&argument={q}&resultIndex=1'
						   f'&disableRhsbl=true&format=2', headers=headers)
		j = req.json()
		j = j['HTML_Value']
		num_reg = re.compile(r'<strong>([\d]+)</strong>')
		num_lists = num_reg.findall(j)[0]
		list_reg = re.compile('<tr>(.+?)</tr>')
		blacklist_reg = re.compile(r'<span class="bld_name">([\d\w\s]+)</span>')
		lists = list_reg.findall(j)[:-1]
	except Exception as e:
		if 'API' in req.text:
			self.error('Mxtoolbox needs a valid API key', 'domain_reputation', 'mxtoolbox')
		else:
			self.error('Mxtoolbox is missed!', 'domain_reputation', 'mxtoolbox')
	else:
		for blacklist in lists:
			if 'LISTED' in blacklist:
				try:
					list_name = blacklist_reg.findall(blacklist)[0]
				except:
					pass
				BLACKLIST.append(list_name)
		LISTS += int(num_lists)

def multirbl(self, q):
	global LISTS
	self.verbose('[Multirbl] Searching in multirbl.valli.org...')
	try:
		req = self.request(f'http://multirbl.valli.org/lookup/{q}.html', verify=False)
		text = req.text
		hash_reg = re.compile(r'"asessionHash": "([\w]+)"')
		l_id_hash = re.compile(r'<td class="l_id">([\d]+)')
		hash = hash_reg.findall(text)[0]
		l_ids = l_id_hash.findall(text)
		num_test_reg = re.compile(r'nof: ([\d]+),')
		num_test = num_test_reg.findall(text)[0]
	except Exception as e:
		self.error('Multirbl is missed', 'domain_reputation', 'multirbl')
	else:
		thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
		futures = (thread_pool.submit(__multirbl, self, l_id, hash, l_ids, q) for l_id in range(int(num_test)))
		for _ in concurrent.futures.as_completed(futures):
			pass
		LISTS += int(num_test)

def __multirbl(self, l_id, hash, l_ids, q):
	try:
		data = {'ash': hash,
				'rid': f'DNSBLBlacklistTest_{l_id}',
				'q': q,
				'lid': l_ids[l_id],
				}
		req = self.request(f'http://multirbl.valli.org/json-lookup.php', method='POST',
						   verify=False, data=data)
		j = req.json()
		if not j['result']:
			BLACKLIST.append(j['name'])
	except Exception as e:
		pass

def module_api(self):
	global LISTS
	query = self.options['domain']
	engines = self.options['engines'].split(',')
	thread(self, search, self.options['thread'], engines, query, meta['sources'])
	OUTPUT['number'] = len(list(set(BLACKLIST)))
	OUTPUT['blacklists'] = list(set(BLACKLIST))
	if LISTS != 0:
		presence = len(list(set(BLACKLIST))) / LISTS
		OUTPUT['absence'] = 100 - (presence*100)
	OUTPUT['norton'] = RESULT
	return OUTPUT

def module_run(self):
	output = module_api(self)
	self.output(f"CATEGORY\n\t{output['category']}")
	self.output(f"NUMBER OF PRESENCE ON BLACKLIST\n\t{output['number']}")
	self.output('BLACKLISTS')
	for i in output['blacklists']:
		self.output(i, 'B')
	self.output(f"ABSENCE PERCENTAGE\n\t{output['absence']}")
	self.output(f"NORTON SAFE WEB REPORT\n\t{output['norton']}")
