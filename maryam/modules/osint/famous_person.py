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

import json

meta = {
	'name': 'Famous Person Report',
	'author': 'Kaushik',
	'version': '0.1',
	'description': 'later',
	'required': ('$search', '$iris'),
	'sources': ('google', 'wikipedia', 'wikileaks', 'twitter', 'sanctionsearch'),
	'options': (
		('name', '', False, 'Name', '-n', 'store', str),
		('family', '', False, 'Family', '-f', 'store', str),
		('query', '', False, 'Query string. Name, Family, or nickname', '-q', 'store', str),
		('limit', 1, False, 'Search limit', '-l', 'store', int),
		('depth', 0, False, 'Search depth (for searching connected people)', '-d', 'store', int),
		('show_plot', False, False, 'show term frequency plot in separate window', '-s', 'store_true', bool),
		('include_tweets', False, False, 'Include recent tweets mentioning the person', '-i', 'store_true', bool),
	),
	'examples': ('famous_person -q <QUERY> -l 5 --output --api',)
}

OUTPUT = {}
VISITED = []

def module_api(self, depth=0):
	global OUPUT, VISITED

	output = {}
	query = self.options['query']
	name = self.options.get('name') or ''
	family = self.options.get('family') or ''
	target_depth = self.options.get('depth') or 0
	show_plot = self.options.get('show_plot')
	include_tweets = self.options.get('include_tweets')

	if name and family:
		fullname = f"{name} {family}"
	elif query:
		fullname = query
	elif name:
		fullname = name
	elif family:
		fullname = family
	else:
		return output

	VISITED.append(fullname)
	if depth != 0:
		print()
		self.output(f"Searching For: {fullname}")

	google_run = self.google(fullname, count=10)
	google_run.run_crawl()
	google_results = google_run.results
	card = google_run.google_card
	wiki = self.wikipedia(fullname, 5)
	wiki.run_crawl()
	links_with_title = wiki.links_with_title

	have_we_wiki = 0
	selected_pid = 0
	selected_link = 0
	selected_title = 0
	# Here I tried to find the best wikipedia page that match the query
	best_match = {}
	score = 0
	for link, title, pid in links_with_title:
		if name in title and family in title and query in title:
			best_match[7+score] = (pid, title, pid)
		elif name in title and family in title:
			best_match[6+score] = (pid, title, pid)
		elif fullname == title:
			best_match[5+score] = (pid, title, pid)
		elif query == title:
			best_match[4+score] = (pid, title, pid)
		elif name.lower() in title and family.lower() in title:
			best_match[3+score] = (pid, title, pid)
		elif fullname in title:
			best_match[2+score] = (pid, title, pid)
		elif query.lower() in title:
			best_match[1+score] = (pid, title, pid)
		score += -1

	if not best_match:
		self.output('We could not find any result in wikipedia.')
	else:
		selected_pid, selected_link, selected_title = best_match[max(best_match.keys())]
		have_we_wiki = 1
		wiki_page = self.wikipedia(selected_pid, 1)
		wiki_extract = wiki_page.page()['extract']
		output['wikipedia'] = f"{selected_link} {selected_title}"

	if 'content' in card:
		output['description'] = card['content'].replace('Description', 'Description: ')
	else:
		if have_we_wiki:
			output['description'] = wiki_extract[:500] 
	if 'name' in card:
		output['name'] = card['name']
	else:
		output['name'] = fullname
	if 'known_as' in card:
		output['known_as'] = card['known_as']
	if 'img' in card:
		output['img'] = card['img']
	else:
		output['img'] = f"https://bing.com/th?q={fullname}"
	if 'info' in card:
		output['info'] = card['info']

	if include_tweets:
		tweets = self.tweet_search(fullname, limit=10)
		tweets.run_crawl()
		output['tweet_mentions'] = tweets.tweets['all']

	output['social'] = card['social']
	output['top_urls'] = []
	keywords = self.keywords(fullname)
	keywords.run_crawl()
	output['top_searched_queries'] = keywords.keys[:15]

	data = ''
	if have_we_wiki:
		data = wiki_extract

	data += ' ' + ' '.join([x['t'] + x['d'] for x in google_results[3:]])
	url_counter = 0
	for i in google_results:
		if url_counter == 3:
			break
		url = i['a']
		if '.wikipedia.org' in url.lower():
			if have_we_wiki:
				continue
		else:
			output['top_urls'].append(url)
		try:
			data += ' ' + self.request(url).text
		except:
			continue
		else:
			url_counter += 1

	self.options['query'] = fullname
	self.options['limit'] = 1
	self.options['id'] = None
	self.options['output'] = False
	sanction = self._loaded_modules['sanctionsearch']
	san_out = sanction.module_api(self)
	if san_out['results']:
		self.options['id'] = int(san_out['results'][0]['link'].split('?id=')[1])
		self.options['query'] = None
		sanction.NAMESEARCH = False
		san_out = sanction.module_api(self)
		output['is_in_blacklist'] = True
		output['usa_blacklist'] = san_out
	else:
		output['is_in_blacklist'] = False
		output['usa_blacklist'] = {}

	self.output('Getting term-frequencies related to person...')
	data +=  ' ' + ' '.join(output['top_searched_queries'])
	plot_histogram = self.tf_histogram(data, 'html')
	plot_histogram.remove_stopwords([name.lower(), family.lower(), fullname.lower(), query.lower()]+query.lower().split(' '))
	output['term_frequency'] = plot_histogram.plot_histogram(f"Top 10 Most Common Words for {fullname}", 15, should_show=show_plot)

	OUTPUT[fullname] = output

	if depth < target_depth:
		child_nodes = []
		for item in output.get('info'):
			if item.startswith('Spouse: '):
				spouses = item[8:].split(',')
				names = list(map(lambda x: x[:x.index("(")].strip(), spouses))
				child_nodes.extend(names)
			if item.startswith('Children: '):
				child_nodes.extend(list(map(lambda x: x.strip(), item[10:].split(','))))

			child_nodes = list(filter(lambda x: 'MORE' not in x, child_nodes))

		for node in child_nodes:
			if node not in VISITED:
				self.options['query'] = node
				module_api(self, depth+1)

def module_run(self):
	module_api(self)
	print()
	self.alert_results(OUTPUT)
