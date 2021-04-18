class main:
	def __init__(self):
		self.framework = main.framework
     
	def make_cite(self, url: 'URL String') -> 'cite':
		default_pages = ['index']
		details = self.framework.urlib(url)
		print(details)
		
		s = f"{details.scheme}://{details.netloc}"
		if len(details.netloc) > 30:
			s = f"{details.scheme}://{details.netloc[:5]}...{details.netloc[-25:]}"
	
		p = details.path if len(details.path) > 1 else ""
		if len(p) > 30:
			p = f"{p[:15]}...{p[-15:]}"
		p = p.replace("/"," › ").replace("%20"," ")
		return f"{s}{p}"
