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
from bs4 import BeautifulSoup

def remove_tags(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text()

meta = {
	'name': 'Pwned database search',
	'author': 'Vikas Kundu',
	'version': '1.2',
	'description': 'Search your email for data breaches',
	'comments': (
			'Using XmlHttp API of haveibeenpwned.com',
			'to get JSON data'
	),
	'sources': ('haveibeenpwned.com',),
	'options': (
		('email', None, True, 'Email to search for breach', '-e', 'store', str),
	),
	'examples': ('email_pwned -e <email> --output',)
}


def scrap(email):
	import cloudscraper
	url = f"https://eapi.pcloud.com/checkpwned?checkemail={email}"
	scraper = cloudscraper.create_scraper()
	result = scraper.get(url)
	if result.text:
		return remove_tags(result.text)
	else:
		return False


def module_api(self):
	output = {'content':[]}
	email = self.options['email']
	self.verbose('[PAWNED] Searching for pwning...')
	pwns = scrap(email)
	if pwns:
		output['content'] = pwns
	else:
		output['content'] = 'no breach'
	self.save_gather(output, 'osint/email_pwned', email,
					 output=self.options['output'])
	return output


def module_run(self):
	output = module_api(self)
	self.alert_results(output)
