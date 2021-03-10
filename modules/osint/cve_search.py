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

from concurrent.futures import thread
from core.module import BaseModule
import re
import concurrent.futures


class Module(BaseModule):

	meta = {
		'name': 'Common Vulnerabilities and Exposures Searcher',
		'author': 'Dimitrios Papageorgiou',
		'version': '0.3',
		'description': 'Search in open-sources to find CVEs.',
		'sources': ('mitre', 'nist', 'packetstormsecurity'),
		'options': (
				('query', BaseModule._global_options['target'],
				 True, 'Query string', '-q', 'store'),
				('engines', 'mitre', False,
				 'DB source to search. e.g mitre,...(default=mitre)', '-e', 'store'),
				('count', 20, False,
				 'Number of results per search(default=20, -1 for all available)', '-c', 'store'),
				('thread', 2, False,
				 'The number of engine that run per round(default=2)', '-t', 'store'),
				('output', False, False, 'Save output to  workspace',
				 '--output', 'store_true'),
		),
		'examples': ('cve_search -q sql -e mitre --output',)
	}

	names = []
	links = []
	descriptions = []

	def clear(self):
		self.names = []
		self.links = []
		self.descriptions = []

	def mitre(self, q, count):
		self.verbose('[MITRE] Searching in mitre...')
		try:
			req = self.request(
				f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={q}")
		except Exception as e:
			self.error('Mitre is missed!')
		else:
			self.names.extend(re.findall(
				r'<a href="[^"]+">(CVE-[^<]+)</a>', req.text)[:count])
			hrefs = re.findall(
				r'<a href="(/cgi-bin/cvename.cgi\?name=[^"]+)">', req.text)[:count]
			self.links.extend(
				list(map(lambda x: f"https://cve.mitre.org{x}", hrefs)))
			descriptions = re.findall(
				r'<td valign="top">(.*?)<\/td>', req.text.replace('\n', ''))[:-1]
			self.descriptions.extend(descriptions[:count])

	def nist(self, q, count):
		self.verbose('[NIST] Searching in nist...')
		try:
			req = self.request(
				f"https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={q}&resultsPerPage={count}")
		except Exception as e:
			self.error('Nist is missed!')
		else:
			cve_items = req.json()['result']['CVE_Items']
			names = [cve['cve']['CVE_data_meta']['ID'] for cve in cve_items]
			links = [f"https://nvd.nist.gov/vuln/detail/{id}" for id in names]
			desc = [cve['cve']['description']['description_data'][0]['value']
					for cve in cve_items]
			self.names.extend(names)
			self.links.extend(links)
			self.descriptions.extend(desc)

	def packetstormsecurity(self, q, count):
		self.verbose('[Packetstormsecurity] Searching in packetstormsecurity...')
		try:
			req = self.request(
				f"https://packetstormsecurity.com/search/?q={q}", timeout=60)
		except Exception as e:
			self.error('Packetstormsecurity is missed')
		else:
			names = re.findall(r'<a class="ico text-plain"[^>]+>([^<]+)</a>', req.text)[:count]
			links = re.findall(r'<a class="ico text-plain" href="([^"]+)"[^>]+>', req.text)[:count]
			descriptions = re.findall(r'<dd class="detail"><p>([^<]+)</p></dd>', req.text)[:count]
			self.names.extend(names)
			self.links.extend([f"https://packetstormsecurity.com{link}" for link in links])
			self.descriptions.extend(descriptions)

	def thread(self, function, thread_count, sources, q, count):
		threadpool = concurrent.futures.ThreadPoolExecutor(
			max_workers=thread_count)
		futures = (threadpool.submit(function, source, q, count)
				   for source in sources if source in self.meta['sources'])
		for _ in concurrent.futures.as_completed(futures):
			pass

	def search(self, source, q, count):
		getattr(self, source)(q, count)

	def module_run(self):
		self.clear()
		q = self.options['query']
		sources = self.options['engines'].split(',')
		count = self.options['count']
		thread_count = self.options['thread']

		self.thread(self.search, thread_count, sources, q, count)

		if self.names == []:
			self.output('No CVE found', 'O')

		for i in range(len(self.names)):
			self.output(self.names[i], 'G')
			self.output(self.links[i], 'R')
			self.output(f"{self.descriptions[i]}\n")

		self.save_gather({'names': self.names, 'links': self.links,
						  'descriptions': self.descriptions}, 'osint/cve_search',
						 q, output=self.options.get('output'))
