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

meta = {
	'name': 'Common Vulnerabilities and Exposures Searcher',
	'author': 'Dimitrios Papageorgiou',
	'version': '0.3',
	'description': 'Search in open-sources to find CVEs(exploits, vulns).',
	'sources': ('mitre', 'nist', 'packetstormsecurity'),
	'options': (
			('query', None,
			 True, 'Query string', '-q', 'store', str),
			('engines', 'mitre', False,
			 'DB source to search. e.g mitre,...(default=mitre)', '-e', 'store', str),
			('count', 20, False,
			 'Number of results per search(default=20, -1 for all available)', '-c', 'store', int),
			('thread', 2, False,
			 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
	'examples': ('cve_search -q sql -e nist --output',)
}

TITLES = []
LINKS = []
DESCRIPTIONS = []

def set_data(titles, links, descs):
	global TITLES,LINKS,DESCRIPTIONS
	TITLES += titles
	LINKS += links
	DESCRIPTIONS += descs

def search(self, source, q, q_formats, limit, count):
	engine = eval(source)(self, q, count)

def mitre(self, q, count):
	self.verbose('[MITRE] Searching in mitre...')
	try:
		req = self.request(
			f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={q}")
	except Exception as e:
		self.error('Mitre is missed!', 'cve_search', 'mitre')
	else:
		hrefs = re.findall(
			r'<a href="(/cgi-bin/cvename.cgi\?name=[^"]+)">', req.text)[:count]
		titles = re.findall(
			r'<a href="[^"]+">(CVE-[^<]+)</a>', req.text)[:count]
		links = list(map(lambda x: f"https://cve.mitre.org{x}", hrefs))
		desc = re.findall(
			r'<td valign="top">(.*?)<\/td>', req.text.replace('\n', ''))[:-1][:count]
		set_data(titles, links, desc)

def nist(self, q, count):
	self.verbose('[NIST] Searching in nist...')
	try:
		req = self.request(
			f"https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={q}&resultsPerPage={count}")
	except Exception as e:
		self.error('Nist is missed!', 'cve_search', 'nist')
	else:
		cve_items = req.json()['result']['CVE_Items']
		titles = [cve['cve']['CVE_data_meta']['ID'] for cve in cve_items]
		links = [f"https://nvd.nist.gov/vuln/detail/{id}" for id in titles]
		desc = [cve['cve']['description']['description_data'][0]['value']
				for cve in cve_items]
		set_data(titles, links, desc)

def packetstormsecurity(self, q, count):
	self.verbose('[Packetstormsecurity] Searching in packetstormsecurity...')
	try:
		req = self.request(
			f"https://packetstormsecurity.com/search/?q={q}", timeout=60)
	except Exception as e:
		self.error('Packetstormsecurity is missed', 'cve_search', 'packetstormsecurity')
	else:
		titles = re.findall(r'<a class="ico text-plain"[^>]+>([^<]+)</a>', req.text)[:count]
		links = re.findall(r'<a class="ico text-plain" href="([^"]+)"[^>]+>', req.text)[:count]
		links = [f"https://packetstormsecurity.com{link}" for link in links]
		desc = re.findall(r'<dd class="detail"><p>([^<]+)</p></dd>', req.text)[:count]
		set_data(titles, links, desc)

def module_api(self):
	query = self.options['query']
	engines = self.options['engines'].split(',')
	count = self.options['count']
	output = {'exploits': []}
	self.thread(search, self.options['thread'], engines, query, {}, 3, count, meta['sources'])
	output['exploits'] = [[TITLES[x], LINKS[x], DESCRIPTIONS[x]] for x in range(len(TITLES))]
	self.save_gather(output, 'osint/cve_search', query, output=self.options.get('output'))
	return output

def module_run(self):
	output = module_api(self)
	for item in output['exploits']:
		self.output(item[0], 'G')
		self.output(item[1], 'R')
		self.output(f"{item[2]}\n")
