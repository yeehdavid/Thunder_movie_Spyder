from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pymysql
import sys
sys.setrecursionlimit(150000)
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='344126509', db='movie', charset='utf8')
cur=conn.cursor()


pages = set()

start_url='http://www.loldytt.com/'

def save_data(bsobj):
    for i in (bsobj.findAll('a', href=re.compile('thunder'))):
        # print(i['href'],i.get_text())
        # if 'href' in i.attrs:
        name ,thunder = i.get_text(),i.attrs['href']
        if  name.startswith('第') and name.endswith('集'):
            name = bsobj.findAll('title')[0].get_text().split('下载')[0] + name
        cur.execute("INSERT INTO thunder_url (name,thunder) VALUES (\"%s\",\"%s\")", (name ,thunder))
        cur.connection.commit()

def open_link(link):
    try:
        pages.add(link)

        html = urlopen(link)

    except:
        print(None)

    else:
        bsobj = BeautifulSoup(html.read(),'lxml')

        save_data(bsobj)#将本页面的资源链接先保存

        for i in (bsobj.findAll('a',href=re.compile('http://www.loldytt.com'))):
            #print(i['href'],i.get_text())
            #if 'href' in i.attrs:
            if i.attrs['href'] not in pages:
                print(i.attrs['href'])
                open_link(i.attrs['href'])



open_link(start_url)




