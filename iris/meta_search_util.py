
class main:
	def __init__(self):
		self.framework = main.framework

	def make_cite(self, url: 'URL string') -> 'cite':
		default_pages = ['index']
		urlib = self.framework.urlib(url)
		path = urlib.path
		host = f"{urlib.scheme}://{urlib.netloc}"
		host_len = len(host)
		if host_len >= 60 and host_len <= 110:
			if path != '':
				return f"{host} › ..."
			else:
				return host
		elif host_len > 110:
			host_split = urlib.netloc.split('.')
			suffix = host_split[-1:]
			if path != '':
				return f"{'.'.join(host_split)[:100]} ... .{suffix[0]} › ..."
			else:
				return f"{'.'.join(host_split)[:90]} ... .{suffix[0]}"
		if path in ('', '/'):
			return host
		path_join = []

		if '?' in path:
			path = path[:path.rfind('?')]
		counter = 0
		path_split = path.split('/')
		path_split = path_split[:3]+['...'] if len(path_split) > 3 else path_split 
		for section in path_split:	
			if not section or section == ' ':
				continue
			if '.' in section and section != '...':
				section = section[:section.rfind('.')]
			if section not in default_pages and len(section) > 1:
				if len(section) > 22:
					path_join.append(f"{section[:22]}...")
					break
				counter += len(section)
				if counter > 30:
					path_join.append(f"{section[:27]}...")
					break
				path_join.append(section)
			else:
				path_join.append('...')
				break
		path = "/".join(path_join)
		path = path.replace('/', ' › ')
		cite = f"{host} › {path}"
		return cite
