
# class main:
# 	def __init__(self):
# 		self.framework = main.framework

# 	def make_cite(self, url: 'URL string') -> 'cite':
# 		default_pages = ['index']
# 		urlib = self.framework.urlib(url)
# 		path = urlib.path
# 		host = f"{urlib.scheme}://{urlib.netloc}"
# 		host_len = len(host)
# 		if host_len >= 60 and host_len <= 110:
# 			if path != '':
# 				return f"{host} › ..."
# 			else:
# 				return host
# 		elif host_len > 110:
# 			host_split = urlib.netloc.split('.')
# 			suffix = host_split[-1:]
# 			if path != '':
# 				return f"{'.'.join(host_split)[:100]} ... .{suffix[0]} › ..."
# 			else:
# 				return f"{'.'.join(host_split)[:90]} ... .{suffix[0]}"
# 		if path in ('', '/'):
# 			return host
# 		path_join = []

# 		if '?' in path:
# 			path = path[:path.rfind('?')]
# 		counter = 0
# 		path_split = path.split('/')
# 		path_split = path_split[:3]+['...'] if len(path_split) > 3 else path_split 
# 		for section in path_split:	
# 			if not section or section == ' ':
# 				continue
# 			if '.' in section and section != '...':
# 				section = section[:section.rfind('.')]
# 			if section not in default_pages and len(section) > 1:
# 				if len(section) > 22:
# 					path_join.append(f"{section[:22]}...")
# 					break
# 				counter += len(section)
# 				if counter > 30:
# 					path_join.append(f"{section[:27]}...")
# 					break
# 				path_join.append(section)
# 			else:
# 				path_join.append('...')
# 				break
# 		path = "/".join(path_join)
# 		path = path.replace('/', ' › ')
# 		cite = f"{host} › {path}"
# 		return cite

class main:
	def __init__(self):
		self.framework=main.framework
     
	def make_cite(self, url: 'URL String') -> 'cite':
		default_pages=['index']
		details=self.framework.urlib(url)
		qs=details.query
		qs='&' + qs
		l=len(qs)

		word=''
		query_key=''
		query_value=''
		query={}
		k=0
		j=0

		for i in range(l):
			if qs[i]=='&'and k<l-1:
				k=i+1
				query_key=''
				if k<l:
					while qs[k] != '=' and k<l:
						if qs[k]=='+':
							query_value=query_value + ' '
						else:
							query_key=query_key + qs[k]

						if k<l-1:
							k=k+1
						else:
							break
						
					
			if qs[i]=='=' and k<l-1:
				j=i+1
				query_value=''
				if j<l:
					while qs[j] != '&' and j<l:
						if qs[j]=='+':
							query_value=query_value + ' '
						else:    
							query_value=query_value + qs[j]

						if j<l-1:
							j=j+1
						else:
							break
					
			
			query[query_key]=query_value

		#Processing starts now

		pt=f" {details.path}" #+details[2]

		pt=pt.replace("/"," > ")
		if details.path=="":
			pt=""
		qr=" : "
		qk=query.keys()
		for i in qk:
			qr+=i + "=" + query[i]+" : "
		qr=f" : q : {query['q']}" if 'q' in query.keys() else ""
		params=" >>> "+(details.params).replace("%20"," ").replace("+"," ")
		if len(details.params)==0:
			params=""
		if details.query=='':
			qr=""    
		frag=" #"+(details.fragment).replace("%20"," ").replace("+"," ")
		if len(details.fragment)==0:
			frag=""    
		fs=f"{details.scheme}://{details.netloc}{pt}{params}{qr}{frag}" 

		if len(fs) > 50:
			cr=fs[fs.rfind(" > "):]
			fs=f"{details.scheme}://{details.netloc} > ...{cr}"
		return fs

