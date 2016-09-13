"""爬虫，抓取PandaTv上的直播封面和主播名字"""
import requests
import os
from lxml import etree

class Spider():
    def __init__(self, url):
        self.url = url              #要抓取的页面
        self.path = os.getcwd()     #当前目录

    #创建储存图片的文件夹，并更新图片
    def createDir(self):
        if 'PandaImg' not in os.listdir(self.path):
            os.mkdir(self.path+'/PandaImg')
        os.chdir(self.path+'/PandaImg')
        for i in os.listdir(os.getcwd()):
            if '.jpg' in i:
                os.remove(i)

    #获取页面的html并转码为utf-8
    def getHtml(self):
        self.html = requests.get(self.url).content.decode('utf-8')

    #分析html并下载图片
    def getImg(self):
        page = etree.HTML(self.html)
        names = page.xpath(u'//span[@class="video-nickname"]')
        imgs = page.xpath(u'//img[@data-original]')
        name = [x.text for x in names]
        img = [x.values()[1] for x in imgs]
        L = list(zip(name,img))
        for name,img in L:
            u = requests.get(img,stream=True)
            with open(name+'.jpg','wb') as f:               #下载图片
                for chunk in u.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)


if __name__ == '__main__':
    url = "http://www.panda.tv/all"
    S = Spider(url)
    S.createDir()
    S.getHtml()
    S.getImg()