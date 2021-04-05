import requests
from bs4 import BeautifulSoup
import time

class main:

    def __init__(self, use=False):
        '''
        use : Determine whether to use proxy or not.
        '''
        self.use=use

    iplist=[]
    proxydict={}

    def getproxy(self,use=False):
        if self.use==True:
            print("[PROXY] Gathering proxies. It's quite time consuming, so do some pushups in the meantime :P")
            URL=['https://premproxy.com/list/']

            i=2

            while i<=8:
                purl='https://premproxy.com/list/0'+str(i)+".htm"
                URL.append(purl)
                i+=1    

            ips=[]
            ips2=[]
            purl=URL[0]

            try:
                for purl in URL:
                    r=requests.get(purl)
                    sp=BeautifulSoup(r.content,'html.parser')
                    lst=list(sp.find_all('input',attrs={"name" : "proxyIp[]"}))
                    for l in lst:
                        ip=str(l.get('value'))[0:-6]
                        ips.append(ip)
                    time.sleep(2)
                #print(ips[0:5])
                print("[PROXY] Proxies gathered.")
            except Exception as e1:
                print(f"An error occured. Error details: {e1}")    
            j=0    
            while(j<len(ips)):
                ips[j]="http://"+ips[j]
                j+=1
            j=0

            print("[PROXY]  Now checking for availability of the proxies...")
            while(j<len(ips)):
                try:
                    if int(requests.get(ips[j]).status_code)==200:
                        ips2.append(ips[j])
                    
                    print(f"{ips[j]} is available! Yay! :D")
                except Exception as e2:
                    print(f"{ips[j]} is not available. :(")
                    print(f"An error occured. Error details: {e2}")
                finally:
                    j+=1 
            ips=[]                   
            #print(ips2)
            print("[PROXY] Availability check completed! Writing to file...")
            f=open('proxy_fetch.txt','w')
            
            i=ips2[0]
            for i in ips2:
                f.write(i)
                if i!=ips2[-1]:
                    f.write('\n')
            f.close()
            #readip()
#For debugging purposes, uncomment the line below     
#getproxy(use=True)   

    def readip(self):
        global iplist
        print("[PROXY] Reading from generated proxy list...")
        iplist=open("proxy_fetch.txt","r").readlines()

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

# print("Starting to rotate ips:")   
# ct=0
# while(True):
#  req=requests.get("https://www.google.com/?q=hello",proxies=rotateip(ct))
#  print(req.status_code)
#  if(req.status_code!=200):
#     if rotateip(ct+1)==-1:
#         print("Proxies finished!")
#         break
#     else:
#         ct+=1

