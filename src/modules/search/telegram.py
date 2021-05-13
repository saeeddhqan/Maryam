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
	'name': 'Search public telegram groups',
	'author': 'Vikas Kundu',
	'version': '0.1',
	'description': 'Search the publicly listed telegram groups for juicy info like emails, phone numbers etc',
	'sources': ('telegramchannels.me','google', 'carrot2', 'bing', 'yahoo', 'millionshort', 'qwant', 'duckduckgo'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store', int),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
		('engine', '', False, 'Engine names for search(default=telegramchannels.me)', '-e', 'store', str),
	),
    'examples': ('telegram -q <QUERY> -l 15 --output',)
}


LINKS = []
PAGES = ''

def search(self, name, q, q_formats, limit, count):
	global PAGES,LINKS
	engine = getattr(self, name)
	q = q_formats[f"{name}_q"] if f"{name}_q" in q_formats else q_formats['default_q']
	varnames = engine.__init__.__code__.co_varnames
	if 'limit' in varnames and 'count' in varnames:
		attr = engine(q, limit, count)
	elif 'limit' in varnames:
		attr = engine(q, limit)
	else:
		attr = engine(q)

	attr.run_crawl()
	LINKS += attr.links
	PAGES += attr.pages

def scrap(self,query,limit):
	global PAGES,LINKS	
	channel_links = []
	for page_no in range(1, limit + 1): # Scrapping all groups available
		self.verbose(f'[TELEGRAMCHANNELS] Searching in page {page_no}')
		try:
			req = self.request(f'https://telegramchannels.me/search?type=channel&page={page_no}&search={query}').text
		except Exception as e:
			self.error('Telegramchannels.me is missed!', 'telegram', 'scrap')

		if 'There are no media! Try another search!' in req:
			break
		else:
			channel_links += set(re.findall(r"https://telegramchannels\.me/channels/[\w]+", req)) # Find all channels
	
	pointer, total = 0, len(channel_links) # Variables for progress monitor
	# not using {channel_links.index(link)}/{len(channel_links)} as sometimes out of order iteration happens
	for link in set(channel_links): # Scraping channels individually
		pointer += 1
		self.verbose(f'[Telegramchannels.me ] Searching in channel {pointer}/{total}' )
		try:
			req = self.request(f'{link}').text
			LINKS += set(re.findall(r"t\.me/[\w]+", req))
			PAGES += req
		except Exception as e:
			self.error(f"Channel {link} is missed!", 'telegram', 'scrap')
	
def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	engines = self.options['engine'].split(',')
	output = {'group-links': [], 'handles': [], 'phone-numbers': []}
	q_formats = {
		'default_q': f"site:t.me/joinchat {query}",
		'millionshort_q': f'site:t.me/joinchat "{query}"',
		'qwant_q': f'site:t.me/joinchat {query}'
	}

	self.thread(search, self.options['thread'], engines, query, q_formats, limit, count, meta['sources'])
	
	scrap(self, query, limit)
	global LINKS #To avoid the error: local variable 'LINKS' referenced before assignment.
	LINKS = list(set(LINKS)) 
	output['group-links'] = list(self.reglib().filter(r"https?://([\w\-\.]+\.)?t\.me/joinchat/", LINKS))
	
	output['group-links'] += list(self.reglib().filter(r"t\.me/[\w]+", LINKS)) # Output for scraping sepertely

	output['handles'] = [i for i in set(re.findall(r"@[\w]+", PAGES)) if i not in ['@media', '@keyframes', '@font'] ]
	
	phone_set = [str(i) for i in set(re.findall(r"(\+?\d{1,3}[- ]?)?(\d{10}\s)", PAGES)) ]
	# The regex is that: (it may start with a + or digits ranging from 1 to 3 optionally followed by space or -) or
	# ... (simply 10 digits followed by a space)
	
	for i in phone_set:	# Cleaning up the mobile numbers format
		i = re.sub(r"[^\d\+-]", '', i) # Remove all chars except digits, + and -
		output['phone-numbers'].append(i)
		
	self.save_gather(output, 'search/telegram', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))
