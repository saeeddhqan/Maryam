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

import os
import string
import random
import urllib.parse as urlparse
from concurrent.futures import ThreadPoolExecutor
import requests

class main:

	def __init__(self, response: requests.models.Response, type=[]):
		""" Downloader

			response 	: Web request response
		"""
		self.framework = main.framework
		self.acceptedTypes = type
		self.response = response
		self.headers = response.headers
		self._url = response.url
		self._parsedUrl = urlparse.urlparse(self._url)
		self._name = None
		self._extention = None
		self._save_file = False
		self._filename = None
		
	def run_crawl(self) :
		# get the name and extention 

		self.filename_from_url()
		self.needToContinue and self.filename_from_headers()
		
		# sanitize the name and fix file overwrite
		self._name = os.path.join(self.framework.workspace, \
			self._name.replace('/', '').replace('\\', ''))

		# fix path if exist
		self.needToContinue 
		self.get_file_name and self.fix_if_file_exist()
				
		# save the file 
		self._save_file and self.get_file_name and self.save_file() 
		if self._save_file:
			return self._filename
		return None
	
	def filename_from_url(self):
		"""return: Filename from the url if exist else random name"""
		fname = requests.utils.unquote(os.path.basename(self._parsedUrl.path)\
			.strip(" \n\t.")).replace(' ','-')
		if '.' in fname :
			self._name,self._extention = os.path.splitext(fname)
			if self._extention and self._name == '':
				self._name = self._parsedUrl.netloc.split('.')[-2] + '-' + self.random_filename
		else :
			self._name = self._parsedUrl.netloc.split('.')[-2] + '-' + self.random_filename

	@property
	def needToContinue(self):
		if self._name and self._extention:
			if (self._extention[1:] if '.' in self._extention else self._extention) \
				in self.acceptedTypes or self.acceptedTypes == [] :
				self._save_file = True
			return False
		return True

	@property
	def random_filename(self):
		"""return a random name of 8 char long"""
		return "".join([random.choice(string.ascii_lowercase + string.digits) \
			for _ in range(8)])

	def filename_from_headers(self):
		"""find filename from response header 
		return the filename or random filename with filetype if exist else just filename
		example - (image/jpeg) (application/pdf) (text/javascript (obsolete)) application/something+pdf ; charset=utf-8
		"""
		content_type = self.headers.get('Content-Type')
		if not content_type : 
			return 
		elif '/' in content_type :
			# extract the extention for the file
			splited_content_type = content_type.split(';', 1)
			if len(splited_content_type) > 1 :
				parameters = { ele[0]: ele[1] \
					for ele in [par.strip().split('=') \
						for par in splited_content_type[1].split(';') \
							if '=' in par]}
				tempname = parameters.get('filename')
				if tempname and '.' in tempname: 
					self._name, self._extention = os.path.splitext(tempname)
					
			self._extention = os.path.basename(splited_content_type[0].strip().split(' ')[0]).split('+')[-1]

	@property
	def get_file_name(self):
		if self._extention in ['.javascript','javascript']:
			self._extention = 'js'
		if '.' in self._extention:
			self._filename = (self._name or '') + (self._extention or '')
		else :
			self._filename = ".".join([(self._name or ''),(self._extention or '')])
		return self._filename

	def fix_if_file_exist(self):
		"""check if file exist in workspace true then add random char in name end"""
		if os.path.exists(self._filename) :
			self._name += f"-{self.random_filename[:4]}"      

	def save_file(self):
		"""save the content in the file """
		open(self._filename, 'wb').write(self.response.content)
		self.framework.output(f"[DOWNLOADER] File is saved as {os.path.basename(self._filename)} in workspace")

	@staticmethod
	def make_req(url):
		try:
			return main.framework.request(url=url)
		except :
			main.framework.error(f"response issue with this url - {url}", 'util/downloader', 'make_req')
			return None

	@classmethod
	def get(cls, **kwargs):
		""" takes only url or response(of request module) as input kwargs 
		and make request if url finally call the __init__ function """
		if 'url' in kwargs:
			if "://" in kwargs['url']:
				# make request to the module
				res = cls.make_req(kwargs.get('url'))
				if res :
					return cls.get(
						response=res,
						type=kwargs.get('type') or []
					)
			else :
				main.framework.error('Not a valid url please check it again', 'util/downloader', 'get classmethod')
		elif 'response' in kwargs:
			if isinstance(kwargs.get('response'), requests.models.Response):
				a = cls(
						response=kwargs['response'],
						type=kwargs.get('type') or []
					)
				a.run_crawl()
				return a
			else :
				# show error response should be of request type not anything else
				main.framework.error('Response should be of request type not anything else', 'util/downloader', 'get classmethod')
		else :
			# show error else 
			main.framework.error(f"Not valid Arguments {kwargs.keys()}", 'util/downloader', 'get classmethod')

	@classmethod
	def getAll(cls, urls : list , type : list ):
		"""take list of urls and get the info"""
		with ThreadPoolExecutor() as executor:
			executor.map(lambda url_: cls.get(url=url_, type=type), urls)
