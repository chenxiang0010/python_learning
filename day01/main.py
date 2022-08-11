# coding=utf-8
import os
import time


# 重命名文件
def renameFile():
    file_path = r'C:\\Users\\chenxiang\\Desktop\\Images\\wx'
    file_list = getFileList(file_path)
    if not file_list:
        print('当前目录下没有文件')
        return
        # 进入到文件夹内，对每个文件进行循环遍历
    for i in range(0, len(file_list)):
        # 判断文件后缀
        _, file_type = os.path.splitext(file_list[i])
        file_type_list = ['.jpg', '.png', '.jpeg', '.gif', '.HEIC']
        # 文件开头
        begin_name = 'default_'
        if file_type in file_type_list:
            begin_name = 'IMG_'

        num = str(i)
        if i < 10:
            num = '0' + str(i)
        # 重命名
        os.rename(os.path.join(file_path, file_list[i]),
                  os.path.join(file_path,
                               (begin_name + time.strftime("%Y%m%d", time.localtime()) + '_00' + num + file_type)))
    print('文件重命名成功')


# 按修改时间返回路径下文件列表
def getFileList(file_path):
    file_list = os.listdir(file_path)
    if not file_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        file_list = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        # print(dir_list)
        return file_list


if __name__ == '__main__':
    renameFile()
