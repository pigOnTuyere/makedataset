import os
import numpy as np
import shutil

'''
    克隆一个类似的数据集，数据标签相同，图像名相同，图片的数据不同
'''

copy_from = "D:\code\Makedataset\data\classdata_6"
new_img_floder = 'D:\code\Makedataset\object2class\makdata'

save_path = 'output'

def check_make_foder(path):

    if not os.path.exists(path):
        # 文件夹不存在，创建它
        os.makedirs(path)
        print(f"文件夹 {path} 已创建。")
    else:
        print(f"文件夹 {path} 已存在。")

if __name__ == "__main__":
    # 构建存储文件夹
    for p in ['train', 'test']:
        absoluteP = os.path.join(copy_from, p)
        # 寻找当前文件夹下的所有文件夹（类别）
        folders = [f for f in os.listdir(absoluteP) if os.path.isdir(os.path.join(absoluteP, f))]
        for f in folders:
            cls_path = os.path.join(save_path, p, f)
            check_make_foder(cls_path)
            copy_from_path = os.path.join(absoluteP,f)
            imglist = os.listdir(copy_from_path)
            for im in imglist:
                new_img_path = os.path.join(new_img_floder,im)
                if not os.path.exists(new_img_path):
                    print('数据集错误，请检查数据集')
                else:
                    target_path = os.path.join(save_path, p, f, im)
                    shutil.copyfile(new_img_path, target_path)
