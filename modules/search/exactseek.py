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
	'name': 'Exactseek Search',
	'author': 'Divya Goswami',
	'version': '1.0',
	'description': 'Backend engine for activesearch. Gives better SEO based results',
	'sources': ('exactseek.com',),
	'options': (
		('query', '', False, 'Enter a location name', '-q', 'store', str),
		('limit', '3', False, 'Search results upto how many pages', '-l', 'store', str),
		('engine', 'exactseek', False, 'Engine used is photon', '-e', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
	'examples': ('exactseek -q OSINT --output',
				'exactseek -q owasp -l 6',
				)
	}

def module_api(self):
	global PAGES
	query = self.options['query']
	limit = self.options['limit']
	engine = self.options['engine']
	output = {'RESULTS':[]}
	run = self.exactseek(query, limit)
	run.run_crawl()
	PAGES = run.pages
	trimmed = re.findall(r'<ol>(<.+>)<\/ol>', PAGES)
	split_reg = r'a.+>(.*)<\/a><br \/>(.*)<br \/>.*"nofollow">(.*)<\/a> &middot;'
	for each in trimmed:
		groups = re.search(split_reg, each)
		title = groups.group(1)
		body = groups.group(2)
		link = groups.group(3)
		output['RESULTS'].append(f"{title}\n{body}\nDetails: {link}")
	self.save_gather(output, 'search/exactseek', query, output=self.options.get('output'))
	return output

def module_run(self):
	output = module_api(self)
	for each in output['RESULTS']:
		self.output(each, 'G')
		print()