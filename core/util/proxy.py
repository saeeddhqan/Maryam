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

#import self.framework.requests
from bs4 import BeautifulSoup
import time
#Python proxy module. Contributed by: @anuran-roy under @saeeddhqan
class main:

    def __init__(self, verbose = False):
        '''
        use : Determine whether to use proxy or not.
        '''
        self.use=self._global_options_['autoproxy']
        self.verbose = verbose
    iplist = []
    proxydict = {}

    def getproxy(self):
        if self.use == True:
            self.framework.output("[PROXY] Gathering proxies. It's quite time consuming, so do some pushups in the meantime :P")
            URL = [ 'https://premproxy.com/list/' ]
            i = 2
            while i<=8:
                purl = 'https://premproxy.com/list/0'+str(i)+".htm"
                URL.append(purl)
                i += 1    
            ips = []
            ips2 = []
            purl = URL[0]
            try:
                for purl in URL:
                    r = self.framework.requests.get(purl)
                    sp = BeautifulSoup(r.content,'html.parser')
                    lst = list(sp.find_all('input',attrs={"name" : "proxyIp[]"}))
                    for l in lst:
                        ip = str(l.get('value'))[0:-6]
                        ips.append(ip)
                    time.sleep(2)
                #self.framework.output(ips[0:5])
                self.framework.output("[PROXY] Proxies gathered.")
            except Exception as e1:
                self.framework.error(f"[PROXY] An error occured. Error details: {e1}")    
            j = 0
            while(j<len(ips)):
                ips[j] = f"http://{ips[j]}"
                j += 1
            j = 0
            self.framework.output("[PROXY] Now checking for availability of the proxies...")
            while(j<len(ips)):
                try:
                    if int(self.framework.requests.get(ips[j]).status_code)==200:
                        ips2.append(ips[j])
                    if self.verbose == True:
                        self.framework.output(f"[PROXY] {ips[j]} is available! Yay! :D")
                except Exception as e2:
                    if self.verbose == True:
                        self.framework.error(f"[PROXY] {ips[j]} is not available. :(")
                        self.framework.error(f"[PROXY] An error occured. Error details: {e2}")
                finally:
                    j += 1 
                ips = []                   
            #self.framework.output(ips2)
            self.framework.output("[PROXY] Availability check completed! Writing to file...")
            f = open('proxy_fetch.txt','w')
            i = ips2[0]
            for i in ips2:
                f.write(i)
                if i != ips2[-1]:
                    f.write('\n')
            f.close()
            #readip()
#For debugging purposes, uncomment the line below     
#getproxy(use=True)   

    def readip(self):
         global iplist
        self.framework.output("[PROXY] Reading from generated proxy list...")
        iplist = open("proxy_fetch.txt","r").readlines()
#For debugging purposes, uncomment the line below     
#readip()     

    def rotateip(self,k):
        global iplist
        if k<iplist[k]:
            return {"http":iplist[k]}
        else:
            return -1

#For debugging purposes, uncomment the line below     
#rotateip()

# self.framework.output("Starting to rotate ips:")   
# ct=0
# while(True):
#  req=self.framework.requests.get("https://www.google.com/?q=hello",proxies=rotateip(ct))
#  self.framework.output(req.status_code)
#  if(req.status_code!=200):
#     if rotateip(ct+1)==-1:
#         self.framework.output("Proxies finished!")
#         break
#     else:
#         ct+=1

