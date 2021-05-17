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
from bs4 import BeautifulSoup
import json

meta = {
	'name': 'GitHub Leaks',
	'author': 'Aman Singh',
	'version': '0.1',
	'description': 'Search your query in the GitHub and show the potentially leaked info.',
	'sources': ('google', 'carrot2', 'bing','yahoo', 'millionshort', 'qwant', 'duckduckgo', 'github'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store', int),
		('engine', 'google,github', False, 'Engine names for search(default=google, github)', '-e', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
    'examples': ('github_leaks-q <QUERY> -l 15 -e carrot2,bing,qwant --output',)
}

LINKS = []
PAGES = ''
REPO = []
OUTPUT = {'links': {}}

def checks(self, repo):
	checks = ['filename:.npmrc filename:.dockercfg filename:id_rsa filename:credentials filename:.s3cfg',#NOT MORE THAN 500 CHAR IN ONE QUERY
	'filename:wp-config.php filename:.htpasswd filename:.git-credentials filename:.bashrc filename:.bash_profile', 
	'filename:.netrc filename:config filename:connections.xml filename:express.conf filename:.pgpass', 
	'filename:proftpdpasswd filename:server.cfg filename:.bash_history filename:.cshrc filename:.history filename:.sh_history filename:sshd_config', 
	'filename:dhcpd.conf filename:prod.exs filename:shadow filename:passwd filename:.esmtprc filename:logins.json', 
	'filename:CCCam.cfg filename:settings filename:secrets filename:master.key filename:WebServers.xml',
	'password', 'DB_USERNAME', 'TOKEN', 'API_KEY' , 'SECRET_KEY', 'credentials',
	'extension:pem extension:ppk extension:sql extension:sls'
	]
	for term in checks:
		threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
		futures = (threadpool.submit(leaks, self, link, term) for link in repo)
		for results in concurrent.futures.as_completed(futures):
			print(f"Found {len(OUTPUT['links'])} links" , end= '\r')
	print('\n')

def leaks(self, repo, term):
	url = f"{repo}/search?q={self.urlib(term).quote_plus.replace('.','%2E')}"
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		req = self.request(url, headers=headers, timeout=20)
		if 'We couldn’t find any code matching' in req.text:
			return
	except Exception as e:
		return
	else:
		try:
			soup = BeautifulSoup(req.content, 'html.parser')
			results = soup.find_all('div', class_='width-full')
			if len(results) > 0:
				for result in results:
					OUTPUT['links'][json.loads(result.find('a')['data-hydro-click'])['payload']['result']['url']] = [re.sub(' +', ' ', line) for line in str(''.join([code.text for code in result.find_all('td' ,class_ ="blob-code blob-code-inner")])).split('\n') if term in line]
		except:
			return

def search(self, name, q, q_formats, limit, count):
	global PAGES,LINKS, USERS, REPO
	engine = getattr(self, name)
	eng = name
	q = q_formats[f"{name}"] if f"{name}" in q_formats else q_formats['default']
	varnames = engine.__init__.__code__.co_varnames
	if 'limit' in varnames and 'count' in varnames:
		attr = engine(q, limit, count)
	elif 'limit' in varnames:
		attr = engine(q, limit)
	else:
		attr = engine(q)
	if eng == 'github':
		run = self.github(q)
		run.run_crawl()
		REPO += run.repositories
	else:
		attr.run_crawl()
		LINKS += attr.links
		PAGES += attr.pages


def module_api(self):
	global REPO
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	engines = self.options['engine'].split(',')
	q_formats = {
		'default': f"site:github.com {query}",
		'millionshort': f'site:github.com "{query}"',
		'qwant': f'site:github.com {query}',
		'github': f'{query}'
	}

	self.thread(search, self.options['thread'], engines, query, q_formats, limit, count, meta['sources'])

	explore = self.page_parse(PAGES).get_networks
	bactery = ['marketplace', 'pulls', 'explore', 'issues','notifications', 'account', 'settings', 'login','about', 'pricing', 'site']

	for link in self.reglib().filter(r"https://(www\.)?github\.com/[\w-]{1,39}/[\w\-\.]+", list(set(LINKS))):
		repo = re.search(r"(https://(www\.)?github\.com/([\w-]{1,39})/[\w\-\.]+)", link)
		if repo.group(3) not in bactery:
			repo = repo.group(0)
			REPO.append(repo)

	REPO = list(set(REPO))
	checks(self, REPO)
	self.save_gather(OUTPUT,
	 'osint/github_leaks', query, output=self.options.get('output'))
	return OUTPUT

def module_run(self):
	output = module_api(self)
	self.alert('Links\n')
	for url in output['links']:
		self.output(url, 'G')
		for line in output['links'][url]:
			self.output(f"{line}")
		print('')
