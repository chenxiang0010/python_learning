#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 导入模块
import os
import random
import time

# 需要重命名文件的路径
rootPath = ""


class ReNameFile:
    def __init__(self):
        self.spendTime()

    def main(self, root_path):
        if root_path == "":
            print("需要重命名的根目录不存在")
            return
        if root_path.endswith("/"):
            root_path = root_path
        else:
            root_path = root_path + "/"
        if not self.isPathExisting(root_path):
            print("需要重命名的根目录不存在")
            return
        files_list = self.getFileList(root_path)
        if not files_list:
            return

        for idx, item in enumerate(files_list):
            if self.isFile(root_path + item):
                self.reNameFile(idx, root_path, item)

            if self.isDir(root_path + item):
                print("{}目录开始重命名".format(root_path + item))
                self.main(root_path + item)
                print("{}目录完成重命名".format(root_path + item))

    # 按修改时间返回路径下文件列表
    @staticmethod
    def getFileList(file_path):
        file_list = os.listdir(file_path)
        if not file_list:
            print("当前目录，{} 没有任何文件".format(file_list))
            return
        else:
            # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
            # os.path.getmtime() 函数是获取文件最后修改时间
            # os.path.getctime() 函数是获取文件最后创建时间
            file_list = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
            return file_list

    # 判断是否为文件
    @staticmethod
    def isFile(path):
        return os.path.isfile(path)

    # 判断是否为文件夹
    @staticmethod
    def isDir(path):
        return os.path.isdir(path)

    # 判断路径是否存在
    @staticmethod
    def isPathExisting(path):
        return os.path.exists(path)

    # 重命名
    @staticmethod
    def reNameFile(idx, file_path, file_name):
        # 判断文件后缀
        _, file_type = os.path.splitext(file_path + file_name)
        file_type_list = ['.jpg', '.png', '.jpeg', '.gif', '.HEIC']
        # 文件开头
        begin_name = 'default_'
        if file_type in file_type_list:
            begin_name = 'IMG_'

        num = str(idx)
        if idx < 10:
            num = '0' + str(idx)
        random_str = '_'
        for idx in range(1, 6):
            random_str += str(random.randint(0, 9))

        # 重命名
        old_file_path = os.path.join(file_path, file_name)
        new_file_path = os.path.join(file_path,
                                     (begin_name + time.strftime("%Y%m%d",
                                                                 time.localtime()) + random_str + '_00' + num +
                                      file_type))
        try:
            os.rename(old_file_path, new_file_path)
        except OSError as err:
            print(err)
        else:
            print("Old Name:{}, New Name:{}".format(file_name,
                                                    (begin_name + time.strftime("%Y%m%d",
                                                                                time.localtime()) + random_str + '_00' +
                                                     num + file_type)))

    # 查询耗时
    def spendTime(self):
        start = time.time()
        self.main(rootPath)
        end = time.time()
        print("所有文件重命名完成，共计耗时{}s".format(end - start))


if __name__ == '__main__':
    ReNameFile()
