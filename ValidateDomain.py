import urllib2
import threading
allDomainList={}
class FetchThread(threading.Thread):
    def __init__(self, threadName, lines):
        self.threadName= threadName
        self.lines= lines
        threading.Thread.__init__(self)
    def run(self):
        getDomainStatus(self.threadName, self.lines)
def getDomainStatus(threadName,lines):
    output=''
    for domain in lines:
        domain=domain.strip()
        domainStatus=''
        if domain:
            domainStatus=domain+','
            if 'www.' in domain:
                domain=domain.replace('www.', '')
            try:
                response = urllib2.urlopen('http://www.google.com/a/'+domain)
                data = response.read()
                if not 'Server error' in data:
                   domainStatus=domainStatus+'yes,'
                else:
                    domainStatus=domainStatus+'no,'

                response = urllib2.urlopen('http://mail.google.com/a/'+domain)
                data = response.read()
                if not 'Server error' in data:
                   domainStatus=domainStatus+'yes'
                else:
                    domainStatus=domainStatus+'no'
            except:
                domainStatus=domain+',NA'+',NA'
        print domainStatus
        if threadName not in allDomainList:
           allDomainList[threadName]=[]
        allDomainList[threadName].append(domainStatus+'\n')

f=open('domains.txt', 'r')
domains=f.read().splitlines()
f.close()

split=1000;
lines=[]
start=0
threads=[]
for i in range(1,20):
    lines.append(domains[start:i*1000])
    start=start+1000
i=0
for line in lines:
    i=i+1
    threads.append(FetchThread(i,line))

for thread in threads:
    thread.start()

for t in threads:
    t.join()

keylist = allDomainList.keys()
keylist.sort()

f = open('domainChecked.csv', 'w')
output='Domain Name,Google Apps,Google Mail'
f.writelines(output)
for key in keylist:
    f.writelines(allDomainList[key])
f.close()