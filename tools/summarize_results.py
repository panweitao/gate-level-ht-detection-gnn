import os
import openpyxl as op


# ###########################SAED-数据集#########################
# def write_excel(tpr_list, tpr_aver, tnr_list, tnr_aver, acc_list, acc_aver, f1_list, f1_aver):
#     ht_files_name = [
#         'RS232-T1000',
#         'RS232-T1100',
#         'RS232-T1200',
#         'RS232-T1300',
#         'RS232-T1400',
#         'RS232-T1500',
#         'RS232-T1600',
#         's15850-T100',
#         's35932-T100',
#         's35932-T200',
#         's35932-T300',
#         's38417-T100',
#         's38417-T200',
#         's38417-T300',
#         's38584-T100',
#         's38584-T200',
#         's38584-T300']
#     # https://blog.csdn.net/l734971107/article/details/109635668
#     # https://blog.csdn.net/canpian7/article/details/115644685
#     score_class = ['TPR', 'TNR', 'ACC', 'F1']
#     bg = op.load_workbook(r"统计.xlsx")  # 应先将excel文件放入到工作目录下
#     sheet = bg["Sheet1"]  # “Sheet1”表示将数据写入到excel文件的sheet1下
#     for i in range(2, len(ht_files_name) + 2):
#         sheet.cell(i, 1, ht_files_name[i - 2])  # sheet.cell(1,1,num_list[0])表示将num_list列表的第0个数据1写入到excel表格的第一行第一列
#         sheet.cell(i, 3, tpr_list[i - 2])
#         sheet.cell(i, 4, tnr_list[i - 2])
#         sheet.cell(i, 5, acc_list[i - 2])
#         sheet.cell(i, 6, f1_list[i - 2])
#         sheet.cell(i, 2, 'mean_0_4_weight800')
#     sheet.cell(len(ht_files_name) + 2, 2, 'mean_0_4_weight800')
#     sheet.cell(len(tpr_list)+2, 3, tpr_aver)
#     sheet.cell(len(tnr_list)+2, 4, tnr_aver)
#     sheet.cell(len(acc_list)+2, 5, acc_aver)
#     sheet.cell(len(f1_list)+2, 6, f1_aver)
#     sheet.cell(len(ht_files_name)+2, 1, 'average')
#
#     for i in range(3, len(score_class) + 3):  # 表头的写入
#         sheet.cell(1, i, score_class[i - 3])
#     bg.save("统计.xlsx")  # 对文件进行保存
#
#
# if __name__ == '__main__':
#     ht_files_name = [
#         'RS232-T1000',
#         'RS232-T1100',
#         'RS232-T1200',
#         'RS232-T1300',
#         'RS232-T1400',
#         'RS232-T1500',
#         'RS232-T1600',
#         's15850-T100',
#         's35932-T100',
#         's35932-T200',
#         's35932-T300',
#         's38417-T100',
#         's38417-T200',
#         's38417-T300',
#         's38584-T100',
#         's38584-T200',
#         's38584-T300']
#
#     maxf1_scoredic = {}
#     score_path = os.path.abspath('./GCN_result_SAED/mean_0_4_weight800')
#     # score_path = os.path.abspath('./result/pool_no_weight')
#
#     # 将最大的f1值找出来
#     for score_listname in ht_files_name:
#         f1_score = []
#         with open(score_path + os.sep + score_listname + ".txt", "r") as f:
#             for line in f:
#                 if not ('F1:' in line and '0' in line):
#                     continue
#                 else:
#                     line_data = float(line.split(':')[1])
#                     f1_score.append(line_data)
#             f1_score.sort(reverse=True)
#             print(score_listname, '网表的F1最大值为', f1_score[0])
#             maxf1_scoredic[score_listname] = f1_score[0]
#     # print(maxf1_scoredic)
#
#     # 将f1最大值所在的行数找出来
#     maxf1_linecnt = {}
#     for score_listname in ht_files_name:
#         linecnt = 0
#         with open(score_path + os.sep + score_listname + ".txt", "r") as f:
#             for line in f:
#                 linecnt += 1
#                 if not ('F1:' in line and '0' in line):
#                     continue
#                 else:
#                     line_data = float(line.split(':')[1])
#                     if line_data == maxf1_scoredic[score_listname]:
#                         maxf1_linecnt[score_listname] = linecnt
#                         break
#     # print(maxf1_linecnt)
#
#     # 根据f1最大的行数统计对应的tpr、tnr、prec、f1、acc等
#     maxf1_tpr_scoredic = {}
#     maxf1_tnr_scoredic = {}
#     maxf1_pre_scoredic = {}
#     maxf1_acc_scoredic = {}
#
#     for score_listname in ht_files_name:
#         linecnt1 = 0
#         with open(score_path + os.sep + score_listname + ".txt", "r") as f:
#             for line in f:
#                 linecnt1 += 1
#                 if linecnt1 > maxf1_linecnt[score_listname] + 7:
#                     break
#                 if not ('0' in line):
#                     continue
#                 else:
#                     if linecnt1 == maxf1_linecnt[score_listname] - 2:
#                         line_data = float(line.split(':')[1])
#                         maxf1_tpr_scoredic[score_listname] = round(line_data, 4)
#                     elif linecnt1 == maxf1_linecnt[score_listname] - 1:
#                         line_data = float(line.split(':')[1])
#                         maxf1_tnr_scoredic[score_listname] = round(line_data, 4)
#                     elif linecnt1 == maxf1_linecnt[score_listname] + 1:
#                         line_data = float(line.split(':')[1])
#                         maxf1_pre_scoredic[score_listname] = round(line_data, 4)
#                     elif linecnt1 == maxf1_linecnt[score_listname] + 7:
#                         line_data = float(line.split()[1])
#                         maxf1_acc_scoredic[score_listname] = round(line_data, 4)
#                     else:
#                         continue
#
#     # 将最大值f1的精度改为小数点后4位
#     for i in maxf1_scoredic:
#         maxf1_scoredic[i] = round(maxf1_scoredic[i],4)
#
#     print('tpr', maxf1_tpr_scoredic)
#     print('tnr', maxf1_tnr_scoredic)
#     print('f1 ', maxf1_scoredic)
#     print('pre', maxf1_pre_scoredic)
#     print('acc', maxf1_acc_scoredic)
#
#     tpr_list = []
#     for tpr in maxf1_tpr_scoredic:
#         tpr_list.append(maxf1_tpr_scoredic[tpr])
#     tpr_aver = round(sum(tpr_list)/len(tpr_list), 4)
#
#     tnr_list = []
#     for tnr in maxf1_tnr_scoredic:
#         tnr_list.append(maxf1_tnr_scoredic[tnr])
#     tnr_aver = round(sum(tnr_list) / len(tnr_list), 4)
#
#     acc_list = []
#     for acc in maxf1_acc_scoredic:
#         acc_list.append(maxf1_acc_scoredic[acc])
#     acc_aver = round(sum(acc_list) / len(acc_list), 4)
#
#     f1_list = []
#     for f1 in maxf1_scoredic:
#         f1_list.append(maxf1_scoredic[f1])
#     f1_aver = round(sum(f1_list) / len(f1_list), 4)
#
#     write_excel(tpr_list, tpr_aver, tnr_list, tnr_aver, acc_list, acc_aver, f1_list, f1_aver)

# ###################################end#########################################


# ###########################LARGE-netlist-数据集#########################
def write_excel(tpr_list, tpr_aver, tnr_list, tnr_aver, acc_list, acc_aver, f1_list, f1_aver):
    ht_files_name = ['EthernetMAC10GE-T700', 'EthernetMAC10GE-T710', 'EthernetMAC10GE-T720', 'EthernetMAC10GE-T730']
    # https://blog.csdn.net/l734971107/article/details/109635668
    # https://blog.csdn.net/canpian7/article/details/115644685
    score_class = ['TPR', 'TNR', 'ACC', 'F1']
    bg = op.load_workbook(r"large_统计.xlsx")  # 应先将excel文件放入到工作目录下
    sheet = bg["Sheet1"]  # “Sheet1”表示将数据写入到excel文件的sheet1下
    for i in range(2, len(ht_files_name) + 2):
        sheet.cell(i, 1, ht_files_name[i - 2])  # sheet.cell(1,1,num_list[0])表示将num_list列表的第0个数据1写入到excel表格的第一行第一列
        sheet.cell(i, 3, tpr_list[i - 2])
        sheet.cell(i, 4, tnr_list[i - 2])
        sheet.cell(i, 5, acc_list[i - 2])
        sheet.cell(i, 6, f1_list[i - 2])
        sheet.cell(i, 2, 'mean_0_4_weight800')
    sheet.cell(len(ht_files_name) + 2, 2, 'mean_0_4_weight800')
    sheet.cell(len(tpr_list)+2, 3, tpr_aver)
    sheet.cell(len(tnr_list)+2, 4, tnr_aver)
    sheet.cell(len(acc_list)+2, 5, acc_aver)
    sheet.cell(len(f1_list)+2, 6, f1_aver)
    sheet.cell(len(ht_files_name)+2, 1, 'average')

    for i in range(3, len(score_class) + 3):  # 表头的写入
        sheet.cell(1, i, score_class[i - 3])
    bg.save("large_统计.xlsx")  # 对文件进行保存


if __name__ == '__main__':
    ht_files_name = ['EthernetMAC10GE-T700', 'EthernetMAC10GE-T710', 'EthernetMAC10GE-T720', 'EthernetMAC10GE-T730']

    maxf1_scoredic = {}
    score_path = os.path.abspath('./result_largenetlist/mean_0_4_weight800')
    # score_path = os.path.abspath('./result/pool_no_weight')

    # 将最大的f1值找出来
    for score_listname in ht_files_name:
        f1_score = []
        with open(score_path + os.sep + score_listname + ".txt", "r") as f:
            for line in f:
                if not ('F1:' in line and '0' in line):
                    continue
                else:
                    line_data = float(line.split(':')[1])
                    f1_score.append(line_data)
            f1_score.sort(reverse=True)
            print(score_listname, '网表的F1最大值为', f1_score[0])
            maxf1_scoredic[score_listname] = f1_score[0]
    # print(maxf1_scoredic)

    # 将f1最大值所在的行数找出来
    maxf1_linecnt = {}
    for score_listname in ht_files_name:
        linecnt = 0
        with open(score_path + os.sep + score_listname + ".txt", "r") as f:
            for line in f:
                linecnt += 1
                if not ('F1:' in line and '0' in line):
                    continue
                else:
                    line_data = float(line.split(':')[1])
                    if line_data == maxf1_scoredic[score_listname]:
                        maxf1_linecnt[score_listname] = linecnt
                        break
    # print(maxf1_linecnt)

    # 根据f1最大的行数统计对应的tpr、tnr、prec、f1、acc等
    maxf1_tpr_scoredic = {}
    maxf1_tnr_scoredic = {}
    maxf1_pre_scoredic = {}
    maxf1_acc_scoredic = {}

    for score_listname in ht_files_name:
        linecnt1 = 0
        with open(score_path + os.sep + score_listname + ".txt", "r") as f:
            for line in f:
                linecnt1 += 1
                if linecnt1 > maxf1_linecnt[score_listname] + 7:
                    break
                if not ('0' in line):
                    continue
                else:
                    if linecnt1 == maxf1_linecnt[score_listname] - 2:
                        line_data = float(line.split(':')[1])
                        maxf1_tpr_scoredic[score_listname] = round(line_data, 4)
                    elif linecnt1 == maxf1_linecnt[score_listname] - 1:
                        line_data = float(line.split(':')[1])
                        maxf1_tnr_scoredic[score_listname] = round(line_data, 4)
                    elif linecnt1 == maxf1_linecnt[score_listname] + 1:
                        line_data = float(line.split(':')[1])
                        maxf1_pre_scoredic[score_listname] = round(line_data, 4)
                    elif linecnt1 == maxf1_linecnt[score_listname] + 7:
                        line_data = float(line.split()[1])
                        maxf1_acc_scoredic[score_listname] = round(line_data, 4)
                    else:
                        continue

    # 将最大值f1的精度改为小数点后4位
    for i in maxf1_scoredic:
        maxf1_scoredic[i] = round(maxf1_scoredic[i],4)

    print('tpr', maxf1_tpr_scoredic)
    print('tnr', maxf1_tnr_scoredic)
    print('f1 ', maxf1_scoredic)
    print('pre', maxf1_pre_scoredic)
    print('acc', maxf1_acc_scoredic)

    tpr_list = []
    for tpr in maxf1_tpr_scoredic:
        tpr_list.append(maxf1_tpr_scoredic[tpr])
    tpr_aver = round(sum(tpr_list)/len(tpr_list), 4)

    tnr_list = []
    for tnr in maxf1_tnr_scoredic:
        tnr_list.append(maxf1_tnr_scoredic[tnr])
    tnr_aver = round(sum(tnr_list) / len(tnr_list), 4)

    acc_list = []
    for acc in maxf1_acc_scoredic:
        acc_list.append(maxf1_acc_scoredic[acc])
    acc_aver = round(sum(acc_list) / len(acc_list), 4)

    f1_list = []
    for f1 in maxf1_scoredic:
        f1_list.append(maxf1_scoredic[f1])
    f1_aver = round(sum(f1_list) / len(f1_list), 4)

    write_excel(tpr_list, tpr_aver, tnr_list, tnr_aver, acc_list, acc_aver, f1_list, f1_aver)

# ###########################LEDA-com数据集#########################
# def write_excel_comleda(tpr_list, tpr_aver, tnr_list, tnr_aver, acc_list, acc_aver, f1_list, f1_aver):
#     com_list = ['c2670_T016', 'c2670_T054', 'c2670_T073', 'c2670_T093', 'c2670_T095',
#                 'c3540_T005', 'c3540_T012', 'c3540_T015', 'c3540_T017', 'c3540_T087',
#                 'c5315_T004', 'c5315_T047', 'c5315_T057', 'c5315_T063', 'c5315_T064',
#                 'c6288_T041', 'c6288_T048', 'c6288_T049', 'c6288_T066', 'c6288_T082',
#                 's13207_T002', 's13207_T005', 's13207_T011', 's13207_T013', 's13207_T014',
#                 's1423_T003', 's1423_T005', 's1423_T008', 's1423_T011', 's1423_T014',
#                 's15850_T002', 's15850_T003', 's15850_T009', 's15850_T012', 's15850_T014',
#                 's35932_T005', 's35932_T006', 's35932_T015', 's35932_T016', 's35932_T018']
#     # https://blog.csdn.net/l734971107/article/details/109635668
#     # https://blog.csdn.net/canpian7/article/details/115644685
#     score_class = ['TPR', 'TNR', 'ACC', 'F1']
#     bg = op.load_workbook(r"统计leda_com.xlsx")  # 应先将excel文件放入到工作目录下
#     sheet = bg["Sheet1"]  # “Sheet1”表示将数据写入到excel文件的sheet1下
#     for i in range(2, int((len(com_list)/2) + 2)):
#         sheet.cell(i, 2, com_list[i - 2])  # sheet.cell(1,1,num_list[0])表示将num_list列表的第0个数据1写入到excel表格的第一行第一列
#         sheet.cell(i, 7, com_list[i + int(len(com_list)/2) - 2])
#         sheet.cell(i, 3, tpr_list[i - 2])
#         sheet.cell(i, 8, tpr_list[i + int(len(com_list)/2) - 2])
#         sheet.cell(i, 4, tnr_list[i - 2])
#         sheet.cell(i, 9, tnr_list[i + int(len(com_list)/2) - 2])
#         sheet.cell(i, 5, acc_list[i - 2])
#         sheet.cell(i, 10, acc_list[i + int(len(com_list)/2) - 2])
#         sheet.cell(i, 6, f1_list[i - 2])
#         sheet.cell(i, 11, f1_list[i + int(len(com_list)/2) - 2])
#         sheet.cell(i, 1, 'gcn_1_0_weight200')
#     sheet.cell(int(len(com_list)/2) + 2, 1, 'gcn_1_0_weight200')
#     # sheet.cell(int(len(tpr_list)/2) + 2, 3, tpr_aver)
#     # sheet.cell(int(len(tnr_list)/2) + 2, 4, tnr_aver)
#     # sheet.cell(int(len(acc_list)/2) + 2, 5, acc_aver)
#     # sheet.cell(int(len(f1_list)/2 ) + 2, 6, f1_aver)
#
#     sheet.cell(int(len(tpr_list)/2) + 2, 3, 'TPR = ' + str(tpr_aver) + '    TNR = ' + str(tnr_aver) + '    ACC = ' + str(acc_aver) + '    F1 = ' + str(f1_aver))
#     sheet.cell(int(len(com_list)/2) + 2, 2, 'average')
#
#     for i in range(3, len(score_class) + 3):  # 表头的写入
#         sheet.cell(1, i, score_class[i - 3])
#         sheet.cell(1, i + 5, score_class[i - 3])
#     bg.save("统计leda_com.xlsx")  # 对文件进行保存
#
#
# if __name__ == '__main__':
#     com_list = ['c2670_T016', 'c2670_T054', 'c2670_T073', 'c2670_T093', 'c2670_T095',
#                 'c3540_T005', 'c3540_T012', 'c3540_T015', 'c3540_T017', 'c3540_T087',
#                 'c5315_T004', 'c5315_T047', 'c5315_T057', 'c5315_T063', 'c5315_T064',
#                 'c6288_T041', 'c6288_T048', 'c6288_T049', 'c6288_T066', 'c6288_T082',
#                 's13207_T002', 's13207_T005', 's13207_T011', 's13207_T013', 's13207_T014',
#                 's1423_T003', 's1423_T005', 's1423_T008', 's1423_T011', 's1423_T014',
#                 's15850_T002', 's15850_T003', 's15850_T009', 's15850_T012', 's15850_T014',
#                 's35932_T005', 's35932_T006', 's35932_T015', 's35932_T016', 's35932_T018']
#
#     maxf1_scoredic = {}
#     score_path = os.path.abspath('./result_LEDA1/com/gcn_1_0_weight200')
#
#     # 将最大的f1值找出来
#     for score_listname in com_list:
#         f1_score = []
#         with open(score_path + os.sep + score_listname + ".txt", "r") as f:
#             for line in f:
#                 if not ('F1:' in line and '0' in line):
#                     continue
#                 else:
#                     line_data = float(line.split(':')[1])
#                     f1_score.append(line_data)
#             f1_score.sort(reverse=True)
#             print(score_listname, '网表的F1最大值为', f1_score[0])
#             maxf1_scoredic[score_listname] = f1_score[0]
#     # print(maxf1_scoredic)
#
#     # 将f1最大值所在的行数找出来
#     maxf1_linecnt = {}
#     for score_listname in com_list:
#         linecnt = 0
#         with open(score_path + os.sep + score_listname + ".txt", "r") as f:
#             for line in f:
#                 linecnt += 1
#                 if not ('F1:' in line and '0' in line):
#                     continue
#                 else:
#                     line_data = float(line.split(':')[1])
#                     if line_data == maxf1_scoredic[score_listname]:
#                         maxf1_linecnt[score_listname] = linecnt
#                         break
#     # print(maxf1_linecnt)
#
#     # 根据f1最大的行数统计对应的tpr、tnr、prec、f1、acc等
#     maxf1_tpr_scoredic = {}
#     maxf1_tnr_scoredic = {}
#     maxf1_pre_scoredic = {}
#     maxf1_acc_scoredic = {}
#
#     for score_listname in com_list:
#         linecnt1 = 0
#         with open(score_path + os.sep + score_listname + ".txt", "r") as f:
#             for line in f:
#                 linecnt1 += 1
#                 if linecnt1 > maxf1_linecnt[score_listname] + 7:
#                     break
#                 if not ('0' in line):
#                     continue
#                 else:
#                     if linecnt1 == maxf1_linecnt[score_listname] - 2:
#                         line_data = float(line.split(':')[1])
#                         maxf1_tpr_scoredic[score_listname] = round(line_data, 4)
#                     elif linecnt1 == maxf1_linecnt[score_listname] - 1:
#                         line_data = float(line.split(':')[1])
#                         maxf1_tnr_scoredic[score_listname] = round(line_data, 4)
#                     elif linecnt1 == maxf1_linecnt[score_listname] + 1:
#                         line_data = float(line.split(':')[1])
#                         maxf1_pre_scoredic[score_listname] = round(line_data, 4)
#                     elif linecnt1 == maxf1_linecnt[score_listname] + 7:
#                         line_data = float(line.split()[1])
#                         maxf1_acc_scoredic[score_listname] = round(line_data, 4)
#                     else:
#                         continue
#
#     # 将最大值f1的精度改为小数点后4位
#     for i in maxf1_scoredic:
#         maxf1_scoredic[i] = round(maxf1_scoredic[i],4)
#
#     print('tpr', maxf1_tpr_scoredic)
#     print('tnr', maxf1_tnr_scoredic)
#     print('f1 ', maxf1_scoredic)
#     print('pre', maxf1_pre_scoredic)
#     print('acc', maxf1_acc_scoredic)
#
#     tpr_list = []
#     for tpr in maxf1_tpr_scoredic:
#         tpr_list.append(maxf1_tpr_scoredic[tpr])
#     tpr_aver = round(sum(tpr_list)/len(tpr_list), 4)
#
#     tnr_list = []
#     for tnr in maxf1_tnr_scoredic:
#         tnr_list.append(maxf1_tnr_scoredic[tnr])
#     tnr_aver = round(sum(tnr_list) / len(tnr_list), 4)
#
#     acc_list = []
#     for acc in maxf1_acc_scoredic:
#         acc_list.append(maxf1_acc_scoredic[acc])
#     acc_aver = round(sum(acc_list) / len(acc_list), 4)
#
#     f1_list = []
#     for f1 in maxf1_scoredic:
#         f1_list.append(maxf1_scoredic[f1])
#     f1_aver = round(sum(f1_list) / len(f1_list), 4)
#
#     write_excel_comleda(tpr_list, tpr_aver, tnr_list, tnr_aver, acc_list, acc_aver, f1_list, f1_aver)

# ######################################end#############################################

# ###########################LEDA-seq数据集#########################
# def write_excel_seqleda(tpr_list, tpr_aver, tnr_list, tnr_aver, acc_list, acc_aver, f1_list, f1_aver):
#     seq_list = ['s13207_T425', 's13207_T440', 's13207_T444', 's13207_T449', 's13207_T450',
#                 's13207_T461', 's13207_T462', 's13207_T468', 's13207_T473', 's13207_T484',
#                 's1423_T405', 's1423_T407', 's1423_T408', 's1423_T411', 's1423_T412',
#                 's1423_T413', 's1423_T418', 's1423_T421', 's1423_T422', 's1423_T429',
#                 's15850_T406', 's15850_T417', 's15850_T429', 's15850_T433', 's15850_T434',
#                 's15850_T439', 's15850_T443', 's15850_T450', 's15850_T468', 's15850_T475',
#                 's35932_T402', 's35932_T408', 's35932_T411', 's35932_T413', 's35932_T414',
#                 's35932_T421', 's35932_T427', 's35932_T430', 's35932_T434', 's35932_T435']
#     # https://blog.csdn.net/l734971107/article/details/109635668
#     # https://blog.csdn.net/canpian7/article/details/115644685
#     score_class = ['TPR', 'TNR', 'ACC', 'F1']
#     bg = op.load_workbook(r"统计leda_seq.xlsx")  # 应先将excel文件放入到工作目录下
#     sheet = bg["Sheet1"]  # “Sheet1”表示将数据写入到excel文件的sheet1下
#     for i in range(2, int((len(seq_list)/2) + 2)):
#         sheet.cell(i, 2, seq_list[i - 2])  # sheet.cell(1,1,num_list[0])表示将num_list列表的第0个数据1写入到excel表格的第一行第一列
#         sheet.cell(i, 7, seq_list[i + int(len(seq_list)/2) - 2])
#         sheet.cell(i, 3, tpr_list[i - 2])
#         sheet.cell(i, 8, tpr_list[i + int(len(seq_list)/2) - 2])
#         sheet.cell(i, 4, tnr_list[i - 2])
#         sheet.cell(i, 9, tnr_list[i + int(len(seq_list)/2) - 2])
#         sheet.cell(i, 5, acc_list[i - 2])
#         sheet.cell(i, 10, acc_list[i + int(len(seq_list)/2) - 2])
#         sheet.cell(i, 6, f1_list[i - 2])
#         sheet.cell(i, 11, f1_list[i + int(len(seq_list)/2) - 2])
#         sheet.cell(i, 1, 'gcn_1_0_weight200')
#     sheet.cell(int(len(seq_list)/2) + 2, 1, 'gcn_1_0_weight200')
#     # sheet.cell(int(len(tpr_list)/2) + 2, 3, tpr_aver)
#     # sheet.cell(int(len(tnr_list)/2) + 2, 4, tnr_aver)
#     # sheet.cell(int(len(acc_list)/2) + 2, 5, acc_aver)
#     # sheet.cell(int(len(f1_list)/2 ) + 2, 6, f1_aver)
#
#     sheet.cell(int(len(tpr_list)/2) + 2, 3, 'TPR = ' + str(tpr_aver) + '    TNR = ' + str(tnr_aver) + '    ACC = ' + str(acc_aver) + '    F1 = ' + str(f1_aver))
#     sheet.cell(int(len(seq_list)/2) + 2, 2, 'average')
#
#     for i in range(3, len(score_class) + 3):  # 表头的写入
#         sheet.cell(1, i, score_class[i - 3])
#         sheet.cell(1, i + 5, score_class[i - 3])
#     bg.save("统计leda_seq.xlsx")  # 对文件进行保存
#
#
# if __name__ == '__main__':
#     seq_list = ['s13207_T425', 's13207_T440', 's13207_T444', 's13207_T449', 's13207_T450',
#                 's13207_T461', 's13207_T462', 's13207_T468', 's13207_T473', 's13207_T484',
#                 's1423_T405', 's1423_T407', 's1423_T408', 's1423_T411', 's1423_T412',
#                 's1423_T413', 's1423_T418', 's1423_T421', 's1423_T422', 's1423_T429',
#                 's15850_T406', 's15850_T417', 's15850_T429', 's15850_T433', 's15850_T434',
#                 's15850_T439', 's15850_T443', 's15850_T450', 's15850_T468', 's15850_T475',
#                 's35932_T402', 's35932_T408', 's35932_T411', 's35932_T413', 's35932_T414',
#                 's35932_T421', 's35932_T427', 's35932_T430', 's35932_T434', 's35932_T435']
#
#     maxf1_scoredic = {}
#     score_path = os.path.abspath('./result_LEDA1/seq/gcn_1_0_weight200')
#
#     # 将最大的f1值找出来
#     for score_listname in seq_list:
#         f1_score = []
#         with open(score_path + os.sep + score_listname + ".txt", "r") as f:
#             for line in f:
#                 if not ('F1:' in line and '0' in line):
#                     continue
#                 else:
#                     line_data = float(line.split(':')[1])
#                     f1_score.append(line_data)
#             f1_score.sort(reverse=True)
#             print(score_listname, '网表的F1最大值为', f1_score[0])
#             maxf1_scoredic[score_listname] = f1_score[0]
#     # print(maxf1_scoredic)
#
#     # 将f1最大值所在的行数找出来
#     maxf1_linecnt = {}
#     for score_listname in seq_list:
#         linecnt = 0
#         with open(score_path + os.sep + score_listname + ".txt", "r") as f:
#             for line in f:
#                 linecnt += 1
#                 if not ('F1:' in line and '0' in line):
#                     continue
#                 else:
#                     line_data = float(line.split(':')[1])
#                     if line_data == maxf1_scoredic[score_listname]:
#                         maxf1_linecnt[score_listname] = linecnt
#                         break
#     # print(maxf1_linecnt)
#
#     # 根据f1最大的行数统计对应的tpr、tnr、prec、f1、acc等
#     maxf1_tpr_scoredic = {}
#     maxf1_tnr_scoredic = {}
#     maxf1_pre_scoredic = {}
#     maxf1_acc_scoredic = {}
#
#     for score_listname in seq_list:
#         linecnt1 = 0
#         with open(score_path + os.sep + score_listname + ".txt", "r") as f:
#             for line in f:
#                 linecnt1 += 1
#                 if linecnt1 > maxf1_linecnt[score_listname] + 7:
#                     break
#                 if not ('0' in line):
#                     continue
#                 else:
#                     if linecnt1 == maxf1_linecnt[score_listname] - 2:
#                         line_data = float(line.split(':')[1])
#                         maxf1_tpr_scoredic[score_listname] = round(line_data, 4)
#                     elif linecnt1 == maxf1_linecnt[score_listname] - 1:
#                         line_data = float(line.split(':')[1])
#                         maxf1_tnr_scoredic[score_listname] = round(line_data, 4)
#                     elif linecnt1 == maxf1_linecnt[score_listname] + 1:
#                         line_data = float(line.split(':')[1])
#                         maxf1_pre_scoredic[score_listname] = round(line_data, 4)
#                     elif linecnt1 == maxf1_linecnt[score_listname] + 7:
#                         line_data = float(line.split()[1])
#                         maxf1_acc_scoredic[score_listname] = round(line_data, 4)
#                     else:
#                         continue
#
#     # 将最大值f1的精度改为小数点后4位
#     for i in maxf1_scoredic:
#         maxf1_scoredic[i] = round(maxf1_scoredic[i],4)
#
#     print('tpr', maxf1_tpr_scoredic)
#     print('tnr', maxf1_tnr_scoredic)
#     print('f1 ', maxf1_scoredic)
#     print('pre', maxf1_pre_scoredic)
#     print('acc', maxf1_acc_scoredic)
#
#     tpr_list = []
#     for tpr in maxf1_tpr_scoredic:
#         tpr_list.append(maxf1_tpr_scoredic[tpr])
#     tpr_aver = round(sum(tpr_list)/len(tpr_list), 4)
#
#     tnr_list = []
#     for tnr in maxf1_tnr_scoredic:
#         tnr_list.append(maxf1_tnr_scoredic[tnr])
#     tnr_aver = round(sum(tnr_list) / len(tnr_list), 4)
#
#     acc_list = []
#     for acc in maxf1_acc_scoredic:
#         acc_list.append(maxf1_acc_scoredic[acc])
#     acc_aver = round(sum(acc_list) / len(acc_list), 4)
#
#     f1_list = []
#     for f1 in maxf1_scoredic:
#         f1_list.append(maxf1_scoredic[f1])
#     f1_aver = round(sum(f1_list) / len(f1_list), 4)
#
#     write_excel_seqleda(tpr_list, tpr_aver, tnr_list, tnr_aver, acc_list, acc_aver, f1_list, f1_aver)

# ######################################end#############################################
