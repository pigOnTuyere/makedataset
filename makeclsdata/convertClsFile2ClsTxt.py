import os
import shutil

def convert_labels(folder_path,an_path,dsetImagefile):
    '''

    :param folder_path:
    :param an_path:
    :param dsetImagefile: 存储合并文件夹后的图片
    :return: 标签（list）

    '''
    labels = []
    file_names = []
    # 获取文件夹中的所有文件\

    # 获取子文件夹列表，每个子文件夹的名称将作为标签
    fileindexs = [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]
    for fid in fileindexs:
        path  = folder_path + '\\' + fid
        file_list = os.listdir(path)

        for file_name in file_list:
            # 检查是否为图片文件（可根据需要调整）
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg','.bmp')):
                # 提取文件名
                file_names.append(file_name)
                labels.append(fid)
                # 复制图片到目标文件夹中
                oringin_img_path = path + "\\" + os.path.basename(file_name)
                # 复制图片
                shutil.copyfile(oringin_img_path, dsetImagefile + '//' + os.path.basename(oringin_img_path))

    # 使用"with open"语句打开文件，并以写入模式('w')写入数据
    with open(an_path, 'w') as file:
        # 使用循环遍历列表中的数据，并将每个数据写入一行
        for file_name, lb in zip(file_names, labels):
            file.write(str(file_name) + ' '+str(lb)+'\n')
    return  labels

if __name__ == '__main__':
    # 需要转换的文件夹路径
    folder_path = 'D:\code\Makedataset\data\classdata\\val'
    # 存储结果文件夹
    rusult_path= "D:\code\Makedataset\makeclsdata\\result"
    dst_Imgfile = rusult_path+'\\'+'val'
    # 检查路径是否存在
    if not os.path.exists(dst_Imgfile):
        # 如果路径不存在，创建它
        os.makedirs(dst_Imgfile)
        print(f"路径 {dst_Imgfile} 不存在，已成功创建。")
    else:
        print(f"路径 {dst_Imgfile} 已经存在。")
    an_path = rusult_path+'\\'+'val.txt'

    labels = convert_labels(folder_path, an_path, dst_Imgfile)

