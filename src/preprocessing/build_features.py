import numpy as np
import re
import pandas as ps
import os
import json
from pathlib import Path
import heapq
import collections
import time
from collections import defaultdict
import networkx as nx
from networkx import Graph
import csv

temp_in_dict = dict()
temp_out_dict = dict()
feature_list = []
type_list_cbow = ['pad', 'unknow']
# 当需要打印内容很多时，会出现...的问题。
np.set_printoptions(threshold=np.inf)  # 取消限制打印数组的元素数量
ps.set_option('display.max_columns', None)  # 取消限制显示列的数量，使得可以显示DataFrame中的所有列


'''
读入库文件，对其中使用门类型进行划分  并提取输入、输出端口信号，并对各例化模块按照门类型进行划分 对规整化后的文件操作
'''
'''
net_analysis函数的作用：
读入库文件，提取所有标准单元的类型，对其中使用标准单元的类型进行划分
提取标准单元的输入、输出端口信号，并对各例化模块按照标准单元类型进行划分
返回值(只列出后续有用的)：classfy_list = []  # 所有标准单元的名称
pin_dict = dict()  # pin_dict = {标准单元名称：输入端口列表}
pout_dict = dict()  # pout_dict = {标准单元名称：输出端口列表}
fan_in_dct = dict()  # fan_in_dct = {标准单元名称：扇入系数}
node_type_dic = {}  # node_type_dic = {例化名称：标准单元名称}
'''


def net_analysis(str):
    classfy_list = []  # 所有门的名称
    pin_dict = dict()  # pin_dict = {门名称：输入端口列表}
    pout_dict = dict()  # pout_dict = {门名称：输出端口列表}
    reset_dict = dict()
    clk_dict = dict()
    node_type_dic = {}  # node_type_dic = {例化名称：门类型名称}
    AND_name = []
    NOR_name = []
    NAND_name = []
    XNOR_name = []
    BUF_name = []
    INV_name = []
    AO_name = []
    XOR_name = []
    OR_name = []
    DFF_name = []  # 保存dff类型的名字
    MUX_name = []
    OAI_name = []
    OA_name = []
    AOI_name = []
    DEC_name = []
    HADD_name= []
    FADD_name= []
    SDFF_name = []
    others = []

    #   ELSE_name = []

    # mux_node = []  # mux类型node的名字
    fan_in_dct = dict()  # fan_in_dct = {门名称：扇入系数}

    fp = open(str, mode="r")
    for line in fp:
        pin_list = []
        pout_list = []
        line_data = line.split("//")[0]
        node_name = line_data.split(' ')  # node_name=每行空格分开的所有信息
        if "." not in line_data:
            continue
        else:
            feature = re.findall(r'\S+', line_data)[0]  # feature = 门的名称  r'\S+' 匹配一个或多个非空字符 返回一个列表 末尾的[0]选择了找到的第一个匹配项
            node = re.findall(r'\S+', line_data)[1]  # node = 门例化名称
            in_out_list = re.findall(r'[\.](.*?)[\(]', line_data)  # in_out_list=端口信号 提取以.开头且在(之前结束的子字符串列表
            if feature not in pout_dict:
                pout_dict[feature] = []  # pout_dict = {门名称：输出端口}
                pin_dict[feature] = []
            for i in in_out_list:
                if "Q" in i or "QN" in i or "Y" in i or "C1" in i or "SO" in i:
                    pout_list.append(i)  # pout_list = 输出端口
                    if len(pout_list) > len(pout_dict[feature]):
                        pout_dict[feature] = pout_list  # pout_dict = {门名称：输出端口}

                else:
                    pin_list.append(i)  # pin_list = 输入端口
                    if len(pin_list) > len(pin_dict[feature]):
                        pin_dict[feature] = pin_list  # pin_dict = {门名称：输入端口}

            if feature in ["module", "wire", "reg", "input", "output", "assign", "always"]:
                continue
            elif feature in classfy_list:  # classfy_list 所有门的名称
                if feature in SDFF_name:
                    node_type_dic[node] = 'sdff'  # node_type_dic = {例化名称：门类型名称}  并分类 sdff类 的例化名称对应的类统一化
                elif feature in DFF_name:
                    node_type_dic[node] = 'dff'  # dff类 的例化名称对应的类统一化
                elif feature in MUX_name:
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'mux'  # +# repr(lenf)  # mux类 的例化名称对应的类统一化
                elif feature in NOR_name:  #
                    lenf = len(pin_dict[feature])  #
                    node_type_dic[node] = 'nor'  # +# repr(lenf)  # nor类 的例化名称对应的类统一化
                elif feature in XNOR_name:  #
                    lenf = len(pin_dict[feature])  #
                    node_type_dic[node] = 'xnor'  # + repr(lenf)  # xnor类 的例化名称对应的类统一化
                elif feature in NAND_name:  #
                    lenf = len(pin_dict[feature])  #
                    node_type_dic[node] = 'nand'  # + repr(lenf)  # nand类 的例化名称对应的类统一化
                elif feature in AND_name:  #
                    lenf = len(pin_dict[feature])  #
                    node_type_dic[node] = 'and'  # +# repr(lenf)  # and类 的例化名称对应的类统一化
                elif feature in OR_name:
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'or'  # + repr(lenf)    # or类 的例化名称对应的类统一化
                elif feature in OAI_name:  #
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'oai'  # + repr(lenf)   # oai类 的例化名称对应的类统一化
                elif feature in OA_name:  #
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'oa'  # + repr(lenf)    # oa类 的例化名称对应的类统一化
                elif feature in XOR_name:  #
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'xor'  # + repr(lenf)   # xor类 的例化名称对应的类统一化
                elif feature in BUF_name:  #
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'buf'  # #              # buf类 的例化名称对应的类统一化
                elif feature in INV_name:
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'inv'  # #              # inv类 的例化名称对应的类统一化
                elif feature in AO_name:
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'ao'  # + repr(lenf)    # ao类 的例化名称对应的类统一化
                elif feature in AOI_name:  #
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'aoi'  # + repr(lenf)   # aoi类 的例化名称对应的类统一化
                elif feature in DEC_name:  #
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'dec'  # + repr(lenf)   # dec类 的例化名称对应的类统一化
                elif feature in HADD_name:  #
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'hadd'  # + repr(lenf)  # hadd类 的例化名称对应的类统一化
                elif feature in FADD_name:  #
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'fadd'  # + repr(lenf)  # fadd类 的例化名称对应的类统一化
                else:  #
                    node_type_dic[node] = 'unknow'                # clasify中没有的类
            else:
                classfy_list.append(feature)  # classfy_list中没有的门类型名称 加入到classfy_list中
                if "sdf" in feature or "SDF" in feature and feature not in SDFF_name:  # 可能有错 应该是SDFF_name
                    SDFF_name.append(feature)  # 创建SDFF_name 获取SDFF标准单元的名称
                    node_type_dic[node] = 'sdff'  # 创建第一个sdff类实例化名对应的类别 (统一化) （即第一个实例化——对应分类统一化）
                elif "df" in feature or "DF" in feature and feature not in DFF_name:
                    DFF_name.append(feature)  # 创建DFF_name
                    node_type_dic[node] = 'dff'  # 创建第一个dff类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "MUX" in feature or "mx" in feature or "MX" in feature and feature not in MUX_name:
                    MUX_name.append(feature)  # 创建MUX_name
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'mux'  # + repr(lenf)  # 创建第一个mux类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "xn" in feature or "XN" in feature and feature not in XNOR_name:
                    XNOR_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'xnor'  # + repr(lenf)  # 创建第一个xnor类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "oai" in feature or "OAI" in feature and feature not in OAI_name:
                    OAI_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'oai'  # + repr(lenf)  # 创建第一个oai类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "xor" in feature or "XOR" in feature and feature not in XOR_name:
                    XOR_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'xor'  # + repr(lenf)  # 创建第一个xor类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "oa" in feature or "OA" in feature and feature not in OA_name:
                    OA_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'oa'  # + repr(lenf)  # 创建第一个oa类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "nnd" in feature or "NA" in feature and feature not in NAND_name:
                    NAND_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'nand'  # + repr(lenf)  # 创建第一个nand类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "nor" in feature or "NO" in feature and feature not in NOR_name:
                    NOR_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'nor'  # + repr(lenf)  # 创建第一个nor类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "and" in feature or "AN" in feature and feature not in AND_name:
                    AND_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'and'  # + repr(lenf)  # 创建第一个and类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "or" in feature or "OR" in feature and feature not in OR_name:
                    OR_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'or'  # + repr(lenf)  # 创建第一个or类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "ib" in feature or "BU" in feature and feature not in BUF_name:
                    BUF_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'buf'  # 创建第一个buf类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                # elif "i" in feature or "IN" in feature and feature not in INV_name:
                #     INV_name.append(feature)
                #     lenf = len(pin_dict[feature])
                #     node_type_dic[node] = 'inv'  # 创建第一个inv类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "aoi" in feature or "AOI" in feature and feature not in AOI_name:
                    AOI_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'aoi'  # + repr(lenf)  # 创建第一个aoi类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "ao" in feature or "AO" in feature and feature not in AO_name:
                    AO_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'ao'  # + repr(lenf)  # 创建第一个ao类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "i" in feature or "IN" in feature and feature not in INV_name:
                    INV_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'inv'  # 创建第一个inv类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "HADD" in feature or "hadd" in feature and feature not in HADD_name:
                    HADD_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'hadd'  # + repr(lenf)  # 创建第一个hadd类实例化名对应的类的统一化 （即第一个实例化——对应类统一化）
                elif "DEC" in feature or "dec" in feature and feature not in DEC_name:
                    DEC_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'dec'  # + repr(lenf)
                elif "FADD" in feature or "fadd" in feature and feature not in FADD_name:
                    FADD_name.append(feature)
                    lenf = len(pin_dict[feature])
                    node_type_dic[node] = 'fadd'  # + repr(lenf)
                else:
                    others.append(feature)
                    node_type_dic[node] = 'unknow'
    for key in node_type_dic:
        if node_type_dic[key] not in type_list_cbow:
            type_list_cbow.append(node_type_dic[key])  # 将所有门类型放到type_list_cbow中

    # np.save(path + os.sep +'node_type_dic.npy', node_type_dic)

    for key in pin_dict:
        fan_in_dct[key] = len(pin_dict[key])  # pin_dict = {门名称：输入端口} 获得每个门的扇入系数

    return classfy_list, pin_dict, pout_dict, clk_dict, reset_dict, DFF_name, MUX_name, fan_in_dct, node_type_dic
    # 经查询clk_dict，reset_dict在后面的函数中也没用使用 所以本模块中未对其进行提取


# 获得例化名称node_name_list，例化模块中的输入输出信号net_name_list 及例化名称和门名称的对应关系node_type_dic
# 并获得了输入信号和输出信号与例化名称的对应关系temp_in/out_dict 以便后续获得 每一级的连接关系(但未返回)
'''
verilog_file_process函数的作用：
返回值：
获得一个网表中所有模块的例化名称node_name_list = [模块例化名称]，
获得实例化模块的所有连线net信号net_name_list = [net连线信号]
例化名称和标准单元名称的对应关系node_type_dic = {例化名称：标准单元名称}
并更改了全局变量：temp_in_dict和temp_out_dict字典
temp_in_dict = {实例化模块中的输出net连线信号：例化名称列表}
temp_out_dict= {实例化模块中的输入net连线信号：例化名称列表}
'''


def verilog_file_process(pro_netlist, dff_name, pin_dict, pout_dict, clk_dict, reset_dict, classfy_list_sorted, data_path):
    fp = open(pro_netlist, mode="r")
    node_name_list = []
    dff_nodes = []

    node_type_dic = {}  # node name dic = key = node ; value = type : type = and\or\dff\mux\buffer
    # node_type_dic = {例化名称：标准单元名称}
    net_name_list = []
    temp_in_list = []
    temp_out_list = []

    for line in fp:
        line_data = line.split("//")[0]
        pin_list2 = []
        # print(line)
        if "." not in line_data or "module" in line_data:
            continue
        else:
            feature = re.findall(r'\S+', line_data)[0]
            node_name = re.findall(r'\S+', line_data)[1]
            node_name_list.append(node_name)  # 获取例化名称
            feature_list.append(feature)  # 获取标准单元类型名称
            node_type_dic[node_name] = feature  # node_type_dic = {例化名称：标准单元名称}
            if feature in dff_name:
                dff_nodes.append(node_name)  # 获取dff的例化名称
            # 匹配以 . 开头，后面跟着一个或多个非空白字符（\S+），然后是一个左括号 (，接着是零个或多个任意字符（.*?），最后以右括号 ) 结尾
            pin_list = re.findall(r'\.\S+\(.*?\)', line_data)  # 匹配例化模块行的()内信息
            for i in pin_list:
                temp = i.split(",")
                pin_list2.extend(temp)  # TODO 无用操作
            # for i in pin_list2:
                # 匹配例化模块的端口信号a和连接信号b   当存在{}拼接时出现错误 例如：s38584中 RareVectorTrigger_DW01_inc_0 add_73已在mytest中验证
            for i in pin_list:  # 修改
                a = re.findall(r'[.](.*?)[(]', i)[0].strip()
                b = re.findall(r'[(](.*?)[)]', i)[0]
                flag = 0
                if ('{' in b) and (',' in b) and ('}' in b):
                    flag = 1
                    temp_b = re.split('{|,| |}', b)  # 根据大括号{、逗号,、空格 或右大括号}的任何一个作为分隔符，并返回一个包含拆分后部分的列表
                    b = [x for x in temp_b if x != '']  # 去除列表中空白的信息

                if "\'b1" not in b and "\'B1" not in b:
                    if flag:
                        net_name_list.extend(b)  # 将不是常量信号'b1和'B1的连接信号添加到net_name_list中
                    else:
                        net_name_list.append(b)  # 将不是常量信号'b1和'B1的连接信号添加到net_name_list中
                    # 注意 append是将整个列表加入 而extend是将列表中的值一个个加入 若使用append后续set去重时 由于列表是不可hashable的 会报错
                if a in pin_dict.get(feature):  # pin_dict = {门名称：输入端口}
                    if flag:
                        for b in b:
                            if b not in temp_out_list and b != "":  # 输入端口一般是上级输出信号连接过来的 所以为temp_out_list
                                temp_out_list.append(b)  # temp_out_list = [连接信号b]
                                temp_out_dict[b] = [node_name]
                            elif b != "":
                                temp_out_dict.get(b).append(node_name)  # temp_out_dict = {本级输入信号/上级输出：[本级和其他级例化名称1,例化名称2...]}
                    elif b not in temp_out_list and b != "":  # 输入端口一般是上级输出信号连接过来的 所以为temp_out_list
                        temp_out_list.append(b)  # temp_out_list = [连接信号b]
                        temp_out_dict[b] = [node_name]
                    elif b != "":
                        temp_out_dict.get(b).append(node_name)  # temp_out_dict = {本级输入信号/上级输出：[本级和其他级例化名称1,例化名称2...]}
                elif a in pout_dict.get(feature):  # pout_dict = {门名称：输出端口}
                    if flag:
                        for b in b:
                            if b not in temp_in_list and b != "":  # 输出端口一般是连接下级输入信号 所以为temp_in_list
                                temp_in_list.append(b)  # temp_in_list = [连接信号b]
                                temp_in_dict[b] = [node_name]
                            elif b != "":
                                temp_in_dict.get(b).append(node_name)  # temp_in_dict = {本级输出信号/下级输入：[本级和其他级例化名称1,例化名称2...]}
                    elif b not in temp_in_list and b != "":  # 输出端口一般是连接下级输入信号 所以为temp_in_list
                        temp_in_list.append(b)  # temp_in_list = [连接信号b]
                        temp_in_dict[b] = [node_name]
                    elif b != "":
                        temp_in_dict.get(b).append(node_name)  # temp_in_dict = {本级输出信号/下级输入：[本级和其他级例化名称1,例化名称2...]}

                else:
                    continue
    net_name_list = list(set(net_name_list))  # 所有连接信号 去重

    # with open(data_path + os.sep + testname+  r'\node_name_list.txt', 'w+') as b:
    #     b.write('\n'.join(node_name_list))

    for i in temp_in_dict.keys():
        temp_in_dict[i] = list(set(temp_in_dict.get(i)))  # 使用集合去重

    for i in temp_out_dict.keys():
        temp_out_dict[i] = list(set(temp_out_dict.get(i)))  # 使用集合去重
    return node_name_list, net_name_list, node_type_dic


# 获取某字典中对应值的键组成的列表 eg：getKey(temp_out_dict, node) 返回例化名称node所有本模块输入信号的列表（也是上级输出信号的列表）
def getKey(dic, value):
    result = []
    for key in dic:
        if value in dic.get(key):
            result.append(key)
    return result


# 寻找当前node例化模块对应的所有上级例化模块，并返回上级例化模块node_next和 本例化模块与上级例化模块的连接信号net_next
# net_next(对于本级信号为输入信号、上级为输出 存在本级的temp_out_dict中 上级的temp_in_dict中)
# todo 将形参node节点当作输入信号对应的节点来找上级node节点(因输入信号要连接到上级节点)
'''
get_last_level_node函数的作用：根据实例化名称从temp_out_dict字典中获取该模块的输入net连接信号列表；
根据该输入net连接信号从temp_in_dict字典中根据键获取相同net连接信号所连接的实例化模块名称(输出net连接信号所属的模块/上级模块实例化名)
返回值：
node_next = [] # 包含node节点对应的所有上级node节点
net_next  = [] # 包含node节点有连接到上级node节点的所有输入信号
'''


def get_last_level_node(node):      # 输入node为[,,,,]形式
    net_next = []
    net = []  # [[],[],[]]
    node_return = []  # [[],[],[]...]
    if(node != None) :
        net_next = getKey(temp_out_dict, node)  # ※获取字典temp_out_dict中node值(例化名)对应的键(本级输入信号或上级输出)
        net.extend(net_next)
        node_next = []
        for i in net_next.copy():  # 找到本模块的上级模块
            if temp_in_dict.get(i) != None:  # 如果该输出信号的temp_in_dict值非空(即有对应的上级输出信号) 则通过temp_in_dict找出上级的例化名
                node_next.extend(temp_in_dict.get(i))    # append 改成 extend 丢掉列表结构
            else:
                net_next.remove(i)            # 如果检索是没有即可能是输入的node，将该input-net 删除
        node_return.append(node_next)

    return node_next, net_next  # node_return,net_return都是具有对应位置的形式 [,,,,]


# 寻找当前node例化模块对应的所有下级例化模块，并返回下级例化模块node_next和 本级例化模块与下级例化模块的连接信号net_next
# todo 将形参node节点当作输出信号对应的节点来找下级node节点(因输出信号要连接到下级节点)
'''
get_next_level_node函数的作用：根据node形参实例化名称从temp_in_dict字典中获取该模块的输出net连接信号列表；
根据该输出net连接信号从temp_out_dict字典中根据键获取相同net连接信号所连接的实例化模块名称(输入net连接信号所属的模块/下级模块实例化名)
返回值：
node_next = [] # 包含node节点对应的所有下级node节点
net_next  = [] # 包含node节点有连接到下级node节点的所有输出信号
'''


def get_next_level_node(node):      # 输入node为[,,,,]形式
    net_next = []
    net = []  # [[],[],[]]
    node_return = []  # [[],[],[]...]
    if (node != None):
        net_next = getKey(temp_in_dict, node)  # 获取字典temp_in_dict中node值(例化名)对应的键(本级输出信号或下级输入)
        net.extend(net_next)
        node_next = []
        for i in net_next.copy():
            if temp_out_dict.get(i) != None:  # 如果该输入信号的temp_out_dict值非空(即有对应的下级输入信号) 则通过temp_out_dict找出下级的例化名
                node_next.extend(temp_out_dict.get(i))
            else:
                net_next.remove(i)  # 如果检索是没有即可能是输出的node，将该output-net 删除
        node_return.append(node_next)
    return node_next, net_next  # node_return,net_return都是具有对应位置的形式 [,,,,]


# 生成每个代表每个标准单元类型的独热码
def to_one_hot(label, dimension=46):  # 根据门类型获取19维独热码特征 返回一个包含19个键的字典 在mytest中已经验证
    one_hot_dict = dict()
    results = np.zeros((len(label), dimension))  # 数字大小19*19
    for i, lab in enumerate(label):
        results[i, label.index(lab)] = 1  # 生成了一个19*19的单位阵 表示门类型的独热码特征
        one_hot_dict[lab] = results[i]
    return one_hot_dict


# 该函数根据一个.v文件中所有net信号来获取例化模块(节点)的上下级连接关系，即获取图数据中的连接关系
def get_edge(nets, node_index_dict):  # 形参1：nets为一个.v中例化模块中的所有信号 形参2：.v中所有例化模块组成：node_index_dict{node例化名称:index索引}
    edges = []
    node_last = []
    node_next = []
    for net in nets:  # 如果nets为本级输入 则必然在temp_out_dict中(下级输出) 可以通过其找到下级模块例化名 同理nets为本级输出也可以找到上级模块例化名
        has_key = 1
        if net in temp_in_dict.keys():  # temp_in_dict = {本级输出信号/下级输入：[本级和其他级例化名称1,例化名称2...]}
            node_last = temp_in_dict[net]  # 获取上级模块例化名
            has_key = 0
        if net in temp_out_dict.keys():
            node_next = temp_out_dict[net]  # 获取下级模块例化名
            has_key = 0

        if has_key == 1:
            continue
        else:
            for nl in node_last:
                for nn in node_next:
                    edges.append((node_index_dict[nl], node_index_dict[nn]))

    return edges


# 该函数用于获取.v文件中输入输出in\output信号字典 已在mytest中验证
'''
get_port_name2函数的作用：获取网表中的输入/输出信号的字典(将多bit输入/输出端口信号拆分为单bit)
返回值：
output_dict = {output声明的输出信号：assign直连信号/output中的输出信号}
input_dict = {input声明的输入信号：assign直连信号/input中的输入信号}
'''


def get_port_name2(st):
    input_dict = dict()
    output_dict = dict()
    fp = open(st, mode="r")
    data = fp.read()  # 调用 read() 方法，将文件的全部内容读取到字符串变量data中。
    input_list = []
    output_list = []
    p = re.findall(r"output.*?(?=;)", data, re.S)  # 以 "output" 开头、以分号 ";" 结尾（不含;但含output）
    # re.S：这是一个标志参数，元字符可以匹配任何字符，包括换行符
    q = re.findall(r"input.*?(?=;)", data, re.S)  # 匹配# 以 "input" 开头、以分号 ";" 结尾的字符串
    o = re.findall(r"assign.*?(?=;)", data, re.S)  # 匹配# 以 "assign" 开头、以分号 ";" 结尾的字符串
    for line in p:
        line1 = " ".join(line.split(','))  # 将output中以逗号，隔开的信号换成用空格隔开
        data1 = line1.split("//")[0]  # 删除注释
        data_1_r = data1.split(' ')  # 以空格分割data1

        if ':' in data1:
            temp_list = []
            for i in data_1_r:
                if (i=='output'):
                    continue
                elif '[' in i:
                    w1 = re.findall(r'[\[](.*?)[:]',i)  # 匹配前位宽
                    w2 = re.findall(r'[:](.*?)[\]]',i)  # 匹配后位宽
                    w1 = int(w1[0])
                    w2 = int(w2[0])
                    if (w1 >= w2):  # 得到输出信号的位宽
                        width = w1
                    else:
                        width = w2
                else:
                    for j in range(0, width+1):
                        temp_list.append(str(i)+'['+str(j)+']')
            output_list.extend(temp_list)  # 获取多位宽输出信号outputlist
        else:
            temp_list = []
            for i in data_1_r:
                if i == 'output' or i == '':
                    continue
                else:
                    temp_list.append(i)
            output_list.extend(temp_list)  # 获得单位宽输出信号outputlist
        if 'assign' in data1:  # 此条件多余
            break

    print('output_list->', output_list)

    for line in q:
        line1 = " ".join(line.split(','))  # 将input中以逗号，隔开的信号换成用空格隔开
        data1 = line1.split("//")[0]  # 删除注释
        data_1_r = data1.split(' ')  # 以空格分割data1
        if ':' in data1:
            temp_list = []
            for i in data_1_r:
                if (i == 'input'):
                    continue
                elif '[' in i:
                    w1 = re.findall(r'[\[](.*?)[:]', i)
                    w2 = re.findall(r'[:](.*?)[\]]', i)
                    w1 = int(w1[0])
                    w2 = int(w2[0])
                    if (w1 >= w2):
                        width = w1
                    else:
                        width = w2
                else:
                    for j in range(0, width + 1):
                        temp_list.append(str(i) + '[' + str(j) + ']')
            input_list.extend(temp_list)  # 获取多位宽输出信号inputlist
        else:
            temp_list = []
            for i in data_1_r:
                if i == 'input' or i == '':
                    continue
                else:
                    temp_list.append(i)
            input_list.extend(temp_list)  # 获取单位宽输出信号outputlist
        if 'assign' in data1:  # 此条件多余
            break
    print('input_list->', input_list)
    for i in input_list:
        input_dict[i] = i  # input_dict = {input中的输入信号：input中的输入信号}

    for i in output_list:
        output_dict[i] = i  # output_dict = {output中的输出信号：output中的输出信号}

    for line in o:
        data1 = line.split(";")[0]  # 去除; 保留;前的内容
        data_1_s = data1.split(' ')  # 以空格分割
        if '' in data_1_s:
            data_1_s.remove('')
        if 'assign' in data1:  # 将一些assign直接连的输入输出信号字典进行改变 将字典值放松到assign直接连接的信号上
            if data_1_s[1] in output_list:
                output_dict[data_1_s[1]] = data_1_s[3]  # output_dict = {output中的输出信号：assign直连信号/output中的输出信号}
            elif data_1_s[3] in input_list:
                input_dict[data_1_s[3]] = data_1_s[1]  # input_dict = {input中的输入信号：assign直连信号/input中的输入信号}

    return input_dict, output_dict


# 寻找一个模块的所有输入信号连接的例化模块节点input_node_list和输出信号连接的例化模块节点output_node_list 即获得输入节点与输出节点
'''
get_port函数的作用：
    调用get_port_name2函数获取网表中的输入/输出信号的字典input_dict、output_dict
    随后获取输入信号和输出信号所连接的例化模块，存储到字典input_node_dict、output_node_dict中
    input_node_dict = {input输入信号：连接的例化模块列表}
    output_node_dict = {output输出信号：连接的例化模块列表}
    再将非ckl、rst、test信号连接的例化模块去除掉，剩余的例化模块节点存储到列表input_node_list、output_node_list
返回值：
input_node_list = [整个网表最外围input信号所连接的节点]    ----作为主输入节点
output_node_list = [整个网表最外围output信号所连接的节点]  ----作为主输出节点
'''


def get_port(after_process_name):
    input_dict, output_dict = get_port_name2(after_process_name)
    input_node_dict = dict()
    output_node_dict = dict()
    for i in input_dict:
        temp = input_dict[i]
        node_next = []  #
        if temp_out_dict.get(temp) != None:
            node_next.extend(temp_out_dict.get(temp))
            input_node_dict[temp] = node_next  # 获取输入信号接的例化模块 input_node_dict = {input输入信号：连接的例化模块列表}

    for i in output_dict:
        temp = output_dict[i]
        node_last = []  # 此处名称应该为node_next
        if temp_in_dict.get(temp) != None:
            node_last.extend(temp_in_dict.get(temp))
            output_node_dict[temp] = node_last  # 获取输出信号接的例化模块 output_node_dict = {output输出信号：连接的例化模块列表}

    output_node_list = []  # 输出接的节点  “节点”——例化模块
    input_node_list = []  # 输入接的节点

    for i in input_node_dict:
        if 'CK' in i or 'clk' in i or 'rst' in i or 'test' in i:
            continue
        else:
            temp = input_node_dict[i]  # 输入信号连接的例化模块节点
            if len(temp) != 0:
                for j in temp:
                    if j not in input_node_list:
                        input_node_list.append(j)

    for i in output_node_dict:
        if 'CK' in i or 'clk' in i or 'rst' in i or 'test' in i:
            continue
        else:
            temp = output_node_dict[i]  # 输出信号连接的例化模块节点
            if len(temp) != 0:
                for j in temp:
                    if j not in output_node_list:
                        output_node_list.append(j)

    return input_node_list, output_node_list


# 获取网表的 harmonic centrality、到主输入的距离和到主输出的距离。
'''
hc2函数的作用：
    首先调用get_port函数获取网表的主输入/输出节点input_node_list、output_node_list
    根据该函数的形参G访问整个网表的每一个节点；
    使用networkx库的shortest_path获取每一个节点到其它连接到该节点的所有节点的最短路径(以字典形式呈现)
    t_steps_set[node] = result = {与node节点连接/可以搜索的节点序号：[最短路径]}
    其次按照harmonic的定义，计算该节点到所有节点距离的倒数之和
    计算node节点到所有输入/出节点的距离之和(使用input/output_node_list计算---此处设置了最短距离的最大值阈值为999)
    将harmonic特征写入_harmonic.txt文件中
返回值：
harmonic = {节点序号：harmonic值}
pi_dict = {节点序号：到主输入节点的最短距离}
po_dict = {节点序号：到主输出节点的最短距离}
_harmonic.txt文件
'''


def hc2(G, feature_path='./data/SAED/aftpro_netfeature', test_name='new', node_name_dict=(), after_process_name='', node_index_dict={}):
    harmonic = dict()
    pi_dict = dict()
    po_dict = dict()
    t_steps_set = defaultdict(lambda: 0)  # 用于存储最短路径结果
    # defaultdict是内置字典（dict）类型的子类,用于为字典中不存在的键提供默认值0。
    t_steps = defaultdict(defaultdict)

    input_node_list, output_node_list = get_port(after_process_name)  # 获取输入输出节点
    # 获取输入输出节点的索引值 即图中节点的标号
    input_index = [node_index_dict[i] for i in input_node_list]  # 获取输入信号连接的例化模块的索引 # node_index_dict{node例化节点名称:index索引}
    output_index = [node_index_dict[i] for i in output_node_list]  # 获取输出信号连接的例化模块的索引

    for node in G.nodes:
        print(node, '节点最短距离-harmonic-PI-PO计算')
        result = nx.shortest_path(G, node)  # 使用nx.shortest_path计算从当前节点(例化模块)到所有其他节点(例化模块)的最短路径  已在networkx_test中验证
        t_steps_set[node] = result  # 将当前节点到所有其连接的节点最短路径结果存储在t_steps_set字典中，键为当前节点(当前例化模块)  已在networkx_test中验证
        # t_steps_set[node] = {可以到达的节点id:[到达的路径列表]}  见networkx_test中最后
        # 初始化harmonic、pi_dict和po_dict中与当前节点(例化模块)对应的值
        harmonic[node_name_dict[node]] = 0  # node_name_dict{index索引:node例化名称}  G.nodes其node已经是标号了
        pi_dict[node_name_dict[node]] = 999
        po_dict[node_name_dict[node]] = 999

        # ##harmonic
        # print(node, "===>start harmonic", after_process_name)
        # 这部分代码计算了每个节点(例化模块)的调和中心性（harmonic centrality）
        # for i in t_steps_set:  # 从t_steps_set字典中获取每个节点(例化模块)的最短路径集合
        for j in t_steps_set[node]:  # 遍历这些最短路径集合。对于每个节点i的最短路径集合中的每个路径j
            harmonic[node_name_dict[node]] += 1/len(t_steps_set[node][j])  # harmonic[node_name_dict[i]]表示节点i到所有其他节点的倒数之和

        # 计算了每个节点(例化模块)到所有输入节点的最短路径长度
        # 检查节点i的最短路径集合中是否存在比pi_dict[node_name_dict[i]](默认到所有输入距离的阈值)更短的路径
        # 如果存在小于阈值的路径，则将pi_dict[node_name_dict[i]]的值更新为该较短路径的长度
        for k in input_index:
            if len(t_steps_set[node][k]) < pi_dict[node_name_dict[node]]:
                pi_dict[node_name_dict[node]] = len(t_steps_set[node][k])

        # 计算了每个节点(例化模块)到所有输出节点的最短路径长度
        for z in output_index:
            if len(t_steps_set[node][z]) < po_dict[node_name_dict[node]]:
                po_dict[node_name_dict[node]] = len(t_steps_set[node][z])

        # 为了节省运行时内存的消耗 运算完成后则删除字典中对应的内容
        t_steps_set.popitem()

    with open(feature_path + os.sep + test_name + "_harmonic.txt", "w") as f:
        for node in harmonic:
            f.write(node + ' ' + str(harmonic[node]))  # 将harmonic特征写入
            f.write('\n')

    return harmonic, pi_dict, po_dict  # harmonic={节点例化名称：特征} pi_dict={节点例化名称：该节点到输入节点特征} po_dict={节点例化名称：该节点到输出节点特征}


'''
feature_normalize函数的作用：
    采用零均值归一化(Z-Score Normalization)对每一维度的特征进行归一化处理，消除不同特征间量纲尺度差异的影响，
    以对每一维特征同等看待。使损失函数的等高线更接近圆形，梯度下降方向的震荡更小，收敛更快，可以更容易通过梯度下降方法找到最优解。
输入值：一个维度的特征字典
返回值：归一化后一个维度的特征字典
'''


def feature_normalize(data_dict):  # 特征归一化
    data = []
    for i in data_dict:  # data_dict = {例化名称：某特征值}
        data.append(data_dict[i])

    mu = np.mean(data, axis=0)  # 按列计算均值 对于一维列表axis=0则是求其均值
    std = np.std(data, axis=0)  # 按列计算标准差 对于一维列表axis=0则是求其标准差
    if std != 0:
        data = (data - mu) / std  # 标准差不为0 则标准化 在mytest中已经验证

    index = 0
    for i in data_dict:
        data_dict[i] = data[index]  # 将标准化后的特征值替换原特征值
        index += 1


# 此函数用于对规整化后的网表文件进行 图构建(节点和连接边的产生.cites文件) 特征的提取、标准化和合并以及标签的生成(.content)
def get_sage_data(data_path, test_name, aftprocess_netpath, feature_path):
    after_process_name = aftprocess_netpath + os.sep + test_name + '_process.v'
    classfy_list, pin_dict, pout_dict, clk_dict, reset_dict, dff_name, mux_name, fan_in_dct, node_type_dic = net_analysis(
        after_process_name)  # 按照门类型提取并分类after_process_name中的相关信息
    # node_type_dic = {例化名称：19个门类型名称}  classfy_list为所有的门类型
    classfy_list_sorted = sorted(classfy_list, key=lambda i: len(i), reverse=True)  # 按名称从长到短对所有门的类型classfy_list进行排序

    # 通过verilog_file_process函数获取一个规整化网表中的所有例化名称node_name_list，例化模块中的输入输出信号net_name_list 及例化名称和门名称的对应关系node_feature_dict
    print("开始——————获取网表所有例化名称及输入输出信号、例化名称和门名称的对应关系")
    node_name_list, net_name_list, node_feature_dict = verilog_file_process(after_process_name, dff_name, pin_dict,
                                                                            pout_dict,  # 后面参数都没用到
                                                                            clk_dict, reset_dict,
                                                                            classfy_list_sorted, data_path)
    print("结束——————获取网表所有例化名称及输入输出信号、例化名称和门名称的对应关系")
    type_list = ["sdff", "dff", 'mux', 'xnor', 'oai', 'oa', 'nand', 'nor', 'and', 'or', 'buf', 'inv', 'ao', 'aoi', "dec", "hadd", "fadd", "xor", 'unknow']
    one_hot_dict = to_one_hot(type_list, 19)  # 获取19维独热码特征 one_hot_dict{门类型：19维特征向量}
    fan_in_node_dict = {}
    fan_out_node_dict = {}
    dff_nodes = []
    print("开始——————获取网表所有节点的上下级关系")
    for i in range(len(node_name_list)):
        node = node_name_list[i]  # 本级模块例化名
        node_last, net_last = get_last_level_node(node)  # 获取本级的上级例化模块名 和 本级与上级连接的信号
        fan_in_node_dict[node] = node_last  # fan_in_node_dict = {本级模块例化名：上级模块例化名列表}  为获取入度特征作准备
        node_next, net_next = get_next_level_node(node)  # 获取本级的下级例化模块名 和 本级与下级连接的信号
        fan_out_node_dict[node] = node_next  # fan_out_node_dict = {本级模块例化名：下级模块例化名列表} 为获取出度特征作准备
        if(len(node_next) == 0 and len(node_last) == 0):
            print(str(i) + " " + node, '没有上下级模块')  # 如果该级没有上下级模块 则输出该例化模块在列表中的位置索引
        if node_type_dic[node] == 'dff':
            dff_nodes.append(node)
    print("结束——————获取网表所有节点的上下级关系")
    print("开始——————将模块名称写入.node")
    with open(feature_path + os.sep + test_name + ".nodes", "w") as f:  # .nodes文件中存放一个.v文件的所有例化模块名称
        for node in node_name_list:
            f.write(node)
            f.write('\n')
    print("结束——————将模块名称写入.node")
    node_name_dict = dict(list(enumerate(node_name_list)))  # 使用列表创建字典的方法 node_name_dict{index索引:node例化名称}
    node_index_dict = dict()  # dict {node:index}
    for i, element in enumerate(node_name_list):
        node_index_dict[element] = i  # node_index_dict{node例化名称:index索引}  在mytest中验证

    edge1 = get_edge(net_name_list, node_index_dict)  # 获取一个.v文件的边连接 edge1 = [(,),(,),...]
    edge1 = list(set(edge1))  # 去重
    print("开始——————networkx图构建")
    G = Graph()  # 使用networkx库创建无向图
    for edge in edge1:
        G.add_edge(edge[0], edge[1])  # 根据节点连接关系为图添加边
    print("结束——————networkx图构建")
    print("开始——————将模块连接关系写入.cites、_edge.txt")
    with open(feature_path + os.sep + test_name + ".cites", "w") as f:
        for edge in edge1:  # .cites文件中存放一个.v文件的所有连接关系 即一个图的节点及节点连接关系
            f.write(str(edge[0]) + '\t' + str(edge[1]))
            f.write('\n')

    with open(feature_path + os.sep + test_name + "_edge.txt", "w") as f:
        f.write(str(len(node_name_list)) + '\t' + str(len(edge1)))  # 统计一个网表的节点数量和边数量
        f.write('\n')
        for edge in edge1:  # edge.txt文件中存放一个.v文件的所有连接关系 即一个图的节点及节点连接关系 相比于.cites 多了统计第一行的例化模块节点数量+边数量
            f.write(str(edge[0]) + '\t' + str(edge[1]))
            f.write('\n')
    print("结束——————将模块连接关系写入.cites、_edge.txt")
    # label_list = []
    trojan_list = []  # trojan.txt获取木马的例化模块名称
    with open(aftprocess_netpath + os.sep + "trojan_node.txt", "r") as f:
        for line in f:
            temp = line.strip('\n')
            trojan_list.append(temp)

    label_dict = dict()
    print('开始————节点加标签')
    # 为每个节点加上标签
    for node in node_name_list:
        if node in trojan_list:
            label_dict[node] = 1
            # label_list.append(node)
        else:
            label_dict[node] = 0  # 将正常节点与木马节点分别打上标签0/1  节点——模块例化名
    print('结束————节点加标签')
    # npy文件转换为csv文件 ——见mytest中 以label为例
    np.save(feature_path + os.sep + test_name + "_label.npy", label_dict)  # 将标签保存为test_namelabel.npy文件
    # label_dict = np.load(feature_path + os.sep + test_name + "_label.npy", allow_pickle=True).item()
    print('开始————获取调和中心性特征')
    # 获取网表的harmonic调和中心性、pi_dict到主输入的距离, po_dict到主输出的距离 这几个特征
    harmonic_dict, pi_dict, po_dict = hc2(G, feature_path, test_name, node_name_dict, after_process_name, node_index_dict)
    print('结束————获取调和中心性特征')
    np.save(feature_path + os.sep + test_name + "_pi.npy", pi_dict)  # 将到主输入距离特征保存为pi.npy文件
    np.save(feature_path + os.sep + test_name + "_po.npy", po_dict)  # 将到主输出距离特征保存为po.npy文件

    # betweenness_dict = get_betweenness(feature_path, test_name,node_name_dict)
    # ##归一化
    # ##生成一一对应的列表
    print('开始————harmonic特征标准化')
    feature_normalize(harmonic_dict)  # harmonic_dict调和中心性特征标准化
    print('结束————harmonic特征标准化')
    # feature_normalize(betweenness_dict)

    # ####合并特征 ： 节点类型 ， 扇入扇出大小， between\harmonic
    feature_dict = dict()  # 合并特征存放的地方
    in_degree = dict()
    out_degree = dict()
    print('开始————入度、出度、独热码特征统计及标准化')
    feature_onehot = dict()  # dict()
    for node_name in node_name_list:
        in_degree[node_name] = (len(fan_in_node_dict.get(node_name)))  # 节点入度量化特征 节点——模块实例化名称
        out_degree[node_name] = (len(fan_out_node_dict.get(node_name)))  # 节点出度量化特征
        feature_onehot[node_name] = one_hot_dict[node_type_dic[node_name]]  # 获取该节点的19维独热码特征
    # 特征标准化
    feature_normalize(in_degree)
    feature_normalize(out_degree)
    feature_normalize(pi_dict)
    feature_normalize(po_dict)
    print('结束————入度、出度、独热码特征统计及标准化')

    # np.concatenate() 用于沿指定轴连接（合并）多个数组
    # 合并19维独热码特征、入度、出度特征、调和中心性、到主输入/出距离特征  共24维
    print('开始————特征拼接')
    for node_name in node_name_list:  # node_index_dict{node例化名称:index索引}
        feature_dict[node_index_dict[node_name]] = np.concatenate((feature_onehot[node_name],
                                                                   [in_degree[node_name], out_degree[node_name], harmonic_dict[node_name],
                                                                    pi_dict[node_name], po_dict[node_name]]))
    # feature_dict = {例化名索引：合并后特征}
    print('结束————特征拼接')
    np.save(feature_path + os.sep + test_name + "_feature.npy", feature_dict)  # 合并所有特征后的特征保存到feature.npy
    np.save(feature_path + os.sep + test_name + "_node_index.npy", node_name_dict)  # node_name_dict{index索引:node例化名称}保存在node_index.npy

    # ###生成cora数据集content与cites
    print('开始————特征写入.content')
    with open(feature_path + os.sep + test_name + ".content", "w") as f:
        for node in feature_dict:  # .content文件中存放一个.v文件的所有节点的特征向量 及标签值
            f.write(str(node)+'\t')  # 例化名称序号
            for i in feature_dict[node]:
                f.write(str(i)+'\t')  # 所有特征
            f.write(str(label_dict[node_name_dict[node]])+'\t')  # 标签值
            f.write('\n')
    print('结束————特征写入.content')


def get_path():
    # 设置路径
    # os.path.abspath() 函数返回给定相对路径的绝对路径

    # ##############SAED数据集库########################
    initialnetlist_path = os.path.abspath('./data/SAED/initial_netlist')
    aftprocess_netlist_path = os.path.abspath('./data/SAED/aftprocess_netlist')
    aftpro_netfeature = os.path.abspath('./data/SAED/aftpro_netfeature')

    # ##############SAED数据集库-特征提取时间########################
    # initialnetlist_path = os.path.abspath('./data_SAED/initial_netlist')
    # aftprocess_netlist_path = os.path.abspath('./data_SAED/aftprocess_netlist1')
    # aftpro_netfeature = os.path.abspath('./data_SAED/aftpro_netfeature1')

    # ##############万门级数据集库########################
    # initialnetlist_path = os.path.abspath('./data_largenetlist/initial_netlist')
    # aftprocess_netlist_path = os.path.abspath('./data_largenetlist/aftprocess_netlist')
    # aftpro_netfeature = os.path.abspath('./data_largenetlist/aftpro_netfeature')

    # ##############万门级数据集库-特征提取时间########################
    # initialnetlist_path = os.path.abspath('./data_largenetlist/initial_netlist')
    # aftprocess_netlist_path = os.path.abspath('./data_largenetlist/aftprocess_netlist1')
    # aftpro_netfeature = os.path.abspath('./data_largenetlist/aftpro_netfeature1')

    # ##############LEDA数据集库########################
    # initialnetlist_path = os.path.abspath('./data_LEDA/initial_netlist')
    # aftprocess_netlist_path = os.path.abspath('./data_LEDA/aftprocess_netlist')
    # aftpro_netfeature = os.path.abspath('./data_LEDA/aftpro_netfeature')

    # ##############LEDA数据集库-特征提取时间########################
    # initialnetlist_path = os.path.abspath('./data_LEDA/initial_netlist')
    # aftprocess_netlist_path = os.path.abspath('./data_LEDA/aftprocess_netlist1')
    # aftpro_netfeature = os.path.abspath('./data_LEDA/aftpro_netfeature1')
    return initialnetlist_path, aftprocess_netlist_path, aftpro_netfeature


if __name__ == '__main__':
    # 本py对规整化后的网表进行图数据的生成 以及特征的生成

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

    _, aftprocess_netlist_path, aftpro_netfeature = get_path()
    # ##############SAED数据集库########################
    ht_files_name = os.listdir(aftprocess_netlist_path)
    for i in ht_files_name:
        aftpro_nlst_path = aftprocess_netlist_path + os.sep + i   # + os.sep + i + '_process.v'
        aftpro_netlistfeature = aftpro_netfeature + os.sep + i
        print('\n\n\n', i, '开始提取特征')
        get_sage_data(data_path='', test_name=i, aftprocess_netpath=aftpro_nlst_path, feature_path=aftpro_netlistfeature)
        temp_in_dict.clear()
        temp_out_dict.clear()
        feature_list.clear()

    # ##############SAED数据集库-特征提取时间########################
    # ht_files_name = os.listdir(aftprocess_netlist_path)
    # for i in ht_files_name:
    #     aftpro_nlst_path = aftprocess_netlist_path + os.sep + i   # + os.sep + i + '_process.v'
    #     aftpro_netlistfeature = aftpro_netfeature + os.sep + i
    #     print('\n\n\n', i, '开始提取特征')
    #     t0 = time.time()
    #     get_sage_data(data_path='', test_name=i, aftprocess_netpath=aftpro_nlst_path, feature_path=aftpro_netlistfeature)
    #     t1 = time.time()
    #     with open(aftpro_netlistfeature + os.sep + i + "_time.txt", "w") as f:  # 存储特征提取与图构建的总时间
    #         f.write(str(t1-t0))
    #     temp_in_dict.clear()
    #     temp_out_dict.clear()
    #     feature_list.clear()
    # ##############万门级数据集库########################
    # ht_files_name = os.listdir(aftprocess_netlist_path)
    # ht_files_name = ['EthernetMAC10GE-T700', 'EthernetMAC10GE-T710', 'EthernetMAC10GE-T720', 'EthernetMAC10GE-T730']
    # ht_files_name = ['wb_conmax-T100-free']
    # for i in ht_files_name:
    #     aftpro_nlst_path = aftprocess_netlist_path + os.sep + i   # + os.sep + i + '_process.v'
    #     aftpro_netlistfeature = aftpro_netfeature + os.sep + i
    #     print('\n\n\n', i, '开始提取特征')
    #     get_sage_data(data_path='', test_name=i, aftprocess_netpath=aftpro_nlst_path, feature_path=aftpro_netlistfeature)
    #     temp_in_dict.clear()
    #     temp_out_dict.clear()
    #     feature_list.clear()
    # ##############万门级数据集库+时间提取########################
    # ht_files_name = ['EthernetMAC10GE-T700', 'EthernetMAC10GE-T710', 'EthernetMAC10GE-T720', 'EthernetMAC10GE-T730']
    # for i in ht_files_name:
    #     aftpro_nlst_path = aftprocess_netlist_path + os.sep + i   # + os.sep + i + '_process.v'
    #     aftpro_netlistfeature = aftpro_netfeature + os.sep + i
    #     print('\n\n\n', i, '开始提取特征')
    #     t0 = time.time()
    #     get_sage_data(data_path='', test_name=i, aftprocess_netpath=aftpro_nlst_path, feature_path=aftpro_netlistfeature)
    #     t1 = time.time()
    #     with open(aftpro_netlistfeature + os.sep + i + "_time.txt", "w") as f:  # 存储特征提取与图构建的总时间
    #         f.write(str(t1-t0))
    #     temp_in_dict.clear()
    #     temp_out_dict.clear()
    #     feature_list.clear()

    # ##############LEDA数据集库########################
    # # ##############LEDA数据集库组合型com电路-特征提取过程########################
    # ht_files_namecom = os.listdir(aftprocess_netlist_path + os.sep + 'com')
    # for i in ht_files_namecom:
    #     aftpro_nlst_path = aftprocess_netlist_path + os.sep + 'com' + os.sep + i   # + os.sep + i + '_process.v'
    #     aftpro_netlistfeature = aftpro_netfeature + os.sep + 'com' + os.sep + i
    #     print('\n\n\n', i, '组合型木马网表开始提取特征')
    #     get_sage_data(data_path='', test_name=i, aftprocess_netpath=aftpro_nlst_path, feature_path=aftpro_netlistfeature)
    #     temp_in_dict.clear()
    #     temp_out_dict.clear()
    #     feature_list.clear()
    # ##############LEDA数据集库组合型com电路-特征提取过程+时间提取########################
    # ht_files_namecom = os.listdir(aftprocess_netlist_path + os.sep + 'com')
    # for i in ht_files_namecom:
    #     aftpro_nlst_path = aftprocess_netlist_path + os.sep + 'com' + os.sep + i   # + os.sep + i + '_process.v'
    #     aftpro_netlistfeature = aftpro_netfeature + os.sep + 'com' + os.sep + i
    #     print('\n\n\n', i, '组合型木马网表开始提取特征')
    #     t0 = time.time()
    #     get_sage_data(data_path='', test_name=i, aftprocess_netpath=aftpro_nlst_path, feature_path=aftpro_netlistfeature)
    #     t1 = time.time()
    #     with open(aftpro_netlistfeature + os.sep + i + "_time.txt", "w") as f:  # 存储特征提取与图构建的总时间
    #         f.write(str(t1-t0))
    #     temp_in_dict.clear()
    #     temp_out_dict.clear()
    #     feature_list.clear()
    #
    # # ##############LEDA数据集库时序型seq电路-特征提取过程########################
    # ht_files_nameseq = os.listdir(aftprocess_netlist_path + os.sep + 'seq')
    # for i in ht_files_nameseq:
    #     aftpro_nlst_path = aftprocess_netlist_path + os.sep + 'seq' + os.sep + i   # + os.sep + i + '_process.v'
    #     aftpro_netlistfeature = aftpro_netfeature + os.sep + 'seq' + os.sep + i
    #     print('\n\n\n', i, '时序型木马网表开始提取特征')
    #     get_sage_data(data_path='', test_name=i, aftprocess_netpath=aftpro_nlst_path, feature_path=aftpro_netlistfeature)
    #     temp_in_dict.clear()
    #     temp_out_dict.clear()
    #     feature_list.clear()
    # # ##############LEDA数据集库时序型seq电路-特征提取过程+时间提取########################
    # ht_files_nameseq = os.listdir(aftprocess_netlist_path + os.sep + 'seq')
    # for i in ht_files_nameseq:
    #     aftpro_nlst_path = aftprocess_netlist_path + os.sep + 'seq' + os.sep + i   # + os.sep + i + '_process.v'
    #     aftpro_netlistfeature = aftpro_netfeature + os.sep + 'seq' + os.sep + i
    #     print('\n\n\n', i, '时序型木马网表开始提取特征')
    #     t0 = time.time()
    #     get_sage_data(data_path='', test_name=i, aftprocess_netpath=aftpro_nlst_path, feature_path=aftpro_netlistfeature)
    #     t1 = time.time()
    #     with open(aftpro_netlistfeature + os.sep + i + "_time.txt", "w") as f:  # 存储特征提取与图构建的总时间
    #         f.write(str(t1-t0))
    #     temp_in_dict.clear()
    #     temp_out_dict.clear()
    #     feature_list.clear()
