# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import re
import requests
import csv
import os



def getHTMLText(url):
    try:
        headers = {
            'User-agent': 'your User-agent',
            'Host': 'weibo.cn',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': 'my cookie',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        r = requests.get(url, headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # r.encoding = 'utf-8'
        return r.text
    except:
        return ""


f = open('jieduan4.csv', 'a+')
csv_writer = csv.writer(f)
if not os.path.getsize("jieduan4.csv"):
    csv_writer.writerow(["内容", "赞"])


result = ""
sours = "http"
path_list = sours.split(";")
for path in path_list:
    for i in range(1, 50):
        html = getHTMLText(path+"&page="+str(i))
        # html = html.encode('ISO-8859-1')
        # html = html.decode('ISO-8859-1')
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')
        # print soup.prettify()
        # ps = soup.select(".m-text-cut")
        pl = soup.select("span")
        for li_quick in pl:
            r0 = re.sub(r'<[\w\s]+="[\w\S]+"([\s\w]+="[0-9]")*>|</\w+>|<\w+>$', ' ', str(li_quick))
            r1 = re.sub(r'<[\w]*>', '', r0)
            r = r1.lstrip()
            if r.split('[')[0] == "赞":
                result2 = r.split('[')[1]
                csv_writer.writerow([result, result2])
            else:
                result = r
            # print r
