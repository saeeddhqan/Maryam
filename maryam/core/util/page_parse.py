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
from lxml import html

class main:
	def __init__(self, page):
		""" Page parser

			Page  		: web page content
		"""
		self.framework = main.framework
		self.page = page.decode('utf-8') if isinstance(page, bytes) else page

	@property
	def pclean(self):
		subs = r'<em>|<b>|</b>|</em>|<strong>|</strong>|<wbr>|</wbr>|<span class="vivbold qt0">\
				|%22|<span dir="[\w]+">|</span>|<h\d>|</h\d>|<q>|</q>'
		self.remove_comments
		self.page = re.sub(subs, '', self.page)
		self.page = re.sub(r"%3a", ' ', self.page)
		self.page = re.sub(r"%2f", ' ', self.page)
		self.page = re.sub(r"%2f", ' ', self.page)

	def html_fromstring(self, xpath, parent=None, results={}):
		if self.page == '':
			self.framework.error(f"document is nil", 'util/page_parse', 'html_fromstring')
			return False

		if isinstance(xpath, dict):
			for root in xpath:
				results[root] = self.html_fromstring(xpath[root], root)
		elif isinstance(xpath, list):
			results = {}
			for x in xpath:
				results[x] = self.html_fromstring(x, parent)
		else:
			tree = html.fromstring(self.page)
			results = []
			try:
				if parent:
					for node in tree.xpath(parent):
						results += node.xpath(xpath)
				else:
					results = tree.xpath(xpath)
			except:
				self.framework.error(f"invalid xpath: {xpath} or {parent}", 'util/page_parse', 'html_fromstring')
		return results

	def dork_clean(self, host):
		# Clear dork's fingerprints
		host = re.sub(r"(['\"]+)|(%40|@)", '', host)
		return host

	def findall(self, reg):
		return re.compile(reg).findall(self.page)

	@property
	def sites(self):
		self.pclean
		reg = re.compile(r'<cite>(.*?)</cite>')
		resp = []
		for itr in reg.findall(self.page):
			resp.append(self.framework.urlib(itr).netroot)
		return resp

	@property
	def remove_html_tags(self):
		""" Remove html tags with regex"""
		self.remove_comments
		scripts = re.compile(r"<script[^>]*>.*?</script>", 
				flags=re.DOTALL)
		styles = re.compile(r"<style[^>]*>.*?</style>",
				flags=re.DOTALL)
		tags = re.compile(r'<[^>]+>|&nbsp|&amp|&lt|&gt|&quot|&apos')
		self.page = re.sub(tags, '', re.sub(styles, '', re.sub(scripts, '', self.page)))

	@property
	def remove_comments(self):
		self.page = re.sub(r'(?=<!--)([\s\S]*?)-->', '', self.page)
		self.page = re.sub(r'(?=/\*)([\s\S]*?)\*/', '', self.page)

	@property
	def get_networks(self):
		self.pclean
		reg_id = self.framework.reglib().social_network_ulinks
		resp = {}
		page = self.page.replace('www.', '')
		for i in reg_id:
			if isinstance(reg_id[i], list):
				name = []
				for j in reg_id[i]:
					name += re.findall(j, page)
			else:
				name = re.findall(reg_id[i], page)
			names = []
			for j in name:
				if j not in names:
					names.append(j)
			resp[i] = names
		return resp

	def get_emails(self, host):
		self.pclean
		host = self.dork_clean(host + '.' if '.' not in host else host)
		emails = re.findall(r"[A-z0-9.\-]+@[A-z0-9\-\.]{0,255}?%s" % host, self.page)
		return [x.replace('\\', '') for x in list(set(emails))]

	@property
	def all_emails(self):
		self.pclean
		emails = self.framework.reglib(self.page).emails
		return emails

	def get_dns(self, host, urls=None):
		if urls:
			data = self.dork_clean(str(urls))
		else:
			self.pclean
			data = self.page

		resp = []
		reg = r"[A-z0-9\.\-%s]+\.%s" % ('%', host.replace('"', '').replace("'", ''))
		for i in re.findall(reg, re.sub(r'\\n', '', data)):
			i = i.replace('\\', '').replace('www.', '')
			if i not in resp and '%' not in resp:
				if i.lower().count(host) > 1:
					i = i.split(host)
					for j in i:
						j = f"{j}{host}"
						resp.append(j)
					continue
				resp.append(i)

		return resp

	def get_docs(self, query, urls=None):
		self.pclean
		if '%' in query:
			query = self.framework.urlib(query).unquote
		ext = re.search(r'filetype:([A-z0-9]+)', query)
		if ext:
			docs = []
			ext = f".{ext.group(1)}"
			if urls is None:
				urls = self.get_links
			for url in urls:
				if ext in url:
					docs.append(url)
			return list(set(docs))
		else:
			self.framework.error("Filetype not specified. Concat 'filetype:doc' to the query")
			return []

	def get_attrs(self, tag, attrs=None):
		if attrs is None:
			attrs = []
		reg = r"['\"\s]([^=][\w\-\d_]+)="
		# Find all attribute names
		if not attrs:
			attrs = re.findall(reg, tag)
		resp = {}
		for attr in attrs:
			if not re.search(fr"{attr.lower()}\s*=", tag.lower()):
				continue
			# Get the first char
			fchar = re.search(fr'{attr}=([\s]+)?.', tag)
			content= False
			if fchar:
				c = fchar.group()[-1:]
				# Get content of attrs
				if c not in "'\"":
					content = re.search(fr'{attr}=([^\s>]+)', tag)
				else:
					content = re.search(fr'{attr}={c}([^{c}]*){c}', tag)
			if content:
				content = content.group(1)
			content = content or ''
			resp[attr.lower()] = content
		return resp

	@property
	def get_metatags(self):
		self.remove_comments
		reg = r"<(?i)meta[^>]+/?>"
		reg = re.compile(reg)
		resp = []
		find = reg.findall(self.page)
		for tag in find:
			tag_attrs = self.get_attrs(tag)
			resp.append(tag_attrs)
		return resp

	@property
	def get_jsfiles(self):
		self.remove_comments
		reg = r"<(?i)script[^>]+>"
		reg = re.compile(reg)
		resp = []
		find = reg.findall(self.page)
		for tag in find:
			tag_attrs = self.get_attrs(tag, ['src'])
			for attr in tag_attrs:
				if 'src' in tag_attrs:
					src = tag_attrs[attr]
					urlib = self.framework.urlib(src)
					if urlib.check_urlfile('js'):
						resp.append(src)
		return resp

	@property
	def get_cssfiles(self):
		self.remove_comments
		reg = r"<(?i)link[^>]+/>"
		reg = re.compile(reg)
		resp = []
		find = reg.findall(self.page)
		for tag in find:
			tag_attr = self.get_attrs(tag, ['href'])
			for link in tag_attr:
				if 'href' in link:
					href = link.get('href')
					urlib = self.framework.urlib(href)
					if urlib.check_urlfile('css'):
						resp.append(href)
		return resp

	@property
	def get_links(self):
		self.remove_comments
		reg = r'[\'"](/.*?)[\'"]|[\'"](http.*?)[\'"]'
		reg = re.compile(reg)
		find = reg.findall(self.page)
		links = []
		for link in find:
			link = list(link)
			link.pop(link.index(''))
			link = link[0]
			if not re.search(r'<|>|/>', link):
				link = link.replace('\'', '').replace('"', '')
				links.append(link)
		return links

	@property
	def get_ahref(self):
		self.remove_comments
		reg = re.compile(r'<[aA].*(href|HREF)=([^\s>]+)')
		find = reg.findall(self.page)
		links = []
		for link in find:
			link = list(link)
			link.pop(link.index(''))
			link = link[0]
			links.append(link)
		return links

	@property
	def get_credit_cards(self):
		reg = re.compile(r"[0-9]{4}[ ]?[-]?[0-9]{4}[ ]?[-]?[0-9]{4}[ ]?[-]?[0-9]{4}")
		find = reg.findall(self.page)
		return list(set(find))

	@property
	def get_html_comments(self):
		reg = re.compile(r'<!--(.*?)-->')
		js_reg = re.compile(r'/\*(.*?)\*/')
		find = reg.findall(self.page)
		find.extend(js_reg.findall(self.page))
		return list(set(find))

	@property
	def get_forms(self):
		resp = {}
		self.remove_comments
		reg = re.compile(r'(?i)(?s)<form.*?</form.*?>')
		forms = reg.findall(self.page)
		form_attrs = ['action', 'method', 'name', 'autocomplete', 'novalidate', 'target', 'role']
		input_attrs = ['accept', 'alt', 'disabled', 'form', 'formaction', 'formenctype', 'formmethod',
					   'max', 'maxlength', 'min', 'minlength', 'name', 'pattern', 'readonly', 'required',
					   'selected', 'size', 'src', 'type', 'value', 'for']
		for form in range(len(forms)):
			form_tag = re.compile(r'<(?i)form.*?>')
			form_tag = form_tag.findall(forms[form])[0]
			get_form_attrs = self.get_attrs(form_tag, form_attrs)
			if 'action' not in get_form_attrs:
				get_form_attrs['action'] = '/'
			resp[form] = {'form': get_form_attrs}
			resp[form]['inputs'] = {}
			inputs = re.findall(r'<(?i)input.*?/?>', forms[form])
			textareas = re.findall(r'<textarea.*?>', forms[form])

			for inp in range(len(textareas)):
				inp_attrs = self.get_attrs(textareas[inp], input_attrs)
				if 'textarea' in resp[form]['inputs']:
					resp[form]['inputs']['textarea'].append(inp_attrs)
				else:
					resp[form]['inputs'].update({'textarea': [inp_attrs]})

			for inp in range(len(inputs)):
				inp_attrs = self.get_attrs(inputs[inp], input_attrs)
				if not 'type' in inp_attrs:
					type_attr = 'text'
					inp_attrs['type'] = 'text'

				type_attr = inp_attrs['type'].lower()
				# Set default submit value
				if type_attr == 'submit' and 'value' not in inp_attrs:
					inp_attrs['value'] = 'Submit Query'

				if type_attr in resp[form]['inputs']:
					resp[form]['inputs'][type_attr].append(inp_attrs)
				else:
					resp[form]['inputs'].update({type_attr: [inp_attrs]})

		return resp
