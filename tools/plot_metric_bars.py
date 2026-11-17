import numpy as np
import matplotlib.pyplot as plt

# https://zhuanlan.zhihu.com/p/183877990
# 绘制结果比较的柱状图
# 虚拟数据
x = ["tpr", "tnr", "F1"]
# y = [0.9139, 0.9984, 0.9038]  # GraphSAGE-pool-1weight
# y = [0.9048, 0.9987, 0.8941]  # GraphSAGE-mean-1weight
# y = [0.9240, 0.9988, 0.9059]  # GraphSAGE-lstm-1weight
# y = [0.6533, 0.9860, 0.5755]  # GraphSAGE-gcn-1weight

# y = [0.8057, 0.9995, 0.8534]  # GraphSAGE-pool-no-weight
# y = [0.8330, 0.9998, 0.8779]  # GraphSAGE-mean-no-weight
# y = [0.8369, 0.9997, 0.8726]  # GraphSAGE-lstm-no-weight
y = [0.3002, 0.9959, 0.3768]  # GraphSAGE-gcn-no-weight

# 柱状图和散点图不同，散点图的(x,y)均为数值变量
# 柱状图的x轴显示分类变量
# 方法：让Matplotlib自动完成映射

fig, ax = plt.subplots(figsize=(4, 3))  # figsize=(7, 6) 参数指定了图形的尺寸，其中 (7, 6) 表示宽度为 7 英寸，高度为 6 英寸
ax.bar(x=x, height=y, width=0.5, color='purple')  # orange / red / green / purple
ax.set_title("GraphSAGE-gcn-no-weight", fontsize=10)
xticks = ax.get_xticks()
for i in range(len(y)):
    xy = (xticks[i], y[i] * 1.005)
    text = str(y[i])
    ax.annotate(
        text=text,  # 要添加的文本
        xy=xy,  # 将文本添加到哪个位置
        fontsize=8,  # 标签大小
        color="blue",  # 标签颜色
        ha="center",  # 水平对齐
        va="baseline"  # 垂直对齐
    )

plt.show()


# # https://blog.csdn.net/weixin_44293949/article/details/114590319
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码
#
# labels = ['pool', 'mean', 'lstm', 'gcn']
# no_weight_tpr = [0.8057, 0.8330, 0.8369, 0.3002]
# weight_tpr = [0.9139, 0.9048, 0.9240, 0.6533]
#
# no_weight_tnr = [0.9995, 0.9998, 0.9997, 0.9959]
# weight_tnr = [0.9984, 0.9987, 0.9988, 0.9860]
#
# no_weight_f1 = [0.8534, 0.8779, 0.8726, 0.3768]
# weight_f1 = [0.9038, 0.8941, 0.9059, 0.5755]
#
# x = np.arange(len(labels))  # the label locations
# width = 0.35  # the width of the bars
#
# fig, ax = plt.subplots()
# rects1 = ax.bar(x - width/2, no_weight_f1, width, label='no_weight_f1')
# rects2 = ax.bar(x + width/2, weight_f1, width, label='weight_f1')
#
# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('f1-score')
# ax.set_title('Scores of different train_method')
# ax.set_xticks(x)
# ax.set_xticklabels(labels)
# ax.legend()
#
#
# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(height),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')
#
#
# autolabel(rects1)
# autolabel(rects2)
# # 将图例置于当前坐标轴下
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#           fancybox=True, shadow=True, ncol=5)
# # fig.tight_layout()
# plt.show()
