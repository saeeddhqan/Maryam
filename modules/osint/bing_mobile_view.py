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
import urllib
import json
import datetime
from os.path import dirname as up 

meta = {
	'name': 'Bing Mobile View',
	'author': 'Vikas Kundu',
	'version': '0.1',
	'description': 'Get screenshot of a URL in Bing mobile friendly view',
	'sources': (['bing']),
	'options': (
		('url', None, True, 'URL whose mobile screenshot needs to be taken', '-u', 'store', str),
		('blacklist', None, False, 'If this image is found retry, available= \
		[linkedin_authwall_en, add-your-custom]', '-b', 'store', str),
		('retries', 2, False, 'Number of times to try again if blacklist image found, default=2', '-r', 'store', int),
	),
	'examples': ('bing_mobile_view -u <URL>  --output',)
}

def blacklist_check(self, image_data):
	project_root = project_root = up(up(up(__file__)))
	black_img_path = os.path.join(project_root, 'data', 'images', 'blacklist', f'{self.options["blacklist"]}.json')

	if os.path.isfile(black_img_path) == False: #Check if blacklisted image exists?
		self.error('[Mobile Screenshot] The blacklisted image name entered by user does not exist.')
		return False
	
	blacklisted_image_data = json.load(open(black_img_path)) #Load the data of blacklisted image
	
	counter, run = 1, self.bing_mobile_view(self.options['url'])
	while blacklisted_image_data["img-data"] == image_data and counter <= self.options['retries']:
		self.verbose(f'[Bing Mobile View] Image scraped is blacklisted. Retry No:{counter}')
		if run.screenshot() == False:
			self.verbose(f'[Bing Mobile View] Error on retry no. {counter} \
			Maybe this is not a public profile.')
			return False
	
		image_data = run.raw_image_data
		counter+=1
	
	if counter-1 == self.options['retries']: #If all retries are done then return false otherwise image data
		self.error('[Bing Mobile View] Exhausted retries, maybe this is not a public profile.')
		return False
	else:
		return image_data

def url_split(url):
	folder_name = re.findall(r"/{2}[\w\.-]+/{1}",url) #Find string between // and /
	folder_name = folder_name[0].replace('/','') #Use first such string as folder name i.e. domain name

	trim_point = url.index(folder_name[-1:]) #Find index of last element of folder_name 
	image_name = f'{url[trim_point+1:]} {str(datetime.datetime.now())}.jpg' #Start file name from that point and add timestamp
	image_name = image_name.replace('/','-') #Replace char '/' to avoid directory errors
	#image_name = urllib.parse.quote_plus(image_name) #Or use full url encoding if still errors 
	
	return [folder_name, image_name]

def module_api(self):
	url = self.options['url']
	blacklisted_img_name = self.options['blacklist']
	retries = self.options['retries']
	output = {'Image-Location': [] }

	run = self.bing_mobile_view(url)

	if run.screenshot() == False: #If some error has occured while taking screenshot, return output to avoid further errors.
		return output

	image_data = run.raw_image_data

	'''
	Blacklisted images are images like authwall of linkedin, if they are found, retry.
	To add your own image, go to data/images/blacklist/ and save in file_name.json format
	like {'img-data':'base-64-data-of-image'}. Then pass it using -b param i.e. -b custom-blacklist-image
	For more info, see add-your-custom.json file.
	'''
	if blacklisted_img_name is not None:
		self.verbose('[Bing Mobile View] Checking if the image obtained is blacklisted...')
		image_data = blacklist_check(self, image_data)	
		if image_data == False: #If some error while blacklist_check function then exit
			return output
			
	'''
	When the image file is finally saved, it is saved inside the customer folder which is the same as
	the domain name. The rest of the url is the file name. i.e. if url = https://www.example.com/abc
	then file will be saved inside www.example.com folder and its name will be abc-timestamp.jpg
	where timestamp is added to make each image name unique.	
	'''

	splitted_url = url_split(url) #Fucntion to split URL into folder name and file name
	folder_name = splitted_url[0]
	file_name = splitted_url[1]

	project_root = project_root = up(up(up(__file__)))
	folder_filepath = os.path.join(project_root, 'data', 'images', folder_name)

	if os.path.isdir(folder_filepath) == False: #If no pre-existing folder for image, make one
		os.mkdir(folder_filepath)
	
	final_filepath = os.path.join(folder_filepath, f'{file_name}')

	response = urllib.request.urlopen(image_data)
	self.verbose('[Bing Mobile View] Dumping the image...')

	with open(final_filepath, 'wb') as f:
        	f.write(response.file.read())
    
	output['Image-Location'] += [str(final_filepath)]

	self.save_gather(output, 'osint/bing_mobile_view', url, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))
