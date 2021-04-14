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

import requests
import json

class main :
	def __init__(self, q, limit=50, session_id=''):
		""" instagram.com search
			
			q 		  : The query for search
			limit	  : The number of details min 50 if exist
			session_id: Your Instagram session id
		"""
		
		self.q = q
		self.limit = int(limit/50) or 1
		self.session_id = session_id
		self.base_url = 'https://www.instagram.com/'
		self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		if self.session_id :
			self.headers['Cookie'] = f"sessionid={self.session_id};"

		# request requrements
		self.data = {}
		self.posts_next_page = None
		self.followers_next_page = None
		self.following_next_page = None
		self.is_private = None

		# output_data
		self._userdata = {}
		self._followers = []
		self._following = []
		self._post = []

		self.session = requests.Session()

	def run_crawl(self) :
		self.framework.verbose('[INSTAGRAM] Extracting Data From API')
		# 1.1 account details find user on instagram 
		req = self.get_user_account_info()
		if req.status_code == 404 or self.data == {}:
			# user not found - show similar account names
			self.framework.error('Account not Found.', 'util/instagram', 'run_crawl')
			similar_users = self.get_similar_users()
			if similar_users :
				self.framework.heading('showing similar users', 0)

			for index, user in enumerate(similar_users, 1):
				self.framework.alert(f" {index}. user: {user['username']} --> {self.base_url + user['username']}")
			return

		if self.is_private or req.status_code != 200:
			# return if account is private or request fails
			if self.is_private: 
				self.framework.error('Account is Private.', 'util/instagram', 'run_crawl')
				if self.session_id == '':
					return

			else:
				self.framework.error(f"Request Fails, Url: {req.url}", 'util/instagram', 'run_crawl')
				return
		
		# 2. get post and follwers and following
		for _ in range(self.limit):
			if not self.get_user_posts():
				break
		
		for _ in range(self.limit):
			if not self.get_user_followers():
				break
		
		for _ in range(self.limit):
			if not self.get_user_following():
				break


	def get_user_account_info(self):
		"""extracting required user info form request"""
		req = self.session.get(url=f'{self.base_url}{self.q}/?__a=1', headers=self.headers)    
		try: 
			self.data = req.json()
		except:
			self.framework.error('Request Fail!! Too many tries', 'util/instagram', 'get_user_account_info')
			return
		if self.data:
			# id
			self._userdata['id'] = self.data['graphql']['user']['id']
			# username
			self._userdata['username'] = self.data['graphql']['user']['full_name']
			# bio
			self._userdata['bio'] = self.data['graphql']['user']['biography']
			# followers
			self._userdata['followers'] = self.data['graphql']['user']['edge_followed_by']['count']
			# following
			self._userdata['following'] = self.data['graphql']['user']['edge_follow']['count']
			# post 
			self._userdata['post_count'] = self.data['graphql']['user']['edge_owner_to_timeline_media']['count']
			# profile_pic
			self._userdata['profile_pic'] = self.data['graphql']['user']['profile_pic_url_hd']
			# is a private account
			self.is_private = self.data['graphql']['user']['is_private']
		return req

	def get_similar_users(self):
		"""return 20 similar users"""
		url = f"{self.base_url}web/search/topsearch/?query={self.q}"
		r = requests.get(url=url, headers=self.headers)
		# return first 20 similar names 
		return [i['user'] for i in r.json()['users']][:20]

	def get_user_posts(self):
		"""return boolean: if there is more data to extract"""
		url = f"{self.base_url}graphql/query/?"

		# set payload - id is target-id and have max limit is 50 at a request
		payload = {'id': self._userdata['id'], 'first': 50}
		if self.posts_next_page:
			payload['after'] = self.posts_next_page
		
		payload = json.dumps(payload)

		# encode the payload and add in params
		params = {'query_hash': '003056d32c2554def87228bc3fd9668a', 'variables': payload.encode()} 
		
		# geting response
		data = self.session.get(url, params=params, headers=self.headers).json()

		# extracting data from the response
		if data['status'] == 'ok':
			for node in data['data']['user']['edge_owner_to_timeline_media']['edges']:
				post = f"{self.base_url}p/{node['node']['shortcode']}"
				self._post.append(post)
				
			# have more posts 
			if data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']:
				self.posts_next_page = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
				return True
			else:
				self.posts_next_page = None
				return False
		else:
			self.framework.error('Request For collecting User POST is unsuccessful.', 'util/instagram', 'get_user_posts')
			return False

	def get_user_followers(self):
		"""return boolean: if there is more data to extract"""
		url = f"{self.base_url}graphql/query/?"

		# set payload - id is target-id and have max limit is 50 at a request
		payload = {'id': self._userdata['id'], 'include_reel': True, 'fetch_mutual': True, 'first': 50}
		if self.followers_next_page:
			payload['after'] = self.followers_next_page
		
		payload = json.dumps(payload)

		# encode the payload and add in params
		params = {'query_hash': 'c76146de99bb02f6415203be841dd25a', 'variables': payload.encode()}
		
		# geting response
		data = self.session.get(url, params=params, headers=self.headers).json()
		
		# extracting data from the response
		if data['status'] == 'ok':
			response_users = data['data']['user']['edge_followed_by']['edges']
			for node in response_users:
				user = {'id': node['node']['id'],
						'username': node['node']['username'],
						'profile_pic_url': node['node']['profile_pic_url']}
				self._followers.append(user)

			# have more followers 
			if data['data']['user']['edge_followed_by']['page_info']['has_next_page']:
				self.followers_next_page = data['data']['user']['edge_followed_by']['page_info']['end_cursor']
				return True
			else:
				self.followers_next_page = None
				return False

		else:
			self.framework.error('Request For collecting User Followers is unsuccessful.', 'util/instagram', 'get_user_followers')
			return False
	
	def get_user_following(self):
		"""return boolean: if there is more data to extract"""
		url = f"{self.base_url}graphql/query/?"

		# set payload - id is target-id and have max limit is 50 at a request
		payload = {'id': self._userdata['id'], 'include_reel': True, 'fetch_mutual': True, 'first': 50}
		if self.following_next_page:
			payload['after'] = self.following_next_page
		
		payload = json.dumps(payload)
		
		# encode the payload and add in params
		params = {'query_hash': '3dec7e2c57367ef3da3d987d89f9dbc8', 'variables': payload.encode()}
		
		# geting response
		data = self.session.get(url, params=params, headers=self.headers).json()
		
		# extracting data from the response
		if data['status'] == 'ok':
			response_users = data['data']['user']['edge_follow']['edges']
			for node in response_users:
				user = {'id': node['node']['id'],
						'username': node['node']['username'],
						'profile_pic_url': node['node']['profile_pic_url']}
				self._following.append(user)

			# have more followers 
			if data['data']['user']['edge_follow']['page_info']['has_next_page']:
				self.following_next_page = data['data']['user']['edge_follow']['page_info']['end_cursor']
				return True
			else:
				self.following_next_page  = None
				return False

		else:
			self.framework.error('[INSTAGRAM] Request For collecting User Following is unsuccessful.')
			return False


	@property
	def userdata(self):
		return self._userdata
	
	@property
	def followers(self):
		return self._followers
	
	@property
	def following(self):
		return self._following
	
	@property
	def post(self):
		return self._post
