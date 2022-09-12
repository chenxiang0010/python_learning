#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import os
import re
import sys
import time

import requests


class TikTok:
    # 初始化
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66 '
        }

        # 抓获所有视频
        self.Isend = False
        self.uid = 'https://v.douyin.com/6h8wNd8/'
        self.count = 35
        self.musicarg = 'no'
        self.mode = 'post'
        self.nickname = ''
        self.like_counts = 0
        self.save = "C:/Users/chenxiang/Desktop/Images/douyin/"

        # 用户唯一标识
        self.sec = ''

    # 判断个人主页api链接
    def judge_link(self):
        r = requests.get(url=self.uid)
        # 获取用户sec_uid
        if '?' in r.request.path_url:
            for one in re.finditer(r'user/([\d\D]*)([?])', str(r.request.path_url)):
                self.sec = one.group(1)
        else:
            for one in re.finditer(r'user/([\d\D]*)', str(r.request.path_url)):
                self.sec = one.group(1)

        # 第一次访问页码
        max_cursor = 0

        # 构造第一次访问链接
        api_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/%s/?sec_uid=%s&count=%s&max_cursor=%s&aid=1128' \
                       '&_signature=PDHVOQAAXMfFyj02QEpGaDwx1S&dytk=' % (
                           self.mode, self.sec, str(self.count), max_cursor)

        response = requests.get(url=api_post_url, headers=self.headers)
        html = json.loads(response.content.decode())
        self.nickname = html['aweme_list'][0]['author']['nickname']

        self.get_data(api_post_url, max_cursor)
        return api_post_url, max_cursor, self.sec

    # 获取第一次api数据
    def get_data(self, api_post_url, max_cursor):
        # 尝试次数
        index = 0
        # 存储api数据
        result = []
        while not result:
            index += 1
            print('[  提示  ]:正在进行第 %d 次尝试\r' % index)
            time.sleep(0.3)
            response = requests.get(
                url=api_post_url, headers=self.headers)
            html = json.loads(response.content.decode())
            # with open('r.json', 'wb')as f:
            #     f.write(response.content)
            if not self.Isend:
                # 下一页值
                print('[  用户  ]:', str(self.nickname), '\r')
                max_cursor = html['max_cursor']
                result = html['aweme_list']
                print('[  提示  ]:抓获数据成功!\r')

                # 处理第一页视频信息
                self.pic_info(result, max_cursor)
            else:
                max_cursor = html['max_cursor']
                self.next_data(max_cursor)
                # self.Isend = True
                print('[  提示  ]:此页无数据，为您跳过......\r')

        return result, max_cursor

    # 下一页
    def next_data(self, max_cursor):
        # 构造下一次访问链接
        api_naxt_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/%s/?sec_uid=%s&count=%s&max_cursor=%s&aid' \
                            '=1128&_signature=RuMN1wAAJu7w0.6HdIeO2EbjDc&dytk=' % (
                                self.mode, self.sec, str(self.count), max_cursor)

        index = 0

        while not self.Isend:
            # 回到首页，则结束
            if max_cursor == 0:
                self.Isend = True
                return
            index += 1
            print('[  提示  ]:正在对', max_cursor, '页进行第 %d 次尝试！\r' % index)
            time.sleep(0.3)
            response = requests.get(url=api_naxt_post_url, headers=self.headers)
            html = json.loads(response.content.decode())
            if not self.Isend:
                # 下一页值
                max_cursor = html['max_cursor']
                result = html['aweme_list']
                print('[  提示  ]:%d页抓获数据成功!\r' % max_cursor)
                # 处理下一页视频信息
                self.pic_info(result, max_cursor)
            else:
                self.Isend = True
                print('[  提示  ]:%d页抓获数据失败!\r' % max_cursor)
                # sys.exit()

    # 处理视频信息
    def pic_info(self, result, max_cursor):
        # 作品id
        aweme_id = []

        for v in range(self.count):
            try:
                aweme_id.append(str(result[v]['aweme_id']))
            except Exception as error:
                print(str(error))
                pass
        for aid in aweme_id:
            self.pic_download(aid)
        self.next_data(max_cursor)

    def pic_download(self, aid):

        # 官方接口
        jx_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={aid}'
        js = json.loads(requests.get(url=jx_url, headers=self.headers).text)

        try:

            pic_title = str(js['item_list'][0]['desc'])
            nickname = str(js['item_list'][0]['author']['nickname'])
            # 检测下载目录是否存在
            if not os.path.exists(self.save + nickname + '/' + pic_title):
                os.makedirs(self.save + nickname + '/' + pic_title)
            for i in range(len(js['item_list'][0]['images'])):
                # 尝试下载图片
                try:
                    pic_url = str(js['item_list'][0]['images'][i]['url_list'][0])
                    picture = requests.get(url=pic_url, headers=self.headers)
                    p_url = self.save + nickname + '/' + pic_title + '/' + str(
                        i) + '.jpeg'  # + now2ticks()
                    with open(p_url, 'wb') as file:
                        file.write(picture.content)
                        print('[  提示  ]:' + p_url + '下载完毕\r')
                except Exception as error:
                    print('[  错误  ]:' + str(error) + '\r')
                    print('[  提示  ]:发生了点意外！\r')
                    break
        except Exception as error:
            print('[  错误  ]:' + str(error) + '\r')
            print('[  提示  ]:获取图集失败\r')
            return


# 主模块执行
if __name__ == "__main__":
    # 获取命令行函数
    def begin():
        TikTok().judge_link()
        print('下载完成，5秒后退出')
        time.sleep(5000)
        sys.exit(0)


    try:
        begin()
    except Exception as e:
        print('[  警告  ]:', e, '可以复制此报错内容发issues')
        print('[  提示  ]:未输入命令或意外出错，自动退出!')
        sys.exit(0)
