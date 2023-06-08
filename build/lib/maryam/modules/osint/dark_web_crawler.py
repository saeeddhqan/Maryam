#!/usr/bin/env python3
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
import os
import sys
import json
import shutil
import socket
import threading
from requests import get
from time import sleep, time
from base64 import b64decode
from hashlib import md5

from maryam.core.basedir import BASEDIR

meta = {
	'name': 'Dark Web Crawler',
	'author': 'Kaushik',
	'version': '0.1',
	'description': 'A Dark Web Crawler that uses Best First Snowball Sampling',
	'options': (
		('query', None, True, 'Comma separated query strings', '-q', 'store', str),
		('depth', 1, False, 'Scraper depth level', '-d', 'store', int),
		('threads', 5, False, 'The number of workers', '-t', 'store', int),
	),
	'examples': ('dark_web_crawler -q <DOMAIN>',)
}

def _search(self, query, df):
    retriever = self.retriever(ngram_range=(1, 2), min_df=0, max_df=10, stop_words='english')
    df = retriever.filter_pages(df)
    retriever.fit(df)
    best = retriever.predict(query)
    best_indexes = list(best.keys())
    best_scores = list(best.values())
    return best_scores, list(df.iloc[inx] for inx in best_indexes)

def calculate_rank(self, query, data):
	"""Sort data by similarity to query"""
	import pandas as pd

	pages = list(data.values())
	df = pd.DataFrame(pages, columns=['pages'])
	df['pages'] = df['pages'].apply(lambda x:[x])
	scores, pages = _search(self, query, df)
	return scores, list(map(lambda x: x.tolist()[0][0], pages))

def assign_ranks(self):
	"""Assign ranks and save result"""
	global locked, \
			depth, \
			pos_q, \
			neg_q, \
			data,  \
			RESULTS

	locked = True
	scores, sorted_pages = calculate_rank(self, ' '.join(query), data)
	data = {}

	try:
		sorted_urls = list(map(lambda x: x[:x.index(' || ')], sorted_pages))
	except Exception:
		self.output(f"\r{' '*cols()}\r|| ERROR {sorted_pages[i]}", color='R')
		locked = False
		return 1

	for url in reversed(sorted_urls):
		# If url has children shift all children to beginning of q
		if url in children:
			pos_q = children[url][0] + list(set(pos_q)-set(children[url][0]))
			neg_q = children[url][1] + list(set(neg_q)-set(children[url][1]))

	clrline()
	separator = '\n' + ' ' * 24
	toprint = separator.join(sorted_urls[:5])
	self.output(f'Best result at depth {depth}: {toprint}\n', color='Y')

	if depth not in RESULTS:
		RESULTS[depth] = []

	for i in range(min(len(sorted_pages), 10)):
		try:
			a = sorted_pages[i].index(' || ')
			headers = sorted_pages[i][a+4:a+56].strip().replace('\n','')
			RESULTS[depth].append(f"{sorted_urls[i]} - {headers}")
		except Exception:
			self.output(f"\r{' '*cols()}\r|| ERROR {sorted_pages[i]}", color='R')

	depth += 1
	locked = False

def main(self):
	"""Actual searcher"""
	global visited,    \
		data,		   \
		children,	   \
		locked,		   \
		depth,		   \
		should_exit,   \
		pos_q,		   \
		neg_q,		   \
		page_hashes,   \
		blacklist,     \
		cols

	q_len = lambda: len(pos_q) + len(neg_q)
	print_status = lambda: self.output((f"\r{' '*cols()}\rDepth: {depth}  Queued: {q_len()}  "
		f"Searched: {len(data)}  Current: {curr[:70]+'...' if len(curr)>75 else curr}"), linesep=False, color='G')

	while depth <= maxdepth and not should_exit:
		start = time()
		while q_len() == 0 or locked:
			sleep(1)
			if time() - start > 9:
				if len(data) > 0:
					assign_ranks(self)
				should_exit = True
				return None

		if len(pos_q) > 0:
			curr = pos_q.pop(0)
			timeout = 10
		else:
			curr = neg_q.pop(0)
			timeout = 8

		print_status()

		fqdn_end = curr.index('onion') + 5

		# if subdirs of site have been visited more than 20 times then dont visit site
		# again
		if curr not in visited:
			visited.append(curr)
		else:
			continue

		try:
			tosearch = get(
				curr, 
				proxies = {
					'http':'socks5h://localhost:9050',
					'https':'socks5h://localhost:9050'
				},
				timeout = timeout
			).text
			sleep(1)
		except Exception as err:
			self.output(f"\r{' '*cols()}\r{curr} took too long to respond", color="R")

			# If a url is unresponsive remove all its subdirectories from queues
			pos_q = list(filter(lambda x: not x.startswith(curr[:fqdn_end]), pos_q))
			neg_q = list(filter(lambda x: not x.startswith(curr[:fqdn_end]), neg_q))

			continue

		if len(tosearch) < 30 or any(list(map(lambda x: x in tosearch, blacklist))):
			# print(f'\r{" "*cols()}\r{red}{curr} too small or contains blacklisted token(s){reset}')
			continue

		# There are often redirects to the same page by different urls.
		# Confirm that hash of current page is unique before proceeding
		page_hash = md5(tosearch.encode('utf-8')).hexdigest()
		if page_hash not in list(page_hashes.values()):
			page_hashes[curr] = page_hash
		else:
			continue

		score, _ = calculate_rank(self, ' '.join(query), {'_': tosearch})

		if score[0] > 0.01 * (depth + 1) and not should_exit:
			pp = self.page_parse(tosearch)
			pp.remove_html_tags

			# Doing this because after ranking pages we can grab url easily
			data[curr] = curr + ' || ' + pp.page

			complete_urls = set(re.findall(url_regex, tosearch))
			unique_complete = complete_urls - set(visited) - (set(pos_q).union(set(neg_q)))

			subdirs = set(
				map(
					lambda x: curr[:fqdn_end] + x if x.startswith('/') else curr[:fqdn_end] + '/' + x, 
					re.findall(subdir_regex, tosearch)
				)
			)
			unique_subdirs = subdirs - set(visited) - (set(pos_q).union(set(neg_q)))

			unique = unique_complete.union(unique_subdirs)
			# else:
			#	  unique = unique_complete

			# Positive set contains all the url that contain one or more keywords in them
			positive_set = set(
				filter(lambda x: any(list(keyword in x.lower() for keyword in query)), unique)
			)

			# Everything else goes in negative_set
			negative_set = unique - positive_set

			pos_q.extend(list(positive_set))
			neg_q.extend(list(negative_set))

			if len(unique) > 0:
				if len(negative_set) > 0:
					clrline()
					print('\n'.join(list(negative_set)[:30]))
				if len(positive_set) > 0:
					clrline()
					print('\n'.join(positive_set))

				children[curr] = [list(positive_set), list(negative_set)]

			else:
				self.output(f"\r{' '*cols()}\rNo links found in {curr}", color = "R")

		if len(data) > 15*(depth):
			assign_ranks(self)

def module_api(self):
	global RESULTS,    \
		visited,       \
		data,		   \
		maxdepth,      \
		children,	   \
		locked,		   \
		depth,		   \
		should_exit,   \
		pos_q,		   \
		neg_q,		   \
		page_hashes,   \
		blacklist, 	   \
		query,         \
		cols,          \
		clrline,       \
		url_regex,     \
		subdir_regex

	RESULTS = {}
	maxdepth = self.options['depth']

	cols = lambda: shutil.get_terminal_size().columns
	clrline = lambda : self.output('\r' + ' '*cols() + '\r', linesep=False)

	query = list(map(lambda x: x.lower(), self.options['query'].split(',')))

	banned_types = "|".join([
		'png',
		'svg',
		'gif',
		'jpg',
		'mp4',
		'js',
		'css',
		'xml',
		'rss',
		'webp',
		'jpeg',
		'woff',
		'eot',
		'ttf',
		'zip'
	])

	url_regex = rf'((?:https?:\/\/)\w+.onion\/?(?!\S+?(?:{banned_types}))[\w\/\-%\.\?]*\/?)'
	subdir_regex = r'<a href="(\/?\S+(?:html|php)\?.*?)"'

	visited = []
	page_hashes = {}
	children = {}
	data = {}

	depth = 1
	locked = False
	should_exit = False

	# Must do this if you want colours to work on windows
	iswin = sys.platform.startswith('win')
	if iswin:
		os.system('color')

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	host = socket.getaddrinfo('127.0.0.1', 9050)
	status = sock.connect_ex(host[-1][4])
	if status != 0:
		self.error('Tor proxy not found on port 9050, aborting', 'dark_web_crawler', 'main')
		self.error(
			'Refer to https://2019.www.torproject.org/docs/debian.html.en for installation', 
			'dark_web_crawler', 
			'main'
		)
		should_exit = True
		exit(0)

	# Load blacklist
	blacklist = []
	with open(os.path.join(BASEDIR, 'data', 'blacklist.txt')) as f:
		for line in f:
			blacklist.append(b64decode(line).decode())

	if any(list(word in query for word in blacklist)):
		self.output('Blacklist disabled because query contains blacklisted token', color='Y')
		blacklist = []

	# Use search engine results for query as starting urls for crawler
	self.alert('Grabbing results from Phobos')
	neg_q = []
	for i in range (1,4):
		url = f"http://phobosxilamwcg75xt22id7aywkzol6q6rfl2flipcqoc4e4ahima5id.onion/search?query={'+'.join(query)}&p={i}"
		headers = {
			'Referer': url
		}
		phobos_page = get(
			url, 
			proxies={
				'http':'socks5h://localhost:9050',
				'https':'socks5h://localhost:9050'
			},
			headers = headers,
			timeout=10
		).text
		neg_q.extend(re.findall('<a class="titles" href="(.*?)"', phobos_page))

	self.alert('Grabbing results from Ahmia')
	url = f"https://ahmia.fi/search/?q={'+'.join(query)}"
	ahmia_page = get(url).text
	neg_q.extend(re.findall(r'redirect_url=(.*?)">', ahmia_page))

	pos_q = []

	threadcount = self.options['threads']
	threads=[]
	# Anything above four causes tor to ban us within depth 2
	for _ in range(threadcount):
		threads.append(threading.Thread(target=main, args=(self,)))
		threads[-1].start()
	
	while depth <= maxdepth and not should_exit:
		sleep(2)

	return RESULTS

def module_run(self):
	module_api(self)
	self.output('Waiting for outstanding requests to finish.')
	sleep(8)
	print()
	for depth in RESULTS.keys():
		self.output(f"Depth {depth} :")
		for result in RESULTS[depth]:
			self.output('\t' + result)
