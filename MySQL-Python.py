__author__ = 'administrator'
#!/usr/bin/python
#-*-coding:utf-8-*-
#coding=utf-8
import MySQLdb
import urllib
import urllib2
import re
x=0
cxn=MySQLdb.connect(host="localhost",user="root",passwd="11024617",db="test1",charset="utf8")
cur=cxn.cursor()
def jianshu(url):
        myurl=url
        m=urllib2.urlopen(myurl)
        page=m.read().decode('utf-8')
        title=find_title(page)
        writer=find_writer(page)
        print title
        print writer
        cont=sava_content(myurl,title,writer)
        #val={'title':title,'content':contents,'auther':writer}
        sql="insert into article values("+title+","+cont+","+writer+")"
        #cur.execute(sql)
        cxn.commit()
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
        print len(contentlist)
        tpo1=dele1.subn(r'\n    ',contentlist[0])
        tpo2=dele2.subn(r'',tpo1[0])
        tpo3=dele3.subn(r'\n',tpo2[0])
        ftp=open(title+'.txt','w+')
        ftp.write('title:'+title.encode('utf-8')+'\n')
        ftp.write('auther:'+writer.encode('utf-8')+'\n')
        ftp.write(tpo3[0].encode('utf-8'))
        ftp.close()
        return  tpo3[0]
        raw_input()
def downloadimg(page,i):
	    pattern5=r'src="(.*?.jpg)"'
	    imgre=re.compile(pattern5)
	    imglist=re.findall(imgre,page)
	    x=i
	    for imgurl in imglist:
		  urllib.urlretrieve(imgurl,'%s.jpg' %x)
		  x=x+1
def get_lj(mypage):
        ljlist=re.findall(r'class="title" href="(.*?)"',mypage)
        return ljlist
urll='http://www.jianshu.com/'
def main(urll):
        m=urllib2.urlopen(urll)
        mypage=m.read().decode('utf-8')
        i=0
        cur.execute("drop table if exists article")
        cur.execute("create table article(title varchar(500),content mediumtext,auther varchar(200))")
        #cur.execute("select * from article")
        #results=cur.fetchall()
        #for row in results:
           #print row
        for lj in get_lj(mypage):
            jianshu(urll+lj)
            m=urllib2.urlopen(urll+lj)
            page=m.read().decode('utf-8')
            downloadimg(page,i)
            i=i+x
        cxn.close()
        cur.close()

main(urll)
