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

class main:

	def __init__(self, string=None):
		self.string = str(string)

	protocol_s = r"^([A-z0-9]+:\/\/)"
	protocol_m = r"([A-z0-9]+:\/\/)"
	email_s = r"^\w+@[A-z_\-.0-9]{5,255}$"
	email_m = r"\w+@[A-z_\-.0-9]{5,255}"
	phone_s = r"^([0-9]( |-)?)?(\(?[0-9]{3}\)?|[0-9]{3})( |-)?([0-9]{3}( |-)?[0-9]{4}|[A-z0-9]{7})$"
	phone_m = r"([0-9]( |-)?)?(\(?[0-9]{3}\)?|[0-9]{3})( |-)?([0-9]{3}( |-)?[0-9]{4}|[A-z0-9]{7})"
	domain_s = r"^([A-z0-9]([A-z0-9\-]{0,61}[A-z0-9])?\.)+[A-z]{2,6}(\:[0-9]{1,5})*$"
	domain_m = r"[A-z0-9\-]{0,61}\.+[A-z]{2,6}"
	url_s = r"^([A-z0-9]+:\/\/)?(www.|[A-z0-9].)[A-z0-9\-\.]+\.[A-z]{2,6}(\:[0-9]{1,5})*(\/($|[A-z0-9.,;?\'\\+&amp;%$#=~_-]+))*$"
	url_m = r"ftp|https?://[A-z0-9\-.]{2,255}[\/A-z\.:\-0-9%~@#?&()+_;,\']+"
	id_s = r"^@[A-z_0-9\.\-]{2,255}$"
	id_m = r"@[A-z_0-9\.\-]{2,255}"
	ip_s = r"^\d+\.[\d]+\.[\d]+\.[\d]+$"
	ip_m = r"\d+\.[\d]+\.[\d]+\.[\d]+"
	social_network_ulinks = {
		'Instagram': r"instagram\.com/[A-z_0-9.\-]{1,30}",
		'Facebook': [r"facebook\.com/[A-z_0-9\-]{2,50}", r"fb\.com/[A-z_0-9\-]{2,50}"],
		'Twitter': r"twitter\.com/[A-z_0-9\-.]{2,40}",
		'Github': r"github\.com/[A-z0-9_-]{1,39}",
		'Github site': [r"[A-z0-9_-]{1,39}\.github\.io", r"[A-z0-9_-]{1,39}\.github\.com"],
		'Telegram': r"telegram\.me/[A-z_0-9]{5,32}",
		'Youtube user': r"youtube\.com/user/[A-z_0-9\-\.]{2,100}",
		'Youtube channel': [r"youtube\.com/c/[A-z_0-9\-\.]{2,100}", \
				r"youtube\.com/channel/[A-z_0-9\-\.]{2,100}"],
		'Linkedin company': r"linkedin\.com/company/[A-z_0-9\.\-]{3,50}",
		'Linkedin individual': r"linkedin\.com/in/[A-z_0-9\.\-]{3,50}",
		'Googleplus': r"\.?plus\.google\.com/[A-z0-9_\-.+]{3,255}",
		'WordPress': r"[A-z0-9\-]+\.wordpress\.com",
		'Reddit': r"reddit\.com/user/[A-z0-9_\-]{3,20}",
		'Tumblr': r"[A-z0-9\-]{3,32}\.tumblr\.com",
		'Blogger': r"[A-z0-9\-]{3,50}\.blogspot\.com"
		}

	def search(self, regex, _type=list):
		regex = re.compile(regex)
		regex = regex.findall(self.string)
		return regex

	def sub(self, regex, sub_string):
		data = re.sub(regex, sub_string, self.string)
		return data
	
	def filter(self, regex, _list: list) -> list:
		if not isinstance(regex, str):
			return filter(regex, _list)
		else:
			return filter(re.compile(regex).match, _list)

	@property
	def emails(self):
		emails = self.search(self.email_m)
		return emails
	
	@property
	def urls(self):
		urls = self.search(self.url_m)
		return urls
	
	@property
	def domains(self):
		domains = self.search(self.domain_m)
		return domains
