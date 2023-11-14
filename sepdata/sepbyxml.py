import os
import numpy as np
import shutil


# 源XML文件夹和目标文件夹
XML_PATH = "D:\code\Makedataset\object2class\data\\annotations"
IMG_PATH = "D:\code\Makedataset\object2class\data\BMPImages"
# 创建分配后的文件夹
train = "output\\train"
val = 'output\\defect'

# 创建目标的标签路径和图像路径
basepath = 'output'
paths = [
    "\\train\\images",     # 训练图片路径
    "\\train\\ann",        # 训练图片标签路径
    "\\val\\images",       # 验证图片路径
    "\\val\\ann",          # 验证图片标签路径
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
xmllist = os.listdir(XML_PATH)
# 随机排序XML文件
np.random.seed(100)
np.random.shuffle(xmllist)

if __name__ == "__main__":
    # 按比例划分打乱后的数据集
    train_ratio = 0.8                           # 训练集比例
    val_ratio = 0.2                             # 验证集比例
    train_num = int(len(xmllist) * train_ratio)
    val_num = int(len(xmllist) * val_ratio)
    xml_list_train = xmllist[:train_num]
    xml_list_val = xmllist[train_num: train_num + val_num]

    # 复制训练集中xml文件和图像文件
    for xml in xml_list_train:
        imgName = xml[:-4] + ".bmp"
        oringin_img_path = IMG_PATH +"\\" + os.path.basename(imgName)
        oringin_xml_path = XML_PATH + "\\" + os.path.basename(xml)
        # 复制图片
        shutil.copyfile(oringin_img_path, basepath + paths[0] + '//' + os.path.basename(oringin_img_path))
        # 复制标签文件
        shutil.copyfile(oringin_xml_path, basepath + paths[1] + '//' + os.path.basename(oringin_xml_path))

    # 复制测试集中xml文件和图像文件
    for xml in xml_list_val:
        imgName = xml[:-4] + ".bmp"
        oringin_img_path = IMG_PATH +"\\" + os.path.basename(imgName)
        oringin_xml_path = XML_PATH + "\\" + os.path.basename(xml)
        # 复制图片
        shutil.copyfile(oringin_img_path, basepath + paths[2] + '//' + os.path.basename(oringin_img_path))
        # 复制标签文件
        shutil.copyfile(oringin_xml_path, basepath + paths[3] + '//' + os.path.basename(oringin_xml_path))

