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
	'name': 'Discord Search',
	'author': 'Divya Goswami',
	'version': '1.0',
	'description': 'Search the name of any user or server on discord [from disboard and discordhub]',
	'sources': ('discord',),
	'options': (
		('user', None, False, 'User flag (search for a user)', '-u', 'store', str),
		('server', None, False, 'Server flag (search for a server)', '-s', 'store', str),
		('limit', 3, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('engine', 'discord', False, 'Engine used is discord', '-e', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
	'examples': ('discord -u <QUERY> --output', 'discord -s <QUERY> -l 5')
	}

PAGES = ''

def search(self, name, q, q_formats, limit, count):
	global PAGES, LINKS
	engine = getattr(self, name)
	name = engine.__init__.__name__
	varnames = engine.__init__.__code__.co_varnames
	if 'limit' in varnames:
		attr = engine(q, limit)
	attr.run_crawl()
	PAGES += attr.pages

def module_api(self):
	user = self.options['user']
	server = self.options['server']
	if user and server:
		self.error("Choose to search only one among user and server.")
		return
	elif user:
		if user.isdigit():
			query = f'{user}_u'
		else:
			self.error("Enter user's 4 digit tag only [ #<Number> ]")
			return
	elif server:
		query = f'{server}_s'
	else:
		self.output("Provide either user or a server as a query")
		return
	limit = self.options['limit']
	engine = ['discord']
	output = { 'servers': [], 'users': [] }
	u_list = []
	s_list = []
	self.thread(search, self.options['thread'], engine, query, {}, limit, 0, meta['sources'])
	user_reg = r'<h4 class="title"><a href="\/profile\/(\d+)">(.+)<\/a'
	server_reg = r'<img src="https:\/\/cdn\.discordapp\.com\/icons\/(\d+).+alt="(.+)" width'
	u_list += [i for i in set(re.findall(user_reg, PAGES))]
	s_list = [i for i in set(re.findall(server_reg, PAGES))]
	output['servers'] += [f"{i[1]}\n Join: \thttps://disboard.org/server/join/{i[0]}" for i in s_list]
	output['users'] += [f"{i[1]}\n Check Full Profile: \thttps://discord.id/?prefill={i[0]}" for i in u_list]

	self.save_gather(output, 'osint/discord_search', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))
