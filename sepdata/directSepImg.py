import os
import numpy as np
import shutil

'''
脚本功能：
    该脚本适用于图片分类任务
    按照比例随机分配训练集和验证集，这里没有对gt进行操作
'''

IMG_PATH = "D:\code\Makedataset\sepdata\\bg4\\val"

# 创建目标的标签路径和图像路径
basepath = 'bg42'
paths = [
    "\\train",     # 训练图片路径
    "\\val",       # 验证图片路径
]

# 检查路径是否存在
for path in paths:
    true_path = basepath + path
    if not os.path.exists(true_path):
        # 文件夹不存在，创建它
        os.makedirs(true_path)
        print(f"文件夹 {true_path} 已创建。")
    else:
        print(f"文件夹 {true_path} 已存在。")

# 获取所有XML文件
img_list = os.listdir(IMG_PATH)
# 随机排序XML文件
np.random.seed(100)
np.random.shuffle(img_list)

if __name__ == "__main__":
    # 按比例划分打乱后的数据集
    train_ratio = 1800/len(img_list)                             # 训练集比例
    val_ratio = 1-1800/len(img_list)                        # 验证集比例
    train_num = int(len(img_list) * train_ratio)
    val_num = int(len(img_list) * val_ratio)
    img_list_train = img_list[:train_num]
    img_list_val = img_list[train_num: train_num + val_num]

    # 复制训练集中图像文件
    for img in img_list_train:
        oringin_img_path = IMG_PATH +"\\" + os.path.basename(img)
        # 复制图片
        shutil.copyfile(oringin_img_path, basepath + paths[0] + '//' + os.path.basename(oringin_img_path))

    # 复制测试集中图像文件
    for img in img_list_val:
        oringin_img_path = IMG_PATH +"\\" + os.path.basename(img)
        # 复制图片
        shutil.copyfile(oringin_img_path, basepath + paths[1] + '//' + os.path.basename(oringin_img_path))



