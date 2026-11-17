import matplotlib.pyplot as plt
import os

filename = 'wb_conmax-T100'
result_path = os.path.abspath('./result_largenetlist' + os.sep + "pool_0_3_weight1200-1")
data_path = os.path.abspath(result_path + os.sep + filename + "_loss-acc.txt")
epoch_losses = []
epoch_accurc = []
cnt = 0
with open(data_path, "r", encoding="utf-8") as f:
	for line in f:  # .content文件中存放一个.v文件的所有节点的特征向量 及标签值
		cnt = cnt + 1
		if cnt > 1000:
			break
		# if float(epch_loss) > 1:
		# 	epch_loss = 1.0
		data = line.strip().split()
		epoch_losses.append(float(data[0]))
		epoch_accurc.append(float(data[1]))
plt.switch_backend('Agg')  # 后端设置'Agg' 参考：https://cloud.tencent.com/developer/article/1559466

plt.figure()                   # 设置图片信息 例如：plt.figure(num = 2,figsize=(640,480))
plt.plot(epoch_losses, 'r', label = 'loss')        # epoch_losses 传入模型训练中的 loss[]列表,在训练过程中，先创建loss列表，将每一个epoch的loss 加进这个列表
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend()        # 个性化图例（颜色、形状等）
plt.savefig(os.path.join(result_path, filename + "_loss.jpg"))  # 保存图片 路径：/imgPath/
plt.clf()

plt.switch_backend('Agg')  # 后端设置'Agg' 参考：https://cloud.tencent.com/developer/article/1559466

plt.figure()                   # 设置图片信息 例如：plt.figure(num = 2,figsize=(640,480))
plt.plot(epoch_accurc, 'b', label='acc')        # epoch_losses 传入模型训练中的 loss[]列表,在训练过程中，先创建loss列表，将每一个epoch的loss 加进这个列表
plt.ylabel('acc')
plt.xlabel('epoch')
plt.legend()        # 个性化图例（颜色、形状等）
plt.savefig(os.path.join(result_path, filename + "_acc.jpg"))  # 保存图片 路径：/imgPath/
plt.clf()