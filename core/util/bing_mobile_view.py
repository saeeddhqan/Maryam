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

	def __init__(self, url):
		""" Bing mobile friendly test screenshot
		
			url	: url for screenshot
		"""
		self.framework = main.framework
		self.url = url
		self._raw_image_data = []
				
	def screenshot(self):
		self.framework.verbose('[Bing Mobile View] Fetching mobile view of the URL...')
		bing_api_url = 'https://www.bing.com/webmaster/tools/mobile-friendliness-result'
		self.framework._global_options['rand_agent'] = True
		try:
			response = self.framework.request(url=bing_api_url, method='POST', \
			data={'url': self.url, 'retry': '0'}, timeout=40).text # Setting high timeout of as some req take long
		except:
			self.framework.error('ConnectionError.', 'util/bing_mobile_view', 'screenshot')
			return  False
		else:
			
			if 'Bing Webmaster services could not be reached' in response :
				self.framework.error('Bing Webmaster services could not be reached', 'util/bing_mobile_view', 'screenshot')
				return False

			self._raw_image_data = re.findall(r'data\:image.*"', response) # Regex for base64 encoded image 

	@property
	def raw_image_data(self):
		if self._raw_image_data == []: # If no image return empty string else first image
			return ''
		return self._raw_image_data[0]

