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
	'name': 'Instagram Search',
	'author': 'Aman Singh, Rishabh Jain',
	'version': '0.2',
	'description': 'Search your query in the Instagram and show the results.',
	'sources': ('google', 'carrot2', 'bing', 'yippy', 'yahoo', 'millionshort', 'qwant', 'duckduckgo', 'instagram'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store', int),
		('engine', 'google,instagram', False, 'Engine names for search(default=google, instagram)', '-e', 'store', str),
		('session_id', None, False, 'Insta Account Session_id for more details results (default="")', '-s', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
    'examples': ('instagram -q <QUERY> -l 150 -s <session> --output',)
}

LINKS = []
PAGES = ''
USERDATA = {}
FOLLOWERS = []
FOLLOWING = []
POST = []

def search(self, name, q, q_formats, limit, count,session_id):
	global PAGES,LINKS,USERDATA,FOLLOWERS,FOLLOWING,POST
	eng = name
	query = q
	engine = getattr(self, name)
	name = engine.__init__.__name__
	q = f"{name}_q" if f"{name}_q" in q_formats else q_formats['default_q']
	varnames = engine.__init__.__code__.co_varnames

	# for instagram
	if eng == 'instagram':
		attr = self.instagram(query, limit=limit, session_id=session_id)
		attr.run_crawl()
		USERDATA = attr.userdata
		FOLLOWERS = attr.followers
		FOLLOWING = attr.following
		POST = attr.post

	# for others
	else :
		if 'limit' in varnames and 'count' in varnames:
			attr = engine(q, limit, count)
		elif 'limit' in varnames:
			attr = engine(q, limit)
		else:
			attr = engine(q)
		# append data to return here
		attr.run_crawl()
		LINKS += attr.links
		PAGES += attr.pages
		USERDATA = attr.userdata

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	session_id = self.options['session_id'] or ''
	engine = self.options['engine'].split(',')

	output = {
		'people': [],
		'posts': [],
		'hashtags': [],
		}
	q_formats = {
		'google_q': f"site:www.instagram.com inurl:{query}",
		'default_q': f"site:www.instagram.com {query}",
		'yippy_q': f"www.instagram.com {query}",
		'instagram': f"{query}"
	}
	
	self.thread(search, self.options['thread'], engine, query, q_formats, limit, count,session_id, meta['sources'])

	# for other modules
	usernames = self.page_parse(PAGES).get_networks
	for _id in list(set(usernames.get('Instagram'))):
		if _id[-2:] == '/p' or _id[-8:] == '/explore':
			continue
		_id = f"{_id[_id.find('/')+1:]}"
		if _id not in output['people']:
			output['people'].append(_id)

	links = list(self.reglib().filter(r"https?://(www\.)?instagram\.com/", list(set(LINKS))))
	for link in self.reglib().filter(lambda x: '/explore/tags/' in x, links):
		tag = re.sub(r'https?://(www\.)?instagram\.com/explore/tags/', '', link)
		if re.search(r'"[\w\d_\-\/]+$", tag):
			tag = tag.rsplit('/')
			output['hashtags'].append(tag[0])

	post_data_extracted= self.reglib().filter(r"https?://(www\.)?instagram\.com/p/[\w_\-0-9]+/", links)
	for link in post_data_extracted:
		output['posts'].append(link)

	# for insta
	saving_output = output.copy()
	if USERDATA :
		saving_output['USERDATA'] = USERDATA
		self.heading('Extracting User account', 0)
		for key,value in saving_output['USERDATA'].items():
			if isinstance(value, str) and '\n' in value: 
				value = value.encode('utf-8')
			self.output(f"\t{key} : {value}", color='G')

	if POST:
		saving_output['POSTS'] = POST
		if output['posts']:
			for po in output['posts']:
				if po not in saving_output['POSTS']:
					saving_output['POSTS'].append(po) 
			else:
				output.pop('posts')
		self.heading('Extracting User Post', 0)
		for i in saving_output['POSTS']:
			self.output('\t' + i, color='G')

	if FOLLOWERS:
		saving_output['FOLLOWERS'] = FOLLOWERS
		self.heading('Extracting User followers', 0)
		for user in saving_output['FOLLOWERS'] :
			self.output(f"\tuser: {user['username']} --> https://www.instagram.com/{user['username']}", color="G")

	if FOLLOWING:
		saving_output['FOLLOWING']= FOLLOWING
		self.heading('Extracting User following', 0)
		for user in saving_output['FOLLOWING']:
			self.output(f"\tuser: {user['username']} --> https://www.instagram.com/{user['username']}", color="G")

	output = {key: val for key, val in output.items() if val} 

	self.save_gather(saving_output,'search/instagram', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))
