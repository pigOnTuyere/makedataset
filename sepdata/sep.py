import os, random, shutil


def moveimg(fileDir, tarDir_val,classes,tardir_test = '', maketest =False):
    pathDir = os.listdir(fileDir)  # 取图片的原始路径
    val_rate = 0.2  # 自定义抽取图片的比例，比方说100张抽10张，那就是0.1
    test_rate = 0.1  # 自定义抽取图片的比例，比方说100张抽10张，那就是0.1
    filenumber = len(pathDir)
    print(pathDir)
    for i in classes:
        # 拆分各个类
        files = []
        for j in pathDir:
            typename = j[:j.rindex('_')]
            if i == typename:
                files.append(j)
                # print(typename)

        filenumber = len(files)
        picknumber_val = int(filenumber * val_rate)  # 按照rate比例从文件夹中取一定数量图片
        picknumber_test = int(filenumber * test_rate)

        sample_val = random.sample(files, picknumber_val)  # 随机选取picknumber数量的样本图片
        print(len(sample_val))

        sample_temp = [file_name for file_name in files if file_name not in sample_val]
        sample_test = random.sample(sample_temp, picknumber_test)  # 随机选取picknumber数量的样本图片
        print(len(sample_test))
        # 分割验证集到指定文件夹
        for name in sample_val:
            shutil.move(fileDir + name, tarDir_val + "\\" + name)
        if maketest == True:
            # 重新获取图片路径
            for name in sample_test:
                shutil.move(fileDir + name, tardir_test + "\\" + name)
    return


def movelabel(file_list, file_label_train, file_label_val):
    for i in file_list:
        if i.endswith('.jpg'):
            # filename = file_label_train + "\\" + i[:-4] + '.xml'  # 可以改成xml文件将’.txt‘改成'.xml'就可以了
            filename = file_label_train + "\\" + i[:-4] + '.txt'  # 可以改成xml文件将’.txt‘改成'.xml'就可以了
            if os.path.exists(filename):
                shutil.move(filename, file_label_val)
                print(i + "处理成功！")


if __name__ == '__main__':
    # classes = ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled-in_scale', 'scratches']
    classes = ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled-in_scale', 'scratches']
    # classes = ['0', '1', '2', '3', '4', '5']
    # 移动图片到指定文件夹
    path = 'version_8/version_8'
    fileDir = path+r"/coco/images/train" + "\\"  # 源图片文件夹路径
    tarDir_val = path+r'/coco/images/val'  # 图片移动到新的文件夹路径
    #tarDir_test = r'NEU-DET-offical-md/coco/images/test'  # 图片移动到新的文件夹路径
    moveimg(fileDir, tarDir_val, classes,  maketest=False)
    #moveimg(fileDir, tarDir_val, classes, tarDir_test, maketest=False)
    # 移动标签到指定文件夹
    file_list = os.listdir(tarDir_val)
    file_label_train = path+r"\coco\labels\train"  # 源图片标签路径
    file_label_val = path+r"\coco\labels\val"  # 标签
    # 移动到新的文件路径
    movelabel(file_list, file_label_train, file_label_val)

    # # 移动标签到指定文件夹
    # file_list = os.listdir(tarDir_test)
    # file_label_train = r"NEU-DET-offical-md\coco\labels\train"  # 源图片标签路径
    # file_label_test = r"NEU-DET-offical-md\coco\labels\test"  # 标签
    # # 移动到新的文件路径
    # movelabel(file_list, file_label_train, file_label_test)