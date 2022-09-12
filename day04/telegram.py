# coding=utf-8
# !/usr/bin/python
# 导入requests库
import importlib
# 导入文件操作库
import os
import random
import sys
import time
from urllib.parse import unquote

import bs4
import requests
from bs4 import BeautifulSoup

importlib.reload(sys)

headers_list = [
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
]
# 定义存储位置
savePath = "C:/Users/chenxiang/Desktop/Images/telegram/"
telegramBegin = "https://telegra.ph"


# 创建文件夹
def createDir(file_path):
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
        return False
    return True


# 下载文件
def download(pic_url: str):
    pic_name = pic_url.replace(telegramBegin + '/', "").split('-')[0]
    img_save_path = savePath + pic_name
    if createDir(img_save_path):
        print('当前套图{}已下载，跳过'.format(pic_name))
        return
    print("{}开始下载".format(pic_name))
    res_sub = requests.get(pic_url, headers={'User-Agent': random.choice(headers_list)})
    # 解析html
    soup_sub = BeautifulSoup(res_sub.text, 'html.parser')
    # 获取当前套图地址下所有图片链接
    pics = soup_sub.findAll('img', class_='')

    for index, pic in enumerate(pics, start=1):
        try:
            if isinstance(pic, bs4.element.Tag):
                # 提取src
                url = telegramBegin + pic.attrs['src']
                array = url.split('/')
                file_name = array[len(array) - 1]
                img = requests.get(url)
                while str(img.content).find('nginx') != -1:
                    img = requests.get(url)
                file = open(img_save_path + "/" + file_name, 'ab')
                file.write(img.content)
                print('{}保存成功，当前进度{}/{}'.format(file_name, index, len(pics)))
                file.close()
        except Exception as e:
            print('*' * 15)
            print(e)
            print('*' * 15)
    else:
        print("{} 下载完成，共计{}张图片！".format(pic_name, len(pics)))
        print('休息5秒，请求下一波图片')
        time.sleep(5)


pic_urls = list(
    map(lambda a: a.attrs['href'], BeautifulSoup(requests.get('http://192.168.31.99:8080/').text, 'html.parser')
        .findAll('a', class_='')))
for picUrl in pic_urls[100:201]:
    if picUrl.find(telegramBegin) != -1:
        download(unquote(picUrl))
    else:
        print('套图链接{}不合法，跳过！'.format(picUrl))
