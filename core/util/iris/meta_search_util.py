class main:
	def __init__(self):
		self.framework = main.framework
     
	def make_cite(self, url: 'URL String') -> 'cite':
		default_pages = ['index']
		details = self.framework.urlib(url)
		
		p=details.path if len(details.path) > 1 else ""
		p=p.replace("/"," › ")
		s=f"{details.scheme}://{details.netloc}{p}"
		if len(s) > 110:
		    s=f"{s[:110]}..."
		return s
