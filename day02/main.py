#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 导入模块
import os
import random
import time

# 需要重命名文件的路径
parmsObj = {"root_path": "C:/Users/chenxiang/Desktop/Images/meitubz", "begin_name": "IMG"}


class ReNameFile:
    success_count = 0
    fail_count = 0
    parmsObj = {"root_path": "./", "begin_name": "default_"}

    def __init__(self, *obj):
        if len(obj):
            parms = obj[0]
            for parm in parms:
                if parm in self.parmsObj.keys():
                    self.parmsObj[parm] = parms[parm]
            self.parmsObj["begin_name"] += "_"
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
                self.reNameFile(idx, root_path, item, self.parmsObj["begin_name"])

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
    def reNameFile(self, idx, file_path, file_name, begin_name):
        # 判断文件后缀
        _, file_type = os.path.splitext(file_path + file_name)
        file_type_list = ['.jpg', '.png', '.jpeg', '.gif', '.HEIC']
        if file_type not in file_type_list:
            print("仅支持图片类型文件，传入文件类型为 {}".format(file_type))
            return
            # idx小于10添0
        num = str(idx)
        if idx < 10:
            num = '0' + str(idx)
        random_str = '_'
        # 防止文件名存在，导致重命名失败
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
            self.success_count += 1
        except OSError as err:
            print(err)
            self.fail_count += 1
        else:
            print("Old Name:{}, New Name:{}".format(file_name,
                                                    (begin_name + time.strftime("%Y%m%d",
                                                                                time.localtime()) + random_str + '_00' +
                                                     num + file_type)))

    # 查询耗时
    def spendTime(self):
        start = time.time()
        self.main(self.parmsObj["root_path"])
        end = time.time()
        print("所有文件重命名完成，共计{}个文件，成功{}个文件，失败{}个文件，共计耗时{}s".format(
            self.success_count + self.fail_count,
            self.success_count, self.fail_count, round(end - start, 2)))


if __name__ == '__main__':
    ret = ReNameFile()
