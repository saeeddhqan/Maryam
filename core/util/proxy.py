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

#import requests
from bs4 import BeautifulSoup
import time
#Python proxy module. Contributed by: @anuran-roy under @saeeddhqan
class main:

    def __init__(self):
        self.framework.use = self.framework._global_options_['autoproxy']
        self.framework.iplist = []

    def getproxy(self):
        #if self.use:
        self.framework.output('[PROXY] Gathering proxies. It is quite time consuming, so do some pushups in the meantime :P')
        purls = [ 'https://premproxy.com/list/' ]
        i = 2
        while i<=8:
            purl = f"https://premproxy.com/list/0{str(i)}.htm"
            purls.append(purl)
            i += 1    
        ips = []
        ips2 = []
        purl = purls[0]
        try:
            for purl in purls:
                r = self.framework.request(url=purl, method="GET")
                sp = BeautifulSoup(r.content,'html.parser')
                lst = list(sp.find_all('input',attrs = {"name" : "proxyIp[]"}))
                ips = [str(l.get('value'))[0:-6] for l in lst]    
                time.sleep(2)
            #self.framework.output(ips[0:5])
            self.framework.output('[PROXY] Proxies gathered.')
        except Exception as e1:
            self.framework.error(f'[PROXY] An error occured. Error details: {e1}')    
        j = 0
        while j<len(ips):
            ips[j] = f"http://{ips[j]}"
            j += 1
        j = 0
        #self.framework.output('[PROXY] Now checking for availability of the proxies...')
        # while j<len(ips):
        #     try:
        #         if int(self.framework.request(url=ips[j],method="GET").status_code) == 200:
        #             ips2.append(ips[j])
        #     except:
        #         pass
        #     finally:
        #         j += 1 
        # ips = []                   
        #self.framework.output(ips2)
        #self.framework.output('[PROXY] Availability check completed! Writing to file...')
        f = open('proxy_fetch.txt','w')
        i = ips[0] if len(ips)>0 else None
        for i in ips: 
            f.write(i)
            if i != ips[-1]:
                f.write('\n')
        f.close()
        self.framework.output('[PROXY] Write operation completed!');
        # readip(self)
#For debugging purposes, uncomment the line below     
#getproxy(use=True)   

    def readip(self):
        self.framework.output('[PROXY] Enumerating proxies...')
        self.framework.output('[PROXY] Reading from generated proxy list...')
        self.framework.iplist = open("proxy_fetch.txt","r").readlines()
        self.framework.output(f'[PROXY] {len(self.framework.iplist)} working proxies found!')
#For debugging purposes, uncomment the line below     
#readip()     

    def rotateip(self,k=0):
    	#return {"http":self.framework.iplist[k]} if k<len(self.framework.iplist) else -1
        if k<len(self.framework.iplist):
           return {"http":self.framework.iplist[k]}
        else:
           return -1

#For debugging purposes, uncomment the line below     
#rotateip()

# self.framework.output("Starting to rotate ips:")   
# ct=0
# while(True):
#  req=requests.get("https://www.google.com/?q=hello",proxies=rotateip(ct))
#  self.framework.output(req.status_code)
#  if(req.status_code!=200):
#     if rotateip(ct+1)==-1:
#         self.framework.output("Proxies finished!")
#         break
#     else:
#         ct+=1
