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
import cloudscraper

meta = {
	"name": "Pwned database search",
	"author": "Vikas Kundu",
	"version": "1.0",
	"description": "Search your email for data breaches",
	"comments": (
			"Using XmlHttp API of haveibeenpwned.com",
			"to get JSON data"
	),
	"sources": (["https://www.haveibeenpwned.com"]),
	"options": (
		("email", None, True, "Email to search for breach", "-e", "store", str),
	),
	"examples": ("pwned -e <email> --output",)
}


def scrap(email):
	url = "https://haveibeenpwned.com/unifiedsearch/"+email
	scraper = cloudscraper.create_scraper()
	result = scraper.get(url)
	if(result.text != ""):
		return result.json()
	else:
		return False


def module_api(self):
	output, pwns = {}, {}
	email = self.options["email"]

	if(re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email)):
		self.verbose('Searching for pwning...')
		pwns = scrap(email)
		if pwns:
			output["Breaches"] = [{"BreachName": i["Name"], "BreachDomain":i["Domain"]} for i in pwns["Breaches"]]
			if pwns["Pastes"]:
				output["Pastes"] = [{"PasteId": j["Id"], "PasteSource": j["Source"]} for j in pwns["Pastes"]]
			else:
				output["Pastes"] = "Pastes not available for this email"
		else:
			output["Pastes"] = output["Breaches"] = "Email not pwned"
	else:
		self.error("Invalid Email")

	self.save_gather(output, "osint/email_pwned", email,
					 output=self.options["output"])
	return output


def module_run(self):
	output = module_api(self)

	for section in output.keys():
		if isinstance(output[section], str):
			self.output(output[section])
			break	
		elif not output:
			break
		headers = list(output[section][0].keys())
		rows = []
		for data in output[section]:
			rows.append(list(data.values()))
		self.table(rows, headers, section)
