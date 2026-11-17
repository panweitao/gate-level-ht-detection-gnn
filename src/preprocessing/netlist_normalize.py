import numpy as np
import re
import pandas as ps
import os
import json
from pathlib import Path
import heapq
import collections
from collections import defaultdict
import networkx as nx
from networkx import Graph
import csv


# 将原始网表规整化，方便后续构建图特征。
# 与netlist_redify相比 多了删除多余的空行、去除\t 规整化例化模式
def net_redefined(data_path, data_process_path):
    file_path = data_path  # 读取初始网表路径
    file_data = ''
    after_process_name = data_process_path   # 生成网表路径
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data = line.split("//")[0]  # 去除注释
            if ('--' in line) or (('//' in line) and ('Trojan' in line)):
                continue
            elif data == '' or data == '\n':
                temp = line.strip()  # 删除首尾多余空格
                temp = ''.join(temp.split())  # 以空格或\n划分 同时删除多余的空行 与netlist_redify相比 多了此功能
                file_data += temp
            elif "\t" in data:
                file_data += line.replace('\t', '').replace('(.', ' (.')  # 与netlist_redify相比 多了去除\t 规整化例化模式
            elif "(\n" in data:
                file_data += line.strip().replace('\n', ' ')  # 与netlist_redify相比 多了 规整化例化模式
            elif (";" not in data) and ("endmodule" not in data):
                file_data += line.strip()  # 一行未完 将首尾多余空格、回车删掉 即规整化到一行
            else:
                file_data += line.replace('\t', '').replace('(.', ' (.').strip() + '\n'
    with open(after_process_name, "w", encoding="utf-8") as f:
        f.write(file_data)

    return None


def get_path():
    # 设置路径
    # os.path.abspath() 函数返回给定相对路径的绝对路径

    # ##############SAED数据集库########################
    initialnetlist_path = os.path.abspath('./data/SAED/initial_netlist')
    aftprocess_netlist_path = os.path.abspath('./data/SAED/aftprocess_netlist')

    # ##############万门级数据集库########################
    # initialnetlist_path = os.path.abspath('./data_largenetlist/initial_netlist')
    # aftprocess_netlist_path = os.path.abspath('./data_largenetlist/aftprocess_netlist')

    # ##############LEDA数据集库########################
    # initialnetlist_path = os.path.abspath('./data_LEDA/initial_netlist')
    # aftprocess_netlist_path = os.path.abspath('./data_LEDA/aftprocess_netlist')

    return initialnetlist_path, aftprocess_netlist_path



def tj_netlist_redify(netlist_name, redify_tronetlist):
    file_data = ""
    with open(netlist_name, "r", encoding="utf-8") as f:
        start_redify = 0
        for line in f:
            if ("Trojan Circuit" in line) or ('//' in line) or ('HighActiveRegionDetection' in line) or ('TROJAN BODY' in line):
                start_redify = 1

            if start_redify == 1 and (("Trojan Circuit" not in line) and ('//' not in line) and ('TROJAN BODY' not in line)):
                line = line.strip(' ')
                data = line.split("//")[0]
                if '---' in data:  # LEDA库
                    continue  # LEDA库
                if data == '' or data == '\n':
                    file_data += line.strip(' ')  # 去掉空格、空白符(\n、\r、\t、' ')
                elif "\t" in data:
                    file_data += line.replace('\t', '').replace('(.', ' (.')
                    # 用空字符串替换line中的制表符（\t）,在(.前面加空格
                elif (";" not in data) and ("endmodule" not in data):
                    file_data += line.strip()
                else:
                    file_data += line.replace('\t', '').replace('(.', ' (.')

    with open(redify_tronetlist, "w", encoding="utf-8") as f:
        f.write(file_data)
    return None


# 获取log.txt中的木马例化模块名称 存放到trojan.txt文件下 方便后续进行标签标定 在mytest中已验证
def get_trojan_log(init_tro_path, afte_tro_path):
    file_path = init_tro_path
    trojan_list = []
    after_process_name = afte_tro_path
    with open(file_path, "r", encoding="utf-8") as f:
        start_collect = 0
        for line in f:
            if line == '' or line == '\n':
                continue
            # if "TROJAN BODY" in line:
            #     start_collect = 1

            # if start_collect == 1 and "TROJAN BODY" not in line:
            if (('//' not in line) and (';' in line)) or ((';' in line) and ('.' in line)):
                data = line.strip().split()  # 去除左右空白 再以空白分割  注意.split(' ') 与.split() 的区别 一个是只能分割一个空格 另一个以空白符分割
                if len(data) > 1:  # 最后一行'-----' len为1 不保留
                    trojan_list.append(data[1])

    with open(after_process_name, "w", encoding="utf-8") as f:  # 将得到的木马模块例化名称写入到trojan_list中
        for i in trojan_list:
            f.write(i)
            f.write('\n')

    return None


if __name__ == '__main__':
    # 本py对以下网表进行规整化 及 木马节点的提取

    # ht_files_name = [
    #     'RS232-T1000',
    #     'RS232-T1100',
    #     'RS232-T1200',
    #     'RS232-T1300',
    #     'RS232-T1400',
    #     'RS232-T1500',
    #     'RS232-T1600',
    #     's15850-T100',
    #     's35932-T100',
    #     's35932-T200',
    #     's35932-T300',
    #     's38417-T100',
    #     's38417-T200',
    #     's38417-T300',
    #     's38584-T100',
    #     's38584-T200',
    #     's38584-T300']

    # ##############SAED数据集库########################
    initialnetlist_path, aftprocess_netlist_path = get_path()
    ht_files_name = os.listdir(initialnetlist_path)
    for i in ht_files_name:
        # 规整化网表文件
        init_nlst_path = initialnetlist_path + os.sep + i + os.sep + i + '.v'
        # os.makedirs(aftprocess_netlist_path + os.sep + i)  # 在没有文件夹时运行创建
        # os.remove(initialnetlist_path + os.sep + i + os.sep + i + '_process.v')  # 删除错误的生成路径中的文件
        aftpro_nlst_path = aftprocess_netlist_path + os.sep + i + os.sep + i + '_process.v'
        net_redefined(init_nlst_path, aftpro_nlst_path)  # 规整化网表文件

        init_trojan_path = initialnetlist_path + os.sep + i + os.sep + 'Read me.txt'
        med_trojan_path = initialnetlist_path + os.sep + i + os.sep + 'Read me redify.txt'
        afte_trojan_path = aftprocess_netlist_path + os.sep + i + os.sep + 'trojan_node.txt'
        tj_netlist_redify(init_trojan_path, med_trojan_path)  # 规整化木马网表文件
        get_trojan_log(med_trojan_path, afte_trojan_path)

    # ##############万门级数据集库########################
    # initialnetlist_path, aftprocess_netlist_path = get_path()
    # ht_files_name = os.listdir(initialnetlist_path)
    # for i in ht_files_name:
    #     # 规整化网表文件
    #     init_nlst_path = initialnetlist_path + os.sep + i + os.sep + i + '.v'
    #     # os.makedirs(aftprocess_netlist_path + os.sep + i)  # 在没有文件夹时运行创建
    #     # os.remove(initialnetlist_path + os.sep + i + os.sep + i + '_process.v')  # 删除错误的生成路径中的文件
    #     aftpro_nlst_path = aftprocess_netlist_path + os.sep + i + os.sep + i + '_process.v'
    #     net_redefined(init_nlst_path, aftpro_nlst_path)  # 规整化网表文件
    #
    #     init_trojan_path = initialnetlist_path + os.sep + i + os.sep + 'Read me.txt'
    #     med_trojan_path = initialnetlist_path + os.sep + i + os.sep + 'Read me redify.txt'
    #     afte_trojan_path = aftprocess_netlist_path + os.sep + i + os.sep + 'trojan_node.txt'
    #     tj_netlist_redify(init_trojan_path, med_trojan_path)  # 规整化木马网表文件
    #     get_trojan_log(med_trojan_path, afte_trojan_path)

    # ##############LEDA数据集库########################
    # #############LEDA数据集库组合型电路-网表规整化及木马节点提取###############
    # initialnetlist_path, aftprocess_netlist_path = get_path()
    # ht_files_namecom = os.listdir(initialnetlist_path + os.sep + 'com')
    # for i in ht_files_namecom:
    #     # 规整化网表文件
    #     init_nlst_path = initialnetlist_path + os.sep + 'com' + os.sep + i + os.sep + i + '.v'
    #     # os.makedirs(aftprocess_netlist_path + os.sep + 'com' + os.sep + i)  # 在没有文件夹时运行创建
    #     # os.remove(initialnetlist_path + os.sep + i + os.sep + i + '_process.v')  # 删除错误的生成路径中的文件
    #     aftpro_nlst_path = aftprocess_netlist_path + os.sep + 'com' + os.sep + i + os.sep + i + '_process.v'
    #     net_redefined(init_nlst_path, aftpro_nlst_path)  # 规整化网表文件
    #
    #     init_trojan_path = initialnetlist_path + os.sep + 'com' + os.sep + i + os.sep + 'Read me.txt'
    #     med_trojan_path = initialnetlist_path + os.sep + 'com' + os.sep + i + os.sep + 'Read me redify.txt'
    #     afte_trojan_path = aftprocess_netlist_path + os.sep + 'com' + os.sep + i + os.sep + 'trojan_node.txt'
    #     tj_netlist_redify(init_trojan_path, med_trojan_path)  # 规整化木马网表文件
    #     get_trojan_log(med_trojan_path, afte_trojan_path)
    #     print(i, '组合型木马网表格式规整化完毕，并提取其木马节点')
    #
    # # #############LEDA数据集库时序型电路-网表规整化及木马节点提取###############
    # ht_files_nameseq = os.listdir(initialnetlist_path + os.sep + 'seq')
    # for i in ht_files_nameseq:
    #     # 规整化网表文件
    #     init_nlst_path = initialnetlist_path + os.sep + 'seq' + os.sep + i + os.sep + i + '.v'
    #     # os.makedirs(aftprocess_netlist_path + os.sep + 'seq' + os.sep + i)  # 在没有文件夹时运行创建
    #     # os.remove(initialnetlist_path + os.sep + i + os.sep + i + '_process.v')  # 删除错误的生成路径中的文件
    #     aftpro_nlst_path = aftprocess_netlist_path + os.sep + 'seq' + os.sep + i + os.sep + i + '_process.v'
    #     net_redefined(init_nlst_path, aftpro_nlst_path)  # 规整化网表文件
    #
    #     init_trojan_path = initialnetlist_path + os.sep + 'seq' + os.sep + i + os.sep + 'Read me.txt'
    #     med_trojan_path = initialnetlist_path + os.sep + 'seq' + os.sep + i + os.sep + 'Read me redify.txt'
    #     afte_trojan_path = aftprocess_netlist_path + os.sep + 'seq' + os.sep + i + os.sep + 'trojan_node.txt'
    #     tj_netlist_redify(init_trojan_path, med_trojan_path)  # 规整化木马网表文件
    #     get_trojan_log(med_trojan_path, afte_trojan_path)
    #     print(i, '时序型木马网表格式规整化完毕，并提取其木马节点')
