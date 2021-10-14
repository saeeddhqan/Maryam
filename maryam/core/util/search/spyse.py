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

import cloudscraper
import json

# To add a new tool for Spyse, just add the following queries whichever applicable: 
# para_url, param_data and param_req_type in the method scrap()
# and then add a validate function to sort out relevant fields and send them to output.

class main:

	def __init__(self, search_type, search_param, count=10):
		""" spyse search 
			search_type		: Type of search to perform, i.e. subdomain-finder
			search_param	: Keyword to search
			count			: Number of results
		"""
		self.framework = main.framework
		self.scraper = cloudscraper.create_scraper()
		self.search_type = search_type
		self.search_param = search_param
		self.num = count
		self.url = 'https://spyse.com'
		self._data = {}

	def search(self):
		self.framework.verbose('[SPYSE] Searching...', end='\r')

		res = self.scrap()
		if res is None:
			return 
		
		code = res.status_code
		res = res.json()
		if "error" in res.keys():
			if "errors" in res["error"]:
				for i in res["error"]["errors"]:
					self.framework.error(f"[SPYSE] This error occured in the reponse data: {i['message']}", 'util/search/spyse', 'search')
			else:
				self.framework.error(f"[SPYSE] This error occured in the reponse data: {res['error']['message']}", 'util/search/spyse', 'search')
			return

		if code != 200:
			self.framework.error(f"[SPYSE] Response code not ok, something went wrong!", 'util/search/spyse', 'search')
			return

		prefix = str(self.search_type).split('-')
		self._data = getattr(self, f"{prefix[0]}_parse")(res)	# Calling parse method for each search type


	def scrap(self):
		param_url = {
			"company-lookup": f"{self.url}/api/data-v4/organization/search",
			"whois-lookup": f"{self.url}/api/data-v4/domain/{self.search_param}",
		}

		# JSON Dumps needed to keep double quotes from company-lookup data
		param_data = {
			"company-lookup" : json.dumps({"limit":20,"offset":0,"search_params":[
					{
						"name": {"operator":"contains","value":self.search_param}
					}
				],"query":""}),
				
			"whois-lookup": {}
		}

		param_req_type = {
			"company-lookup": "post",
			"whois-lookup": "get"
		}
		

		if param_url[self.search_type] is None:
			self.framework.error(f"[SPYSE] No valid search method found! Only these methods are available at present {list(param_url.keys())}", 'util/search/spyse', 'scrap')
			return 
			
		
		try:
			if param_req_type[self.search_type] == "get":
				req = self.scraper.get(url=param_url[self.search_type])
			else:
				req = self.scraper.post(url=param_url[self.search_type], data=param_data[self.search_type])
			return req
		except Exception as e:
			self.framework.error(f"ConnectionError: {e}", 'util/search/spyse', 'scrap')
			return None


	def whois_parse(self, api_data):
		return api_data["data"]

	def company_parse(self, api_data):
		return api_data

	@property
	def data(self):
		return self._data


