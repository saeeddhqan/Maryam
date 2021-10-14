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


meta = {
	'name': 'Spyse Search',
	'author': 'Vikas Kundu',
	'version': '0.1',
	'description': 'Search your query through the Spyse tools and show the results. Search types available are: whois-lookup, company-lookup,',
	'sources': (['spyse']),
	'options': (
		('search_type', None, False, 'Type of search to perform(e.g, whois-lookup)', '-s', 'store', str),
		('param', None, False, 'Parameter to search for(e.g, www.google.com)', '-p', 'store', str),
		('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store', int),
	),
	'examples': ('spyse -s whois-lookup -p www.google.com -t domain-name',),
}

def module_api(self):
	search_type = self.options['search_type']
	param = self.options['param']
	count = self.options['count']

	spyse = self.spyse(search_type, param, count)
	spyse.search()
	output = {"results": ""}
	if spyse.data:
		output["results"] = spyse.data 

	self.save_gather(output, 'search/spyse', param, output=self.options.get('output'))	
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
