"""爬虫，抓取DouyuTv上主播直播封面和主播名字"""

import requests
from lxml import etree
import os
import time


#创建一个放图片的文件夹，并更新图片
def createDir():
    if 'DouyuImg' not in os.listdir(os.getcwd()):
        os.mkdir(os.getcwd()+'/DouyuImg')
    os.chdir(os.getcwd()+'/DouyuImg')
    L = os.listdir(os.getcwd())
    for i in L:                     #每次抓取之前，先清除之前下载的图片
        if '.jpg' in i:
            os.remove(i)


#获取目标链接的整个html页面
def getHtml(url):
    html = requests.get(url)
    return html.content


#分析抓取的内容，并下载
def downloadImg(html):
    page = etree.HTML(html.lower().decode('utf-8'))
    names = page.xpath(u'//span[@class="dy-name ellipsis fl"]')
    imgs = page.xpath(u'//img[@data-original]')
    Img = [x.values()[0] for x in imgs]
    name = [x.text for x in names]
    L = list(zip(name,Img))
    for name,img in L:
        time.sleep(0.1)                                 #设置间隔，防止抓取太过暴力
        r = requests.get(img,stream = True)
        with open(name+'.jpg', 'wb') as f:
           for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)


if __name__== '__main__':
    createDir()
    url = "https://www.douyu.com/directory/all"
    Html = getHtml(url)
    downloadImg(Html)

