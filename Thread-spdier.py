__author__ = 'administrator'
import urllib
import urllib2
import re
import threading
x=0
def jianshu(url):
        myurl=url
        m=urllib2.urlopen(myurl)
        page=m.read().decode('utf-8')
        title=find_title(page)
        writer=find_writer(page)
        print title
        print writer
        sava_content(myurl,title,writer)
def find_title(page):
        mymatch=re.search(r'<h1 class="title">(.*?)</h1>',page)
        if mymatch:
         title=mymatch.group(1)
        return  title
def find_writer(page):
        mymatch1=re.search(r'<p><a href=".*?">(.*?)</a></p>',page)
        writer=mymatch1.group(1)
        return writer
def sava_content(url,title,writer):
        url=url
        page=urllib2.urlopen(url).read()
        page1=page.decode('utf-8')
        contentlist=re.findall(r'<div class="show-content">[\w\W]*?</div>',page1)
        dele1=re.compile(r'</p>\s?<p>')
        dele2=re.compile(r'<.*?>')
        dele3=re.compile(r'\n+')
        #print len(contentlist)
        tpo1=dele1.subn(r'\n    ',contentlist[0])
        tpo2=dele2.subn(r'',tpo1[0])
        tpo3=dele3.subn(r'\n',tpo2[0])
        ftp=open(title+'.txt','w+')
        ftp.write('title:'+title.encode('utf-8')+'\n')
        ftp.write('auther:'+writer.encode('utf-8')+'\n')
        ftp.write(tpo3[0].encode('utf-8'))
        ftp.close()
        raw_input()
def downloadimg(page,i):
	    pattern5=r'src="(.*?.jpg)"'
	    imgre=re.compile(pattern5)
	    imglist=re.findall(imgre,page)
	    x=i
	    for imgurl in imglist:
		  urllib.urlretrieve(imgurl,'%s.jpg' %x)
		  x=x+1
urll='http://www.jianshu.com/'
class MyThread(threading.Thread):
    def __init__(self,target,string):
        super(MyThread,self).__init__()
        self.target=target
        self.string=string
    def run(self):
        self.target(self.string)

def main(urll):
    m=urllib2.urlopen(urll)
    mypage=m.read().decode('utf-8')
    ljlist=re.findall(r'class="title" href="(.*?)"',mypage)
    threads=[]
    nljlist=range(len(ljlist))
    for i in nljlist:
        t=MyThread(target=jianshu,string=urll+ljlist[i])
        threads.append(t)
    for th in threads:
        th.start()
    for th in threads:
        th.join()
main(urll)






