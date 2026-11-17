import argparse
import os
import time
from collections import defaultdict

import dgl
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from dgl.nn.pytorch.conv import SAGEConv
from dgl.nn.pytorch.conv import GraphConv
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from get_test import get_name_list


def penalty_tag(scale):
	if scale == 0:
		return '_no_'
	return '_' + format(scale, 'g').replace('.', '_') + '_'


class GCN(nn.Module):
	def __init__(self,
	             in_feats,
	             n_hidden,
	             n_classes,
	             n_layers,
	             activation,
	             dropout):
		super(GCN, self).__init__()
		self.layers = nn.ModuleList()
		self.dropout = nn.Dropout(dropout)
		self.activation = activation
		# input layer
		self.layers.append(GraphConv(in_feats, n_hidden))
		# output layer
		for i in range(n_layers - 1):
			self.layers.append(GraphConv(n_hidden, n_hidden))
		# output layer
		self.layers.append(GraphConv(n_hidden, n_classes))

	# def forward(self, g,features):
	# 	h = self.dropout(features)
	# 	for i, layers in enumerate(self.layers):
	# 		if i != 0:
	# 			h = self.dropout(h)
	# 		h = layers(g, h)
	# 		if i != len(self.layers) - 1:
	# 			h = self.activation(h)
	# 	return h

	def forward(self, g, features):
		h = self.dropout(features)
		# h = features
		for i, layers in enumerate(self.layers):
			h = layers(g, h)
			if i != len(self.layers) - 1:
				h = self.activation(h)
				h = self.dropout(h)
			# h = layers(g, h)
		return h

# class GraphSAGE(nn.Module):  # 与.py类似
# 	def __init__(self,
# 				 in_feats,
# 				 n_hidden,
# 				 n_classes,
# 				 n_layers,
# 				 activation,
# 				 dropout,
# 				 aggregator_type):
# 		super(GraphSAGE, self).__init__()
# 		self.layers = nn.ModuleList()  # 创建一个空的ModuleList对象，用于存储模型的各个层
# 		self.dropout = nn.Dropout(dropout)
# 		self.activation = activation
#
# 		# input layer
# 		self.layers.append(SAGEConv(in_feats, n_hidden, aggregator_type))
# 		# 输入层：将第一个SAGEConv层添加到self.layers中，使用输入特征维度in_feats、隐藏层维度n_hidden和聚合方式'mean'进行初始化
# 		# hidden layers
# 		for i in range(n_layers - 1):
# 			self.layers.append(SAGEConv(n_hidden, n_hidden, aggregator_type))
# 			# 隐藏层：将中间层的SAGEConv层添加到self.layers中，使用隐藏层维度n_hidden、隐藏层维度n_hidden和聚合方式'mean'进行初始化
# 		# output layer
# 		self.layers.append(SAGEConv(n_hidden, n_classes, aggregator_type))  # activation None
# 		# 输出层：将最后一层的SAGEConv层添加到self.layers中，使用隐藏层维度n_hidden、类别数量n_classes和聚合方式'mean'进行初始化
#
# 	def forward(self, graph, inputs):
# 		h = self.dropout(inputs)  # 对输入特征inputs应用dropout操作，将结果赋值给变量h。dropout操作可以随机地将一部分输入特征置为零，以减少过拟合
# 		for l, layer in enumerate(self.layers):
# 			h = layer(graph, h)  # 传入图数据graph和输入特征h，计算得到新的节点表示h
# 			if l != len(self.layers) - 1:
# 				h = self.activation(h)
# 				h = self.dropout(h)
# 		return h


def result(y_test, y_pre, result_path, net_dt):  # 根据预测的标签值和真实的标签值计算混淆矩阵和评价指标 并写入到相应的文件中
	#  print(testname)
	# 混淆矩阵
	y_test = y_test.cpu()
	y_pre = y_pre.cpu()  # 将y_test和y_pre移动到CPU上进行处理，确保数据类型一致

	conf_mat = confusion_matrix(y_test, y_pre)  # 计算真实标签y_test和预测标签y_pre之间的混淆矩阵
	print('混淆矩阵：')
	print(conf_mat)

	tn, fp, fn, tp = confusion_matrix(y_test, y_pre).ravel()  # 将混淆矩阵展平(.ravel()) 并将其值分别赋给tn,tp,fn,fp
	# 评价指标的计算：真阳率、真阴率、精确率  # https://blog.csdn.net/weixin_48964486/article/details/122881350
	try:
		tpr = tp / (tp + fn)
	except ZeroDivisionError:
		tpr = 0
	try:
		tnr = tn / (tn + fp)
	except ZeroDivisionError:
		tnr = 0
	try:
		prec = tp / (tp + fp)
	except ZeroDivisionError:
		prec = 0
	try:
		f1 = 2 / (1 / prec + 1 / tpr)
	except ZeroDivisionError:
		f1 = 0

	os.makedirs(result_path, exist_ok=True)
	with open(os.path.join(result_path, net_dt + ".txt"), "a", encoding="utf-8") as f:
		f.write('TPR:' + str(tpr) + '\n')
		f.write('TNR:' + str(tnr) + '\n')
		f.write('F1:' + str(f1) + '\n')
		f.write('prec:' + str(prec) + '\n')
		f.write(classification_report(y_test, y_pre, digits=4))  # 生成分类指标报告 digits=4参数表示报告中数值的小数位数为4位
	print('TPR:', tpr)
	print('TNR:', tnr)
	print('f-score:', f1)

	# 分类指标文本报告（精确率、召回率、F1值等）
	print('分类指标报告：')
	print(classification_report(y_test, y_pre, digits=4))


def evaluate_test(model, graph, features, labels, nid, result_path, net_dt):  # 模型精确度accuracy计算
	model.eval()  # 将模型设置为评估模式，这会影响一些层（如Dropout层）的行为，使其在评估时不进行随机失活
	#  with torch.no_grad()的使用 https://blog.csdn.net/weixin_43145941/article/details/114757673
	with torch.no_grad():  # 在评估过程中，使用torch.no_grad()上下文管理器，以便在前向传播中不进行梯度计算，从而节省内存并加快计算速度
		logits = model(graph, features)  # 将图和输入特征传递给模型，计算预测结果logits
		logits = logits[nid]
		labels = labels[nid]  # 从预测结果logits和真实标签labels中选择对应的子集
		_, indices = torch.max(logits, dim=1)  # dim=1表示每行的最大值  计算预测结果logits中每个样本的最大值及其对应的索引，将索引保存在indices中
		correct = torch.sum(indices == labels)  # 计算预测正确的数 及预测值和标签值相等的数量 返回值为tensor(预测正确数) 在mytest中已验证
		# indices = estimator.predict(logits.detach().numpy())
		result(labels, indices, result_path, net_dt)  # 混淆矩阵计算

		return correct.item() * 1.0 / len(labels)  # 精确度accuracy计算


def evaluate(model, graph, features, labels, nid):  # 模型精确度accuracy计算
	model.eval()
	with torch.no_grad():
		logits = model(graph, features)
		logits = logits[nid]
		labels = labels[nid]
		_, indices = torch.max(logits, dim=1)
		correct = torch.sum(indices == labels)
		return correct.item() * 1.0 / len(labels)


# 这个函数的作用是将图数据(节点、边)加载到DGL图对象中，并为节点分配特征feat、标签label和掩码mask，以便后续的图神经网络训练和评估
# is_val：一个布尔值，指示是否将所有节点用作测试集
def graph_generate(graph_path, netlist, is_val):
	content_file = graph_path + os.sep + netlist.split('.')[0] + ".content"
	cites_file = graph_path + os.sep + netlist.split('.')[0] + ".cites"
	feat_data = []
	labels = []  # label sequence of node
	node_map = {}  # map node to Node_ID
	label_map = {}  # map label to Label_ID
	with open(content_file) as fp:  # content_file存储每个网表的24维特征
		for i, line in enumerate(fp):
			info = line.strip().split()
			feat_data.append([float(x) for x in info[1:-1]])  # 获取content_file中的[1:-3]特征
			node_map[info[0]] = i  # 获取模块例化的索引 node_map ={模块位置索引：索引}
			if not info[-1] in label_map:
				label_map[info[-1]] = len(label_map)  # 如果标签不在label_map中 label_map ={标签值：该字典键的个数} 用于存储分的类数，给标签打上ID
				# 可以动态构建或更新label_map，以确保每个标签都有一个唯一的标识符。这对于后续的标签处理和分类任务非常有用
			labels.append(label_map[info[-1]])  # 标签的排序
	feat_data = np.asarray(feat_data)  # 将feat_data转换为numpy格式
	labels = np.asarray(labels, dtype=np.int64)

	u = []
	v = []
	with open(cites_file) as fp:  # content_file存储每个网表的边连接关系
		for i, line in enumerate(fp):
			info = line.strip().split()
			assert len(info) == 2  # 观察边的格式是否正确
			paper1 = node_map[info[0]]
			paper2 = node_map[info[1]]
			u.append(paper1)
			v.append(paper2)  # u、v将边的连接关系提取出来

	g = dgl.graph((u, v), num_nodes=len(node_map))  # 构建一个图对象，(u,v)表示边的起始节点或数组，num_nodes表示节点的数量
	g.ndata['feat'] = torch.FloatTensor(feat_data)  # 创建一个名为'feat'的节点浮点型数据张量 用于存储节点特征
	g.ndata['label'] = torch.LongTensor(np.asarray(labels, dtype=np.int64))  # 创建一个名为'label'的节点长整型数据张量，用于存储节点标签。

	if is_val:  # 所有节点用于作测试集
		test_mask = np.full(feat_data.shape[0], True)  # 创建一个形状与feat_data的第一维相同的布尔型数组，所有元素都为 True，表示所有节点都被用作测试集
		train_mask = np.full(feat_data.shape[0], False)  # 创建一个形状与feat_data的第一维相同的布尔型数组，所有元素都为 False，表示所有节点都未被用作训练集
		val_mask = np.full(feat_data.shape[0], False)  # 创建一个形状与feat_data的第一维相同的布尔型数组，所有元素都为 False，表示所有节点都未被用作验证集
	else:
		test_mask, val_mask, train_mask = _split_data(feat_data.shape[0])  # 用于将节点划分为测试集、验证集和训练集的掩码

	g.ndata['train_mask'] = torch.Tensor(train_mask)  # 创建了一个名为'train_mask'的节点数据张量，用于存储训练集的节点掩码。
	g.ndata['val_mask'] = torch.Tensor(val_mask)  # 存储验证集的节点掩码
	g.ndata['test_mask'] = torch.Tensor(test_mask)  # 存储测试集的节点掩码
	return g, len(u)


# _split_data 函数用于将节点划分为测试集、验证集和训练集的掩码
def _split_data(num_nodes, test_split=10, val_split=10):
	rand_indices = np.random.permutation(num_nodes)  # 生成节点索引的随机排列

	test_size = num_nodes // test_split  # 用十分之一的节点进行测试
	val_size = num_nodes // val_split  # 用十分之一的节点进行验证
	train_size = num_nodes - (test_size + val_size)  # 剩下节点进行训练

	test_indexs = rand_indices[:test_size]  # 测试节点选择前1/10
	val_indexs = rand_indices[test_size:(test_size + val_size)]  # 验证节点选择中1/10
	train_indexs = rand_indices[(test_size + val_size):]  # 其余为训练节点

	# 初始掩码都为false
	test_mask = np.full(num_nodes, False)
	train_mask = np.full(num_nodes, False)
	val_mask = np.full(num_nodes, False)

	# 根据测试集、验证集和训练集的索引，将相应位置的掩码设置为 True
	for i in test_indexs:
		test_mask[i] = True
	for i in train_indexs:
		train_mask[i] = True
	for i in val_indexs:
		val_mask[i] = True

	return test_mask, val_mask, train_mask


# k为损失权重遍历传入的接口
def main_saed_cross(k, args):
	# load and preprocess dataset
	ht_files_name = ['RS232-T1000', 'RS232-T1100', 'RS232-T1200', 'RS232-T1300', 'RS232-T1400', 'RS232-T1500', 'RS232-T1600',
					 's15850-T100', 's35932-T100', 's35932-T200', 's35932-T300', 's38417-T100', 's38417-T200', 's38417-T300',
					 's38584-T100', 's38584-T200', 's38584-T300']

	# ht_files_name = ['RS232-T1000', 'RS232-T1100', 'RS232-T1200', 'RS232-T1300', 'RS232-T1400', 'RS232-T1500',
	#                  'RS232-T1600',]

	netlist_path = os.path.abspath('./data/SAED/aftpro_netfeature')
	# result_path = os.path.abspath('./result' + os.sep + args.aggregator_type)
	wt_name = penalty_tag(k)

	# if args.n_layer == 2:
	# 	result_path = os.path.abspath('./results/SAED' + os.sep + wt_name + "weight200")
	# elif args.n_layer == 4:
	# 	result_path = os.path.abspath('./GCN_result_SAED' + os.sep + wt_name + "weight200")
	# elif args.n_layer == 3:
	# 	result_path = os.path.abspath('./GCN_result_SAED' + os.sep + wt_name + "weight200")

	result_path = os.path.abspath('./results/SAED' + os.sep + "GCN" + wt_name + "weight200")
	os.makedirs(result_path, exist_ok=True)

	for net_list_test in ht_files_name:
		# pause_list = ['RS232-T1000', 'RS232-T1100', 'RS232-T1200', 'RS232-T1300']
		# if args.n_layer == 4 and args.n_hidden == 256:
		# 	if net_list_test in pause_list:
		# 		continue
		# ###收集netlist的数据构建测试集
		fdata_path = netlist_path + os.sep + net_list_test
		g_test, n_edges_test = graph_generate(fdata_path, net_list_test, True)  # 根据该网表每个节点的特征和节点见的连接关系，生成图数据g 并将该网表的数据集用作测试集
		features_test = g_test.ndata['feat']  # 获取该数据集的特征
		labels_test = g_test.ndata['label']  # 获取该数据集的标签
		# 获取用于测试的掩码
		test_mask_test = g_test.ndata['test_mask']
		test_nid_test = test_mask_test.nonzero().squeeze()
		in_feats_test = features_test.shape[1]
		# create GraphSAGE model
		model = GCN(in_feats_test,
						  args.n_hidden,
						  2,
						  args.n_layers,
						  F.relu,
						  args.dropout)
		if args.gpu < 0:
			cuda = False
			print("cuda = false")
		else:
			cuda = True
			print("cuda = true")
			# torch.cuda.set_device(args.gpu)
			# 将特征、标签、图移动到对应的gpu设备上
			features_test = features_test.cuda()
			labels_test = labels_test.cuda()
			g_test = g_test.int().to(args.gpu)
			g_test = dgl.remove_self_loop(g_test)  # 预处理图数据，去除自环
			test_mask_test = test_mask_test.cuda()

		if cuda:
			model.cuda()  # 将模型移动到gpu上
		# use optimizer
		optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)  # 创建优化器
		# estimator = DecisionTreeClassifier(criterion="entropy", random_state=3)
		for epoch in range(args.n_epochs):
			for net_list in ht_files_name:
				fedata_path = netlist_path + os.sep + net_list
				if net_list == net_list_test:  # 如果该网表是测试集则跳过
					continue
				else:
					g, n_edges = graph_generate(fedata_path, net_list, False)  # 选择一个为测试集后，其他数据集根据split_data划分为训练、测试、验证集
					features = g.ndata['feat']
					labels = g.ndata['label']
					train_mask = g.ndata['train_mask']  # 再选择训练集、验证集、测试集
					val_mask = g.ndata['val_mask']
					test_mask = g.ndata['test_mask']
					in_feats = features.shape[1]
					n_classes = 2  # #data.num_classes
					# print("""----Data statistics------'
					#   #Edges %d
					#   #Classes %d
					#   #Train samples %d
					#   #Val samples %d
					#   #Test samples %d""" %
					#       (n_edges, n_classes,
					#        train_mask.int().sum().item(),
					#        val_mask.int().sum().item(),
					#        test_mask.int().sum().item()))

					if args.gpu < 0:
						cuda = False
					else:
						cuda = True
						# # 将特征、标签、掩码数据移动到对应的gpu设备上
						torch.cuda.set_device(args.gpu)
						features = features.cuda()
						labels = labels.cuda()
						train_mask = train_mask.cuda()
						val_mask = val_mask.cuda()
						test_mask = test_mask.cuda()
						# print("use cuda:", args.gpu)

					train_nid = train_mask.nonzero().squeeze()
					val_nid = val_mask.nonzero().squeeze()
					test_nid = test_mask.nonzero().squeeze()
					# graph preprocess and calculate normalization factor
					g = dgl.remove_self_loop(g)  # 预处理图数据，去除自环
					n_edges = g.number_of_edges()
					num_negative = labels.int().sum().item()
					if k == 0:
						cross_value = 1
					else:
						cross_value = k * len(labels) / num_negative  # 选择损失函数的权重=一个网表中所有标签的数量/标签为1的数量 https://www.zhihu.com/question/400443029
					# cross_value = 1
					if cuda:
						g = g.int().to(args.gpu)
					# initialize graph
					dur = []

					model.train()
					if epoch >= 3:
						t0 = time.time()
					# forward
					logits = model(g, features)  # 使用模型进行前向传播，得到预测结果 logits
					# cross_weight = (np.array([1.0,cross_value*0.8],dtype=float))
					# cross_weight = (torch.from_numpy(cross_weight)).cuda()
					# loss = torch.sum(logits[range(logits.size(0)), labels], 0)
					# 训练集上的交叉熵损失
					class_weight = torch.tensor([1.0, cross_value], dtype=torch.float32, device=labels.device)
					loss = F.cross_entropy(logits[train_nid], labels[train_nid], weight=class_weight)

					optimizer.zero_grad()  # 使用 zero_grad() 方法来清空之前的梯度信息
					loss.backward()  # 反向传播计算梯度并更新模型参数
					optimizer.step()  # 执行参数更新

					if epoch >= 3:
						dur.append(time.time() - t0)

					acc = evaluate(model, g, features, labels, val_nid)  # 仅计算模型在验证集上的精确度
					# print("Epoch {:05d} | Time(s) {:.4f} | Loss {:.4f} | Accuracy {:.4f} | "
					#       "ETputs(KTEPS) {:.2f}".format(epoch, np.mean(dur), loss.item(),
					#                                     acc, n_edges / np.mean(dur) / 1000))
					#
					# #logits_e = model(g, features)
					# #estimator.fit(logits_e.detach().numpy(), labels)
					#
					# print()
					# acc = evaluate(model, g, features, labels, test_nid)
					# print("Test Accuracy {:.4f}".format(acc))
					time1 = time.time()
					acc = evaluate_test(model, g_test, features_test, labels_test, test_nid_test, result_path,
										net_list_test)
					time2 = time.time()
					print("evaluate time = "+str(time2-time1))

		print()

		acc = evaluate_test(model, g_test, features_test, labels_test, test_nid_test, result_path, net_list_test)
		# 计算模型在测试集上的精确度与混淆矩阵并写入结果目录。
		print("Test Accuracy {:.4f}".format(acc))


def build_parser():
	parser = argparse.ArgumentParser(description='Run GCN gate-level hardware-Trojan experiments on SAED.')
	parser.add_argument('--penalty-scale', type=float, default=0.08,
					help='Minority-class penalty scale k; use 0 for unweighted cross entropy.')
	parser.add_argument('--dropout', type=float, default=0.1)
	parser.add_argument('--gpu', type=int, default=0, help='CUDA device index; use -1 for CPU.')
	parser.add_argument('--lr', type=float, default=0.001)
	parser.add_argument('--n-epochs', type=int, default=200)
	parser.add_argument('--n-hidden', type=int, default=128)
	parser.add_argument('--n-layers', type=int, default=3)
	parser.add_argument('--weight-decay', type=float, default=5e-4)
	return parser


def cli():
	args = build_parser().parse_args()
	if args.gpu >= 0 and not torch.cuda.is_available():
		print('CUDA is unavailable; falling back to CPU.')
		args.gpu = -1
	elif args.gpu >= 0:
		torch.cuda.set_device(args.gpu)
	print(args)
	main_saed_cross(args.penalty_scale, args)


if __name__ == '__main__':
	cli()


if False and __name__ == '__main__':
	# argparse模块的用法见mytest中
	parser = argparse.ArgumentParser(description='GCN')  # 导入该模块；然后创建一个解析对象
	register_data_args(parser)
	parser.add_argument("--dropout", type=float, default=0.2,
						help="dropout probability")  # 添加args中的一个变量
	parser.add_argument("--gpu", type=int, default=0,
						help="gpu")
	parser.add_argument("--lr", type=float, default=0.01,
						help="learning rate")
	parser.add_argument("--n-epochs", type=int, default=200,
						help="number of training epochs")
	parser.add_argument("--n-hidden", type=int, default=200,
						help="number of hidden gcn units")
	parser.add_argument("--n-layers", type=int, default=5,
						help="number of hidden gcn layers")
	parser.add_argument("--weight-decay", type=float, default=1e-4,
						help="Weight for L2 loss")
	# parser = argparse.ArgumentParser(description='GraphSAGE')  # 导入该模块；然后创建一个解析对象
	# register_data_args(parser)
	# parser.add_argument("--dropout", type=float, default=0.3,
	# 					help="dropout probability")  # 添加args中的一个变量
	# parser.add_argument("--gpu", type=int, default=0,
	# 					help="gpu")
	# parser.add_argument("--lr", type=float, default=0.005,
	# 					help="learning rate")
	# parser.add_argument("--n-epochs", type=int, default=150,
	# 					help="number of training epochs")
	# parser.add_argument("--n-hidden", type=int, default=128,
	# 					help="number of hidden gcn units")
	# parser.add_argument("--n-layers", type=int, default=3,
	# 					help="number of hidden gcn layers")
	# parser.add_argument("--weight-decay", type=float, default=5e-4,
	# 					help="Weight for L2 loss")
	# parser.add_argument("--aggregator-type", type=str, default="lstm",
	# 					help="Aggregator type: mean/gcn/pool/lstm")

	print(torch.cuda.is_available())
	# loss_weight = [0, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
	# loss_weight = [0, 0.3, 0.4, 0.6, 1.0]
	loss_weight = [0.8, 1.0]
	# type_netlist = ['com', 'seq']
	# loss_weight = [1]

	#  ###############SAED库训练与测试#######################
	for k in loss_weight:
		args = parser.parse_args()  # 调用parse_args()方法进行解析，解析出来的参数存储在args变量中
		# if torch.cuda.is_available():
		#     args.gpu = 0
		# else:
		#     args.gpu = -1
		print(args)
		main_saed_cross(k, args)
		# main_new(args)

	# ###############LEDA库训练与测试#######################
	# for i in type_agg:
	# 	for k in loss_weight:
	# 		for j in type_netlist:
	# 			if (i == 'lstm' and k == 0.6 and j == 'com'):
	# 				continue
	# 			if (i == 'pool') or (i == 'mean') or (i == 'lstm' and k in used_weight):
	# 				continue
	# 			else:
	# 				parser.aggregator_type = i
	# 				args = parser.parse_args()  # 调用parse_args()方法进行解析，解析出来的参数存储在args变量中
	# 				args.aggregator_type = i
	# 				# if torch.cuda.is_available():
	# 				#     args.gpu = 0
	# 				# else:
	# 				#     args.gpu = -1
	# 				print(args)
	# 				main_leda_cross(j, k, args)
	# 				# main_new(args)
