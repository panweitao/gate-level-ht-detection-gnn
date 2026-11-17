import os
import re
import shutil


# path = os.getcwd()用于获取当前工作目录的路径并将其存储在变量path中
def get_name_list(path=os.getcwd()):

    com_list = []
    seq_list = []

    with open(path + os.sep + "benchmark.txt", 'r') as f:
        for line in f:
            temp = line.split(' ')
            com_list.append(temp[0])
            com_list.append(temp[5])
            seq_list.append(temp[10])
            seq_list.append(temp[15])

    return com_list, seq_list


if __name__ == '__main__':
    com_list, seq_list = get_name_list()

    path_tc = 'TRIT-TC'
    path_ts = 'TRIT-TS'

    new_path_tc = 'com_ht1'
    new_path_ts = 'seq_ht1'

    # shutil.copytree(源目录,目标目录)函数接受源目录路径和目标目录路径作为参数，将源目录及其内容复制到目标目录中
    for i in com_list:
        shutil.copytree(path_tc + os.sep + i, new_path_tc+os.sep + i)

    for i in seq_list:
        shutil.copytree(path_ts + os.sep + i, new_path_ts+os.sep + i)
